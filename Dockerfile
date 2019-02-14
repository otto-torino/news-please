FROM python:3.6.5-alpine3.7

RUN mkdir -p /app
WORKDIR /app

COPY ./ .

RUN apk add -U --no-cache curl git make gcc python-dev libffi-dev musl-dev libxml2-dev libxslt-dev openssl-dev zlib-dev jpeg-dev
RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt

COPY docker.sh /
RUN chmod +x /docker.sh

CMD ["/docker.sh"]