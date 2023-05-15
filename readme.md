# CSSE6400 CLOUD INFRASTRUCTURE ASSIGNMENT
Student Name: Shaoming Teng
Student Number: 44660145

## Dependencies
Before deploying, make sure that you have installed the following dependencies:
- Python 3.10
- Terraform 1.4.6
- Psycopg2 2.9.1
- pipenv
- Docker

## Deployment
1. Fill `credentials` file.
2. Run `./deoply.sh` to deploy the infrastructure.

## Troubleshoot
### everything returned is empty json.
Go to the RDS aws webpage to check the max connections, if it exceeded, the fastest way is to restart the database.

###  Table "Users" already exists
`terroform destroy` and deploy again

###  Error Pushing docker
Sometime, an error like below will happen
```
│ Error: Error pushing docker image: Error pushing image: Post "https://646645496473.dkr.ecr.us-east-1.amazonaws.com/v2/concert/blobs/uploads/": net/http: TLS handshake timeout
│ 
│   with docker_registry_image.concert,
│   on ecr.tf line 53, in resource "docker_registry_image" "concert":
│   53: resource "docker_registry_image" "concert" {
│ 
╵
```
In this case, change current directory to `./terraform` and run `terraform apply -var-file="secret.tfvars" -auto-approve` again.



## Test Records
### Tested on health endpoint.
cpu 1024, mem 2048 - 1/seconds - p(95)=503.78ms - AVG CPU = 15% - MEM 9.77% <br>
cpu 1024, mem 2048 - 10/seconds -  p(95)=568.13ms - AVG CPU = 18% - MEM 9.77% <br>
cpu 1024, mem 2048 - 20/seconds - p(95)=571.5ms  - ACG CPU = 30% - MEM 9.77% <br>
cpu 1024, mem 2048 - 50/seconds - p(95)=680.63ms <br>
cpu 1024, mem 2048 - 100/seconds - p(95)=1.29s <br>
cpu 1024, mem 2048 - 200/seconds - p(95)=3.14s <br>

### General Case
1 cpu 1024, mem 2048 container -  avg=6.66s min=259.1ms med=3.11s  max=22.54s p(90)=18.03s p(95)=19.76s 


### Small-Concern Case
1 cpu 1024, mem 2048 container - avg=665.52ms min=260.79ms med=447.58ms max=3.16s p(90)=1.43s p(95)=1.81s

### Evening Case
cpu1024, mem2046. policy settings: cpu:14, RequestCount:300 - avg=6.4s min=251.14ms med=350.79ms max=47.72s p(90)=30.61s p(95)=42.36s <br>

Settings: 
ticket: cpu2048, mem4096. policy settings: cpu:14, RequestCount:300 <br>
others: cpu1024, mem2046. policy settings: cpu:14, RequestCount:300 <br>
Results:
avg=3.26s    min=250.03ms med=356.72ms max=30.72s   p(90)=11.81s p(95)=12.38s
-


## SVG Generation benchmark
Ticket processing: RAM 128 ~ 50s to generate a ticket
Seating processing: RAM 512 ~ 110s to generate a seating plan




## Running Ports
Ports of each services
service_user is running on 8888
service_ticket is running on 9999
service_concert is running on 7777
