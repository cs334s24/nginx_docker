## nginx_docker

This repo contains a proof-of-concept web application where:

* A React website is served using Node.js
* A Flask API is served using gunicorn
* NGINX is a reverse proxy that routes traffic to the appropriate server

## Setup

In the `flask_api` folder create a virtual environment and install the dependencies

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```


## Version 1: Manual launch of Flask/gunicorn

In the `flask_api` folder, run:

```
gunicorn "app:create_app()"
```

Note: the quotes are necessary because parenthesis are interpreted by the terminal.  This command is in the `up` script.

Test by going to `localhost:8000` with a web browser.  The result should be

```
{
   "data": "Hello, World!"
}
```

Press `control-c` to terminate the server.

## Version 2:  Launch with Docker


### Build the Container
Before we run the container, we have to build it.  In the `flask_api` folder run:

```
docker build -t flask_api .
```

* `-t flask_api` specifies that we want to *tag* the container with the name `flask_api`
* `.` specifies that the `Dockerfile` is in the current directory


### Launch the Container

Once the build completes, we can launch the container:

```
docker run -d --name flask_api --network capstone -p 8000:8000 flask_api
```

* `-d` - run the container in in *detached* mode (in the background)
* `--name flask_api` - name the container so we can refer to it later
* `--network capstone` - run the container in a network space named `capstone`.  This won't matter now, but will allow container-to-container communication later.
* `-p 8000:8000` - map port 8000 in the container to port 8000 on `localhost`.  This allows us to communicate with the container from our laptop.
* `flask_api` - The container image we specified in the build

Test by going to `localhost:8000` with a web browser.  The result should be the same as before.

This command is in `docker_up`.

### Stop the Container

To stop the container we run:

```
docker rm -f flask_api
```

* `-f` - stop and remove the container.  The long version is `docker stop flask_api` followed by `docker rm flask_api`.
* `flask_api` - the name of the container to stop/remove

This command is in `docker_down`


## Version 3: NGINX as a Reverse Proxy

NGINX is an efficient and secure front end for web servers like `gunicorn`.  We could install it on our laptop and run it locally, but it is easier to just go right to the Docker container:

### Launch the Container

NOTE:  The Flask/gunicorn container must already be running.  NGINX checks for proxy servers at launch and will fail if one is not available.

```
docker run -d --name nginx --network capstone -p 80:80 -v $(pwd)/default.conf:/etc/nginx/conf.d/default.conf:ro nginx
```

* `-d` - run the container in in *detached* mode (in the background)
* `--name nginx` - name the container so we can refer to it later
* `--network capstone` - run the container in a network space named `capstone`.  This matters now but will need to have both containers in the same network to allow container-to-container communication.
* `-p 80:80` - map port 80 in the container to port 80 on `localhost`.  This allows us to communicate with the container from our laptop.
* `-v $(pwd)/default.conf:/etc/nginx/conf.d/default.conf:ro` - Mount a *volume* from your laptop onto the container.  The parameter is `<local path>:<container path>:<permissions>`.  Both paths must be absolute paths.  To ensure this works regardless of where the repo is cloned, `$(pwd)` inserts the current directory in the path.  The `ro` at the end sets the file to be read-only.

This command is in `nginx_up`

### Stop the Container

To stop the container we run:

```
docker rm -f nginx
```

* `-f` - stop and remove the container.  The long version is `docker stop nginx` followed by `docker rm nginx`.
* `nginx` - the name of the container to stop/remove

This command is in `nginx_down`


## Version 4: Docker-Compose

Docker-compose is a tool to specify how to configure multiple Docker containers.  It allows us to specify our *Infrastructure as Code (IaC)*.  The `docker-compose.yml` file contains all the details for our containers.

### Build the System

```
docker-compose build
```

### Launch the System

```
docker-compose up -d
```

* `-d` - launch all containers in *detached* mode.


### Stop the System

```
docker-compose down
```


## References

* [The NGINX Official Docker Page](https://hub.docker.com/_/nginx)
* [The Docker Docs: docker run](https://docs.docker.com/engine/reference/commandline/container_run/)
