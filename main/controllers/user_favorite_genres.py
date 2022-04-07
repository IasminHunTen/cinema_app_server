from extra_modules import db


class UserFavoriteGenres(db.Model):
    pk = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.String(64))
    genre_id = db.Column(db.String(64))

    def __init__(self, user_id, genre_id):
        self.user_id = user_id
        self.genre_id = genre_id

    def db_store(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def favorite_genres_for_user(cls, user_id):
        return {
            'genres': [genre.genre_id for genre in cls.query.filter_by(user_id=user_id).all()]
        }

    @classmethod
    def edit_favorite_genre(cls, user_id, genre_ids: set):
        store_genres_id = set(UserFavoriteGenres.favorite_genres_for_user(user_id))
        for genre_id in store_genres_id.difference(genre_ids):
            db.session.delete(
                cls.query.filter_by(user_id=user_id).filter_by(genre_id=genre_id).first()
            )
        for genre_id in genre_ids.difference(store_genres_id):
            db.session.add(
                UserFavoriteGenres(user_id, genre_id)
            )
        db.session.commit()

    @classmethod
    def on_user_delete(cls, user_id):
        [
            db.session.delete(genre) for genre in cls.query.filter_by(user_id=user_id)
        ]
        db.session.commit()
