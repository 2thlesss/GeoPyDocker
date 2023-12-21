# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Install geoipupdate
RUN apt-get update && apt-get install -y geoipupdate

# Define environment variables for MaxMind AccountID and LicenseKey
ENV MAXMIND_ACCOUNT_ID=YourMaxMindAccountIDHere
ENV MAXMIND_LICENSE_KEY=YourMaxMindLicenseKeyHere

# Create GeoIP.conf file using environment variables
RUN echo "AccountID ${MAXMIND_ACCOUNT_ID}\nLicenseKey ${MAXMIND_LICENSE_KEY}\nEditionIDs GeoLite2-City GeoLite2-Country" > /usr/src/app/GeoIP.conf

# Download the GeoLite2 databases
RUN geoipupdate -v -f /usr/src/app/GeoIP.conf -d /usr/share/GeoIP

# Make port 80 available to the world outside this container
EXPOSE 80

# Run the Python script when the container launches
CMD ["python", "./geo.py"]
