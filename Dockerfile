# Start with the python 3.10 base image
FROM python:3.10

# Install necessary system packages
RUN apt-get update --fix-missing && apt-get install -y --fix-missing \
    build-essential \
    gcc \
    g++ && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory in the docker image
WORKDIR /IX-Production

# Copy the requirements file into the docker image
COPY requirements.txt .

# Install python dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install PyYAML

# Copy the rest of the application into the docker image
COPY . .

# Expose ports for the app to the docker host
EXPOSE 8000 8501

# Set the entrypoint command to run both the Chroma and Streamlit apps
CMD ["streamlit", "run", "app.py", "--server.port", "8501", "--server.address", "0.0.0.0"]
