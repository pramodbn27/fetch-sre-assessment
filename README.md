# HTTP Endpoint Health Checker

## Overview
This program monitors the health of a set of HTTP endpoints provided in a YAML configuration file. It tests the endpoints every 15 seconds, calculates their availability percentage, and logs the results to the console.

## Features
- Parses a list of HTTP endpoints from a YAML configuration file.
- Sends HTTP requests to each endpoint every 15 seconds.
- Tracks the availability percentage of each URL domain over the lifetime of the program.
- Logs the cumulative availability percentage of each domain to the console after each test cycle.

## Requirements
- Python 3.7 or higher
- Required Python libraries:
  - pyyaml
  - requests

Install the required libraries using:
```
pip install pyyaml requests
```

## Installation
- Clone this repository or download the `health_check.py` and `config.yaml` files.

## Usage
1. Ensure `health_check.py` and `config.yaml` are in the same directory or Replace `<path_to_yaml_config_file>` with the path to your YAML configuration file.
2. You can modify the existing `config.yaml` or create your own with the desired endpoints.
3. Run the script using one of the following commands:
   ```
   python health_check.py config.yaml
   ```
   or
   ```
   python health_check.py <path_to_yaml_config_file>
   ```

## Sample Output
When you run the program, you'll see output similar to this:
```
fetch.com has 67% availability percentage
www.fetchrewards.com has 100% availability percentage
fetch.com has 83% availability percentage
www.fetchrewards.com has 100% availability percentage
fetch.com has 89% availability percentage
www.fetchrewards.com has 100% availability percentage
```

The program will continue running and updating the percentages every 15 seconds until you stop it using Ctrl+C.

## Stopping the Program
To stop the program, press Ctrl+C. The program will catch this interrupt and exit gracefully.

## Notes
- An endpoint is considered UP if it returns a 2xx status code and responds in less than 500ms.
- The availability percentage is calculated as: (number of UP responses / total number of requests) * 100
- Percentages are rounded to the nearest whole number.