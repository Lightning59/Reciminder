# Use the official Python base image
FROM python:3.12

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
ADD Django .

#comment out for final non-dev releases
WORKDIR /
ADD db.sqlite3 .
WORKDIR /app

# Expose the port the app will run on
EXPOSE 8000