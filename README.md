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

------------------------------------------------------------------
Jira Ticket
------------------------------------------------------------------

Title: Improve API with customer interactions metrics

**Mandatory:**
- Review the provided business requirements and note down any assumptions or questions to clarify during the team meeting.
- Add new database migration with improved schema.
- Create a new API endpoint to serve customer interaction metrics.
- Add filtering options to the endpoint (e.g., filter by channel, date, customer, or customer type).
- Refactor testing.
- Document the system architecture and improvements to present to the business stakeholders.

**(Optional) Data Engineer XP Boost: Learning and Career Growth:**
- Create a basic CI/CD pipeline to automate testing and deployment of the API.
- Create a autho method for the API.
- Add detailed logging for better monitoring and debugging.
- Refactor to use different database management library.
- Implement an automated alert for anomalies in customer interactions.

Definition of done:

------------------------------------------------------------------

## Overview

## Assumptions
1. **Customers table and External interactions table:**
    - It is reasonable to assume there is a relationship between the tables using the customer ID.
    - This is sufficient to compute the results to return the API response presented as the example.
2. **Products of discussion table:**
    - It is unclear how to utilize it.
    - Not possible to ensure a relatioship between the **Date** field in this table and the **Date Start** field in the External Interactions table.
    - There is no explicit ID linking the product to a specific customer. 
    - Assuming a relationship without confirming with the stakeholders could lead to wrong/misleading results.
3. **API Response:**
    - All possible channels should be displayed for each customer, even if there was no interaction via a certain channel.

## Approach

## Challenges

## Next Steps
- **Proposal for Future Improvements:**
    - API: add the possibility to retrieve the results for all customers at once (instead of selecting a single customer ID).
    - Products of discussion table: confirm the meaning/purpose of the table. Add unique ID to ensure data integrity.
    - Create new endpoints to provide higher level metrics:
        - Number of interactions per channel.
