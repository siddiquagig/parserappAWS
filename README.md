# parserappAWS

This explains the setup of PHP app using Gitlab on kubernetes , you can also find it in python.

## GOAL
Develop a sample PHP application which will parse the CSV file and upload the content of the file into a MySQL RDS Instance. The Kubernetes Cluster is being provisioned using KOPS tool.


## Requirements
​​Route53 hosted zone (Required for KOPS)
​​One S3 Bucket (Required for KOPS to store state information)
​​One S3 bucket (Required to store the processed CSV files, for example, pucdemo-processed-csv)
​​One S3 bucket to store Application Access logs of the Loadbalancer.
​​MySQL RDS in private subnet.3306 port is opened to the Kubernetes Cluster Nodes.
​​Table to store the data from CSV File in supported variables. In our case, we have used the following command to create a table in database.


## Create Database
create database csvdb;
mysql> CREATE TABLE appdata (     sku varchar(255),     name varchar(255),     price varchar(255) );



​​## Setup
​​Cloud: Amazon Web Services
​​Scripting Languages Used: HTML, Javascript and PHP
​​Kubernetes Version: 1.11
​​K8s Cluster Instance Type: t2.medium
​​Instances are launched in Private subnets
​​3 masters and 2 nodes (Autoscaling Configured)
​​K8s Master / Worker node are in Autoscaling group for HA / Scalability / Fault Tolerant
​​S3 buckets to store data (details in Prerequisites)
​​Route53 has been used for DNS Management
​​RDS — MySQL 5.7 (MultiAZ Enabled)



## Provision Kubernetes Cluster on AWS

```
kops create cluster phpapp12 --ssh-public-key ~/.ssh/id_rsa.pub --master-zones ap-south-1a --zones ap-south-1a,ap-south-1b,ap-south-1a --master-size=t2.medium --node-count=2 --master-count 3 --node-size t2.small --topology private --dns public --networking calico --vpc vpc-xxxx --state s3://phpapp-kops-state-store --subnets subnet-xxxx,subnet-xxxx --utility-subnets subnet-xxx,subnet-xxx --kubernetes-version 1.11.0 --api-loadbalancer-type internal --admin-access 172.31.0.0/16 --ssh-access 172.31.xx.xxx/32 --cloud-labels "Environment=TEST" --master-volume-size 100 --node-volume-size 100 --encrypt-etcd-storage;
```


Attach ECR Full access policy to cluster nodes Instance Profile.

## Create Required Kubernetes Resources

# Create Gitlab Instance:

Replace the values for the following variable in the kubernetes-gitlab/gitlab-deployment.yml :

    GITLAB_ROOT_EMAIL
    GITLAB_ROOT_PASSWORD
    GITLAB_HOST
    GITLAB_SSH_HOST
    
    
```
kubectl create -f kubernetes-gitlab/gitlab-ns.yml
kubectl create -f kubernetes-gitlab/postgresql-deployment.yml
kubectl create -f kubernetes-gitlab/postgresql-svc.yml
kubectl create -f kubernetes-gitlab/redis-deployment.yml
kubectl create -f kubernetes-gitlab/redis-svc.yml
kubectl create -f kubernetes-gitlab/gitlab-deployment.yml
kubectl create -f kubernetes-gitlab/gitlab-svc.yml

```


kubectl get svc -n gitlab will give the provisioned Loadbalancer Endpoint. Create a DNS Record for the Endpoint.



Create Gitlab Runner:

Replace the values for the following variable in the gitlab-runners/configmap.yml :

    Gitlab URL
    Registration Token

Go to Gitlab Runners section in the Gitlab console to get the above values.

```
kubectl create -f gitlab-runners/rbac.yaml
kubectl create -f gitlab-runners/configmap.yaml
kubectl create -f gitlab-runners/deployment.yaml
```


# Create CSVParser Application:

Create a base Docker image with Nginx and php7.0 installed on it and push to ECR. Give the base image in csvparser/k8s/deployment.yaml.

```
kubectl create -f csvparser/k8s/deployment.yaml
kubectl create -f csvparser/k8s/service.yaml
```


kubectl get svc, will give the provisioned Loadbalancer Endpoint. Create a DNS Record for the Endpoint.


## App Functionality


-Basic Authentication is enabled for the main page.
    -The browse field will accept the CSV file only.
    -After uploading, the data will be imported into the database by clicking the “Import” button.
    -The processed files can be viewed by clicking on the “View Files” button.
    -“View Data” button will list the records from the database in tabular format.
    -The data record can be edited inline and updated into the database by clicking the “Archive” button.
    -A particular row can be deleted from the database by clicking the “Delete” button.
    -The application is running on two different nodes in different subnets and is being deployed under a Classic LoadBalancer.


    
    
    
    
    
    
    
## CI/CD 
    
-The Gitlab Instance and Runner are running as pods on the Kubernetes Cluster.
    -The application code is available in the Gitlab Repository along with Dockerfile and .gitlab-ci.yml
    -The pipeline is implemented in Gitlab Console using .gitlab-ci.yml file.
    -Whenever a commit is pushed to the Repository, the pipeline is triggered which will execute the following steps in a    pipeline:
    -Build: Build a docker image from the Dockerfile and push to AWS ECR Repo.
    -Deploy: Updates the docker image for the already running application pod on Kubernetes Cluster.
    
    
    
    
## Application in Action

Hit the Gitlab service using the credentials and push the code, you will also see your pipelines

The application will look like 

![alt text](https://github.com/ahmed531/parserappAWS/blob/master/Content/mysql11.JPG)

![alt text](https://github.com/ahmed531/parserappAWS/blob/master/Content/mysql22.JPG)


![alt text](https://github.com/ahmed531/parserappAWS/blob/master/Content/mysql33.JPG)
    
