import requests


def test_get_wrong_table(base_url):
    table_name = "wrong_table"
    response = requests.get(f"{base_url}/api/v1/stats/{table_name}")
    assert response.status_code == 404, f"Response text: {response.text}"

def test_number_of_customers(base_url):
    table_name = "customers"
    response = requests.get(f"{base_url}/api/v1/stats/{table_name}")
    assert response.status_code == 200, f"Response text: {response.text}"
    assert response.json()["rows"] > 0, f"Response text: {response.text}"

def test_existing_customer_interactions_per_channel(base_url):
    customer_id = 4
    response = requests.get(f"{base_url}/api/v1/stats/interactions/{customer_id}")
    assert response.status_code == 200
    json_response = response.json()
    assert "data" in json_response
    assert "interactions" in json_response.get("data")
    assert json_response["data"]["customer_id"] == 4

def test_customer_not_found(base_url):
    customer_id = 9999
    response = requests.get(f"{base_url}/api/v1/stats/interactions/{customer_id}")
    assert response.status_code == 404

def test_invalid_customer(base_url):
    customer_id = "abc"
    response = requests.get(f"{base_url}/api/v1/stats/interactions/{customer_id}")
    assert response.status_code == 400

def test_invalid_date_format(base_url):
    start_date = "20200113"
    response = requests.get(f"{base_url}/api/v1/stats/interactions/4?start_date={start_date}")
    assert response.status_code == 400
    json_response = response.json()
    assert json_response.get("error") == "Invalid start_date format. Use YYYY-MM-DD."

def test_invalid_date_range(base_url):
    start_date = "2020-01-01"
    end_date = "2019-02-15"
    response = requests.get(f"{base_url}/api/v1/stats/interactions/4?start_date={start_date}&end_date={end_date}")
    assert response.status_code == 400
    json_response = response.json()
    assert json_response.get("error") == "start_date cannot be later than end_date."

def test_valid_date_range(base_url):
    start_date = "2019-01-01"
    end_date = "2020-02-15"
    response = requests.get(f"{base_url}/api/v1/stats/interactions/4?start_date={start_date}&end_date={end_date}")
    assert response.status_code == 200
    json_response = response.json()
    assert "data" in json_response
    assert "interactions" in json_response.get("data")