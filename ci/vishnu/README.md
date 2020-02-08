# Introduction

This is the helm chart that is used for deploying the vishnu
application.

## Install

Run this one level up from this directory

```
helm install --name=vishnu --namespace=vishnu --set postgresql.password="real password" .
```

## Upgrade

```
helm upgrade vishnu --set postgresql.password="real password" .
```