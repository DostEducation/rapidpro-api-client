from api import app
import requests
from api.models.user_group import UserGroup


class RpUserGroupService:
    def fetch_existing_groups_of_user(self, user_id):
        groups = []
        user_group = UserGroup.query.get_by_user_id(user_id)
        for record in user_group:
            groups.append(record.group_name)
        return groups

    def add_group(self, data, new_group):
        for record in data:
            try:
                user_id = record.user_id
                phone = record.user_phone
                group = self.fetch_existing_groups_of_user(user_id)
                group.append(new_group)
                token = app.config["RAPID_PRO_AUTHORIZATION_TOKEN"]
                api_url = app.config["RAPID_PRO_API_URL"]
                headers = {
                    "Authorization": "Token " + token,
                    "Content-Type": "application/json",
                }
                post_data = {"groups": group}

                update_group = requests.post(
                    api_url + phone,
                    headers=headers,
                    json=post_data,
                )
            except Exception as e:
                print(
                    "Error while updating the churned user group in Rapid Pro for User with user_id %s",
                    user_id,
                )
                continue
