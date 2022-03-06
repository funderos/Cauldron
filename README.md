# Cauldron

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

## Running The App

- Run in debug/development mode: `python app/main.py`
- Run on Server with WSG interface using `app/cauldron.wsgi` file
- Run inside docker container
  - Decide which configuration/data files will be inside image or mounted when running

## Viewing The App

Go to `http://127.0.0.1:5000`
