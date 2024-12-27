import requests
from bs4 import BeautifulSoup

# URL to scrape
url = "https://www.nbcsports.com/fantasy/basketball/player-news"

# Send a GET request to the webpage
response = requests.get(url)
response.raise_for_status()  # Ensure the request was successful

# Parse the HTML content
soup = BeautifulSoup(response.text, 'html.parser')

# Find all divs with the class 'PlayerNewsPost-headline'
headlines = soup.find_all('div', class_='PlayerNewsPost-headline')

# Extract and print the text content of each headline
for headline in headlines:
    print(headline.get_text(strip=True))
