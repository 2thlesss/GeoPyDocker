this docker container is intended to be used with a maxmind account

It is a python script that uses the geolocation database from MaxMind, and gives output choices in latlong or UTM for city location
It also includes ANS and Country locations, as well a host name resolution.


docker build \
  --build-arg MAXMIND_ACCOUNT_ID=YourMaxMindAccountIDHere \
  --build-arg MAXMIND_LICENSE_KEY=YourMaxMindLicenseKeyHere \
  -t geolocator-app .



You are able to input your account ID and your key when building the container for the first time.

docker run -e MAXMIND_ACCOUNT_ID=YourMaxMindAccountIDHere \
           -e MAXMIND_LICENSE_KEY=YourMaxMindLicenseKeyHere \
           -p 80:80 -it geolocator-app /bin/bash


After you're in the shell, just run the script with python geo.py




