import pytest
from src.repository.statistics.postgres import PostgresStatisticsRepository


@pytest.fixture
def test_config():
    return {
        "DB_NAME": "business",
        "DB_USER": "postgres",
        "DB_HOST": "localhost",
        "DB_PASSWORD": "thepassword",
        "DB_PORT": 5432,
    }


def test_check_table_name(test_config):
    stats_repo = PostgresStatisticsRepository(test_config)
    table_name = "business"
    assert stats_repo.check_table_name(table_name) == False


def test_get_row_count(test_config):
    stats_repo = PostgresStatisticsRepository(test_config)
    table_name = "customers"
    print(stats_repo.get_number_of_rows(table_name))
    assert stats_repo.get_number_of_rows(table_name) > 1

def test_check_if_customer_exists(test_config):
    stats_repo = PostgresStatisticsRepository(test_config)
    existing_customer_id=1
    non_existing_customer_id=9999
    assert stats_repo.check_if_customer_exists(existing_customer_id) == True
    assert stats_repo.check_if_customer_exists(non_existing_customer_id) == False

def test_get_total_interactions_per_customer_and_channel(test_config):
    stats_repo = PostgresStatisticsRepository(test_config)

    result = stats_repo.get_total_interactions_per_customer_and_channel(1)
    
    assert isinstance(result, list)
    assert isinstance(result[0], dict)
    assert len(result) > 0
    assert len(result[0].get("event")) > 1

def test_get_total_interactions_with_date_filter(test_config):
    stats_repo = PostgresStatisticsRepository(test_config)

    result = stats_repo.get_total_interactions_per_customer_and_channel(
        1, start_date="2019-10-01", end_date="2020-02-15"
    )
    
    assert isinstance(result, list)
    assert isinstance(result[0], dict)
    assert len(result) > 0
    assert len(result[0].get("event")) > 1