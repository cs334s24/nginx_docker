FROM python:slim

# Set the current direcdtory inside the container
# Files will be copied here and commands will be executed here
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Create a virtual environment and install the requirements
RUN python3 -m venv .venv
RUN .venv/bin/pip3 install -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Copy the app into the container
# NOTE: this command is done last because it is the most likely 
# to change.  Docker will cache the previous steps and only re-run
# the steps that have changed.
COPY app.py .

# Run the app and bind it to all networks.  This allows traffic
# from outside the container to reach the app.
CMD [".venv/bin/gunicorn", "--bind=0.0.0.0", "app:create_app()"]