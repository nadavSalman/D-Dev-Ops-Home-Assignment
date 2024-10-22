# Dropit-Dev-Ops-Home-Assignment


![alt text](images/k8s-architecture.png)



## Create loca K8s cluster using Kind
Prerequisite
- Docker
- [Kind](https://kind.sigs.k8s.io/) cli 
    - Setup [kind cluster with Ingress Controller](https://kind.sigs.k8s.io/docs/user/ingress/), chose Nginx. (There is a GitHub flow after settign self hosted agent)
- Optinal - [Install cilium cli](https://docs.cilium.io/en/stable/installation/kind/)


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


Prerequisite
- Add Atlas cluster full URI as GitHub Action secret.


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
  password: ***
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
  "password": "***"
}

```

### Test mongo Atlas connection from a Kubernetes Pod with mongosh
```bash
❯ kubectl run tmp-mongosh --image=rtsp/mongosh -n mongodb  --rm -it -- bash
If you don't see a command prompt, try pressing enter.
18:10:25 tmp-mongosh:/# mongosh mongodb://my-user:***@devops-mongodb-svc.mongodb.svc.cluster.local:40333
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


## MongoDB Dump & Restore (Inside K8s Pod)

setup :
```bash
 kubectl run tmp-mongosh --image=rtsp/mongosh -n mongodb  --rm -it -- bash
```

Dump data (`mongodump`)
```bash
20:39:12 tmp-mongosh:/# mongodump --uri "mongodb+srv://nadavdevops:sQPUhIdPhOumv1pa@cluster01.ypl06.mongodb.net/sample_airbnb?retryWrites=true&w=majority&appName=Cluster01"  --archive > db.dump
2024-10-22T20:39:24.570+0000    writing sample_airbnb.listingsAndReviews to archive on stdout
2024-10-22T20:39:25.354+0000    [........................]  sample_airbnb.listingsAndReviews  0/5555  (0.0%)
2024-10-22T20:39:28.352+0000    [#######.................]  sample_airbnb.listingsAndReviews  1693/5555  (30.5%)
2024-10-22T20:39:31.352+0000    [######################..]  sample_airbnb.listingsAndReviews  5199/5555  (93.6%)
2024-10-22T20:39:31.620+0000    [########################]  sample_airbnb.listingsAndReviews  5555/5555  (100.0%)
2024-10-22T20:39:31.651+0000    done dumping sample_airbnb.listingsAndReviews (5555 documents)
```

Identifiy primary :
```bash
20:46:55 tmp-mongosh:/# PRIMARY_HOST=$(mongosh "mongodb://my-user:***@devops-mongodb-svc.mongodb.svc.cluster.local:40333" --quiet --eval "rs.status()" --json | jq -r '.members[] |
>  select(.stateStr == "PRIMARY") | .name'  | cut -d':' -f1)
20:47:13 tmp-mongosh:/# echo "Primary host: $PRIMARY_HOST"
Primary host: devops-mongodb-1.devops-mongodb-svc.mongodb.svc.cluster.local
```

Load data (`mongorestore`)
```bash
20:47:33 tmp-mongosh:/# mongorestore --uri "mongodb://my-user:***@$PRIMARY_HOST:40333" --archive < db.dump
2024-10-22T20:47:38.055+0000    preparing collections to restore from
2024-10-22T20:47:38.070+0000    reading metadata for sample_airbnb.listingsAndReviews from archive on stdin
2024-10-22T20:47:38.182+0000    restoring sample_airbnb.listingsAndReviews from archive on stdin
2024-10-22T20:47:41.001+0000    sample_airbnb.listingsAndReviews  20.9MB
2024-10-22T20:47:44.000+0000    sample_airbnb.listingsAndReviews  38.1MB
2024-10-22T20:47:47.000+0000    sample_airbnb.listingsAndReviews  50.5MB
2024-10-22T20:47:50.000+0000    sample_airbnb.listingsAndReviews  77.4MB
2024-10-22T20:47:53.000+0000    sample_airbnb.listingsAndReviews  90.0MB
2024-10-22T20:47:53.388+0000    sample_airbnb.listingsAndReviews  90.0MB
2024-10-22T20:47:53.388+0000    finished restoring sample_airbnb.listingsAndReviews (5555 documents, 0 failures)
2024-10-22T20:47:53.389+0000    no indexes to restore for collection sample_airbnb.listingsAndReviews
2024-10-22T20:47:53.389+0000    5555 document(s) restored successfully. 0 document(s) failed to restore.
20:47:53 tmp-mongosh:/# mongosh mongodb://my-user:***@devops-mongodb-svc.mongodb.svc.cluster.local:40333
Current Mongosh Log ID: 67180faa8e8ebfa44ffe6910
Connecting to:          mongodb://<credentials>@devops-mongodb-svc.mongodb.svc.cluster.local:40333/?directConnection=true&appName=mongosh+2.3.2
Using MongoDB:          6.0.5
Using Mongosh:          2.3.2

For mongosh info see: https://www.mongodb.com/docs/mongodb-shell/


To help improve our products, anonymous usage data is collected and sent to MongoDB periodically (https://www.mongodb.com/legal/privacy-policy).
You can opt-out by running the disableTelemetry() command.

------
   The server generated these startup warnings when booting
   2024-10-22T20:23:39.815+00:00: Using the XFS filesystem is strongly recommended with the WiredTiger storage engine. See http://dochub.mongodb.org/core/prodnotes-filesystem
   2024-10-22T20:23:42.603+00:00: /sys/kernel/mm/transparent_hugepage/enabled is 'always'. We suggest setting it to 'never'
   2024-10-22T20:23:42.604+00:00: vm.max_map_count is too low
------

devops-mongodb [direct: secondary] test> show dbs
admin          192.00 KiB
config         240.00 KiB
local           53.13 MiB
sample_airbnb   51.48 MiB
devops-mongodb [direct: secondary] test>
```


### Example queries on the collection `sample_airbnb.listingsAndReviews`

```sql
db.listingsAndReviews.find({ "address.market": "New York" }).limit(5)
db.listingsAndReviews.find({ "price": { $gte: 100, $lte: 200 } }).limit(5)
devops-mongodb [direct: primary] sample_airbnb> db.listingsAndReviews.countDocuments()
5555
devops-mongodb [direct: primary] sample_airbnb>

db.listingsAndReviews.find().sort({ price: 1 }).limit(5)

```


Delete sample_airbnb DB to test dump-job

```bash
21:58:53 tmp-mongosh:/# PRIMARY_HOST=$(mongosh "mongodb://my-user:$MONGODB_LOCAL_PASSWORD@devops-mongodb-svc.mongodb.svc.cluster.local:40333" --quiet --eval "rs.status()" --json | jq -r '.members[] | select(.stateStr == "PRIMARY") | .name' | cut -d':' -f1)
Enter password: ************
21:59:09 tmp-mongosh:/# mongosh mongodb://my-user:***@$PRIMARY_HOST:40333
Current Mongosh Log ID: 6718204c8b2be33d16fe6910
Connecting to:          mongodb://<credentials>@devops-mongodb-1.devops-mongodb-svc.mongodb.svc.cluster.local:40333/?directConnection=true&appName=mongosh+2.3.2
Using MongoDB:          6.0.5
Using Mongosh:          2.3.2

For mongosh info see: https://www.mongodb.com/docs/mongodb-shell/

------
   The server generated these startup warnings when booting
   2024-10-22T20:24:22.669+00:00: Using the XFS filesystem is strongly recommended with the WiredTiger storage engine. See http://dochub.mongodb.org/core/prodnotes-filesystem
   2024-10-22T20:24:24.034+00:00: /sys/kernel/mm/transparent_hugepage/enabled is 'always'. We suggest setting it to 'never'
   2024-10-22T20:24:24.035+00:00: vm.max_map_count is too low
------

devops-mongodb [direct: primary] test> show dbs
admin          192.00 KiB
config         248.00 KiB
local           53.23 MiB
sample_airbnb   51.48 MiB
devops-mongodb [direct: primary] test> use sample_airbnb
switched to db sample_airbnb
devops-mongodb [direct: primary] sample_airbnb> db.dropDatabase()
{ ok: 1, dropped: 'sample_airbnb' }
devops-mongodb [direct: primary] sample_airbnb> show dbs
admin   192.00 KiB
config  248.00 KiB
local    53.23 MiB
devops-mongodb [direct: primary] sample_airbnb>
```


Job Copleted :
```bash
~
❯ k get pods -n mongodb
NAME                                          READY   STATUS      RESTARTS   AGE
devops-mongodb-0                              2/2     Running     0          160m
devops-mongodb-1                              2/2     Running     0          159m
devops-mongodb-2                              2/2     Running     0          159m
mongodb-dump-data-job-gszdq                   0/1     Completed   0          2m35s
mongodb-kubernetes-operator-97dcdd8f9-nj4rb   1/1     Running     0          8h
tmp-mongosh                                   1/1     Running     0          18m

~
❯  k logs mongodb-dump-data-job-gszdq -n mongodb
2024-10-22T23:01:28.643+0000    writing sample_airbnb.listingsAndReviews to archive on stdout
2024-10-22T23:01:30.066+0000    [........................]  sample_airbnb.listingsAndReviews  101/5555  (1.8%)
2024-10-22T23:01:33.218+0000    [###########.............]  sample_airbnb.listingsAndReviews  2771/5555  (49.9%)
2024-10-22T23:01:36.218+0000    [######################..]  sample_airbnb.listingsAndReviews  5199/5555  (93.6%)
2024-10-22T23:01:36.404+0000    [########################]  sample_airbnb.listingsAndReviews  5555/5555  (100.0%)
2024-10-22T23:01:36.426+0000    done dumping sample_airbnb.listingsAndReviews (5555 documents)
Primary Host : devops-mongodb-1.devops-mongodb-svc.mongodb.svc.cluster.local
2024-10-22T23:01:37.745+0000    preparing collections to restore from
2024-10-22T23:01:37.753+0000    reading metadata for sample_airbnb.listingsAndReviews from archive on stdin
2024-10-22T23:01:37.864+0000    restoring sample_airbnb.listingsAndReviews from archive on stdin
2024-10-22T23:01:40.730+0000    sample_airbnb.listingsAndReviews  20.8MB
2024-10-22T23:01:43.729+0000    sample_airbnb.listingsAndReviews  38.1MB
2024-10-22T23:01:46.729+0000    sample_airbnb.listingsAndReviews  38.1MB
2024-10-22T23:01:49.729+0000    sample_airbnb.listingsAndReviews  50.2MB
2024-10-22T23:01:52.730+0000    sample_airbnb.listingsAndReviews  59.0MB
2024-10-22T23:01:55.729+0000    sample_airbnb.listingsAndReviews  77.4MB
2024-10-22T23:01:58.729+0000    sample_airbnb.listingsAndReviews  90.0MB
2024-10-22T23:02:00.436+0000    sample_airbnb.listingsAndReviews  90.0MB
2024-10-22T23:02:00.436+0000    finished restoring sample_airbnb.listingsAndReviews (5555 documents, 0 failures)
2024-10-22T23:02:00.437+0000    no indexes to restore for collection sample_airbnb.listingsAndReviews
2024-10-22T23:02:00.437+0000    5555 document(s) restored successfully. 0 document(s) failed to restore.

~
❯
```