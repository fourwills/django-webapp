# beats web app

A basic [Django](https://www.djangoproject.com) web app that interfaces with the [Beatport API](https://oauth-api.beatport.com/).

## Prerequisites

This app uses the following:

* [Python 3.5](https://www.python.org)
* [Docker and Docker-Compose](https://www.docker.com)

## About

Docker-Compose will build a web container (django served with uwsgi) and nginx (a reverse proxy). The web app should be accessible at `127.0.0.1` after running the setup.

## Setup 

Run the following:

* `docker-compose build` to create containers
* `docker-compose up` to run containers

Get an API key from [BeatPort API](https://oauth-api.beatport.com/). Place your keys in your ENV or under `env.py` ('web/beats/settings/env.py' by replacing `None`). You will need the following in your environment variables:

* `OAUTH_CONSUMER_KEY`
* `OAUTH_CONSUMER_SECRET`
* `OAUTH_TOKEN`
* `OAUTH_TOKEN_SECRET`

## API Endpoints

There are three main API endpoints:

### API Endpoint 1 - PUT /api/v1/tracks/upload

Accepts a file upload with doc and name, saves to `/var/bp/uploads` dir. Operation is idempotent so the file gets replaced if there is an existing file with the same name. For each upload, a record is inserted into the database.

#### Testing API Endpoint 1

Test with `curl -X PUT -F "doc=@hello.txt" -F "name=afile" 127.0.0.1/api/v1/tracks/upload`. You can find a sample `@hello.txt` file under the 'web/fixtures' dir. You should receive a 202 response.

To verify your file saved under `/var/bp/uploads`:

* `docker ps` and find the `CONTAINER_ID` of `beats_web`.
* `docker exec -t -i <insertContainerId> /bin/bash`
* `cd /var/bp/uploads` and see that `hello.txt` file appears
* `python3 /web/manage.py shell_plus` to enter shell, then run `FileUpload.objects.all()` to find your file name
* `exit` out of the docker container when done

### API Endpoint 2 -  GET /api/v1/tracks/list

The second API endpoint returns a list of tracks with their track names.

#### Testing API Endpoint 2

Test with `curl 127.0.0.1/api/v1/tracks/list` and receive a 200 response with names of tracks.

### API Endpoint 3 - GET /api/v1/tracks/<pk>

The third API endpoint returns a specifc Track and shows additional information (more than just 'name')

#### Testing API Endpoint 3

Test with `curl 127.0.0.1/api/v1/tracks/8650404/` and receive a 200 with details for that specifc track.

## Unit Tests

To run unit tests, run `python manage.py test`.* 
