FROM alpine
MAINTAINER bouweceunen

RUN apk update && apk add --update --no-cache curl certbot python3 py-pip
RUN pip3 install idna\<2.6 requests==2.21.0 kubernetes boto3
RUN ln -s /usr/bin/python3 /usr/bin/python

COPY policy.py policy.py
