# Prometheus and Grafana
In this guide, you can install Prometheus operator and Grafana.

+ Install Helm
```bash
$ sudo apt-get install apt-transport-https
$ echo "deb https://baltocdn.com/helm/stable/debian/ all main" | sudo tee /etc/apt/sources.list.d/helm-stable-debian.list
$ sudo apt-get update
$ sudo apt-get install helm
```
+ Add repositories
```bash
$ helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
$ helm repo add stable https://charts.helm.sh/stable
$ helm repo update
```

+ Install Prometheus Kubernetes
```bash
$ helm install prometheus prometheus-community/kube-prometheus-stack
```
+ Validation
```bash
$ kubectl get pods
default       prometheus-grafana-5b55f9d866-mh7wb                      3/3     Running       0        33h
default       prometheus-kube-prometheus-operator-59454c549d-w4czz     1/1     Running       0        33h
default       prometheus-kube-state-metrics-5db49ccbb8-z4p6h           1/1     Running       0        33h
default       prometheus-prometheus-kube-prometheus-prometheus-0       2/2     Running       0        33h
default       prometheus-prometheus-node-exporter-g9hjm                1/1     Running       0        33h
default       prometheus-prometheus-node-exporter-gcsj9                1/1     Running       0        33h
default       prometheus-prometheus-node-exporter-vb6xq                1/1     Running       0        33h
```

+ Change the type of Grafana service to external accessibility 
```bash
$ kubectl patch svc prometheus-grafana -p '{"spec": {"type": "NodePort"}}'
```

+ Login to Grafana
You can find port of Grafana service and open $IP_Address:$Port in your browser. Use the default credentials:

username: admin

password: prom-operator

+ Provisioning Prometheus as a Grafana data source
It is configured by default. 

Note: A Grafana data source is any place from which Grafana can pull data.

+ Add Dashboard to Grafana
You can create your own custom dashboard in Grafana and you can also use many pre-built templates like node-exporter-full or kube-state-metrics.