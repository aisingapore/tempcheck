# Introduction

This folder contains artifacts required to deploy the app either
using docker-compose or kubernetes helm charts.

The [vishnu](vishnu) folder contains the helm chart for the app.

## Helm

### Install

Run from this directory

```
helm install vishnu --name=vishnu --namespace=vishnu --set postgresql.password="real password"
```

### Upgrade

```
helm upgrade vishnu --set postgresql.password="real password"
```

You can also run Skaffold for upgrade. Set the following env:

- POSTGRES_PASSWORD
- INGRESS_HOST

Then run below from the base directory of project.

```
skaffold run --namepsace=vishnu
```


## Docker compose

Instructions are in [README](deployment/docker/README.md) under deployment