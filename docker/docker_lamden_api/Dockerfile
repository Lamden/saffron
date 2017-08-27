FROM alpine

COPY gevent-1.2.1-cp27-cp27mu-linux_x86_64.whl /root/gevent-1.2.1-cp27-cp27mu-linux_x86_64.whl
COPY lxml-3.4.0-cp27-cp27mu-linux_x86_64.whl /root/lxml-3.4.0-cp27-cp27mu-linux_x86_64.whl

RUN apk update \
    && apk add libtool libevent-dev make xz libstdc++ libffi-dev libressl-dev postgresql-dev musl-dev gcc python-dev libxslt pcre libxml2-dev python py-pip ca-certificates py-setuptools \
    && pip install --upgrade pip
RUN pip install /root/gevent-1.2.1-cp27-cp27mu-linux_x86_64.whl
RUN pip install /root/lxml-3.4.0-cp27-cp27mu-linux_x86_64.whl
RUN pip install werkzeug gevent gunicorn
EXPOSE 9001
ENTRYPOINT gunicorn api:application