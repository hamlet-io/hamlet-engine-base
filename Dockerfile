FROM python:3.9-slim-buster as builder

ARG HAMLET_ENGINE="unicycle"

USER root
RUN pip install hamlet

WORKDIR /build/
ENV HAMLET_ENGINE_DIR='/build/'
RUN hamlet engine install-engine

# Copy the latest into the container
FROM scratch as unicycle_package

COPY --from=builder /build/engines/unicycle/engine-core          /engine-core
COPY --from=builder /build/engines/unicycle/engine               /engine
COPY --from=builder /build/engines/unicycle/engine-plugin-aws    /engine-plugin-aws
COPY --from=builder /build/engines/unicycle/engine-plugin-azure  /engine-plugin-azure
COPY --from=builder /build/engines/unicycle/executor-bash        /executor-bash

# Copy the provided tram package into the repository
FROM scratch as release_package

ARG HAMLET_ENGINE="unicycle"

COPY --from=builder /build/engine/engines/${HAMLET_ENGINE}/hamlet-engine-base/engine-core          /engine-core
COPY --from=builder /build/engine/engines/${HAMLET_ENGINE}/hamlet-engine-base/engine               /engine
COPY --from=builder /build/engine/engines/${HAMLET_ENGINE}/hamlet-engine-base/engine-plugin-aws    /engine-plugin-aws
COPY --from=builder /build/engine/engines/${HAMLET_ENGINE}/hamlet-engine-base/engine-plugin-azure  /engine-plugin-azure
COPY --from=builder /build/engine/engines/${HAMLET_ENGINE}/hamlet-engine-base/executor-bash        /executor-bash
