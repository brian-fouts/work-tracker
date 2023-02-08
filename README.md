# Work Tracker

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