import sys
import time
import yaml
import requests
import signal
from collections import defaultdict
from urllib.parse import urlparse

# Handle SIGINT for graceful exit
def signal_handler(sig, frame):
    print("\nProgram interrupted by user. Exiting...")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Parse the YAML configuration file
def parse_yaml(file_path):
    try:
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)
    except (yaml.YAMLError, IOError) as e:
        print(f"Error reading or parsing YAML file: {e}")
        sys.exit(1)

# Check the health of a given endpoint
def check_health(endpoint):
    method = endpoint.get('method', 'GET')
    url = endpoint['url']
    headers = endpoint.get('headers', {})
    body = endpoint.get('body')

    try:
        start_time = time.time()
        response = requests.request(method, url, headers=headers, data=body, timeout=5)
        latency = (time.time() - start_time) * 1000  # Convert to milliseconds

        # An endpoint is UP if it returns a 2xx status code and the latency is under 500 ms
        return 200 <= response.status_code < 300 and latency < 500
    except requests.RequestException as e:
        print(f"Error checking health for {url}: {e}")
        return False

# Log the availability percentage of each domain
def log_availability(domain_stats):
    for domain, stats in domain_stats.items():
        availability = round(100 * stats['up'] / stats['total'])
        print(f"{domain} has {availability}% availability percentage")

# Main function to initiate health checks
def main(config_file):
    endpoints = parse_yaml(config_file)
    domain_stats = defaultdict(lambda: {'up': 0, 'total': 0})

    try:
        while True:
            for endpoint in endpoints:
                domain = urlparse(endpoint['url']).netloc
                is_up = check_health(endpoint)
                
                domain_stats[domain]['total'] += 1
                if is_up:
                    domain_stats[domain]['up'] += 1

            log_availability(domain_stats)
            time.sleep(15)
    except KeyboardInterrupt:
        print("\nProgram terminated by user")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python health_check.py <config_file_path>")
        sys.exit(1)
    
    main(sys.argv[1])
