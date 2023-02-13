# Work Tracker

# Requirements
## Pay attention to the database load and efficiency.

- Using JSON Web Tokens for authentication, which does not rely on storage for session state
- Added a caching layer for the User (for authentication) and ProjectMember (for Work model access control)
- Instrumented database logs to help prove what database calls are being made

## Write readable and well-structured python code.
## Introduce a good architecture and follow reasonable best practices of your choice.

- The framework places tests within the app folder, which has some drawbacks. I have moved these to a separate tests folder where all tests are contained

## Make sure to document your code wherever appropriate.

- Tests are thoroughly documented
- Code is documented when where approriate, but is generally straight forward enough to not require it

## Users should be able to see the logs for all users involved in the same project.
## Creating/updating/deleting logs for others is not allowed.
## Please write a few unit tests as a proof-of-concept

- I have written a few API tests

## Setup Instructions

### Set up environment variables
`cp env.sample .env`
 Update `.env` with a more secure password

### Build docker images
`docker compose build`

## Running instructions

`docker compose up`

### Migrate the database

`docker compose exec  work_tracker_api bin/migrate-db.sh`

### Start the API

## Running

Open in browser: `localhost:8080`

# Developer Workflows

## Formatting

- `black worktracker tests`
- `isort worktracker tests`