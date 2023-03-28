from api import db, app
from flask_sqlalchemy import BaseQuery
from api.mixins import TimestampMixin


class UserProgramQuery(BaseQuery):
    def get_latest_active_user_program(self, user_id):
        return (
            self.filter(
                UserProgram.user_id == user_id,
                UserProgram.status == UserProgram.Status.IN_PROGRESS,
            )
            .order_by(UserProgram.id.desc())
            .first()
        )


class UserProgram(TimestampMixin, db.Model):
    query_class = UserProgramQuery
    __tablename__ = "user_program"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    program_id = db.Column(db.Integer, db.ForeignKey("program.id"))
    preferred_time_slot = db.Column(db.String(50))
    status = db.Column(db.String(50))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)

    @classmethod
    def get_by_user_id(self, user_id):
        return UserProgram.query.get_latest_active_user_program(user_id)
