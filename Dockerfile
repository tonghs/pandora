# 遵循下厨房 Docker 规范
# 详见：https://github.com/xiachufang/sa/blob/master/docker/README.md
#
# docker build . -t registry.xiachufang.com/xiachufang/pandora:latest

FROM registry.xiachufang.com/library/python:3.6

ENV CODEDIR=/opt/code VENVDIR=/opt/venv

WORKDIR "${CODEDIR}"

COPY Pipfile Pipfile.lock "${CODEDIR}/"

RUN set -ex \
    && buildDeps=" \
        gcc \
        git \
        python3-dev \
    " \
    && runDeps=" \
        libexpat1 \
        libmysqlclient-dev \
    " \
    && apt-get update && apt-get install -y --no-install-recommends $buildDeps $runDeps && rm -rf /var/lib/apt/lists/* \
    && pipenv install --deploy && ln -f -s "$(pipenv --venv)" "${VENVDIR}" \
    && uWSGIDeps=" \
        git+https://github.com/ushuz/uwsgimon@0.7.0+launcher.1 \
    " \
    && ${VENVDIR}/bin/pip install $uWSGIDeps \
    && apt-get purge -y --auto-remove $buildDeps \
    && rm -rf $HOME/.cache

COPY . "${CODEDIR}"

EXPOSE 9999

ENV PATH="${VENVDIR}/bin:${PATH}" \
    PYTHONPATH="${CODEDIR}"

ENV C_FORCE_ROOT=true \
    UWSGI_MODULE=wsgi:app \
    UWSGI_WORKERS=4 \
    UWSGI_HTTP=:9999 \
    UWSGI_HTTP_KEEPALIVE=1 \
    UWSGI_ADD_HEADER="Connection: Keep-Alive" \
    UWSGIMON_ROLE=pandora

CMD uwsgimon-launcher
