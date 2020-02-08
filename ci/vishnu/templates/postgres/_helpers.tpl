{{/* vim: set filetype=mustache: */}}
{{/*
Expand the name of the chart.
*/}}
{{- define "vishnu.postgres.name" -}}
{{- $name := default .Chart.Name .Values.nameOverride | trunc 57 | trimSuffix "-" -}}
{{- printf "%s-%s" $name "postgres" -}}
{{- end -}}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "vishnu.postgres.fullname" -}}
{{- if .Values.fullnameOverride -}}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- $name := default .Chart.Name .Values.nameOverride -}}
{{- if contains $name .Release.Name -}}
{{- .Release.Name | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- printf "%s-%s-%s" .Release.Name $name "postgres" | trunc 63 | trimSuffix "-" -}}
{{- end -}}
{{- end -}}
{{- end -}}

{{- define "vishnu.postgres.username" -}}
{{- "vishnu" -}}
{{- end -}}

{{- define "vishnu.postgres.pvc" -}}
{{- "vishnu-pvc-postgresql" -}}
{{- end -}}
