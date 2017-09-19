# Build Geth in a stock Go builder container
FROM golang:1.9-alpine as builder

RUN apk add --no-cache make gcc musl-dev linux-headers git

ADD . /go-ethereum
RUN cd /go-ethereum && make geth

# Pull Geth into a second stage deploy alpine container
FROM alpine:latest

RUN apk add --no-cache ca-certificates
COPY --from=builder /go-ethereum/build/bin/geth /usr/local/bin/

EXPOSE 8545 8546 30303 30303/udp
ENTRYPOINT ["geth", "--rpc", "--rpcaddr", "0.0.0.0", "--rpcport", "8545", "--rpccorsdomain", "*", "--datadir", "/root/.ethereum", "--port", "30303", "--rpcapi", "db,eth,net,web3,personal", "--networkid", "1900", "--gasprice", "0", "--mine"]
