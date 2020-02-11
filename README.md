# Introduction

This is the main repository for the Temperature recording application (codename Vishnu).

## Development

- Setup: Frontend
- Setup: Postgres service
- Setup: Django
- Adding/viewing data in database
- Changing database schema

### Setup: Environment variables

Obtain an `.env` which is a definition of all the environment variables needed for Postgres, Solr and Azure blob storage configurations.

### Setup: Frontend

```bash
cd frontend
```

Run `npm install` if the node_modules don't already exist in your local. Otherwise, run

```bash
npm run serve
```

This starts the webpack server on port 8080 that will serve
the frontend. Any frontend changes should autoreload by default.

The base Django app has been configured to forward frontend requests to the webpack server. This step is **only required for development**. In production, the assets will be built and bundled as one single application.

### Setup: Postgres service

Start a Postgres service in the background by running

```
docker-compose up -d
```

### Setup: Django

First, activate the Python environment using `conda activate` or `venv`. If not available, install using conda or venv.

```bash
# Using conda
conda install -f requirements.txt

# Using venv
python -m venv venv
pip install -r requirements.txt
```

Then run the following:

```bash
python manage.py makemigrations
python manage.py migrate
```

Create a superuser:

```
python manage.py createsuperuser
```

Finally, at the root of the project, run
```
python manage.py runserver
```

This starts the django dev server on http://127.0.0.1:8000/ and should be the
main interface for the app.

### Adding/viewing data in database

TBA

### Changing database schema

If you change the schema of the database, make sure to run: 

`python manage.py makemigrations` 

and
 
`python manage.py migrate`


## Deployment



See [gitlab-ci config](.gitlab-ci.yml)

## APIs

The available APIs can be found under `sensemaker/urls.py`.


## Acknowledgements

This project  is supported by the National Research Foundation, Singapore under its AI Singapore Programme (AISG-RP-2019-050). Any opinions, findings and conclusions or recommendations expressed in this material are those of the author(s) and do not reflect the views of National Research Foundation, Singapore.

<!-- Reference links -->

[1]: https://www.lucidchart.com/publicSegments/view/9643e4df-0c19-483c-a490-5b4fd451e9e5/image.png
