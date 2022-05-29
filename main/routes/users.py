import logging

from flask_restx import Resource
from flask import current_app as app, request
from flask_mail import Message
from sqlalchemy.exc import IntegrityError
import jwt
from datetime import datetime, timedelta
from werkzeug.exceptions import BadRequest

from extra_modules import mail, SQLDuplicateException, NotFound
from controllers import User, UserDevices, UserFavoriteGenres, CreditCard, Tickets, MovieVotes, Movie, TokenOnDevice
from serializable import user_post_model, user_token_model, get_user_devices_model, ufg_model, user_login_model, \
    reset_password_model, delete_user_model, buy_tickets_model, revoke_tickets_model, buy_tickets_response, \
    price_tickets_model, get_tickets_model, get_movie_votes_model, voted_movie_model
from serializable.credit_card import *
from utils import inject_validated_payload, doc_resp, crop_sql_err, required_login, debug_print
from models import UserPost, GetUsers, GetUserDeviceSchema, UFGSchema, UserLogin, ResetPassword, DeleteUser, \
    BuyTickets, RevokeTickets, GetUserTickets, PriceTickets, GetMovieVotes, VotedMovie
from models.credit_card import *
from constants.req_responses import *
from constants.email_template import WELCOME_MAIL, RESET_PASSWORD
from constants import SQL_DUPLICATE_ERR, auth_in_query, string_from_query

ns = api.namespace('users')


def generate_token(user):
    token = jwt.encode({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'isAdmin': user.isAdmin,
        'exp': datetime.now() + timedelta(seconds=app.config['TOKEN_VALIDITY'])
    }, key=app.config['SECRET_KEY'])

    return {'token': token}


@ns.route('/')
class UserResource(Resource):
    @ns.response(*doc_resp(FETCH_RESP))
    @ns.doc(params=auth_in_query)
    @required_login(as_admin=True)
    def get(self, token_data):
        user_list = User.fetch_users()
        return GetUsers(many=True).dump(user_list), 200

    @ns.response(*doc_resp(DELETE_RESP))
    @ns.doc(params=auth_in_query)
    @ns.expect(delete_user_model)
    @required_login()
    @inject_validated_payload(DeleteUser())
    def delete(self, payload, token_data):
        user_id = payload.get('id')
        User.delete_user(user_id)
        UserDevices.on_user_delete(user_id)
        UserFavoriteGenres.on_user_delete(user_id)
        CreditCard.on_user_delete(user_id)
        MovieVotes.on_user_delete(user_id)
        return DELETE_RESP


@ns.route('/register')
class RegisterResource(Resource):
    @ns.response(*doc_resp(CREATE_RESP))
    @ns.expect(user_post_model)
    @ns.marshal_with(user_token_model)
    @ns.doc(params=string_from_query('device_id'))
    @inject_validated_payload(UserPost())
    def post(self, payload):
        try:
            device_id = request.args.get('device_id')
            if device_id is None:
                raise BadRequest('Device id expected in the query')
            user = User(payload['username'], payload['email'], payload['password'])
            user.db_store()
            mail.send(Message(
                subject='Account Created',
                recipients=[payload.get('email')],
                body=WELCOME_MAIL.format(payload.get('username'), app.config['APP_NAME']),
                sender=app.config['MAIL_USERNAME']
            ))
            UserDevices(user.id, device_id).db_store()

        except IntegrityError as ie:
            raise SQLDuplicateException(ie.args[0])
        except Exception as ie:
            logging.error(ie)
        token = generate_token(user)
        TokenOnDevice(device_id, token.get('token')).db_store()
        return token, 201


@ns.route('/login')
class LoginResource(Resource):
    @ns.response(*doc_resp(NOT_FOUND))
    @ns.response(*doc_resp(UNAUTHORIZED))
    @ns.expect(user_login_model)
    @ns.marshal_with(user_token_model)
    @ns.doc(params=string_from_query('device_id'))
    @inject_validated_payload(UserLogin())
    def post(self, payload):
        logging.error(payload)
        device_id = request.args.get('device_id')
        if device_id is None:
            raise BadRequest('Device id expected in the query')
        user = User.login(**payload)
        UserDevices(user.id, device_id).db_store()
        token = generate_token(user)
        TokenOnDevice(device_id, token.get('token')).db_store()
        return token, 201


@ns.route('/logout')
class LogoutResource(Resource):
    @ns.response(*doc_resp(DELETE_RESP))
    @ns.doc(params=auth_in_query)
    @ns.doc(params=string_from_query('device_id'))
    @required_login()
    def delete(self, token_data):
        device_id = request.args.get('device_id')
        if device_id is None:
            raise BadRequest('Device id expected in the query')
        UserDevices.delete(token_data.get('id'), device_id)
        TokenOnDevice.device_token(device_id)
        return DELETE_RESP


