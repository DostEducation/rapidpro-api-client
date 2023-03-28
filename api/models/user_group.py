from api import db
from flask_sqlalchemy import BaseQuery
from api.mixins import TimestampMixin


class UserGroupQuery(BaseQuery):
    def get_by_user_id(self, user_id):
        return self.filter(UserGroup.user_id == user_id).all()


class UserGroup(TimestampMixin, db.Model):
    query_class = UserGroupQuery
    __tablename__ = "user_group"

    class UserGroupStatus(object):
        ACTIVE = "active"
        INACTIVE = "inactive"

    id = db.Column(db.Integer, primary_key=True)
    user_phone = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    registration_id = db.Column(db.Integer, db.ForeignKey("registration.id"))
    group_name = db.Column(db.String(255), nullable=False)
    group_uuid = db.Column(db.String(255))
    status = db.Column(db.String(100))
