# Use an official Python runtime as a parent image
FROM python:3.12.0

# Set the working directory in the container to /app
WORKDIR /app

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Make port 80 available to the world outside this container
EXPOSE 80

# Uncomment the following line if you have a logging configuration file
# ENV UVICORN_LOG_CONFIG=/app/logging.conf

# Run app.py when the container launches using uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
