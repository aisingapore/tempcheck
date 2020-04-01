FROM docker-registry.int.aisingapore.org/gitlab-runner-base:latest

RUN curl -sL https://deb.nodesource.com/setup_12.x | bash - && \
    apt-get install nodejs

RUN curl -LO https://get.helm.sh/helm-v3.0.0-linux-amd64.tar.gz && \
    tar -zxf helm-v3.0.0-linux-amd64.tar.gz && \
    mv linux-amd64/helm /usr/local/bin/helm

# Do not update skaffold version. v1.5 and above will not work correctly with helm 3
# when deploying across namespaces in same kube-context
RUN curl -Lo skaffold https://storage.googleapis.com/skaffold/releases/v1.4.0/skaffold-linux-amd64 && \
    chmod +x skaffold && \
    mv skaffold /usr/local/bin

RUN apt-get update && apt-get install -y libpq-dev

RUN helm repo add stable https://kubernetes-charts.storage.googleapis.com