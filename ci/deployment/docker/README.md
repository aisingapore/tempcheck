## Building the docker image for the app

Run 

`build.sh`

## Running the app

Run 

`docker-compose up -d`

The app should now be avaliable on the port 8080 or whichever port configured.

#### Note

If the app migration is not applied on startup due to database
not ready, just restart the app using docker.

`docker restart container_id_or_name`

