this docker container is intended to be used with a maxmind account

It is a python script that uses the geolocation databese from MaxMind, and give output choices in latlong or UTM for city location
It also includes ANS and Country locations, as well a host name resolution.


docker build --build-arg MAXMIND_ACCOUNT_ID=123456 --build-arg MAXMIND_LICENSE_KEY=abcdef123456 -t geolocator-app .

You are able to input your account ID and your key when building the container for the first time.

docker run -p 4000:80 geolocator-app
after a successful build.

You may need to change the python version in the docker file to what you are running on your host machine.

