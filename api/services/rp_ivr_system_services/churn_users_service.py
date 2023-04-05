from api import app, db
from google.cloud import bigquery
from datetime import datetime, timedelta
from api.models.user_program import UserProgram
from api.models.churned_users import ChurnedUsers
from api.services.rapid_pro_services.rp_user_group_service import RpUserGroupService
from sqlalchemy import update


class ChurnUsersService(object):
    def __init__(self):
        self.bigquery_client = bigquery.Client()
        self.dataset_id = app.config["DATASET_ID"]

    def process_churned_user_data(self):
        query_to_fetch_churned_users = self.query_to_fetch_users_to_mark_churn()
        churned_users_data = self.bigquery_client.query(query_to_fetch_churned_users)

        # Convert churned users data to a list so that we can iterate over it multiple times
        churned_users_list = list(churned_users_data)

        churned_users_added = self.add_churned_user(churned_users_list)
        churned_user_group_name = app.config["CHURNED_USER_GROUP_NAME"]
        if churned_users_added:
            RpUserGroupService().add_group(
                churned_users_list, new_group=churned_user_group_name
            )
        return True

    def query_to_fetch_users_to_mark_churn(self):
        query = f"""
            With user_details as (
                    SELECT
                    right(r.user_phone, 10) as user_phone,
                    r.user_id,
                    up.status,
                    up.id as user_program_id
                    from
                    `{self.bigquery_client.project}.{self.dataset_id}.registration` as r
                    left join `{self.bigquery_client.project}.{self.dataset_id}.user_program` as up on r.user_id = up.user_id
                    and r.data_source = up.data_source
                    where
                    r.data_source = 'rp_ivr'
                    and DATE(up.start_date) < DATE_ADD(CURRENT_DATETIME(), INTERVAL -3 MONTH)
                    AND up.status = 'in-progress'
                    ),
            valid_campaigns AS (
                SELECT
                    DISTINCT(right(cle.from_number, 10)) as user_phone
                FROM
                    `{self.bigquery_client.project}.{self.dataset_id}.call_log_event` as cle
                JOIN
                    user_details ud
                ON
                    ud.user_phone = right(cle.from_number, 10)
                    AND DATE(cle.pick_time) >= DATE_ADD(CURRENT_DATETIME(), INTERVAL -3 MONTH)
                    AND CAST(cle.duration AS INT64) >= 20 )
                SELECT
                ud.user_program_id,
                ud.user_id,
                ud.status,
                ud.user_phone
                FROM
                user_details ud
                LEFT JOIN
                valid_campaigns vc
                ON
                ud.user_phone = vc.user_phone
                WHERE
                vc.user_phone IS NULL
        """
        return query

    def mark_users_as_churned(self, user_ids):
        update_churned_users_status = (
            update(UserProgram)
            .where(UserProgram.user_id.in_(user_ids))
            .values(status="churned")
        )
        db.session.execute(update_churned_users_status)
        db.session.commit()
        return True

    def add_churned_user(self, data):
        churned_users = []
        user_ids = []
        istnow = datetime.utcnow() + timedelta(hours=5, minutes=30)
        start_date = istnow.strftime("%Y-%m-%d")
        for record in data:
            user_ids.append(record.user_id)
            churned_user = ChurnedUsers(
                user_id=record.user_id,
                user_program_id=record.user_program_id,
                user_phone=record.user_phone,
                previous_status=record.status,
                start_date=start_date,
                end_date=None,
            )
            churned_users.append(churned_user)
        db.session.bulk_save_objects(churned_users)
        db.session.commit()
        status_updated = self.mark_users_as_churned(user_ids)
        return status_updated
