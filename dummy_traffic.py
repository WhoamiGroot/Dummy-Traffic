import requests
import random
import time
import sys
from concurrent.futures import ThreadPoolExecutor

# List of example user-agent strings to simulate different browsers
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; SM-G970F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_5_1 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Version/13.1.2 Safari/537.36"
]

# List of example paths to simulate page visits
paths = ['/home', '/about', '/contact', '/products', '/blog']

# Function to log requests to a file
def log_request(url, status_code):
    try:
        with open("traffic_log.txt", "a") as log_file:
            log_file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {url} - Status: {status_code}\n")
    except Exception as e:
        print(f"Error logging request: {e}")

# Function to simulate traffic to a target URL
def generate_traffic(url, delay):
    path = random.choice(paths)
    full_url = f"{url}{path}"

    headers = {
        "User-Agent": random.choice(user_agents),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "Accept-Encoding": "gzip, deflate, br",  # Simulate compressed response
        "Referer": f"{url}/somepage",  # Random or static referer
    }

    # Randomly decide to send a GET or POST request
    try:
        if random.choice([True, False]):
            response = requests.get(full_url, headers=headers, timeout=5)
            print(f"GET request to {full_url} - Status code: {response.status_code}")
        else:
            response = requests.post(full_url, headers=headers, timeout=5)
            print(f"POST request to {full_url} - Status code: {response.status_code}")
        
        # Log the request status to a file
        log_request(full_url, response.status_code)

    except requests.RequestException as e:
        print(f"Error requesting {full_url}: {e}")
        log_request(full_url, "Error")

# Function to generate traffic using multiple threads (to simulate many users)
def generate_traffic_multiple(url, num_requests=100, delay=1):
    with ThreadPoolExecutor(max_workers=20) as executor:
        for _ in range(num_requests):
            executor.submit(generate_traffic, url, delay)
            time.sleep(delay)

if __name__ == "__main__":
    # Check if the correct number of arguments is provided
    if len(sys.argv) != 4:
        print("Usage: python3 dummy_traffic.py <URL> <num_requests> <delay>")
        sys.exit(1)

    # Get the target URL, number of requests, and delay between requests from command-line arguments
    target_url = sys.argv[1]
    num_requests = int(sys.argv[2])
    delay = float(sys.argv[3])

    print(f"Starting traffic generation to {target_url}...")

    try:
        # Generate traffic to the target URL
        generate_traffic_multiple(target_url, num_requests, delay)
    except Exception as e:
        print(f"Error during traffic generation: {e}")

