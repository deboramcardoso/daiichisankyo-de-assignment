# Description 
Congratulations you have inherited the following project! The scenario is as follows:

Some super important business data has been imported from their super secret location in an excel file into the database. For reasons unknown it couldn't come from a better source :(. The data is typical customer data that is similar but not exactly the same as the data in the crm database. Therefore the will most likely need to be some data cleaning and transformation, plus future updates.

The data is as follows:

Customers
| Customer_Id | Occupation   | Type   |
|-------------|--------------|--------|
| 1           | Jedi         | Red    |
| 2           | Batman       | Orange |
| 3           | Santa Claus  | Blue   |
| 11          | Doctor       | Orange |
| 12          | Plummer      | Red    |

External interactions
| Date Start         | Interaction | Customers |
|--------------------|-------------|-----------|
| 04/10/2019 09:00   | Email       | 1         |
| 11/02/2020 16:10   | Call        | 4         |
| 05/03/2020 11:23   | Bird        | 4         |
| 04/06/2021 13:01   | Email       | 3         |

Products of discussion
| Date    | Product |
|---------|---------|
| 01-2019 | Sand    |
| 02-2019 | Sand    |
| 10-2021 | Orange  |


The business folks would really like to have an updated website to provide the number of interactions for different types. To do this the previous data engineer was half way creating a flask api. The api currently only returns some statistics on the data. They want to know per customer how many times per channel were they talking about a certain topic.

- API endpoint: /api/v1/interactions/{customer_id}
- Request: GET
- Response: 
```json
{
    "data": {
        "customer_id": 1,
        "interactions": {
            "Email": 1,
            "Call": 0,
            "Bird": 0
        }
    }
}
```

- The previous hypothetical developer left a couple of tests in the tests folder. To check if the local docker step works.
    - To check your database is there: ```pytest tests/intergration/utils/db/test_postgres.py```
    - To check test the api: ```pytest tests/intergration/test_app.py```
    - To test the factory methods for calling statistics ```pytest tests/intergration/repository/statistics/test_postgres.py```

- Requirements can be found in the pyproject.toml. Requirements are managed via pip-tools.

- The last developer left a helpful shell script to get the database up and running. 
    - ```./start_local_db_docker.sh``` 

- The required items for this project will be: 
    - Python 
    - Docker (Or podman if you like a little spice in your life).

- To build the full application you can run the following command:
    - 1) ```docker-compose up --build``` (Note: for podman ```podman compose -f "docker-compose.yml" up -d --build```  )
    
    - 2) ```yoyo apply artifacts/migrations```

    - 3) ```pytest .``` 

- To remove the containers and images.
    - ```docker-compose down --rmi all``` or ```podman compose down```


# Getting Started

- The main goal of this project is to get the api up and running. The api should be able to return the number of interactions per customer per channel. The api should be stable and have tests.

- So taking into account life is short. Create your own jira (Just a description of work related to a small increment in achieving the desired goal talked about above) ticket related to this project. And create a PR related to some work conducted in relation to your ticket.

- Side Note:
    - Please don't work too hard, Ill feel bad.
    - Please ask any questions you have (90% sure there is an error somewhere).


------------------------------------------------------------------
Example: Jira Ticket - 1
------------------------------------------------------------------

Title: Create landing tables

Setup database to be easily adjustable for future data imports.

- Create a table for customers
- Create a table for external interactions
- Create a table for products of discussion

Management of data model will be managed via code with api repo. Via python yoyo migrations.


Definition of done:

Tables should contain data in a postgres database. Can be accessible to flask app and other users on setup via
a shell script.

------------------------------------------------------------------

Some ticket ideas:
- Create a new endpoint for the api (Like the one above)
- Create a autho method for the api
- Refactor to use different database management library
- Refactor testing.
- Create a CICD pipeline 

Bonus points for:
- Creative ticket ideas.
- Teaching us something new.

Please submit to a git repo and provide link to the repo. The main part of the technical test will be a code review of your PR.
With you walking the team through your code and decisions made.

# Solution

The scope of the Jira ticket presented below was defined based on the context and requirements provided, with a focus on creating a new API endpoint to return customer interaction metrics per channel. The goal was to ensure the new endpoint is robust, meets the business needs, and aligns with the timeline for the ticket, while keeping the scope manageable and focused. Prioritization was given to core functionality, acknowledging that other important tasks, such as authentication and CI/CD, can be addressed in future iterations.

------------------------------------------------------------------
Jira Ticket
------------------------------------------------------------------

**Title**: Improve API with customer interactions metrics

- Review the requirements and note down any assumptions or questions to clarify during the team meeting.
- Add new database migration with improved schema.
- Create a new API endpoint to serve customer interaction metrics.
- Add date filtering options to the endpoint.
- Add API validations.
- Create new integration tests.
- Document how to utilize the new endpoint and propose improvements/next steps to discuss.

**Definition of done**:

The improved schema has been successfully migrated, and the new API endpoint for customer interaction metrics, including date filtering and validations, is implemented. All integration tests pass, documentation is complete, and business requirements are clarified with agreed next steps.

------------------------------------------------------------------

