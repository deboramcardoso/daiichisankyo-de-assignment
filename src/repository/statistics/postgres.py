from ..base import statisticsRepository
from ...utils.db.postgres import QueryRunner
from ...config import Config

TABLES = ["customers", "products", "interactions"]

TABLE_COUNT_SQL = """SELECT COUNT(*) FROM {table_name}; """


class PostgresStatisticsRepository(statisticsRepository):
    def __init__(self, config: Config):
        self.runner = QueryRunner(config)

    def get_number_of_rows(self, table_name) -> int:
        """
        Return the number of content entries in the database.

        Returns:
            Tuple with the number of content entries.
        """

        result = self.runner.execute_query(
            TABLE_COUNT_SQL.format(table_name=table_name), return_dict=False
        )
        return result[0][0]

    def check_table_name(self, table_name) -> bool:
        return table_name in TABLES

    def get_total_interactions_per_customer_and_channel(self, customer_id, start_date=None, end_date=None, channel=None):
        """
        Compute the number of interactions per customer per channel.

        Returns:

        """
        CUSTOMER_INTERACTIONS_PER_CHANNEL_SQL = """
        WITH all_events AS
        (
        SELECT
            DISTINCT event
            FROM interactions
        )

        SELECT
            c.customer_id,
            e.event,
            SUM(CASE WHEN i.event IS NOT NULL THEN 1 ELSE 0 END) AS total_interactions
        FROM customers AS c
        CROSS JOIN all_events AS e
        LEFT JOIN interactions AS i
        ON e.event = i.event
        AND c.customer_id = i.customer_id
        """

        #Apply date filters if provided
        if start_date and end_date:
            CUSTOMER_INTERACTIONS_PER_CHANNEL_SQL += f" AND i.date_start >= '{start_date}' AND i.date_start <= '{end_date}'"
        elif start_date:
            CUSTOMER_INTERACTIONS_PER_CHANNEL_SQL += f" AND i.date_start >= '{start_date}'"
        elif end_date:
            CUSTOMER_INTERACTIONS_PER_CHANNEL_SQL += f" AND i.date_start <= '{end_date}'"

        #Apply channel filter if provided
        if channel:
            CUSTOMER_INTERACTIONS_PER_CHANNEL_SQL += f" AND i.event = '{channel}'"

        CUSTOMER_INTERACTIONS_PER_CHANNEL_SQL += """
        WHERE c.customer_id = {customer_id}
        GROUP BY
            c.customer_id,
            e.event
        """

        result = self.runner.execute_query(
            CUSTOMER_INTERACTIONS_PER_CHANNEL_SQL.format(customer_id=customer_id)
        )
        return result
