#!/usr/bin/python3

import geoip2.database
import socket
import pyproj

# Database paths
city_db_path = '/usr/share/GeoIP/GeoLite2-City.mmdb'
country_db_path = '/usr/share/GeoIP/GeoLite2-Country.mmdb'
asn_db_path = '/usr/share/GeoIP/GeoLite2-ASN.mmdb'

# Function for LatLong to UTM
def latlong_to_utm(latitude, longitude):
    if latitude is not None and longitude is not None:
        # Determine UTM zone
        utm_zone = calc_utm_zone(longitude)
        
        # Create UTM converter using the calculated zone
        utm_converter = pyproj.Proj(proj='utm', zone=utm_zone, ellps='WGS84')
        utm_x, utm_y = utm_converter(longitude, latitude)

        # Determine hemisphere (N for Northern, S for Southern)
        hemisphere = 'N' if latitude >= 0 else 'S'

        return f"{utm_zone}{hemisphere} {utm_x:.2f}E {utm_y:.2f}N"
    else:
        return None

def calc_utm_zone(longitude):
    return int(1 + (longitude + 180.0) / 6.0)

# Function for City Lookup
def city_lookup(ip_address):
    try:
        ip_address = socket.gethostbyname(ip_address)
    except socket.gaierror:
        print('Invalid address or domain name')
        return

    with geoip2.database.Reader(city_db_path) as reader:
        response = reader.city(ip_address)
        print("Country:", response.country.name)
        print("City:", response.city.name)

        # Ask user for coordinate format preference
        coord_format = input("Choose coordinate format (1: Latitude/Longitude, 2: UTM): ").strip()

        if coord_format == '1':
            print("Latitude:", response.location.latitude)
            print("Longitude:", response.location.longitude)
        elif coord_format == '2':
            # Convert to UTM and print the result
            utm_coords = latlong_to_utm(response.location.latitude, response.location.longitude)
            if utm_coords:
                print("UTM Coordinates:", utm_coords)
            else:
                print("Could not convert to UTM coordinates.")
        else:
            print("Invalid coordinate format selection.")


# Function for Country Lookup
def country_lookup(ip_address):
    try:
        ip_address = socket.gethostbyname(ip_address)
    except socket.gaierror:
        print('Invalid address or domain name')
        return

    with geoip2.database.Reader(country_db_path) as reader:
        response = reader.country(ip_address)
        print("Country:", response.country.name)

# Function for ASN Lookup
def asn_lookup(ip_address):
    try:
        ip_address = socket.gethostbyname(ip_address)
    except socket.gaierror:
        print('Invalid address or domain name')
        return

    with geoip2.database.Reader(asn_db_path) as reader:
        response = reader.asn(ip_address)
        print("ASN Number:", response.autonomous_system_number)
        print("ASN Organization:", response.autonomous_system_organization)

# Main program function
def main():
    ip_to_lookup = input('Enter IP Address or domain name to Geolocate: ')

    print("1. City Lookup")
    print("2. Country Lookup")
    print("3. ASN Lookup")
    choice = input("Choose the type of lookup (1-3): ")

    if choice == '1':
        city_lookup(ip_to_lookup)
    elif choice == '2':
        country_lookup(ip_to_lookup)
    elif choice == '3':
        asn_lookup(ip_to_lookup)
    else:
        print("Invalid choice.")

# Run the main function
if __name__ == "__main__":
    main()
