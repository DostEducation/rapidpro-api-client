from api import app, db
import requests
from api.models.user_group import UserGroup
from flask import jsonify


class UpdateUserGroup:
    def fetch_existing_groups_of_user(self, user_id):
        groups = []
        user_group = UserGroup.query.get_by_user_id(user_id)
        for record in user_group:
            groups.append(record.group_name)
        return groups

    def add_group(self, data, new_group):
        for record in data:
            user_id = record.user_id
            phone = record.user_phone
            group = self.fetch_existing_groups_of_user(user_id)
            group.append(new_group)
            token = app.config["RAPID_PRO_AUTHORIZATION_TOKEN"]
            headers = {
                "Authorization": "Token " + token,
                "Content-Type": "application/json",
            }
            post_data = {"groups": group}

            update_group = requests.post(
                "https://rapidpro.ilhasoft.in/api/v2/contacts.json?urn=tel%3A%2B91"
                + phone,
                headers=headers,
                json=post_data,
            )
            if update_group.status_code == 200:
                return True
