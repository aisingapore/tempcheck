FROM python:3.6.9-slim

ARG APP_DIR=/opt/vishnu
WORKDIR $APP_DIR

ARG APP_USER=vishnu
ARG APP_USER_ID=1000

RUN groupadd -r --gid $APP_USER_ID $APP_USER && \
    useradd --no-log-init -r -m --uid $APP_USER_ID -g $APP_USER $APP_USER


RUN apt-get update && apt-get install -y gcc libpq-dev

COPY templates templates
COPY vishnu vishnu
COPY requirements.txt scripts/start_app.sh manage.py ./
COPY frontend frontend

ENV VIRTUAL_ENV=$APP_DIR/venv

RUN python3 -m venv venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN pip install -r requirements.txt && \
    python3 manage.py collectstatic

RUN chown -R $APP_USER:$APP_USER $APP_DIR

USER vishnu

EXPOSE 8000

CMD ["./start_app.sh"]