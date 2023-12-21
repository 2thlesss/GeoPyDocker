# Use an official Golang image as a builder stage
FROM golang:1.18 AS builder

# Set the working directory for building
WORKDIR /app

# Download and build geoipupdate
RUN go install github.com/maxmind/geoipupdate/v6/cmd/geoipupdate@latest

# Use an official Python runtime as a parent image
FROM python:3.11.0-slim-buster

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the application code and requirements.txt into the container
COPY . .

# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the geoipupdate binary from the builder stage
COPY --from=builder /go/bin/geoipupdate /usr/local/bin/geoipupdate

# Use build arguments for MaxMind AccountID and LicenseKey
ARG MAXMIND_ACCOUNT_ID=YourMaxMindAccountIDHere
ARG MAXMIND_LICENSE_KEY=YourMaxMindLicenseKeyHere

# Set environment variables with build arguments as defaults
ENV MAXMIND_ACCOUNT_ID=${MAXMIND_ACCOUNT_ID}
ENV MAXMIND_LICENSE_KEY=${MAXMIND_LICENSE_KEY}

# Create GeoIP.conf file using environment variables
RUN echo "AccountID ${MAXMIND_ACCOUNT_ID}\nLicenseKey ${MAXMIND_LICENSE_KEY}\nEditionIDs GeoLite2-City GeoLite2-Country GeoLite2-ASN" > /usr/src/app/GeoIP.conf

# Download the GeoLite2 databases
RUN geoipupdate -v -f /usr/src/app/GeoIP.conf -d /usr/share/GeoIP

# Make port 80 available to the world outside this container
EXPOSE 80

# Run the Python script when the container launches
CMD ["python", "./geo.py"]
