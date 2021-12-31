FROM backend:dependencies

## Copy local code to the container image.
RUN mkdir -p /app
WORKDIR /app
# COPY ./requirements.txt /app/requirements.txt
# COPY ./backend/main.py /app/main.py
COPY . /app/

# Set an environment variable for the port for 8000
ENV PORT 8000

# Run gunicorn bound to the 8000 port.docker run --rm -p 8000:8000 -e PORT=8000 backend:python
# CMD gunicorn --bind :$PORT --workers 1 --threads 8 server:app
CMD [ "python", "./TornadoServer.py" ]

# docker build --tag backend:dependencies -f DockerFileBuild .
# docker build --tag backend:python -f Dockerfile .
# docker run --rm -p 8000:8000 -e PORT=8000 --name RDP backend:python --security-opt seccomp=unconfined
# docker run --name some-app -p 8888:8888 --link some-redis:redis -d app
