from flask import Blueprint, current_app, jsonify, request
from ..factory import get_statistics_repository
from collections import defaultdict


stats_blueprint = Blueprint("stats_blueprint", __name__)


@stats_blueprint.route("/api/v1/stats/<table_name>", methods=["GET"])
def table_count(table_name):
    stats_repo = get_statistics_repository(current_app.config)
    if stats_repo.check_table_name(table_name):
        row = stats_repo.get_number_of_rows(table_name)
        return jsonify({"message": "Number of Rows", "rows": row}), 200
    return jsonify({"message": "Table name not found"}), 404


@stats_blueprint.route("/api/v1/stats/interactions/<customer_id>")
def customer_interactions_per_channel_count(customer_id):

    # Get optional date filters from the query parameters
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    channel = request.args.get("channel")

    stats_repo = get_statistics_repository(current_app.config)
    query_result = stats_repo.get_total_interactions_per_customer_and_channel(
        customer_id, start_date, end_date, channel
    )

    result = {"data": {}}
    interactions = {}

    for record in query_result:
        event = record.get("event")
        total_interactions = record.get("total_interactions")
        interactions[event] = total_interactions

    result["data"] = {"customer_id": customer_id, "interactions": interactions}

    return jsonify(result), 200
