# Voting System
## url: https://votingsystem-57dd4ece8786.herokuapp.com

## Table of Contents

- [Voting System](#voting-system)
  - [url: https://votingsystem-57dd4ece8786.herokuapp.com](#url-httpsvotingsystem-57dd4ece8786herokuappcom)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Features](#features)
  - [Requirements](#requirements)
  - [Setup](#setup)
    - [1. Clone the repository](#1-clone-the-repository)
    - [2. Create a Heroku app and deploy the application](#2-create-a-heroku-app-and-deploy-the-application)
    - [3. Configure environment variables](#3-configure-environment-variables)
    - [4. Setup Redis](#4-setup-redis)
  - [Running the Application](#running-the-application)
    - [1. Start the Flask application](#1-start-the-flask-application)
  - [Usage](#usage)
    - [User Login](#user-login)
    - [Voting](#voting)
    - [View Results](#view-results)
  - [Project Structure](#project-structure)

## Introduction

The Voting System is a web application that allows users to vote for candidates in an election. The system ensures the security and privacy of votes by using RSA encryption to store the votes. Users can later decrypt their votes using their private keys.

## Features

- User login with name and student ID.
- Voting for president and vice president.
- RSA encryption for secure vote storage.
- Display of the user's encrypted and decrypted votes.
- Tailwind CSS for responsive and modern UI design.

## Requirements

- Python 3.12.3
- Redis server
- Heroku server

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/David810209/voting-system.git
cd voting-system
```

### 2. Create a Heroku app and deploy the application
```bash
heroku login
heroku create your-heroku-app-name
$ heroku git:remote -a your-heroku-app-name  
# deploy your change
git add .
git commit -m "Initial commit"
git push heroku main
# see the detail log
heroku logs --tail -a your-heroku-app-name
```


### 3. Configure environment variables
go to heroku app setup to set the environment config

```
REDIS_HOST=your_redis_host
REDIS_PORT=your_redis_port
REDIS_PASSWORD=your_redis_password
FLASK_SECRET_KEY=your_secret_key
```
or directly run the command
```bash
heroku config:set REDIS_HOST=your_redis_host
heroku config:set REDIS_PORT=your_redis_port
heroku config:set REDIS_PASSWORD=your_redis_password
heroku config:set FLASK_SECRET_KEY=your_secret_key
```

### 4. Setup Redis
Make sure you have a Redis database running online.

## Running the Application
### 1. Start the Flask application
```bash
flask run
```

## Usage
### User Login
1. Navigate to the login page.
2. Enter your name and student ID.
3. Indicate whether you are a member of a specific group.
4. Click "Login".
### Voting
1. On the candidates page, review the candidates.
2. Select your choices for president and vice president.
3. Click "Submit" to confirm your choices.
4. You will be shown a confirmation modal to review your choices.
5. Confirm your choices to submit your vote.
### View Results
1. Navigate to the results page.
2. Enter your user ID and private key.
3. Click "Decrypt Vote" to view your voting results.
   
## Project Structure
```plaintext
voting-system/
├── app.py                   # Main application file
├── config.py                # Configuration file
├── Procfile                 # Heroku process file
├── redis_get/               # Redis handler
│   ├── redis_db.py          # Redis handler
├── encrypt/                 # RSA encryption/decryption utilities
│   ├── rsa_process.py       # RSA encryption/decryption utilities
├── requirements.txt         # Python dependencies
├── templates/               # HTML templates
│   ├── info.html            # Voting page
│   ├── login.html           # Login page
│   ├── check.html          # check decryption page
│   └── success.html         # Success page after voting
└── static/                  # Static files (CSS, JS, images)

```
