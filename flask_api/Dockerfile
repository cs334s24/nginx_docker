FROM python:slim

WORKDIR /app

COPY requirements.txt .

RUN python3 -m venv .venv
RUN .venv/bin/pip3 install -r requirements.txt

EXPOSE 8000

COPY app.py .

CMD [".venv/bin/gunicorn", "--bind=0.0.0.0", "app:create_app()"]