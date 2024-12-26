from flask import Flask, jsonify, send_from_directory, redirect, url_for
from flask_cors import CORS
import os
import subprocess
import pymongo
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
import time
import sys

load_dotenv()

# Flask app initialization
app = Flask(__name__, static_folder='../frontend/dist', static_url_path='/')
CORS(app)

sys.stdout.reconfigure(encoding='utf-8')

# MongoDB setup
client = pymongo.MongoClient(os.getenv("MONGO_URI"))  # Connect to MongoDB
db = client['trending_db']  # Use your desired database name
collection = db['trends']  # Use your desired collection name


def setup_proxy():
    """Set up ProxyMesh proxy configuration for rotating IPs."""
    # Replace these with your actual ProxyMesh username and password
    username = os.getenv('PROXY_USERNAME')
    password = os.getenv('PROXY_PASSWORD')   

    # Proxy URL format
    proxy_url = f"http://{username}:{password}@proxy.proxymesh.com:31280"

    # Set up the proxy configuration
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(f'--proxy-server={proxy_url}')
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("--headless")  # Runs Chrome in headless mode
    chrome_options.add_argument("--disable-gpu")  # Disables GPU acceleration
    chrome_options.add_argument("--no-proxy-server")  # Ensures proxy settings are respected

    return chrome_options

def login_to_twitter(driver, username, password):
    """Logs into Twitter using the provided credentials."""
    driver.get("https://twitter.com/login")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "text"))
    )
    
    # Enter username
    username_field = driver.find_element(By.NAME, "text")
    username_field.send_keys(username)
    username_field.send_keys(Keys.RETURN)
    
    # Wait for the password field
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "password"))
    )
    
    # Enter password
    password_field = driver.find_element(By.NAME, "password")
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)
    
    # Wait for login to complete
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )
    print("Logged in to Twitter successfully!")

def get_ip_address():
    """Fetch the current public IP address being used by the proxy."""
    response = requests.get('https://api.ipify.org?format=json')
    ip_data = response.json()
    return ip_data['ip']

def navigate_to_for_you(driver):
    """Navigates to the 'For You' section of Twitter."""
    explore_url = "https://x.com/explore/tabs/for-you"
    driver.get(explore_url)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "main"))
    )
    print("Navigated to the 'For You' section successfully!")

def extract_trending_topics(driver, limit=5):
    """Extracts trending topics from the 'For You' section."""
    # Use Selenium to fetch the dynamically rendered elements
    elements = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//main//span[@dir='ltr']"))
    )
    
      # Extract the top trends
    trends = [element.text for element in elements[:limit]]
    return trends

def save_trends_to_mongo(ip_address, trends):
    """Saves the trending topics along with the proxy IP to MongoDB."""
    trend_data = {
        "IP": ip_address,  # Store IP in a separate field
        "trends": trends,
        "timestamp": time.time()  # Add a timestamp for record uniqueness
    }
    collection.insert_one(trend_data)
    print(f"Trending topics saved to MongoDB with IP {ip_address}")

@app.route('/run_script')
def run_script():
    """Main function to perform all steps."""
    username = os.getenv('TWITTER_USERNAME')
    password = os.getenv('TWITTER_PASSWORD')

    chrome_options = setup_proxy()
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        # Login to Twitter
        login_to_twitter(driver, username, password)

        time.sleep(5)  # Optional: Allow time to review the browser after login
        
        # Navigate to the 'For You' section
        navigate_to_for_you(driver)
        
        # Extract and print trending topics
        trends = extract_trending_topics(driver, limit=5)

        # Get the IP address used by ProxyMesh
        ip_address = get_ip_address()

        # Save the trends and IP to MongoDB
        save_trends_to_mongo(ip_address, trends)

        time.sleep(5)  
    
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        # Close the browser
        time.sleep(5)  # Optional: Allow time to review the browser before closing
        driver.quit()
        return jsonify({"message": "Script executed successfully!"})

@app.route('/api/trending')
def api_trending():
    """API endpoint to fetch trending topics."""
    try:
        trending_data = list(collection.find())
        
        # Convert ObjectId to string
        for record in trending_data:
            record['_id'] = str(record['_id'])
        
        print(f"Fetched {len(trending_data)} trending records from MongoDB")
        return jsonify(trending_data)
    except Exception as e:
        print(f"An error occurred while fetching trending data: {e}")
        return jsonify({"error": "Failed to fetch trending data"}), 500


@app.route('/')
def index():
    """Serve the React app."""
    return send_from_directory(app.static_folder, 'index.html')


if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5500)
