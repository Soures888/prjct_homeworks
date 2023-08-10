# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in Docker to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY python_script/requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY python_script/script.py /app/

# Run script.py when the container launches
CMD ["python", "./script.py"]
