# Use Python 3.8 as the base image
FROM python:3.8

# Set the working directory in the Docker container
WORKDIR /code

# Copy only the requirements.txt file to use Docker cache
COPY ./requirements.txt /code/requirements.txt

# Install pip and Python dependencies from requirements.txt
RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the entire project directory into the container
COPY . /code/

# Expose port 80
EXPOSE 80

# Command to run the application using uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]
