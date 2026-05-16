{{- define "imageezgen3d.name" -}}
{{- .Chart.Name -}}
{{- end -}}

{{- define "imageezgen3d.fullname" -}}
{{- printf "%s-%s" .Release.Name .Chart.Name | trunc 63 | trimSuffix "-" -}}
{{- end -}}