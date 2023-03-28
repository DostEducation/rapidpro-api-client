from flask import jsonify
from api.services.rp_ivr_system_services.churn_users import ChurnUsers

### Endpoint for Cloud function
def trigger(request):
    if request.method == "POST":
        try:
            request_type = request.json["request_type"]
            if request_type == "churn_users":
                churn_users()
            else:
                return jsonify({"error": "Invalid request type"})
        except Exception as e:
            return jsonify(message="Something went wrong!"), 400

        return jsonify(message="Success"), 200
    else:
        return jsonify(message="Currently, the system do not accept a GET request"), 405


def churn_users():
    request_handler = ChurnUsers().fetch_users_to_mark_churned()
