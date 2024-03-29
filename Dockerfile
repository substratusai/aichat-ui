FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*


COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY main.py main.py

EXPOSE 8081

ENV STREAMLIT_CLIENT_TOOLBAR_MODE="viewer"
HEALTHCHECK CMD curl --fail http://localhost:8081/_stcore/health

ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=8081", "--server.address=0.0.0.0"]