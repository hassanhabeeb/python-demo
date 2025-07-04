# 🐍 Django App Deployment with Docker, AWS EC2 & GitHub Actions

This project demonstrates how to containerize and deploy a Django application using Docker, Docker Compose, AWS EC2, and GitHub Actions for automated CI/CD. It uses AWS Systems Manager (SSM) Parameter Store to securely manage environment variables.

---

## 📁 Project Structure

# machine-test



---

## 🔧 1. Build and Run Locally

### 1.1 Prerequisites

- Docker and Docker Compose installed
- Python 3.10+ if testing outside Docker

### 1.2 Configure `.env.local`

Create `.env.local`:

```env
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_NAME=postgres
DATABASE_USER=postgres
DATABASE_PASSWORD=postgres
DATABASE_HOST=db
DATABASE_PORT=5432
ALLOWED_HOSTS=127.0.0.1,localhost
CSRF_TRUSTED_ORIGINS=http://localhost:8000



docker compose up --build

🚀 2. Deploy to AWS EC2
2.1 Requirements
AWS EC2 Ubuntu Instance (22.04 or later)

Docker & Docker Compose installed

Public IP with open ports: 22, 8000, 80, etc.

SSH Key Pair added to GitHub Secrets

2.2 GitHub Repository Secrets
Name	Description
EC2_HOST	Public IP of your EC2 instance
EC2_USER	SSH user (usually ubuntu)
EC2_SSH_KEY	Private SSH key (without .pub)
DEPLOY_PATH	Directory to deploy app (e.g. /home/ubuntu/ticketing-system)

🔁 3. CI/CD Pipeline with GitHub Actions
Whenever you push to the main branch, this happens automatically:

Archive project files

Upload project to EC2 using rsync

SSH into EC2 and run:

docker compose down (to stop previous containers)

docker compose up --build -d (to rebuild and restart)

.github/workflows/deploy.yml (included in repo)
yaml
Copy
Edit
name: Deploy to EC2

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Sync project to EC2
      uses: burnett01/rsync-deployments@v2
      with:
        switches: -avzr --delete
        remote_path: ${{ secrets.DEPLOY_PATH }}
        remote_host: ${{ secrets.EC2_HOST }}
        remote_user: ${{ secrets.EC2_USER }}
        ssh_private_key: ${{ secrets.EC2_SSH_KEY }}

    - name: SSH & Deploy
      uses: appleboy/ssh-action@v1.0.3
      with:
        host: ${{ secrets.EC2_HOST }}
        username: ${{ secrets.EC2_USER }}
        key: ${{ secrets.EC2_SSH_KEY }}
        script: |
          cd ${{ secrets.DEPLOY_PATH }}
          docker compose down || true
          docker compose up --build -d
🔐 4. AWS SSM Parameter Store
Secrets like database credentials and Django settings are stored in AWS Systems Manager.

Example Parameters
Key	Type	Example Value
/machine-test/SECRET_KEY	SecureString	django-insecure-secret
/machine-test/DEBUG	String	False
/machine-test/DATABASE_NAME	String	postgres
/machine-test/DATABASE_USER	String	postgres
/machine-test/DATABASE_PASSWORD	SecureString	your-db-password
/machine-test/DATABASE_HOST	String	db
/machine-test/DATABASE_PORT	String	5432
/machine-test/ALLOWED_HOSTS	String	13.201.254.96
/machine-test/CSRF_TRUSTED_ORIGINS	String	http://13.201.254.96

These are loaded in settings.py via ssm_loader.py.

🧹 5. Destroy Setup After Testing
On EC2
bash
Copy
Edit
cd ~/ticketing-system
docker compose down --volumes
rm -rf ~/ticketing-system
