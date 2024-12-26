# Trending Topics from Twitter

This project demonstrates how to use Flask, Selenium, MongoDB, and React to scrape trending topics from Twitter, store them in a MongoDB database, and display them on a React frontend.

## Features

- **Web Scraping**: Automates the process of fetching trending topics from Twitter.
- **Data Storage**: Saves the extracted trending topics along with the IP address and timestamp into a MongoDB database.
- **API Endpoint**: Provides an API endpoint to fetch the trending topics from the MongoDB database.
- **Frontend**: Displays the trending topics using a React frontend.

## Tools and Technologies Used

- **Python**: Programming language used for automation and backend development.
- **Flask**: Web framework used to create the backend API.
- **Selenium**: For navigating through Twitter and handling dynamic content.
- **MongoDB**: Database used to store the trending topics.
- **React**: Frontend library used to create the user interface.
- **Vite**: Build tool used for the React frontend.

## Setup Instructions

### Backend Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/your-repository.git
   cd your-repository
   ```

2. **Install Dependencies**:
   Ensure you have Python installed. Then, install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. **Download WebDriver**:
   - Install the appropriate WebDriver for your browser (e.g., ChromeDriver for Google Chrome).
   - Add the WebDriver to your system PATH.

4. **Run the Flask Backend**:
   ```bash
   python script.py
   ```

### Frontend Setup

1. **Navigate to the Frontend Directory**:
   ```bash
   cd frontend
   ```

2. **Install Dependencies**:
   Ensure you have Node.js installed. Then, install the required Node.js packages:
   ```bash
   npm install
   ```

3. **Run the Vite Development Server**:
   ```bash
   npm run dev
   ```

## How It Works

### Backend

1. **Login to Twitter**:
   - The script logs into Twitter using the provided credentials.

2. **Navigate to the 'For You' Section**:
   - Selenium automates the browser to navigate to the 'For You' section on Twitter.

3. **Extract Trending Topics**:
   - Extracts trending topics from the HTML structure of the Twitter page using Selenium.

4. **Save to MongoDB**:
   - Saves the extracted trending topics along with the IP address and timestamp into a MongoDB database.

### Frontend

1. **Fetch Trending Topics**:
   - The React frontend fetches the trending topics from the Flask backend API.

2. **Display Trending Topics**:
   - Displays the trending topics along with the IP address and timestamp on the frontend.

## API Endpoints

### `/run_script`
- **Method**: GET
- **Description**: Runs the script to scrape trending topics from Twitter and save them to MongoDB.
- **Response**: JSON message indicating the success or failure of the script execution.

### `/api/trending`
- **Method**: GET
- **Description**: Fetches the trending topics from MongoDB.
- **Response**: JSON array of trending topics.

## Example Output

### Trending Topics
```json
[
  {
    "_id": "60c72b2f9b1d4c3d8c8e4e5b",
    "IP": "103.159.42.91",
    "trends": ["Trend1", "Trend2", "Trend3", "Trend4", "Trend5"],
    "timestamp": 1623667200
  }
]
```

## Prerequisites

- Python 3.7+
- Node.js and npm
- Browser and corresponding WebDriver (e.g., Google Chrome + ChromeDriver)
- MongoDB instance

## Future Enhancements

- Add support for more social media platforms.
- Include error handling for dynamic content and network issues.
- Visualize the data using charts and graphs.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments

- The Flask, Selenium, MongoDB, and React communities for their excellent libraries and documentation.

Feel free to contribute to this project or raise any issues via the repository’s Issues section!
```

