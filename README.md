# FuelWatch AU Project by SPLATPLAYS

A Flask web application that helps users find the closest and cheapest fuel stations in Western Australia using the FuelWatch API.

## Features

- Search for fuel stations by suburb or address in Western Australia
- Display the 30 closest fuel stations to your location
- Show fuel prices, station details, and distance information
- Real-time data from WA FuelWatch
- Mobile-responsive design

## Prerequisites

- Python 3.8+
- pip (Python package installer)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/SPLATPLAYS/fuelwatch-app.git
cd fuelwatch-app
```

2. Install required packages:
```bash
pip install flask requests feedparser geopy
```

## Usage

1. Start the application:
```bash
python main.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

3. Enter your suburb or address (e.g., "Neerigen St, Armadale WA 6112")

## API Information

This application uses:
- WA FuelWatch RSS Feed API
- OpenStreetMap's Nominatim for geocoding

## Project Structure

```
fuelwatch-app/
├── main.py              # Main application file
├── README.md           # Project documentation
└── templates/          # HTML templates
    └── index.html     # Main page template
```

## Configuration

The application uses the following default settings:
- Development server on localhost:5000
- Debug mode enabled
- Maximum of 30 stations displayed
- Distances in kilometers

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Data provided by [WA FuelWatch](https://www.fuelwatch.wa.gov.au)
- Geocoding by [OpenStreetMap](https://www.openstreetmap.org)

## Author

SPLATPLAYS

## Support

For support, please open an issue in the GitHub repository.
```

This README.md provides:
- Clear project description
- Installation instructions
- Usage guide
- Project structure
- Configuration details
- Contributing guidelines
- License information
- Acknowledgments and support information

You can save this as `README.md` in your project root directory. Feel free to modify any sections to better match your project's specific needs or requirements.
This README.md provides:
- Clear project description
- Installation instructions
- Usage guide
- Project structure
- Configuration details
- Contributing guidelines
- License information
- Acknowledgments and support information

You can save this as `README.md` in your project root directory. Feel free to modify any sections to better match your project's specific needs or requirements.