@ns.route('/token')
class TokenResource(Resource):
    @ns.response(*doc_resp(FETCH_RESP))
    @ns.doc(params=string_from_query('device_id'))
    def get(self):
        device_id = request.args.get('device_id')
        if device_id is None:
            raise BadRequest('Device id expected in the query')
        token = TokenOnDevice.fetch_token(device_id)
        logging.error(f"token: {token}")
        try:
            jwt.decode(token, key=app.config['SECRET_KEY'], algorithms='HS256')
            return {
                'token': token
            }
        except Exception as e:
            logging.error(e)



@ns.route('/prejudice')
@ns.response(*doc_resp(UNAUTHORIZED))
class PrejudiceResource(Resource):
    @ns.response(*doc_resp(FETCH_RESP))
    @ns.doc(params=auth_in_query)
    @ns.doc(params=string_from_query('user_id'))
    @required_login()
    def get(self, token_data):
        user_id = token_data.get('isAdmin')
        if token_data.get('isAdmin'):
            user_id = request.args.get('user_id')
            if user_id is None:
                raise BadRequest('User id expected as query param')
        return {'prejudice': User.get_user_prejudice(user_id)}, 200

    @ns.response(*doc_resp(UPDATE_RESP))
    @ns.doc(params=auth_in_query)
    @ns.doc(params=string_from_query('amount'))
    @required_login()
    def put(self, token_data):
        amount = request.args.get('amount')
        if amount is None:
            raise BadRequest('Amount is expected as query param')
        User.update_prejudice(token_data.get('id'), float(amount))
        return UPDATE_RESP


@ns.route('/reset-password')
class ResetPasswordResource(Resource):
    @ns.response(*doc_resp(CREATE_RESP))
    @ns.response(*doc_resp(BAD_REQUEST))
    @ns.response(*doc_resp(NOT_FOUND))
    @ns.doc(params=string_from_query('email'))
    def post(self):
        email = request.args.get('email')
        if email is None:
            raise BadRequest('Email expected in query')
        user = User.generate_reset_validation_code(email)
        mail.send(Message(
            subject='Reset Password Request',
            recipients=[email],
            body=RESET_PASSWORD.format(user.username, user.reset_password_code),
            sender=app.config['MAIL_USERNAME']
        ))
        return CREATE_RESP

    @ns.response(*doc_resp(UPDATE_RESP))
    @ns.response(*doc_resp(BAD_REQUEST))
    @ns.expect(reset_password_model)
    @inject_validated_payload(ResetPassword())
    def put(self, payload):
        User.reset_password(**payload)
        return UPDATE_RESP


@ns.route('/user-devices')
class UserDeviceResource(Resource):
    @ns.response(*doc_resp(FETCH_RESP))
    @ns.response(*doc_resp(NOT_FOUND))
    @ns.marshal_list_with(get_user_devices_model)
    @ns.doc(params=auth_in_query)
    @required_login()
    def get(self, token_data):
        user_devices = UserDevices.fetch_user_device(token_data.get('id'))
        if not user_devices:
            raise NOT_FOUND('User not found')
        return GetUserDeviceSchema(many=True).dump(user_devices), 200

    @ns.response(*doc_resp(DELETE_RESP))
    @ns.doc(params=auth_in_query)
    @ns.doc(params=string_from_query('device_serial_number'))
    @required_login()
    def delete(self, token_data):
        dsn = request.args.get('device_serial_number')
        if dsn is None:
            raise BadRequest('Missing device serial number from query')
        UserDevices.delete(token_data['id'], dsn.split())
        return DELETE_RESP


@ns.route('/user_favorite_genres')
@ns.response(*doc_resp(UNAUTHORIZED))
class UFGResource(Resource):
    @ns.response(*doc_resp(CREATE_RESP))
    @ns.response(*doc_resp(BAD_REQUEST))
    @ns.doc(params=string_from_query('genre_ids'))
    @ns.doc(params=auth_in_query)
    @required_login()
    def post(self, token_data):
        genres_ids = request.args.get('genre_ids')
        if genres_ids is None:
            raise BadRequest('At Least One genres need to be chosen')
        for genre_id in genres_ids.split():
            UserFavoriteGenres(token_data.get('id'), genre_id).db_store()
        return CREATE_RESP

    @ns.response(*doc_resp(UPDATE_RESP))
    @ns.doc(params=string_from_query('genre_ids'))
    @ns.doc(params=auth_in_query)
    @required_login()
    def put(self, token_data):
        genres_ids = request.args.get('genre_ids')
        updated_genres_ids = {} if genres_ids is None else set(genres_ids.split())
        UserFavoriteGenres.edit_favorite_genre(token_data.get('id'), updated_genres_ids)
        return UPDATE_RESP

    @ns.response(*doc_resp(FETCH_RESP))
    @ns.doc(params=auth_in_query)
    @ns.marshal_with(ufg_model)
    @required_login()
    def get(self, token_data):
        return UFGSchema().dump(UserFavoriteGenres.favorite_genres_for_user(token_data.get('id'))), 200


