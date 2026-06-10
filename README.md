# AWS ECS Service Status Dashboard

A small Flask service status dashboard deployed to **AWS ECS Fargate** using Docker, Terraform, GitHub Actions and CloudWatch Logs.

I built this to practise a realistic ECS deployment workflow without making the application itself too complicated.

---

## What I Built

The app shows a few example backend services and their current status. The app is simple on purpose; the main focus is the cloud deployment.

Routes:

- `/` - service status dashboard
- `/health` - health check used by ECS and the load balancer
- `/api/services` - returns the service list as JSON

---

## Architecture

```text
Docker image
   ↓
Amazon ECR
   ↓
ECS Fargate service
   ↓
Application Load Balancer
   ↓
Public URL
```

The ECS tasks run in private subnets. The public Application Load Balancer sends traffic to the ECS service. Container logs are sent to CloudWatch.

---

## Tech Used

- Python Flask
- Docker
- Amazon ECR
- Amazon ECS Fargate
- Application Load Balancer
- VPC public/private subnets
- CloudWatch Logs
- Terraform
- GitHub Actions

---

## Repository Structure

```text
app/        Flask app and Dockerfile
infra/      Terraform code for AWS infrastructure
.github/    Manual GitHub Actions workflows
```

Main Terraform modules:

```text
vpc = networking
ecr = Docker image repository
alb = public load balancer
ecs = ECS cluster, task definition and service
```

---

## Run Locally

```bash
cd app
pip install -r requirements.txt
python app.py
```

Open:

```text
http://localhost:8080
```

Run with Docker:

```bash
docker build -t service-status-dashboard ./app
docker run -p 8080:8080 service-status-dashboard
```

---

## Deploy with Terraform

```bash
cd infra
cp terraform.tfvars.example terraform.tfvars
terraform init
terraform plan
terraform apply
```

Useful outputs:

```bash
terraform output ecr_repository_url
terraform output application_url
```

---

## Build and Push the Docker Image

After Terraform creates the ECR repository, push the image to ECR:

```bash
aws ecr get-login-password --region eu-west-2 |   docker login --username AWS --password-stdin <ACCOUNT_ID>.dkr.ecr.eu-west-2.amazonaws.com

docker build -t service-status-dashboard ./app
docker tag service-status-dashboard:latest <ECR_REPOSITORY_URL>:latest
docker push <ECR_REPOSITORY_URL>:latest
```

Then redeploy the ECS service:

```bash
aws ecs update-service   --cluster ecs-service-dashboard-dev-cluster   --service ecs-service-dashboard-dev-service   --force-new-deployment   --region eu-west-2
```

---

## GitHub Actions

The workflows are manual so the project does not deploy or spend AWS money every time code is pushed.

Workflows:

- `build-and-push.yml` - builds the Docker image and pushes it to ECR
- `terraform.yml` - runs Terraform `plan`, `apply` or `destroy`

Required GitHub repository variable:

```text
AWS_ROLE_TO_ASSUME
```

---

## What I Learned

- How ECS Fargate runs containers without managing servers
- How an ALB forwards traffic to ECS tasks
- How private subnets and security groups protect the app container
- How Terraform builds repeatable AWS infrastructure
- How ECR stores Docker images for ECS
- How CloudWatch collects container logs
- How GitHub Actions can be used for manual deployment workflows

---

## Teardown

To avoid AWS charges:

```bash
cd infra
terraform destroy
```

Main cost items while running:

- NAT Gateway
- Application Load Balancer
- ECS Fargate task
- CloudWatch logs
