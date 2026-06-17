# rag-system
This is an implementation of the RAG model for question answering.

## Requirements
- Python 3.12.0

#### Install Python using MiniConda
1) Download and install MiniConda from here
2) Create a new environment using the following command:
```bash
$ conda create -n rag-system python=3.12
```
3) Activate the environment:
```bash
$ conda activate rag-system
```

### (Optional) Setup you command line interface for better readability

```bash
export PS1="\[\033[01;32m\]\u@\h:\w\n\[\033[00m\]\$ "
```

## Installation

### Install the required packages

```bash
$ pip install -r requirements.txt
```

### Setup the environment variables

```bash
$ cp .env.example .env
```

Set your environment variables in the `.env` file. Like `OPENAI_API_KEY` value.

## Setup docker

```bash
$ [docker](https://docs.docker.com/desktop/setup/install/windows-install/)
```

### Run Docker Compose Services

```bash
$ cd docker
$ cp .env.example .env
```

- update `.env` with your credentials


```bash
$ cd docker
$ sudo docker compose up -d
```

### Stop Any container
```bash
$ sudo docker stop $(sudo docker ps -aq)
```

### Remove stoped container
```bash
$ sudo docker rm $(sudo docker ps -aq) 
```

### Reomve Images that I get from docker hub
```bash
$ sudo docker rmi $(sudo docker images -q)
``` 

### Remove all volumes that related to docker
```bash
$ sudo docker volume rm $(sudo docker volume ls -q)
```

### Remove anything remains from docker
```bash
$ sudo docker system prune --all
```


## Run the FastAPI server (Development Mode)

```bash
$ uvicorn main:app --reload --host 0.0.0.0 --port 5000
```