@ns.route('/credit_card')
@ns.response(*doc_resp(UNAUTHORIZED))
class CreditCardResource(Resource):
    @ns.response(*doc_resp(CREATE_RESP))
    @ns.response(*doc_resp(BAD_REQUEST))
    @ns.doc(params=auth_in_query)
    @ns.expect(post_card_model)
    @inject_validated_payload(PostCreditCard())
    @required_login()
    def post(self, payload, token_data):
        CreditCard(token_data.get('id'), **payload).db_store()
        return CREATE_RESP

    @ns.response(*doc_resp(FETCH_RESP))
    @ns.doc(params=auth_in_query)
    @ns.marshal_list_with(get_card_model)
    @required_login()
    def get(self, token_data):
        return GetCreditCard(many=True).dump(
            CreditCard.fetch_user_credit_cards(
                token_data.get('id')
            )
        ), 200

    @ns.response(*doc_resp(UPDATE_RESP))
    @ns.doc(params=auth_in_query)
    @ns.expect(edit_card_amount_model)
    @inject_validated_payload(EditCreditCardSold())
    @required_login()
    def put(self, payload, token_data):
        CreditCard.alter_credit_card_sold(**payload)
        return UPDATE_RESP

    @ns.response(*doc_resp(DELETE_RESP))
    @ns.response(*doc_resp(BAD_REQUEST))
    @ns.doc(params=auth_in_query)
    @ns.doc(params=string_from_query('card_number'))
    @required_login()
    def delete(self,  token_data):
        card_number = request.args.get('card_number')
        if card_number is None:
            raise BadRequest("Missing card number from query")
        CreditCard.delete_user_credit_card(card_number)
        return DELETE_RESP


@ns.route('/tickets')
@ns.response(*doc_resp(UNAUTHORIZED))
class TicketsManagement(Resource):
    @ns.response(*doc_resp(BAD_REQUEST))
    @ns.doc(params=auth_in_query)
    @ns.marshal_with(buy_tickets_response)
    @ns.expect(buy_tickets_model)
    @required_login()
    @inject_validated_payload(BuyTickets())
    def post(self, payload, token_data):
        tickets_id, amount = Tickets(user_id=token_data.get('id'), **payload).db_store()
        return {'tickets_id': tickets_id,
                'amount': amount}, 201

    @ns.response(*doc_resp(DELETE_RESP))
    @ns.doc(params=auth_in_query)
    @ns.expect(revoke_tickets_model)
    @ns.marshal_with(price_tickets_model)
    @required_login()
    @inject_validated_payload(RevokeTickets())
    def delete(self, payload, token_data):
        amount = Tickets.revoke_order(**payload)
        return PriceTickets().dump({
            'amount': amount
        })

    @ns.response(*doc_resp(FETCH_RESP))
    @ns.doc(params=auth_in_query)
    @ns.marshal_list_with(get_tickets_model)
    @required_login()
    def get(self, token_data):
        return GetUserTickets(many=True).dump(
            Tickets.get_user_tickets(token_data.get('id'))
        ), 200

    @ns.route('/vote-movie')
    @ns.response(*doc_resp(UNAUTHORIZED))
    class VoteMovieResource(Resource):

        @ns.response(*doc_resp(CREATE_RESP))
        @ns.response(*doc_resp(BAD_REQUEST))
        @ns.doc(params=auth_in_query)
        @ns.doc(params=string_from_query('movie_id'))
        @required_login()
        def post(self, token_data):
            movie_id = request.args.get('movie_id')
            if movie_id is None:
                raise BadRequest('Movie id expected in query')
            if not Movie.movie_exist(movie_id):
                raise NotFound(f'Movie with id={movie_id} not found')
            MovieVotes(movie_id, token_data.get('id')).db_store()
            return CREATE_RESP

        @ns.response(*doc_resp(FETCH_RESP))
        @ns.doc(params=auth_in_query)
        @ns.marshal_with(voted_movie_model)
        @required_login()
        def get(self, token_data):
            return VotedMovie().dump({
                'movies_id': MovieVotes.fetch_user_votes(token_data.get('id'))
            }), 200

        @ns.response(*doc_resp(CREATE_RESP))
        @ns.response(*doc_resp(BAD_REQUEST))
        @ns.doc(params=auth_in_query)
        @ns.doc(params=string_from_query('movie_id'))
        @required_login()
        def delete(self, token_data):
            movie_id = request.args.get('movie_id')
            if movie_id is None:
                raise BadRequest('Movie id expected in query')
            MovieVotes.delete_vote(token_data.get('id'), movie_id)
            return DELETE_RESP




