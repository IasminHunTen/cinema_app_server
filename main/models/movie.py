from marshmallow import Schema, fields, validates
from utils import dict_validator, dict_upside_down


class PostSchema(Schema):
    tag = fields.String(required=True)
    title = fields.String(required=True)
    poster = fields.String(required=True)
    year = fields.Integer(required=True)
    run_time = fields.Integer(required=True)
    top_cast = fields.List(fields.String, required=True)


class PutSchema(Schema):
    id = fields.String(required=True)
    attributes = fields.Dict(required=True)

    @validates('attributes')
    def attributes_validator(self, attributes):
        dict_validator(attributes, dict_upside_down({
            str: 'title plot poster trailer'.split(),
            int: 'year run_time'.split(),
            float: 'imdb_rate',
            bool: 'voting_mode'
        }), 1)


class GetSchema(Schema):
    id = fields.String()
    tag = fields.String()
    title = fields.String()
    plot = fields.String()
    year = fields.Integer()
    imdb_rate = fields.Float()
    run_time = fields.Integer()
    poster = fields.String()
    trailer = fields.String()
    genres = fields.List(fields.String())
    directors = fields.List(fields.String())
    top_cast = fields.List(fields.String())


class DeleteSchema(Schema):
    id = fields.String(required=True)


class GetMovieVotes(Schema):
    movie_id = fields.String()
    votes = fields.Integer()
