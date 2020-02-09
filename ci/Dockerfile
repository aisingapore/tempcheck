FROM docker-registry.int.aisingapore.org/gitlab-runner-base:latest

RUN curl -sL https://deb.nodesource.com/setup_12.x | bash - && \
    apt-get install nodejs

RUN curl -LO https://get.helm.sh/helm-v2.11.0-linux-amd64.tar.gz && \
    tar -zxf helm-v2.11.0-linux-amd64.tar.gz && \
    mv linux-amd64/helm /usr/local/bin/helm

RUN curl -Lo skaffold https://storage.googleapis.com/skaffold/releases/latest/skaffold-linux-amd64 && \
    chmod +x skaffold && \
    mv skaffold /usr/local/bin && \
    helm init --client-only

RUN apt-get update && apt-get install -y libpq-dev