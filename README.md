# Recipe API Setup Guide

This guide will walk you through the steps to set up the Recipe API application in a production environment on an EC2 instance.

## Prerequisites

- An EC2 instance running Amazon Linux 2 or a compatible OS.
- SSH access to the EC2 instance.

## Step 1: Update the System

First, ensure your system is up to date:

```bash
sudo yum update -y
```

## Step 2: Install Docker

Install Docker and start the service:

```bash
sudo amazon-linux-extras install docker -y
sudo service docker start
sudo systemctl enable docker
```

## Step 3: Add User to Docker Group

Add the `ec2-user` to the Docker group to run Docker commands without `sudo`:

```bash
sudo usermod -a -G docker ec2-user
```

## Step 4: Install Docker Compose

Download and install Docker Compose:

```bash
sudo curl -SL "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

## Step 5: Install Git

Install Git to clone the repository:

```bash
sudo yum install -y git
```

## Step 6: Clone the Repository

Clone the Recipe API repository:

```bash
git clone https://github.com/GloriousPurposeVariant/recipe.git
cd recipe/recipe-api
```

## Step 7: Create Environment Variables File

Create a `.env` file and paste your environment variables:

```bash
nano .env
```

### Example .env File

```env
SECRET_KEY=
ALLOWED_HOSTS=

# Database configs
DB_NAME=
DB_USERNAME=
DB_PASSWORD=
DB_HOSTNAME=
DB_PORT=

# Celery config
CELERY_BROKER_URL=

# Email configs
EMAIL_USER=
EMAIL_PASSWORD=
```

## Step 8: Set Docker Socket Permissions

Set permissions for the Docker socket:

```bash
sudo chmod 666 /var/run/docker.sock
```

## Step 9: Build and Run the Application

Finally, build and run the Docker containers:

```bash
docker-compose up --build
```

## Accessing the Application

Once the containers are running, you can access the application via:

```
http://<your-ec2-public-ip>:8000
```

Replace `<your-ec2-public-ip>` with your EC2 instance's public IP.

## Troubleshooting

- Ensure that your security groups allow inbound traffic on port 8000.
- Check the logs for any errors using `docker-compose logs`.

---

## Test cases
`DJANGO_SETTINGS_MODULE=config.settings.development coverage run -m pytest path/to/test.py`

## For report
`coverage html`

### Outstanding Issues

- **Server Hosting**: The application faces issues when hosted on the server.
- **Celery Configuration Issues**: Problems with Celery configuration for Beat. Celery works fine for delay tasks.
- **Logs Fail on Server**: Logging works locally but fails on the server.

### Progress Made

- **Docker Integration**: Successfully containerized the application, and it works locally.
- **Testing and Coverage Report**: Comprehensive test cases written for almost all scenarios except for multipart format for create and update recipe APIs.
- **Asynchronous Task Handling with Celery**: Implemented Celery for handling asynchronous tasks and tried integrating Celery Beat for daily scheduled tasks.
- **Logging Framework**: Implemented logging which works fine in the local Docker container.

---
