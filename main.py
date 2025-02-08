import requests
import feedparser
from flask import Flask, render_template, request, flash
from datetime import datetime
import geopy.distance
from geopy.geocoders import Nominatim
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Required for flashing messages

FUEL_TYPES = {
    '1': 'ULP',
    '2': 'PULP',
    '4': 'Diesel',
    '5': 'LPG',
    '6': 'Brand Diesel',
    '10': '98 RON',
    '11': 'E85'
}

DISTANCE_OPTIONS = {
    '0': 'No limit',
    '5': '5 km',
    '10': '10 km',
    '15': '15 km',
    '20': '20 km',
    '25': '25 km',
    '30': '30 km',
}

def get_coordinates(address):
    logger.debug(f"Attempting to get coordinates for address: {address}")
    try:
        geolocator = Nominatim(user_agent="fuelwatch_app")
        location = geolocator.geocode(f"{address}, Western Australia, Australia")
        if location:
            logger.debug(f"Coordinates found: {location.latitude}, {location.longitude}")
            return (location.latitude, location.longitude)
        else:
            logger.error(f"No coordinates found for address: {address}")
            return None
    except Exception as e:
        logger.error(f"Error getting coordinates: {str(e)}")
        return None

def get_fuel_data(product=1, suburb=None):
    """Get fuel data for specified suburb and surrounding regions"""
    logger.debug(f"Fetching fuel data for {suburb if suburb else 'Perth metro area'}")
    base_url = "http://www.fuelwatch.wa.gov.au/fuelwatch/fuelWatchRSS"
    
    # Extract just the suburb name from the full address
    if suburb:
        # Try to extract just the suburb name (e.g., "Armadale" from "Neerigen St, Armadale WA 6112")
        suburb_parts = suburb.split(',')
        if len(suburb_parts) > 1:
            suburb = suburb_parts[1].strip().split()[0]  # Get just "Armadale"
    
    # First try with specific suburb
    params = {
        "Product": product,
        "Suburb": suburb if suburb else "",
        "Surrounding": "yes"  # Include surrounding areas
    }
    
    try:
        logger.debug(f"Making request with params: {params}")
        response = requests.get(base_url, params=params, headers={'user-agent': 'Mozilla/5.0'})
        logger.debug(f"Response status code: {response.status_code}")
        
        feed_data = feedparser.parse(response.content)
        if feed_data.entries:
            logger.debug(f"Found {len(feed_data.entries)} fuel stations for {suburb}")
            return feed_data.entries
            
        # If no results, try with region search
        logger.debug("No results for suburb, trying region search")
        params = {
            "Product": product,
            "Region": "26",  # Southeast metro (includes Armadale)
            "Surrounding": "yes"
        }
        
        response = requests.get(base_url, params=params, headers={'user-agent': 'Mozilla/5.0'})
        feed_data = feedparser.parse(response.content)
        if feed_data.entries:
            logger.debug(f"Found {len(feed_data.entries)} fuel stations in region")
            return feed_data.entries
            
        logger.error("No fuel data found in feed")
        return None
    except requests.RequestException as e:
        logger.error(f"Error fetching data: {str(e)}")
        return None

def sort_by_distance(fuel_data, user_coords, max_distance=0):
    """Sort stations by distance and filter by max_distance if specified"""
    if not user_coords or not fuel_data:
        return fuel_data

    stations_with_distance = []
    for station in fuel_data:
        try:
            station_coords = (float(station.latitude), float(station.longitude))
            distance = geopy.distance.distance(user_coords, station_coords).km
            station.distance = round(distance, 2)
            # Only add stations within max_distance (if specified)
            if max_distance == 0 or distance <= float(max_distance):
                stations_with_distance.append(station)
        except Exception as e:
            logger.error(f"Error calculating distance: {str(e)}")
            continue

    # Sort all stations by distance
    sorted_data = sorted(stations_with_distance, key=lambda x: x.distance)
    if sorted_data:
        logger.debug(f"Closest station is {sorted_data[0].distance}km away")
    
    return sorted_data[:30]  # Return closest 30 stations within distance limit

@app.route('/', methods=['GET', 'POST'])
def index():
    suburb = request.form.get('suburb', '')
    fuel_type = request.form.get('fuel_type', '1')  # Default to ULP
    max_distance = request.form.get('max_distance', '0')  # Default to no limit
    fuel_data = None
    
    logger.debug(f"Request method: {request.method}")
    logger.debug(f"Address submitted: {suburb}")
    logger.debug(f"Fuel type selected: {FUEL_TYPES.get(fuel_type)}")
    logger.debug(f"Max distance selected: {DISTANCE_OPTIONS.get(max_distance)}")
    
    if request.method == 'POST' and suburb:
        user_coords = get_coordinates(suburb)
        if user_coords:
            fuel_data = get_fuel_data(product=int(fuel_type), suburb=suburb)
            if fuel_data:
                fuel_data = sort_by_distance(fuel_data, user_coords, float(max_distance))
                logger.debug(f"Processed {len(fuel_data)} stations")
                if fuel_data:
                    logger.debug(f"Closest station is {fuel_data[0].distance}km away")
            else:
                flash("Error fetching fuel station data")
        else:
            flash("Could not find the specified location")
    
    return render_template('index.html', 
                         fuel_data=fuel_data, 
                         suburb=suburb, 
                         fuel_types=FUEL_TYPES,
                         distance_options=DISTANCE_OPTIONS,
                         selected_fuel=fuel_type,
                         selected_distance=max_distance)


if __name__ == "__main__":
    app.run(debug=True)