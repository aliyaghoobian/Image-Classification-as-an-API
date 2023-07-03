# Deploy Kubernetes Cluster

+ Disable SELinux
```bash
$ apt install selinux-utils
$ setenforce 0
$ sed -i --follow-symlinks 's/SELINUX=enforcing/SELINUX=disabled/g' /etc/sysconfig/selinux
```
+ Disable firewall and edit Iptables settings
```bash
$ systemctl disable ufw
$ modprobe br_netfilter
$ echo '1' > /proc/sys/net/bridge/bridge-nf-call-iptables
```
+ Add Kubernetes repository
```bash
$ sudo apt install curl apt-transport-https -y
$ curl -fsSL  https://packages.cloud.google.com/apt/doc/apt-key.gpg|sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/k8s.gpg
$ curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
$ echo "deb https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee /etc/apt/sources.list.d/kubernetes.list
$ apt update
```
+ Installing Docker, Enable and start the service
```bash
$ sudo apt-get update
$ sudo apt-get install ca-certificates curl gnupg
$ sudo install -m 0755 -d /etc/apt/keyrings
$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
$ sudo chmod a+r /etc/apt/keyrings/docker.gpg
$ echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
$ sudo apt-get update
$ sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
$ systemctl enable docker
$ systemctl start docker
```

+ Disable swap
```bash
$ sudo swapoff -a
```
Note: Disable Linux swap space permanently in /etc/fstab. Search for a swap line and add # (hashtag) sign in front of the line.

+ Install kubelet, kubeadm and kubectl, and pin their version
```bash
$ sudo apt update
$ sudo apt install wget curl vim git kubelet kubeadm kubectl -y
$ sudo apt-mark hold kubelet kubeadm kubectl
```

+ Enable and start kubelet service
```bash
$ systemctl enable kubelet
$ systemctl start kubelet
```

+ Overriding default docker debian default /etc/containerd/config.toml:
```bash
$ cat <<EOF | tee /etc/containerd/config.toml
    version = 2
    [plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runc]
    runtime_type = "io.containerd.runc.v2"
    [plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runc.options]
    SystemdCgroup = true	
    EOF

$ systemctl restart containerd
```

+ Overriding default Cantainer-runtime configs
```bash
$ cat <<EOF | tee /etc/crictl.yaml
    runtime-endpoint: "unix:///run/containerd/containerd.sock"
	timeout: 0
	debug: false
    EOF
```

+ Initialize Kubernetes Cluster
```bash
# IP_Address = your master node ip address
$ kubeadm init --pod-network-cidr=10.244.0.0/16 --apiserver-advertise-address=$IP_Address >> cluster_initialized.txt
$ mkdir -p $HOME/.kube
$ cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
```

+ Installing Pod Network using Calico network
```bash
$ kubectl apply -f https://raw.githubusercontent.com/projectcalico/calico/v3.25.0/manifests/calico.yaml
```

Finally, you can join worker nodes to cluster by the similar following command. you can find the exact command in cluster_initialized.txt
```bash
kubeadm join 167.235.50.207:6443 --token x7bpa5.q57gt1wqpt7116fx \
        --discovery-token-ca-cert-hash sha256:0d9ef07367b96f919dfe8ec698ffcbfe2929f784bd373cd9220db17fd0491cf8
```
Note: This command should be run in worker nodes after Docker, Kubelet and Kubectl installation. Also, you need to override default /etc/containerd/config.toml and /etc/crictl.yaml as said before.


