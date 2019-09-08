FROM alpine
MAINTAINER bouweceunen

RUN apk update \
  && apk add --update --no-cache curl python py-pip \
  && pip install idna\<2.6 requests==2.21.0 kubernetes logging

COPY policy.py policy.py
