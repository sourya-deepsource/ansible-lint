ARG REGISTRY_NAME
ARG MARVIN_VERSION

FROM $REGISTRY_NAME/marvin:$MARVIN_VERSION AS marvin

FROM cytopia/ansible-lint:5

RUN echo "https://dl-cdn.alpinelinux.org/alpine/v3.14/main" >/etc/apk/repositories
RUN echo "https://dl-cdn.alpinelinux.org/alpine/v3.14/community" >>/etc/apk/repositories
RUN apk update
RUN apk add bash curl git grep make shadow

RUN mkdir -p /toolbox /app /code /artifacts

WORKDIR /code

RUN cp -r . /app

COPY --from=marvin /toolbox/marvin /toolbox/marvin

RUN ls -ltra /toolbox /code /
RUN chmod -R o-rwx /code /toolbox
RUN chown -R 1000:3000 /toolbox /code
RUN ls -ltra /toolbox /code /

RUN useradd -u 1000 runner && \
	mkdir -p /home/runner && \
	chown -R 1000:3000 /home/runner

WORKDIR /app

USER 1000
RUN ls -ltra /toolbox /code /
