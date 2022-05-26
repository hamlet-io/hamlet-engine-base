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

## Release Process

An automated build of the engine is generated each night and published to the container registry. The builds are tagged based on the date the image was created.
Each of these releases are considered as releases candidates for the next release.

The current release is defined in the `engine.ini` file which specifies the details of the specific engine version to release

### Creating a release

1. Determine the current tram release that will be the candidate. You can see all of the available releases with `hamlet engine list-engines --location hidden`
1. Install the engine into your local hamlet install and perform some basic checks on the release candidate (rc) engine
    - `hamlet engine install-engine <rc engine name> --location hidden`
    - `hamlet --engine <rc engine name> -i mock -p aws -p awstest reference list-references`
    - `hamlet --engine <rc engine name> -i mock -p aws -p awstest deploy list-deployments`
    - `hamlet --engine <rc engine name> -i mock -p aws -p awstest layer list-layers`
1. Select the release from the root of this repo run `hamlet engine describe-engine < the name of the selected release> --location installed`
1. From the `describe-engine` result, use the `build_metadata` section to obtain the digests of the container image sources that will be included in the release. There are a few
ways to do this based on the `code_source` `revision` attribute (git commit) value or the corresponding short commit value;
   1. Tag the code repos with the release version
      1. tag each repo with the `x.x.x` release version at the commit (this is also useful in mantaining the changelog information in the repos)
      1. wait for the release action to run
      2. follow the steps in the next alternative, but look for the image tagged with the version number
   1. Lookup the digests in the source repos based on the revision information
      1. Use the revision to find the image in the `Packages` section of the `Code` tab
      1. The image will be tagged `sha-{short commit}`
      1. Click on the elipses next to `Digest` on the entry to obtain the digest
   1. Use docker to look up details of the image built at the time of the git commit based on the `sha-{short commit}` tag
      1. Pull the image
          ```bash
          docker pull ghcr.io/hamlet-io/{repo}:sha-{short commit}
          ```
      1. Inspect the image
          ```bash
          docker inspect ghcr.io/hamlet-io/{repo}:sha-{short commit}
          ```
      2. Obtain the digest from the `RepoDigests` attribute
1. Update the `engine.ini` file in the root of the repo with the digests for the `hamlet_train_release` engine
1. Commit the latest engine selection to the repo
1. Tag the repo with the version of the release
1. Push the commit for the engine state and the tags

    ```bash
    git push --tags
    ```

1. The github workflow will then create the container image, and push to both the `latest` tag and to the version tag

### Updating the changelogs

In order to ensure the changelogs in each repo correctly reflects what was added in each release, each repo needs to be
tagged with the release version at the commit listed in the `describe-engine` result

1. Follow the instructions in the section on "Creating a release" to determine the revision
1. Tag the repo at the revision with the `x.x.x` version
1. Trigger the `changelog` action to update the `chore: update changelog` pull request
1. Merge the `chore: update changelog` pull request (the next commit will trigger the recreation of this pull request)