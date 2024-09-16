from flask import Blueprint, current_app, jsonify, request
from ..factory import get_statistics_repository
from src.utils.validation import validate_date


stats_blueprint = Blueprint("stats_blueprint", __name__)


@stats_blueprint.route("/api/v1/stats/<table_name>", methods=["GET"])
def table_count(table_name):
    stats_repo = get_statistics_repository(current_app.config)
    if stats_repo.check_table_name(table_name):
        row = stats_repo.get_number_of_rows(table_name)
        return jsonify({"message": "Number of Rows", "rows": row}), 200
    return jsonify({"message": "Table name not found"}), 404


@stats_blueprint.route("/api/v1/stats/interactions/<customer_id>", methods=["GET"])
def customer_interactions_per_channel_count(customer_id):

    # Get optional date filters from the query parameters
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    stats_repo = get_statistics_repository(current_app.config)

    # To improve in the future: have the following validations as part of a function.
    if not customer_id.isdigit() or int(customer_id) <= 0:
        return jsonify({"error": "Invalid customer_id provided"}), 400
    if not stats_repo.check_if_customer_exists(customer_id):
        return jsonify({"message": "Customer not found"}), 404
    if start_date and not validate_date(start_date):
        return jsonify({"error": "Invalid start_date format. Use YYYY-MM-DD."}), 400
    if end_date and not validate_date(end_date):
        return jsonify({"error": "Invalid end_date format. Use YYYY-MM-DD."}), 400
    if start_date and end_date and start_date > end_date:
        return jsonify({"error": "start_date cannot be later than end_date."}), 400

    query_result = stats_repo.get_total_interactions_per_customer_and_channel(
        customer_id, start_date, end_date
    )

    result = {"data": {}}
    interactions = {}

    for record in query_result:
        event = record.get("event")
        total_interactions = record.get("total_interactions")
        interactions[event] = total_interactions

    result["data"] = {"customer_id": int(customer_id), "interactions": interactions}
    return jsonify(result), 200
