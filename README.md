# DevOps Health-Check Service on AWS

A small Python web service with a health-check endpoint, packaged with Docker, tested and deployed through GitHub Actions, and provisioned on AWS with Terraform (ECS on Fargate).

## Stack

- Python 3.12, standard library HTTP server (no runtime dependencies)
- Docker image with a non-root user and a container HEALTHCHECK
- GitHub Actions: test, build and smoke-test the image, Terraform validate, optional deploy
- Terraform: ECS cluster, Fargate service, task definition, security group, IAM execution role

## Endpoints

- GET /health returns status, version, hostname and uptime as JSON
- GET /healthz and / return the same payload
- Any other path returns 404

## Run locally

    python app/main.py
    curl http://127.0.0.1:8080/health

## Test

    python -m pytest -q tests

## Build and run with Docker

    docker build -t health-check-app .
    docker run -p 8080:8080 health-check-app

## Deploy

1. Push the image to Amazon ECR and set the repository variables IMAGE_URI, AWS_REGION and DEPLOY_ENABLED=true.
2. Set the repository secret AWS_DEPLOY_ROLE_ARN to an IAM role trusted by GitHub OIDC.
3. Push to main. The pipeline runs terraform apply.

To run Terraform by hand:

    cd terraform
    terraform init
    terraform apply -var="image_uri=<your-image-uri>"

## Notes

- The service has no authentication because it only reports health.
- The security group opens port 8080 to the internet for demo purposes. Restrict it in production.
