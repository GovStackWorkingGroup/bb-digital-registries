# Use an official Python runtime as the base image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /deepDiveDemo

# Copy the current directory contents into the container
COPY . .

# Set environment variable for Python to enable absolute imports
ENV PYTHONPATH=/deepDiveDemo

# Install required packages using pip
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Expose port 5000 for Flask
EXPOSE 5000

# Define environment variable for Flask to run in production mode
ENV FLASK_ENV=production

# Run app.py using Python when the container launches
CMD ["python", "flask_app/app.py"]
