from api import db, app
from flask_sqlalchemy import BaseQuery
from api.mixins import TimestampMixin


class ChurnedUsersQuery(BaseQuery):
    def get_by_user_id(self, user_id):
        return (
            self.filter(ChurnedUsers.user_id == user_id)
            .order_by(ChurnedUsers.id.desc())
            .first()
        )


class ChurnedUsers(TimestampMixin, db.Model):
    query_class = ChurnedUsersQuery
    __tablename__ = "churned_users"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user_program_id = db.Column(db.Integer, db.ForeignKey("user_program.id"))
    user_phone = db.Column(db.String(20), nullable=False)
    previous_status = db.Column(db.String(50), unique=False)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date, nullable=True)
