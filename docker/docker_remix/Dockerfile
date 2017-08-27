FROM mhart/alpine-node

MAINTAINER james.a.munsch@protonmail.com

RUN apk update && apk add git curl libtool g++ libevent-dev make xz libstdc++ libffi-dev libressl-dev musl-dev gcc python-dev libxslt pcre libxml2-dev python py-pip ca-certificates py-setuptools \
    && git clone https://github.com/ethereum/remix \
    && cd remix \
    && echo '{ "allow_root": true }' > /root/.bowerrc \
    && npm install -g bower \
    && npm install



EXPOSE 8080
ENTRYPOINT ['npm', 'start']