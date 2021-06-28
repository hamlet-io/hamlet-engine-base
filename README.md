# hamlet-engine-base

The base hamlet engine build, this repo contains the build and testing process that we use to create the official base releases of the hamlet engine.
The artefacts from this repo are published as docker images and provide fully tested compatible versions of different components which make up the hamlet engine

The image is intended to be used as an engine by the hamlet cli to provide production ready images of hamlet that you can get going with.

## Contents

The hamlet engine base is made up of the following components

| Part Type           | Repo                                             |
|---------------------|--------------------------------------------------|
| engine-wrapper      | https://github.com/hamlet-io/engine-core         |
| engine-core         | https://github.com/hamlet-io/engine              |
| engine-plugin-aws   | https://github.com/hamlet-io/engine-plugin-aws   |
| engine-plugin-azure | https://github.com/hamlet-io/engine-plugin-azure |
| executor-bash       | https://github.com/hamlet-io/executor-bash       |

## Requirements

To be part of the base engine we each part must have testing and provide a core or commonly used purpose within hamlet deployments

## Releases

The hamlet-engine-base produces a collection of images based on different requirements. Each of them are published as tags on the `ghcr.io/hamlet-io/hamlet-engine-base` container image

- **nightly:** The tram build is a nightly build of the latest images from each of the parts
- **stable:** The latest released version of the hamlet-engine-base image. This is the release we recommended as it has been thoroughly tested and allows you to keep up with the latest changes to hamlet
- **x.x.x:** A fixed version of the hamlet-engine-base. The release tags follow semver and provide a locked version for stability

## Build Process

- As this repo doesn't have code itself, we use the hamlet engine process to pull in the latest releases from each of the official part repos.
- We then run the test suites for each of the components in full and fail the build on any test failures
- We then perform some canary tests across the plugins to make sure standard functionality works as expected
  - The full schema set is generated for all providers
  - A collection of entrances are invoked across the test providers to ensure they work as expected and might not be caught by testing
  - Generate a full cmdb set and use the whatif provider to generate default templates included in the engine
- A new docker image is then created using the images
