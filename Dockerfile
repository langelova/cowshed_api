FROM python:3.11-alpine

WORKDIR /app

# prevent Python from writting .pyc files
ENV PYTHONDONTWRITEBYTECODE 1

# ensure Python output is sent to the terminal
ENV PYTHONBUFFERED 1

COPY requirements.txt .

RUN pip install --upgrade pip
COPY ./requirements.txt /app/requirements.txt

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client jpeg-dev && \
    apk add --update --no-cache --virtual .tmp-build-deps \
    build-base postgresql-dev musl-dev zlib zlib-dev && \
    /py/bin/pip install -r requirements.txt && \
    rm -rf /tmp && \
    apk del .tmp-build-deps


# RUN pip install -r requirements.txt
ENV PATH="/py/bin:$PATH"

COPY ./entrypoint.sh /app/entrypoint.sh

COPY . /app/

ENTRYPOINT [ "/app/entrypoint.sh" ]
