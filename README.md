# Dropit-Dev-Ops-Home-Assignment


![alt text](images/k8s-architecture.png)



## Create loca K8s cluster using Kind
Prerequisite
- Docker
- [Kind](https://kind.sigs.k8s.io/) cli 
    - Setup [kind cluster with Ingress Controller](https://kind.sigs.k8s.io/docs/user/ingress/), chose Nginx. (There is a GitHub flow after settign self hosted agent)
- [Install cilium cli](https://docs.cilium.io/en/stable/installation/kind/)





## Adding self-hosted runners
![alt text](images/self-hosted-runner-01.png)
![alt text](images/self-hosted-runner-02.png)

```bash
~/actions-runner
❯ ./run.sh

√ Connected to GitHub

Current runner version: '2.320.0'
2024-10-21 20:19:37Z: Listening for Jobs
```
![alt text](images/self-hosted-runner-03.png)



## MongoDB instalation 

### Create namespace
```bash
Dropit-Dev-Ops-Home-Assignment on  main [!] 
❯ kubectl create ns mongodb
namespace/mongodb created

Dropit-Dev-Ops-Home-Assignment on  main [!] 
❯ k get ns
NAME                 STATUS   AGE
default              Active   8d
kube-node-lease      Active   8d
kube-public          Active   8d
kube-system          Active   8d
local-path-storage   Active   8d
mongodb              Active   2s
```


### Install MongoDB Community Operator
```bash
Dropit-Dev-Ops-Home-Assignment on  main [!] took 10s 
❯ helm repo add mongodb-helm-charts https://mongodb.github.io/helm-charts
"mongodb-helm-charts" has been added to your repositories

Dropit-Dev-Ops-Home-Assignment on  main [!] 
❯ helm repo list
NAME                    URL                                  
mongodb-helm-charts     https://mongodb.github.io/helm-charts

Dropit-Dev-Ops-Home-Assignment on  main [!] 
❯ 
```



```bash
❯ helm search repo  mongodb-helm-charts 
NAME
...                                            CHART VERSION   APP VERSION     DESCRIPTION                                       
mongodb-helm-charts/community-operator          0.11.0          0.11.0          MongoDB Kubernetes Community Operator             
...  
```


```bash
❯ helm install my-community-operator mongodb-helm-charts/community-operator --version 0.11.0 --namespace mongodb
NAME: my-community-operator
LAST DEPLOYED: Mon Oct 21 17:48:45 2024
NAMESPACE: mongodb
STATUS: deployed
REVISION: 1
TEST SUITE: None
```
---


### Deploy and Configure a MongoDB Resource
```bash
Dropit-Dev-Ops-Home-Assignment on  main [!?] 
❯ helm template   mongodb-community  mongodb-configuration/mongodb-community-setup/ -n mongodb 
---
# Source: mongodb-community-setup/templates/secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: my-user-password
type: Opaque
stringData:
  password: Q1w2e3r4t5y6
---
# Source: mongodb-community-setup/templates/mongodbcommunity.yaml
apiVersion: mongodbcommunity.mongodb.com/v1
kind: MongoDBCommunity
metadata:
  name: example-mongodb
spec:
  members: 3
  type: ReplicaSet
  version: "6.0.5"
  security:
    authentication:
      modes: ["SCRAM"]
  users:
    - name: my-user
      db: admin
      passwordSecretRef:
        name: my-user-password
      roles:
        - name: clusterAdmin
          db: admin
        - name: userAdminAnyDatabase
          db: admin
      scramCredentialsSecretName: my-scram
  additionalMongodConfig:
    storage.wiredTiger.engineConfig.journalCompressor: zlib
    net:
      port: 40333

Dropit-Dev-Ops-Home-Assignment on  main [!?] 
❯
Dropit-Dev-Ops-Home-Assignment on  main [!?] 
❯ helm upgrade --install  mongodb-community  mongodb-configuration/mongodb-community-setup/ -n mongodb 
Release "mongodb-community" does not exist. Installing it now.
NAME: mongodb-community
LAST DEPLOYED: Mon Oct 21 19:42:32 2024
NAMESPACE: mongodb
STATUS: deployed
REVISION: 1
TEST SUITE: None  
```


### Retrieve the connection string:
```bash
❯ k get secrets -n mongodb my-user-password -n mongodb -o json  | jq -r '.data | with_entries(.value |= @base64d)'
{
  "password": "Q1w2e3r4t5y6"
}

```

### Test mongo Atlas connection from a kubernetes pod with mongosh
```bash
❯ kubectl run tmp-mongosh --image=rtsp/mongosh -n mongodb  --rm -it -- bash
If you don't see a command prompt, try pressing enter.
18:10:25 tmp-mongosh:/# mongosh mongodb://my-user:Q1w2e3r4t5y6@devops-mongodb-svc.mongodb.svc.cluster.local:40333
Current Mongosh Log ID: 671699e6a0c964d374fe6910
Connecting to:          mongodb://<credentials>@devops-mongodb-svc.mongodb.svc.cluster.local:40333/?directConnection=true&appName=mongosh+2.3.2
Using MongoDB:          6.0.5
Using Mongosh:          2.3.2

For mongosh info see: https://www.mongodb.com/docs/mongodb-shell/

devops-mongodb [direct: secondary] test> show dbs
admin   188.00 KiB
config  176.00 KiB
local   508.00 KiB
devops-mongodb [direct: secondary] test>
```



