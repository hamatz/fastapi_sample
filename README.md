# FastAPI Login and Signup Project

This project demonstrates a simple FastAPI application with login and signup functionality, optimized for mobile display. It includes Docker configuration for deployment and GitHub Actions for CI/CD to AWS ECR.

## Features

- User signup with email verification
- User login with JWT token generation
- Simple mobile-friendly web views for login and signup
- Docker support for containerization
- GitHub Actions for CI/CD to AWS ECR

## Requirements

- Python 3.7+
- Docker
- AWS account with ECR repository
- GitHub account

## Setup

### Clone the repository

```bash
git clone https://github.com/hamatz/fastapi_sample.git
cd fastapi_sample
```

### Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run the application

```bash
uvicorn main:app --reload
```

The application will be available at `http://127.0.0.1:8000`.
API Document can be seen on `http://127.0.0.1:8000/docs`


### Access the web views

- Home: `http://127.0.0.1:8000/`
- Login: `http://127.0.0.1:8000/login`
- Signup: `http://127.0.0.1:8000/signup`

## Docker

### Build the Docker image

```bash
docker build -t my-fastapi-app .
```

### Run the Docker container

```bash
docker run -p 8000:8000 my-fastapi-app
```

The application will be available at `http://127.0.0.1:8000`.

## Deployment to AWS ECR

### Prerequisites

- AWS CLI configured with your credentials
- ECR repository created

### Authenticate Docker to your Amazon ECR registry

```bash
aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin 123456789012.dkr.ecr.us-west-2.amazonaws.com
```

### Tag the Docker image

```bash
docker tag my-fastapi-app:latest 123456789012.dkr.ecr.us-west-2.amazonaws.com/my-repository:latest
```

### Push the Docker image

```bash
docker push 123456789012.dkr.ecr.us-west-2.amazonaws.com/my-repository:latest
```

## GitHub Actions CI/CD

This project includes a GitHub Actions workflow for building and pushing Docker images to AWS ECR.

### Setup GitHub Secrets

In your GitHub repository, add the following secrets:

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `ECR_REPOSITORY`: The URI of your ECR repository (e.g., `123456789012.dkr.ecr.us-west-2.amazonaws.com/my-repository`)

### Workflow file

The GitHub Actions workflow is defined in `.github/workflows/docker-image.yml`.
