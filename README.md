# Fullstack project deploy

This document provides instructions for setting up the FastAPI project, including environment setup, server configuration, and SSH key generation for CI/CD setup.

## Table of Contents
- [Setup Environment](#setup-environment)
- [Setup VS Code](#setup-vs-code)
- [Test Coverage](#test-coverage)
- [Setup Server](#setup-server)
- [Create SSH Key for Existing Server](#create-ssh-key-for-existing-server)
- [CI/CD](#ci-cd)
- [Results](#results)

## Setup Environment

To set up the Python environment, follow these steps:

1. Create a virtual environment:
```bash
python3.12 -m venv venv
```

2. Activate the virtual environment:
```bash
source venv/bin/activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## Setup VS Code

To configure Visual Studio Code to use the correct Python interpreter:

1. Open the command palette by pressing CMD + SHIFT + P.
2. Type and select Python: Select Interpreter.
3. Enter the path to the interpreter: ./venv/bin/python3.12


## Test Coverage

To check test coverage, follow these steps:

1. Install the coverage package:
```bash
pip install pytest-cov
```

2. Run tests with coverage:
```bash
coverage run -m pytest
```

3. Generate an HTML report and open it:
```bash
coverage html & open htmlcov/index.html
```


## Setup Server

To set up the server, perform the following steps:

1. Install docker
Read [there](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository)

2. Make dir and lone the repository: <br>
```bash
cd /home
git clone <URL>
```


3. Install [nginx](https://medium.com/@deltarfd/how-to-set-up-nginx-on-ubuntu-server-fc392c88fb59): <br>
```bash
sudo apt install nginx
sudo service nginx start
sudo systemctl enable nginx<br><br>
sudo ufw app list
sudo ufw allow 'Nginx HTTP'
sudo ufw allow 80
sudo ufw allow 22
sudo ufw allow 443
sudo ufw enable</code>
```

4. Setup nginx config file

```bash
nano /etc/nginx/sites-available/mysite
```

<br>
<br>

```bash
server {
  listen 80;
  server_name [domain or ip];

  location / {
      proxy_pass http://0.0.0.0:4200/;
  }
  location /api/ {
      proxy_pass http://0.0.0.0:8080/;
  }
}
```


## Create SSH Key for Existing Server

To create and set up an SSH key for accessing an existing server:

1. Log in to the server as root using your password.

2. Generate a new SSH key:
   
```bash
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
```

3. Read and copy the public key:

```bash
cat ~/.ssh/id_rsa.pub
echo "yourpublickey" >> ~/.ssh/authorized_keys
```

4. Ensure that the authorized_keys file has the correct permissions:
```bash
chmod 600 ~/.ssh/authorized_keys
```

5. Save the files ~/.ssh/id_rsa.pub and ~/.ssh/id_rsa to your local machine using an SFTP client like Termius.

```bash
ssh -i /path/to/your/private/key/id_rsa username@hostname
```


## CI/CD
Create instruction file for our CI/CD

```bash
touch .github/workflows/deploy_action.yaml
```

Write jobs for github branch" deploy": run_tests and deploy

```yaml
name: Run tests on any Push event
on:
  push:
    branches:
      - 'deploy'
jobs:
  run_tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.12'
          architecture: 'x64'
      - name: Install requirements
        run: pip install -r backend/requirements.txt
      - name: Run tests
        run: cd backend && coverage run -m pytest && coverage report
  build:
    runs-on: ubuntu-latest
    needs: [run_tests]
    steps:
      - name: Checkout code
        uses: actions/checkout@v2
      - name: Deploy to server
        env:
          HOST: ${{ secrets.SERVER_HOST }}
          USERNAME: ${{ secrets.SERVER_USERNAME }}
          PRIVATE_KEY: ${{ secrets.SERVER_SSH_PRIVATE_KEY }}
        run: echo "$PRIVATE_KEY" > id_rsa
      - name: Set file permissions
        run: chmod 600 id_rsa
      - name: Set up SSH Key and Deploy my App on Server
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.SERVER_HOST }}
          username: ${{ secrets.SERVER_USERNAME }}
          key: ${{ secrets.SERVER_SSH_PRIVATE_KEY }}
          port: 22
          script: |
            cd /home/project_dir
            git pull https://zahardimidov:${{secrets.REPO_TOKEN}}@github.com/zahardimidov/${{secrets.REPO_NAME}}.git deploy
            docker compose down
            ENV=.devenv docker compose up --build --scale nginx=1
```

### Results
#### Now we are ready to try to deploy our updates
We shoult commit updates to branch main <br>
```bash
git branch // check our current branch
git checkout main // change brain if it is not main
git add .
git commit -m "commit message"
git push
```

```bash
git add . && git commit -m "update" && git push
```


#### After that we can pull updates to deploy branch when we are ready to rebuild our app
```bash
git checkout deploy && git pull origin main && git push origin deploy && git checkout main
```
