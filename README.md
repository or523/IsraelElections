# Israel Elections

This script is used in order to calculate the elections results.

## Usage

For simple usage, just run:
```bash
python3 elections_results.py [-h] [--city CITY] elections_year
```

## Components

It has 3 main components:

1. `elections_results.py` - provides CLI interface; shows a plotly graph with the results.
2. `bader_ofer.py` - calculate the Bader-Ofer method in order to convert votes to seats.
3. `elections_website.py` - retrieves the elections results from the official website.

