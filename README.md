# Cauldron

## About
The Cauldron Project is a web application and serves as visualization tool for large-scaled graph data and statistics.

## Setup & Installation
Make sure you have the latest version of Python installed.

### Clone the repository
```
git clone https://github.com/funderos/Cauldron.git
```

### Add dependencies to your python environment
```
pip install -r requirements.txt
```

### Add datasets and a configuration file with according names/paths
Copy `app/website/config_example.ini` to `app/website/config.ini` and adapt values

### If you want to build a docker image, run:
```
docker build -t cauldron .
```
Alternatively, you can pull a pre-built image without payload and configuration from [Docker Hub](https://hub.docker.com/repository/docker/funderb91/cauldron).

## Running The App
- Run in Debug/Development mode: `python app/main.py`
- Run on Server with WSG interface using `app/cauldron.wsgi` file
- Run inside docker container
  - Decide which configuration/data files will be inside image or mounted when running

## Viewing The App
Open a web browser and head to the IP and Port or URL the service is running on. In Debug/Development mode, this defaults to `http://127.0.0.1:5000`, inside the Docker container, port 80 is used and has to be mapped according to the respective requirements.
