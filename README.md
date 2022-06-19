# Interview scheduler api
## _using django,postgrsql and docker_

This api can use to add the schedule of candidate and interviewer and a HR can get the available slot for their interview.

## Before trying to test this api

- Docker is needed for this project you can get it [here](https://docs.docker.com/engine/install/ubuntu/)
- Docker compose is also needed [here](https://docs.docker.com/compose/install/)

## Instruction for run the app
 - Clone this repository and pull the code.
 - then inside the folder run:
    ```
    docker-compose up -d --build
    ````
    this do all the tool and library installation and spin up the app.
 - Now we need on more step left that is migration:
    ```
    docker-compose exec web python manage.py migrate
    ```
 - Now the application is fully up you can test the api 😀 🚀.

## Test the api
- In order to test the api open your favourate api testing tool.
- we have 2 api en points available
    ```
    localhost:8000/api/schedule/
    localhost:8000/api/check/
    ```
- The first one is used for adding the time slot of our interviewer/candidate. To test that we need to send a POST request(other requests will be rejected) like
    ```
    {
    "name": "cand",
    "email": "cand@email.com",
    "from_time":"10:00 am",
    "to_time":"2:00 pm",
    "user_type": "interviewer"
    }
    ```
    this example other format of time will be rejected by api.
- The next one is to get the available time for interview you can use it like
    ```
    {
    "candidateEmailId": "cand@email.com",
    "interviewEmailId": "inter@email.com"
    }
    ```