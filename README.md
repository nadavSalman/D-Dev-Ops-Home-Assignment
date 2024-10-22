# Dropit-Dev-Ops-Home-Assignment


![alt text](images/k8s-architecture.png)



## Create loca K8s cluster using Kind
Prerequisite
- Docker
- [Kind](https://kind.sigs.k8s.io/) cli 
    - Setup [kind cluster with Ingress Controller](https://kind.sigs.k8s.io/docs/user/ingress/), chose Nginx. (There is a GitHub flow after settign self hosted agent)
- [Install cilium cli](https://docs.cilium.io/en/stable/installation/kind/)


## Import Mising Post db data (`sample_airbnb.listingsAndReviews`)

One of the component requirements is: "Import the provided ([Link for Dump](https://www.mongodb.com/docs/atlas/sample-data/sample-training/#std-label-sample-training)) MongoDB Dump into the MongoDB instance in the K8s cluster."

To set up MongoDB for dumping the posts data into the MongoDB instance in the K8s cluster, I created a free-tier MongoDB cluster on MongoDB Atlas. Even though the cluster automatically imported sample data, the database and collection for the posts were missing. I had to find a solution to import this data from an open-source source. Below you can find the steps involved in performing the data import from json file.

Get the json data :

```bash
curl -o listingsAndReviews.json  https://raw.githubusercontent.com/neelabalan/mongodb-sample-dataset/refs/heads/main/sample_airbnb/listingsAndReviews.json
```
Import data using mongoimport cli :

```shell
C:\Users\User\Downloads\mongodb-database-tools-windows-x86_64-100.10.0\mongodb-database-tools-windows-x86_64-100.10.0\bin>dir
 Volume in drive C has no label.
 Volume Serial Number is 7893-8CB2

 Directory of C:\Users\User\Downloads\mongodb-database-tools-windows-x86_64-100.10.0\mongodb-database-tools-windows-x86_64-100.10.0\bin

10/22/2024  08:06 PM    <DIR>          .
10/22/2024  08:02 PM    <DIR>          ..
10/22/2024  08:02 PM        16,588,590 bsondump.exe
10/22/2024  08:06 PM        99,656,721 listingsAndReviews.json
10/22/2024  08:02 PM        23,243,614 mongodump.exe
10/22/2024  08:02 PM        22,831,256 mongoexport.exe
10/22/2024  08:02 PM        22,766,308 mongofiles.exe
10/22/2024  08:02 PM        23,056,766 mongoimport.exe
10/22/2024  08:02 PM        23,771,720 mongorestore.exe
10/22/2024  08:02 PM        22,298,759 mongostat.exe
10/22/2024  08:02 PM        21,782,277 mongotop.exe
               9 File(s)    275,996,011 bytes
               2 Dir(s)  906,911,125,504 bytes free

C:\Users\User\Downloads\mongodb-database-tools-windows-x86_64-100.10.0\mongodb-database-tools-windows-x86_64-100.10.0\bin>mongoimport.exe --drop --uri "mongodb+srv://**********:********@cluster01.ypl06.mongodb.net/?retryWrites=true&w=majority&appName=Cluster01" --db "sample_airbnb" --collection "listingsAndReviews" --file listingsAndReviews.json
2024-10-22T20:14:10.678+0300    connected to: mongodb+srv://[**REDACTED**]@cluster01.ypl06.mongodb.net/?retryWrites=true&w=majority&appName=Cluster01
2024-10-22T20:14:10.796+0300    dropping: sample_airbnb.listingsAndReviews
2024-10-22T20:14:13.688+0300    [#####...................] sample_airbnb.listingsAndReviews     23.3MB/95.0MB (24.5%)
2024-10-22T20:14:16.690+0300    [#####...................] sample_airbnb.listingsAndReviews     23.3MB/95.0MB (24.5%)
2024-10-22T20:14:19.686+0300    [##########..............] sample_airbnb.listingsAndReviews     41.4MB/95.0MB (43.6%)
2024-10-22T20:14:22.692+0300    [##########..............] sample_airbnb.listingsAndReviews     41.4MB/95.0MB (43.6%)
2024-10-22T20:14:25.694+0300    [#############...........] sample_airbnb.listingsAndReviews     53.9MB/95.0MB (56.8%)
2024-10-22T20:14:28.693+0300    [###############.........] sample_airbnb.listingsAndReviews     63.0MB/95.0MB (66.3%)
2024-10-22T20:14:31.688+0300    [###############.........] sample_airbnb.listingsAndReviews     63.0MB/95.0MB (66.3%)
2024-10-22T20:14:34.686+0300    [#####################...] sample_airbnb.listingsAndReviews     83.5MB/95.0MB (87.8%)
2024-10-22T20:14:37.683+0300    [#####################...] sample_airbnb.listingsAndReviews     83.5MB/95.0MB (87.8%)
2024-10-22T20:14:40.685+0300    [########################] sample_airbnb.listingsAndReviews     95.0MB/95.0MB (100.0%)
2024-10-22T20:14:41.270+0300    [########################] sample_airbnb.listingsAndReviews     95.0MB/95.0MB (100.0%)
2024-10-22T20:14:41.271+0300    5555 document(s) imported successfully. 0 document(s) failed to import.

C:\Users\User\Downloads\mongodb-database-tools-windows-x86_64-100.10.0\mongodb-database-tools-windows-x86_64-100.10.0\bin>
```

Validate imported data :
![alt text](images/mongodb-import-sample_airbnb-db.png)




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

Test for local (With compus for example)

```bash
kubectl port-forward svc/devops-mongodb-svc 27017:40333 -n mongodb
mongodb://***:***@localhost:27017
```


## MongoDB Dump & Restore 

Local test for dump data :

```bash

```