## Approach

Before the implementation, some time was necessary to prepare and ensure everything was set up correctly. This required three key steps:

1. **Environment Setup**:
The GitHub repository has been set up, the necessary files have been added, a virtual environment has been created, and the provided instructions have been followed to ensure the existing code works smoothly. This included minor adjustments, such as upgrading to Python 3.9 and installing dependencies like `psycopg2`. After these adjustments, the application has been successfully run with the existing endpoint.

2. **Understanding Requirements and Data**:
The given requirements and data have been reviewed, ensuring the understanding of the relationships between tables and identifying any necessary assumptions to be made before starting the implementation. This helped ensure the solution would align with the business needs.

3. **Technical Preparation**:
Due to the lack of direct experience with creating APIs or using Docker, some time was needed to learn general concepts. This provided an important basis for proceeding with the implementation.

Once the preparation was complete, the steps below followed:

- Created a new route for the API endpoint with a simple logic to verify it worked.
- Incrementally added complexity to the code to achieve the desired outcome.
- Implemented filters, validations, and integration tests to ensure robustness.
- Updated the documentation throughout the implementation process to reflect the evolving functionality.

## Assumptions
It is important to highlight the following assumptions to provide clarity and context for certain decisions made during the implementation:

1. **Customers Table and External Interactions Table**:
    - It is assumed that there is a direct relationship between these two tables through the `customer_id`. 
    - This relationship is sufficient to compute the metrics and generate the API response as outlined in the example provided.

2. **Products of Discussion Table**:
    - The purpose and relationship of this table are unclear. 
    - It is not possible to establish a direct connection between the `Date` field in this table and the `Date Start` field in the External Interactions table. 
    - Additionally, there is no explicit `ID` linking the product to a specific customer. 
    - Assuming a relationship without further clarification from stakeholders could lead to inaccurate or misleading results.
    - Therefore, the table will not be used for this context.

3. **API Response**:
    - The API should display all possible channels for the selected customer, even if there are no interactions recorded via a particular channel.
    - Since all channels should be displayed, it does not make sense to have the option to filter the result by channel.

## API Usage Instructions
- **Endpoint:** `/api/v1/stats/interactions/<customer_id>`
- **Method:** `GET`
- **Description:** Retrieves the total number of interactions for a selected customer across different channels. Optional query parameters can be used to filter the interactions by date.

**Parameters:**

1. **Path Parameter:**
- `customer_id` (required): The unique identifier of the customer.
    - **Type:** Integer
    - **Example:** `4`
2. **Query Parameters:** (optional)
- `start_date`
    - **Type:** String (format: `YYYY-MM-DD`)
    - **Example:** `2019-10-01`
- `end_date`
    - **Type:** String (format: `YYYY-MM-DD`)
    - **Example:** `2020-03-05`

**Example Request**

- **URL:** `/api/v1/stats/interactions/4?start_date=2019-10-01&end_date=2020-03-05`

**Response:**
- **200 Success**

**Example Response:**

```json
{
    "data": {
        "customer_id": 4,
        "interactions": {
            "Bird": 1,
            "Boat": 0,
            "Call": 1,
            "Email": 0,
            "Post": 0
        }
    }
}
```

- **Error Responses:**

1. **400 Bad Request**
- If `customer_id` is invalid (e.g., not a positive integer) or if the date format is incorrect.

**Example Responses:**

```json
{
    "error": "Invalid customer_id provided"
}
```
```json
{
    "error": "Invalid start_date format. Use YYYY-MM-DD."
}
```
2. **404 Not Found**
- If the specified `customer_id` does not exist in the database.

**Example Response:**

```json
{
    "error": "Customer not found"
}
```

## Next Steps
- **To align with stakeholders/in the team meeting:**
    - Is there a relationship between the Products of discussion table and the External Interactions table?
    - If confirmed that the product of discussion is the topic related to a customer interaction, would it make sense to include as an additional filter option?
    - What is the meaning of each customer type? Is it possible for a customer to change its type?

- **Proposal for future improvements:**
    - **New endpoints to provide higher level metrics**
        - Number of interactions per customer.
        - Number of interactions per channel.
        - Number of interactions per topic of discussion (if confirmed the relationship).
        - Number of interactions per customer type.
        - Number of customers per customer type.
    - **Products of discussion table:** 
        - Add unique ID to ensure data integrity.
    - **Analytics:**
        - If there is an interest in a more in-depth analysis that other teams could work on, we could add the possibility of retrieving the results for all customers simultaneously (instead of selecting a single customer ID).
        - Customized dashboards could be created and a historical analysis could be performed.

**Notes:** 
1. Having this alignment is important for refining the current solution and defining the project’s timeline. Once clarified, we can outline future tasks, organize the Jira tickets related to the Jira Epic, and establish a clearer timeline for the overall project, ensuring smooth execution and avoiding potential delays.
2. The proposed new endpoints and higher-level metrics could provide valuable insights for decision-makers, helping to optimize customer engagement strategies and improve operational efficiency. In addition, the suggested analytics enhancements could form the basis of more comprehensive dashboards for internal stakeholders.