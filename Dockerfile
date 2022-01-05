FROM alpine:3.14 AS builder

ARG REGISTRY_NAME
ARG MARVIN_VERSION

RUN echo "https://dl-cdn.alpinelinux.org/alpine/v3.14/main" >/etc/apk/repositories
RUN echo "https://dl-cdn.alpinelinux.org/alpine/v3.14/community" >>/etc/apk/repositories
RUN apk update
RUN apk add bash curl git grep make

RUN mkdir /toolbox /macrocode

COPY . /macrocode

WORKDIR /macrocode

# Actual analyzer build step
# All analyzers are expected to have a Makefile inside the .deepsource/analyzer directory in the repo
RUN cd .deepsource/analyzer && make build

FROM $REGISTRY_NAME/marvin:$MARVIN

RUN apt-get update

COPY --from=builder /app /app
COPY --from=builder /toolbox /toolbox

RUN ln -s /usr/local/bin/python3 /usr/bin/python3

RUN chmod -R o-rwx /code /toolbox
RUN chown -R 1000:3000 /toolbox /code
RUN useradd -u 1000 runner && \
	mkdir -p /home/runner && \
	chown -R 1000:3000 /home/runner

WORKDIR /app

USER 1000
