FROM alpine

MAINTAINER james.a.munsch@protonmail.com

RUN apk update && apk add nodejs git curl perl libtool libevent-dev make xz libstdc++ libffi-dev libressl-dev musl-dev gcc python-dev libxslt pcre libxml2-dev python py-pip ca-certificates py-setuptools curl \
    && git clone https://github.com/npm/npm.git \
    && cd npm \
    && /bin/bash ./configure \
    && make install \
    && cd .. \
    && git clone https://github.com/carsenk/explorer \
    && cd explorer \
    && echo '{ "allow_root": true }' > /root/.bowerrc
RUN /usr/bin/npm install -g bower
RUN /usr/bin/npm install
RUN cd /explorer && /explorer/app/node_modules/bower/bin/bower install
RUN rm -rf /usr/local/bin/geth
COPY explorer/package.json /explorer/package.json
COPY explorer/app/app.js /explorer/app/app.js
EXPOSE 8000
WORKDIR "/explorer"
ENTRYPOINT ["/usr/bin/npm", "start"]