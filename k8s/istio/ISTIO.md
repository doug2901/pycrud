helm repo add istio https://istio-release.storage.googleapis.com/charts
helm repo update

helm install istio-base istio/base -n istio-system --set defaultRevision=default --create-namespace --debug

helm install istiod istio/istiod -n istio-system --wait

kubectl label namespace ingress-nginx istio-injection=enabled --overwrite
kubectl rollout restart deployment -n ingress-nginx


nginx.ingress.kubernetes.io/service-upstream: "true"
Client → Ingress NGINX → ClusterIP Service → Envoy sidecar → App

kiali
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.27/samples/addons/prometheus.yaml
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.27/samples/addons/grafana.yaml
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.27/samples/addons/jaeger.yaml
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.27/samples/addons/kiali.yaml