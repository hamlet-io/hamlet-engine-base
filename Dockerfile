FROM openjdk:8-slim-buster AS builder
COPY --from=python:3.8-slim-buster / /

ARG engine=unicycle

USER root

RUN apt-get update && apt-get install -y \
        jq dos2unix

RUN pip3 install hamlet

WORKDIR /build/

ENV HAMLET_HOME_DIR='/build/'

RUN [ "${engine}" != "unicyle" ] && hamlet engine install-engine "unicycle"
RUN [ "${engine}" != "tram" ] && hamlet engine install-engine "tram"
RUN hamlet engine set-engine "${engine}"

# Copy the latest into the container
FROM scratch as unicycle_package

COPY --from=builder /build/engine/engines/unicycle/engine-core          /engine-core
COPY --from=builder /build/engine/engines/unicycle/engine               /engine
COPY --from=builder /build/engine/engines/unicycle/engine-plugin-aws    /engine-plugin-aws
COPY --from=builder /build/engine/engines/unicycle/engine-plugin-azure  /engine-plugin-azure
COPY --from=builder /build/engine/engines/unicycle/executor-bash        /executor-bash

# Copy the provided tram package into the repository
FROM scratch as release_package

ARG engine="tram"

COPY --from=builder /build/engine/engines/${engine}/hamlet-engine-base/engine-core          /engine-core
COPY --from=builder /build/engine/engines/${engine}/hamlet-engine-base/engine               /engine
COPY --from=builder /build/engine/engines/${engine}/hamlet-engine-base/engine-plugin-aws    /engine-plugin-aws
COPY --from=builder /build/engine/engines/${engine}/hamlet-engine-base/engine-plugin-azure  /engine-plugin-azure
COPY --from=builder /build/engine/engines/${engine}/hamlet-engine-base/executor-bash        /executor-bash
