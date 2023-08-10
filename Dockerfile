# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Install any necessary dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev

# Install Python libraries
RUN pip install Flask
RUN pip install flask_cors
RUN pip install numpy
RUN pip install pandas
RUN pip install joblib
RUN pip install haversine
RUN pip install scikit-learn==1.2.0
RUN pip install pycaret

# Make port 5000 available to the world outside this container
EXPOSE 5001

# Run predict.py when the container launches
CMD ["python", "predict.py"]