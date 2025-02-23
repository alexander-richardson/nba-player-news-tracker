# NBA Scrolling Headlines

This project displays dynamically scrolling NBA player news headlines fetched from [NBC Sports Fantasy Basketball](https://www.nbcsports.com/fantasy/basketball/player-news). The application is designed to run on a Raspberry Pi, outputting to an HDMI-connected display, such as a 5-inch screen, for real-time updates.

See it in action! https://youtu.be/YfccXdPllzo

## Features

- **Dynamic Headline Fetching:**
  - Headlines are fetched every 30 seconds from the NBA player news section of NBC Sports.
- **Smooth Scrolling:**
  - Headlines scroll horizontally across the screen with customizable speed and text size.
- **Repetition and Order:**
  - Each headline is displayed in sequence, repeated three times for better visibility.
- **Customizable Design:**
  - Easily modify the font size, colors, scrolling speed, or add background images and other enhancements.

## Requirements

### Hardware

- Raspberry Pi (e.g., Raspberry Pi Zero 2 W)
- HDMI-connected screen (e.g., 5-inch display)
- Power supply for the Pi and screen

### Software

- Python 3.7+
- Pygame
- BeautifulSoup4
- Requests

## Installation

1. **Clone the Repository:**
   ```bash
   git clone <repository-url>
   cd <repository-directory>

2. **Install Dependencies:**
 ```bash
sudo apt update
sudo apt install python3-pip
pip3 install pygame beautifulsoup4 requests
```
3 **Run the Application:**
```bash
DISPLAY=:0 python3 app.py ```
```
## How It Works

### Headline Fetching

- The `fetch_updates()` function fetches the latest player news headlines every 30 seconds.
- Headlines are parsed from the HTML of the source webpage using BeautifulSoup.

### Scrolling Logic

- Headlines are stored as `(headline, x_position)` pairs and rendered at calculated positions.
- Each headline scrolls leftward until it moves off-screen, after which it is removed.

### Dynamic Updates

- New batches of headlines are only fetched after the current batch finishes scrolling.

### Dynamic Speed

- Scrolling speed is slightly varied for smooth and visually dynamic motion.





