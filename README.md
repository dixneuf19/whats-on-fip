# What's on FIP ?

[![TestS](https://github.com/dixneuf19/whats-on-fip/actions/workflows/test.yaml/badge.svg)](https://github.com/dixneuf19/whats-on-fip/actions/workflows/test.yaml) [![CD](https://github.com/dixneuf19/whats-on-fip/actions/workflows/build-and-release.yaml/badge.svg)](https://github.com/dixneuf19/whats-on-fip/actions/workflows/build-and-release.yaml) [![codecov](https://codecov.io/gh/dixneuf19/whats-on-fip/branch/master/graph/badge.svg?token=40722DSHFS)](https://codecov.io/gh/dixneuf19/whats-on-fip)
## Local development

You can build the *Docker* image with `make build` and then run it with `make run`.

The app is available at <http://localhost:8000>.

## Create k8s secret

Add your RADIO_FRANCE_API_TOKEN token into your `.env` file for development (**don't commit this file**).

Then you can create the secret with `kubectl create secret generic radio-france-api-token --from-env-file=.env`.
