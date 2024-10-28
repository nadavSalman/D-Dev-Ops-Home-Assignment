# Dropit-Dev-Ops-Home-Assignment


![alt text](images/k8s-architecture.png)



## Create loca K8s cluster using Kind
Prerequisite
- Docker
- [Kind](https://kind.sigs.k8s.io/) cli 
    - Setup [kind cluster with Ingress Controller](https://kind.sigs.k8s.io/docs/user/ingress/), chose Nginx. (There is a GitHub flow after settign self hosted agent)
- **Optinal** - [Install cilium cli](https://docs.cilium.io/en/stable/installation/kind/) 


## Import Mising Post db data (`sample_training.posts`)

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

10/27/2024  05:19 PM    <DIR>          .
10/22/2024  07:02 PM    <DIR>          ..
10/22/2024  07:02 PM        16,588,590 bsondump.exe
10/22/2024  07:06 PM        99,656,721 listingsAndReviews.json
10/22/2024  07:02 PM        23,243,614 mongodump.exe
10/22/2024  07:02 PM        22,831,256 mongoexport.exe
10/22/2024  07:02 PM        22,766,308 mongofiles.exe
10/22/2024  07:02 PM        23,056,766 mongoimport.exe
10/22/2024  07:02 PM        23,771,720 mongorestore.exe
10/22/2024  07:02 PM        22,298,759 mongostat.exe
10/22/2024  07:02 PM        21,782,277 mongotop.exe
10/27/2024  05:19 PM        17,215,951 posts.json
              10 File(s)    293,211,962 bytes
               2 Dir(s)  882,452,078,592 bytes free

C:\Users\User\Downloads\mongodb-database-tools-windows-x86_64-100.10.0\mongodb-database-tools-windows-x86_64-100.10.0\bin>mongoimport.exe --drop --uri "mongodb+srv://nadavdevops:13k6WO3uxLmG6xxe@cluster01.sv6iv.mongodb.net/?retryWrites=true&w=majority&appName=Cluster01" --db "sample_training" --collection "posts" --file posts.json
2024-10-27T17:20:12.529+0200    connected to: mongodb+srv://[**REDACTED**]@cluster01.sv6iv.mongodb.net/?retryWrites=true&w=majority&appName=Cluster01
2024-10-27T17:20:12.617+0200    dropping: sample_training.posts
2024-10-27T17:20:15.536+0200    [########################] sample_training.posts        16.4MB/16.4MB (100.0%)
2024-10-27T17:20:18.355+0200    [########################] sample_training.posts        16.4MB/16.4MB (100.0%)
2024-10-27T17:20:18.355+0200    500 document(s) imported successfully. 0 document(s) failed to import.

C:\Users\User\Downloads\mongodb-database-tools-windows-x86_64-100.10.0\mongodb-database-tools-windows-x86_64-100.10.0\bin>
```
### Test the data with the BE server app :
```bash
❯ curl localhost:5050/posts/latest | jq
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   665  100   665    0     0   3994      0 --:--:-- --:--:-- --:--:--  4006
[
  {
    "_id": "50ab0f8dbcf1bfe2536dc7de",
    "author": "machine",
    "title": "Bill of Rights",
    "tags": [
      "watch",
      "speedboat",
      "zoo",
      "authority",
      "coach",
      "gasoline",
      "side",
      "author",
      "purpose",
      "shrimp"
    ],
    "date": "2012-11-20T05:05:17.032Z"
  },
  {
...
```


Prerequisite
- Add Atlas cluster full URI as GitHub Action secret.



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


###  Artifacts Repository Management

| Container Images              | Helm Charts                        |
|:------------------------------|:-----------------------------------|
| `nadavdev/dropit-data-sync-job`| `nadavdev/dropit-helm-data-sync-job`|
| `nadavdev/dropit-server-be`    | `nadavdev/dropit-helm-server-be`    |
| `nadavdev/dropit-app-fe`       | `nadavdev/dropit-helm-app-fe`       |





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
20:39:12 tmp-mongosh:/# mongodump --uri "mongodb+srv://`nadavdev/dropit`ops:sQPUhIdPhOumv1pa@cluster01.ypl06.mongodb.net/sample_airbnb?retryWrites=true&w=majority&appName=Cluster01"  --archive > db.dump
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

Load data : `mongodump` - `mongorestore` (`K8s Pod`)
```bash
❯ k run tmp-mongosh --image=rtsp/mongosh -n mongodb  --rm -it -- bash
19:44:55 tmp-mongosh:/# mongodump --uri "mongodb+srv://nadavdevops:***@cluster01.sv6iv.mongodb.net/?retryWrites=true&w=majority&appName=Cluster01" --db "sample_training" --collection "posts" --archive > db.dump
2024-10-27T19:45:09.834+0000    writing sample_training.posts to archive on stdout
2024-10-27T19:45:12.649+0000    [........................]  sample_training.posts  0/500  (0.0%)
2024-10-27T19:45:15.649+0000    [........................]  sample_training.posts  0/500  (0.0%)
2024-10-27T19:45:18.650+0000    [........................]  sample_training.posts  0/500  (0.0%)
2024-10-27T19:45:21.649+0000    [........................]  sample_training.posts  0/500  (0.0%)
2024-10-27T19:45:24.649+0000    [........................]  sample_training.posts  0/500  (0.0%)
2024-10-27T19:45:27.649+0000    [........................]  sample_training.posts  0/500  (0.0%)
2024-10-27T19:45:30.650+0000    [####....................]  sample_training.posts  101/500  (20.2%)
2024-10-27T19:45:33.732+0000    [####....................]  sample_training.posts  101/500  (20.2%)
2024-10-27T19:45:36.732+0000    [####....................]  sample_training.posts  101/500  (20.2%)
2024-10-27T19:45:39.732+0000    [####....................]  sample_training.posts  101/500  (20.2%)
2024-10-27T19:45:42.732+0000    [####....................]  sample_training.posts  101/500  (20.2%)
2024-10-27T19:45:45.732+0000    [####....................]  sample_training.posts  101/500  (20.2%)
2024-10-27T19:45:48.732+0000    [####....................]  sample_training.posts  101/500  (20.2%)
2024-10-27T19:45:51.732+0000    [####....................]  sample_training.posts  101/500  (20.2%)
2024-10-27T19:45:54.732+0000    [####....................]  sample_training.posts  101/500  (20.2%)
2024-10-27T19:45:57.732+0000    [####....................]  sample_training.posts  101/500  (20.2%)
2024-10-27T19:46:00.732+0000    [####....................]  sample_training.posts  101/500  (20.2%)
2024-10-27T19:46:04.056+0000    [####....................]  sample_training.posts  101/500  (20.2%)
2024-10-27T19:46:07.055+0000    [####....................]  sample_training.posts  101/500  (20.2%)
2024-10-27T19:46:10.055+0000    [####....................]  sample_training.posts  101/500  (20.2%)
2024-10-27T19:46:13.055+0000    [####....................]  sample_training.posts  101/500  (20.2%)
2024-10-27T19:46:16.055+0000    [####....................]  sample_training.posts  101/500  (20.2%)
2024-10-27T19:46:19.055+0000    [####....................]  sample_training.posts  101/500  (20.2%)
2024-10-27T19:46:22.055+0000    [####....................]  sample_training.posts  101/500  (20.2%)
2024-10-27T19:46:25.055+0000    [####....................]  sample_training.posts  101/500  (20.2%)
2024-10-27T19:46:28.056+0000    [####....................]  sample_training.posts  101/500  (20.2%)
2024-10-27T19:46:31.055+0000    [####....................]  sample_training.posts  101/500  (20.2%)
2024-10-27T19:46:31.360+0000    [########################]  sample_training.posts  500/500  (100.0%)
2024-10-27T19:46:31.362+0000    done dumping sample_training.posts (500 documents)
19:46:31 tmp-mongosh:/# ls -la
total 17M
drwxr-xr-x   1 root root 4.0K 2024-10-27 19:45 ./
drwxr-xr-x   1 root root 4.0K 2024-10-27 19:45 ../
lrwxrwxrwx   1 root root    7 2024-09-26 00:00 bin -> usr/bin/
drwxr-xr-x   2 root root 4.0K 2024-08-14 16:10 boot/
-rw-r--r--   1 root root  17M 2024-10-27 19:46 db.dump
drwxr-xr-x   5 root root  380 2024-10-27 19:44 dev/
drwxr-xr-x   1 root root 4.0K 2024-10-27 19:44 etc/
drwxr-xr-x   2 root root 4.0K 2024-08-14 16:10 home/
lrwxrwxrwx   1 root root    7 2024-09-26 00:00 lib -> usr/lib/
lrwxrwxrwx   1 root root    9 2024-09-26 00:00 lib64 -> usr/lib64/
drwxr-xr-x   2 root root 4.0K 2024-09-26 00:00 media/
drwxr-xr-x   2 root root 4.0K 2024-09-26 00:00 mnt/
drwxr-xr-x   2 root root 4.0K 2024-09-26 00:00 opt/
dr-xr-xr-x 638 root root    0 2024-10-27 19:44 proc/
-rw-r--r--   1 root root   37 2024-10-27 19:44 product_uuid
drwx------   1 root root 4.0K 2024-10-10 22:37 root/
drwxr-xr-x   1 root root 4.0K 2024-10-27 19:44 run/
lrwxrwxrwx   1 root root    8 2024-09-26 00:00 sbin -> usr/sbin/
drwxr-xr-x   2 root root 4.0K 2024-09-26 00:00 srv/
dr-xr-xr-x  11 root root    0 2024-10-27 19:44 sys/
drwxrwxrwt   2 root root 4.0K 2024-09-26 00:00 tmp/
drwxr-xr-x   1 root root 4.0K 2024-09-26 00:00 usr/
drwxr-xr-x   1 root root 4.0K 2024-09-26 00:00 var/
19:47:28 tmp-mongosh:/# export PRIMARY_HOST=$(mongosh "mongodb://my-user:******@devops-mongodb-svc.mongodb.svc.cluster.local:40333" --quiet --eval "rs.status()" --json | jq -r '.memb
ers[] | select(.stateStr == "PRIMARY") | .name' | cut -d':' -f1)
19:48:43 tmp-mongosh:/# echo $PRIMARY_HOST
devops-mongodb-2.devops-mongodb-svc.mongodb.svc.cluster.local
19:48:50 tmp-mongosh:/# mongorestore --uri "mongodb://my-user:******@$PRIMARY_HOST:40333" --archive < db.dump
2024-10-27T19:49:25.011+0000    preparing collections to restore from
2024-10-27T19:49:25.019+0000    reading metadata for sample_training.posts from archive on stdin
2024-10-27T19:49:25.125+0000    restoring sample_training.posts from archive on stdin
2024-10-27T19:49:26.528+0000    finished restoring sample_training.posts (500 documents, 0 failures)
2024-10-27T19:49:26.529+0000    no indexes to restore for collection sample_training.posts
2024-10-27T19:49:26.529+0000    500 document(s) restored successfully. 0 document(s) failed to restore.
19:49:26 tmp-mongosh:/# mongosh  "mongodb://my-user:******@$PRIMARY_HOST:40333"
Current Mongosh Log ID: 671e995d2e5efee918fe6910
Connecting to:          mongodb://<credentials>@devops-mongodb-2.devops-mongodb-svc.mongodb.svc.cluster.local:40333/?directConnection=true&appName=mongosh+2.3.2
Using MongoDB:          6.0.5
Using Mongosh:          2.3.2

For mongosh info see: https://www.mongodb.com/docs/mongodb-shell/


To help improve our products, anonymous usage data is collected and sent to MongoDB periodically (https://www.mongodb.com/legal/privacy-policy).
You can opt-out by running the disableTelemetry() command.

------
   The server generated these startup warnings when booting
   2024-10-27T16:35:36.642+00:00: Using the XFS filesystem is strongly recommended with the WiredTiger storage engine. See http://dochub.mongodb.org/core/prodnotes-filesystem
   2024-10-27T16:35:39.966+00:00: /sys/kernel/mm/transparent_hugepage/enabled is 'always'. We suggest setting it to 'never'
   2024-10-27T16:35:39.966+00:00: vm.max_map_count is too low
------

devops-mongodb [direct: primary] test> show dbs
admin            192.00 KiB
config           244.00 KiB
local            161.64 MiB
sample_training    3.90 MiB
devops-mongodb [direct: primary] test> use sample_training
switched to db sample_training
devops-mongodb [direct: primary] sample_training> db.getCollectionNames();
[ 'posts' ]
devops-mongodb [direct: primary] sample_training>
```



Debug k8s job Init Container - `restored successfully`:

```bash
❯  k logs dump-sync-job-dt7wf -c init-load-data -f -n mongodb
2024-10-27T19:58:28.457+0000    writing sample_training.posts to archive on stdout
2024-10-27T19:58:31.159+0000    [........................]  sample_training.posts  0/500  (0.0%)
2024-10-27T19:58:34.159+0000    [........................]  sample_training.posts  0/500  (0.0%)
2024-10-27T19:58:37.239+0000    [........................]  sample_training.posts  0/500  (0.0%)
2024-10-27T19:58:40.239+0000    [........................]  sample_training.posts  0/500  (0.0%)
2024-10-27T19:58:43.239+0000    [####....................]  sample_training.posts  101/500  (20.2%)
2024-10-27T19:58:46.240+0000    [####....................]  sample_training.posts  101/500  (20.2%)
2024-10-27T19:58:49.239+0000    [####....................]  sample_training.posts  101/500  (20.2%)
2024-10-27T19:58:52.239+0000    [####....................]  sample_training.posts  101/500  (20.2%)
2024-10-27T19:58:55.239+0000    [####....................]  sample_training.posts  101/500  (20.2%)
2024-10-27T19:58:58.239+0000    [####....................]  sample_training.posts  101/500  (20.2%)
2024-10-27T19:59:01.240+0000    [####....................]  sample_training.posts  101/500  (20.2%)
2024-10-27T19:59:04.239+0000    [####....................]  sample_training.posts  101/500  (20.2%)
2024-10-27T19:59:07.453+0000    [####....................]  sample_training.posts  101/500  (20.2%)
2024-10-27T19:59:10.454+0000    [####....................]  sample_training.posts  101/500  (20.2%)
2024-10-27T19:59:13.453+0000    [####....................]  sample_training.posts  101/500  (20.2%)
2024-10-27T19:59:16.453+0000    [####....................]  sample_training.posts  101/500  (20.2%)
2024-10-27T19:59:19.453+0000    [####....................]  sample_training.posts  101/500  (20.2%)
2024-10-27T19:59:22.453+0000    [####....................]  sample_training.posts  101/500  (20.2%)
2024-10-27T19:59:25.453+0000    [####....................]  sample_training.posts  101/500  (20.2%)
2024-10-27T19:59:28.453+0000    [####....................]  sample_training.posts  101/500  (20.2%)
2024-10-27T19:59:31.453+0000    [####....................]  sample_training.posts  101/500  (20.2%)
2024-10-27T19:59:34.453+0000    [####....................]  sample_training.posts  101/500  (20.2%)
2024-10-27T19:59:37.661+0000    [####....................]  sample_training.posts  101/500  (20.2%)
2024-10-27T19:59:40.660+0000    [####....................]  sample_training.posts  101/500  (20.2%)
2024-10-27T19:59:43.661+0000    [####....................]  sample_training.posts  101/500  (20.2%)
2024-10-27T19:59:46.660+0000    [####....................]  sample_training.posts  101/500  (20.2%)
2024-10-27T19:59:49.661+0000    [####....................]  sample_training.posts  101/500  (20.2%)
2024-10-27T19:59:52.661+0000    [####....................]  sample_training.posts  101/500  (20.2%)
2024-10-27T19:59:53.281+0000    [####....................]  sample_training.posts  101/500  (20.2%)
2024-10-27T19:59:53.291+0000    Failed: error writing data for collection `sample_training.posts` to disk: error reading collection: connection(cluster01-shard-00-01.sv6iv.mongodb.net:27017[-8]) incomplete read of full message: read tcp 10.244.2.128:60860->13.73.152.69:27017: use of closed network connection
Primary Host : devops-mongodb-2.devops-mongodb-svc.mongodb.svc.cluster.local
2024-10-27T19:59:54.302+0000    preparing collections to restore from
2024-10-27T19:59:54.307+0000    reading metadata for sample_training.posts from archive on stdin
2024-10-27T19:59:54.395+0000    restoring sample_training.posts from archive on stdin
2024-10-27T19:59:54.740+0000    finished restoring sample_training.posts (101 documents, 0 failures)
2024-10-27T19:59:54.740+0000    no indexes to restore for collection sample_training.posts
2024-10-27T19:59:54.740+0000    101 document(s) restored successfully. 0 document(s) failed to restore.

~ took 47s
❯
```