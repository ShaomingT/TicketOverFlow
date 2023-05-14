# Dockerfile to run the python unit tests
FROM python:3.10

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . tests

# Install any needed packages specified in requirements.txt
RUN pip install requests pytest pytest-reportlog

# Run the unit tests
CMD ["python", "-m", "pytest", "--report-log", "report.log", "tests"]