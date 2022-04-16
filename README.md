# CSE 412 Group Project - API

Group \#20: Matthew Bulger, Jeffrey Adams, Ellis Osborn, Jerry Che

# Table of contents
1) [Quickstart](#quickstart)
1) [Installation](#installation)
2) [Startup](#startup)
3) [UI](#ui)

# Quickstart
The following manual details how to run the API locally, but **you don't need to do that** to start using the application. To see the publicly hosted version, visit:

### [https://cse412.mattbulger.me](https://cse412.mattbulger.me)

# Installation
Before doing anything, run `cd groupproject` to enter the proper root of the project.

## IMPORTANT!
For security reasons, `connection.txt` is not checked into Github, because it contains sensitive information (username and password). When cloning this repository, you must create a new file, `connection.txt` on the same level as `.flaskenv`, containing a string like the following:

`dbname=groupproject user=YOURUSERNAME password=YOURPASSWORD host=localhost port=5432`

Be sure to replace `YOURUSERNAME` and `YOURPASSWORD` with the appropriate values for your system.

## Install API Dependencies
We assume that Python (specifically Python 3) is already installed, and therefore `pip`. Run the following command to install dependenies:

`pip install -e .`

## Initialize Database
We assume that PostgreSQL is already installed.

To initialize the database and insert sample data:
1. `chmod a+x setup.sh`
2. `./setup.sh 5432`
    - The first parameter is the name of the database, and the directory (relative to `$HOME`) the database will be created in.
    - The second parameter is the port the database should start on. Port `5432` is the default, but it can be useful to change if you have multiple databases running, or another port conflict.

# Startup
Ensure that you have already run the `setup.sh` script to start and initialize the database.

You can start the API in HTTP mode or HTTPS mode. You can use HTTP for testing, but HTTPS is required in production. By default, the API listens to requests on port 5000.

## HTTP
To start the API in HTTP mode run the following commands:
1. `cd app`
2. `python3 -m flask run`
    - Flask will automatically hot-reload whenever you save a file, so you can keep this command running in the terminal while you develop, no need to restart.

## HTTPS
HTTPS is required for CORS cross-origin requests to work (as well as coming from a domain whitelisted in the allow-origins list). Also note that you need to have a signed SSL certificate and key in your home directory for HTTPS to work. Our group used [ZeroSSL](https://zerossl.com/) to generate a free 30-day SSL certificate.

To start the API in HTTPS mode, run the following script:
1. `chmod a+x startApi.sh`
1. `./startApi.sh`

# UI
Once the API is running, you can start sending HTTP (or HTTPS) requests to the server's address. You can do this directly in the browser.

There is also a corresponding UI project that interfaces with this API. Once the API is running, you can startup the UI to test the project locally.
