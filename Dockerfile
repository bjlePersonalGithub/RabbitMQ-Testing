FROM alpine:3.18.6 AS builder

RUN apk update
RUN apk add \
    --update \
    --no-cache \
    gcc \
    make \
    g++ \
    libxslt-dev \
    libpq-dev \
    python3-dev \
    py3-pip 

RUN mkdir -p /requirements/
WORKDIR /requirements/

COPY ./requirements.txt /requirements/
RUN /usr/bin/python -m pip install --upgrade pip
RUN /usr/bin/python -m pip install -r requirements.txt

## Base Layer
FROM alpine:3.18.6

RUN apk update
RUN apk add python3

RUN mkdir -p /app/bin/
WORKDIR /app/bin/

COPY --from=builder /usr/lib/python3.11/site-packages/ /usr/lib/python3.11/site-packages/

COPY ./Source/Python/ /app/bin/

RUN adduser -D appUser
USER appUser

CMD ["/usr/bin/python", "-u", "/app/bin/queue_start.py", "producer"]