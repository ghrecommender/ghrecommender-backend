FROM alpine:3.6

ENV base_dir /srv/github

# ToDo: https://github.com/vishnubob/wait-for-it/pull/6
ADD https://raw.githubusercontent.com/iturgeon/wait-for-it/8f52a814ef0cc70820b87fbf888273f3aa7f5a9b/wait-for-it.sh /bin

RUN apk --update add bash make ca-certificates \
    && apk --update add python uwsgi uwsgi-python py-pip py-psycopg2 \
    && pip install --upgrade pipenv \

    # cleanup
    && rm -rf /var/cache/apk/* \

    # prepare
    && chmod +x /bin/wait-for-it.sh

WORKDIR ${base_dir}

ADD ["./Pipfile", "./Pipfile.lock", "$base_dir/"]

RUN pipenv install --verbose --system \
    && rm -rf /root/.cache/pip/

# ADD . $base_dir

ADD ["Makefile", "wait-for-it.sh", "docker-entrypoint.sh", "$base_dir/"]
ADD ["conf", "$base_dir/conf/"]
ADD ["src", "$base_dir/src/"]

EXPOSE 8000
VOLUME /srv/github/src/static
CMD sh docker-entrypoint.sh
