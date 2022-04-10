from werkzeug.exceptions import BadRequest

from extra_modules import db


class MovieVotes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.String(64))
    user_id = db.Column(db.String(64))

    def __init__(self, movie_id, user_id):
        self.movie_id = movie_id
        self.user_id = user_id

    def db_store(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def fetch_votes(cls, movie_id):
        return len(cls.query.filter_by(movie_id=movie_id).all())

    @classmethod
    def fetch_user_votes(cls, user_id):
        return [vote.movie_id for vote in cls.query.filter_by(user_id=user_id).all()]

    @classmethod
    def delete_vote(cls, user_id, movie_id):
        vote = cls.query.filter_by(user_id=user_id).filter_by(movie_id=movie_id).first()
        if vote is None:
            raise BadRequest('Vote not found')
        db.session.delete(vote)
        db.session.commit()

    @classmethod
    def on_user_delete(cls, user_id):
        for vote in cls.query.filter_by(user_id=user_id).all():
            db.session.delete(vote)
        db.session.commit()

    @classmethod
    def on_movie_delete(cls, movie_id):
        for vote in cls.query.filter_by(movie_id=movie_id).all():
            db.session.delete(vote)
        db.session.commit()
