# Work Tracker

# Requirements
## Pay attention to the database load and efficiency.

- Using JSON Web Tokens for authentication, which does not rely on storage for session state
- Added a caching layer for the User (for authentication) and ProjectMember (for Work model access control).
  It should be noted that this doesn't capture every mechanism for fetching, but it does handle permission control
- Instrumented database logs to help prove what database calls are being made

## Write readable and well-structured python code.

- I've taken care to maintain readability and maintainability.

## Introduce a good architecture and follow reasonable best practices of your choice.
- I have dockerized the API
- I have set up the project dependencies using docker-compose and moved secrets to an environment file that does not get checked in
- I have created a setup.py file to manage python dependencies
- The framework places tests within the app folder, which has some drawbacks. I have moved these to a separate tests folder where all tests are contained
- Additional configuration options added are defined in settings.py and can be overidden with environment variables
- I have created a custom auth user which is used to facilitate caching, and can be extended as needed

## Make sure to document your code wherever appropriate.

- Tests are thoroughly documented
- Code is documented when where approriate, but is generally straight forward enough to not require it

## Users should be able to see the logs for all users involved in the same project.
## Creating/updating/deleting logs for others is not allowed.
## Please write a few unit tests as a proof-of-concept

- I have written a few API tests
- I have leveraged core features of pytest such as markers, parametrization, conftest, and fixtures

## Setup Instructions

### Set up environment variables
`cp env.sample .env`
 Update `.env` with a more secure password

### Build docker images
`docker compose build`

## Running instructions

`docker compose up`

### Migrate the database

`docker compose exec work_tracker_api bin/migrate-db.sh`

### Start the API

## Running

Open in browser: `localhost:8080`

# Developer Workflows

## Formatting

- `black worktracker tests`
- `isort worktracker tests`
- `flake8`