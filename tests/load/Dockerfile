FROM loadimpact/k6

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Run the tests
ENTRYPOINT ["/bin/sh", "./bin/runk6.sh"]
