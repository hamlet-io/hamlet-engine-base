FROM python:3.9-slim-buster as base

USER root
RUN pip install hamlet
COPY engine.ini /engine.ini

ENV HAMLET_ENGINE_DIR='/build/'
ENV HAMLET_ENGINE_CONFIG='/'


# Build the tram engine
FROM base as tram_builder
RUN hamlet engine install-engine hamlet_tram_release

# Generate the tram container package
FROM scratch as tram_package

COPY --from=tram_builder /build/engines/hamlet_tram_release/tram_core           /engine-core
COPY --from=tram_builder /build/engines/hamlet_tram_release/tram_engine         /engine
COPY --from=tram_builder /build/engines/hamlet_tram_release/tram_bash           /executor-bash
COPY --from=tram_builder /build/engines/hamlet_tram_release/tram_plugin_aws     /engine-plugin-aws
COPY --from=tram_builder /build/engines/hamlet_tram_release/tram_plugin_azure   /engine-plugin-azure


# Build the train engine
FROM base as train_builder
RUN hamlet engine install-engine hamlet_train_release

# Create the train container package
FROM scratch as train_package

COPY --from=train_builder /build/engines/hamlet_train_release/train_core           /engine-core
COPY --from=train_builder /build/engines/hamlet_train_release/train_engine         /engine
COPY --from=train_builder /build/engines/hamlet_train_release/train_bash           /executor-bash
COPY --from=train_builder /build/engines/hamlet_train_release/train_plugin_aws     /engine-plugin-aws
COPY --from=train_builder /build/engines/hamlet_train_release/train_plugin_azure   /engine-plugin-azure
