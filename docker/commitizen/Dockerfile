FROM python:3-alpine

WORKDIR /app

# Add dependencies
RUN apk add --update -t --no-cache git curl alpine-sdk

RUN ["pip3", "install", "--no-cache-dir", "-U", "Commitizen>=2,<3"]

ADD scripts/ /opt/scripts

ENTRYPOINT ["/opt/scripts/entrypoint"]
