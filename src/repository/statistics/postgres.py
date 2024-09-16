from ..base import statisticsRepository
from ...utils.db.postgres import QueryRunner
from ...config import Config
from datetime import datetime

TABLES = ["customers", "products", "interactions"]

TABLE_COUNT_SQL = """SELECT COUNT(*) FROM %(table_name)s; """

CHECK_CUSTOMER_SQL = (
    """SELECT customer_id FROM customers WHERE customer_id = %(customer_id)s """
)


class PostgresStatisticsRepository(statisticsRepository):
    def __init__(self, config: Config):
        self.runner = QueryRunner(config)

    def get_number_of_rows(self, table_name) -> int:
        """
        Return the number of content entries in the database.

        Returns:
            Integer with the number of content entries.
        """

        result = self.runner.execute_query(
            TABLE_COUNT_SQL, params={"table_name": table_name}, return_dict=False
        )
        return result[0][0]

    def check_table_name(self, table_name) -> bool:
        return table_name in TABLES

    def get_total_interactions_per_customer_and_channel(
        self, customer_id, start_date=None, end_date=None
    ):
        """
        Compute the number of interactions per customer per channel.

        Returns:
            List of dictionaries with the total customer interactions per channel.

        """
        CUSTOMER_INTERACTIONS_PER_CHANNEL_SQL = """
        WITH all_events AS
        (
        SELECT
            DISTINCT event
            FROM interactions
        ),

        compute_existing_interactions AS (
        SELECT
            c.customer_id,
            i.event,
            COUNT(*) AS total_interactions
        FROM customers AS c
        LEFT JOIN interactions AS i
        ON c.customer_id = i.customer_id
        WHERE c.customer_id = %(customer_id)s
        """

        query_params = {"customer_id": customer_id}

        # Apply date filters if provided
        if start_date:
            CUSTOMER_INTERACTIONS_PER_CHANNEL_SQL += (
                " AND i.date_start >= %(start_date)s"
            )
            query_params["start_date"] = start_date
        if end_date:
            CUSTOMER_INTERACTIONS_PER_CHANNEL_SQL += " AND i.date_start <= %(end_date)s"
            query_params["end_date"] = end_date

        CUSTOMER_INTERACTIONS_PER_CHANNEL_SQL += """
        GROUP BY
            c.customer_id,
            i.event
        )

        SELECT
            cei.customer_id,
            e.event,
            COALESCE(cei.total_interactions, 0) AS total_interactions
        FROM all_events AS e
        LEFT JOIN compute_existing_interactions AS cei
        ON e.event = cei.event
        """

        result = self.runner.execute_query(
            CUSTOMER_INTERACTIONS_PER_CHANNEL_SQL, params=query_params
        )
        return result

    def check_if_customer_exists(self, customer_id) -> bool:
        result = self.runner.execute_query(
            CHECK_CUSTOMER_SQL, params={"customer_id": customer_id}
        )
        return True if result else False
