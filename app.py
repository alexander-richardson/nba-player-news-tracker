import pygame
import requests
from bs4 import BeautifulSoup
import threading
import time
import math 

# URL to scrape headlines
url = "https://www.nbcsports.com/fantasy/basketball/player-news"

# Global variables
scrolling_data = []  # Stores tuples of (headline, x_position)
running = True
lock = threading.Lock()  # Add a lock to prevent race conditions

# Pygame setup
pygame.init()
screen_width = 800
screen_height = 100
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Scrolling Headlines")
font = pygame.font.Font(None, 72)
clock = pygame.time.Clock()

# Colors
black = (0, 0, 0)
white = (255, 255, 255)

# Scrolling variables
speed = 2
text_gap = 200  # Minimum space between consecutive headlines
repeats = 3  # Number of times each headline should scroll

# Function to fetch updates from the website
def fetch_updates():
    global scrolling_data
    while running:
        try:
            # Fetch and parse the website
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract all headlines in order
            new_headlines = [
                headline.get_text(strip=True)
                for headline in soup.find_all('div', class_='PlayerNewsPost-headline')
            ]

            with lock:
                # Only add new headlines if scrolling_data is empty
                if not scrolling_data:
                    current_x = screen_width  # Start from the right edge
                    for _ in range(repeats):  # Repeat each headline 3 times
                        for headline in new_headlines:
                            scrolling_data.append((headline, current_x))
                            current_x += font.size(headline)[0] + text_gap

                print(f"fetch_updates: {len(scrolling_data)} items loaded")

        except Exception as e:
            print(f"Error fetching updates: {e}")

        time.sleep(30)  # Wait before the next update

# Start the background thread for updates
thread = threading.Thread(target=fetch_updates, daemon=True)
thread.start()

# Main loop
running = True
while running:
    screen.fill(black)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update the speed dynamically
    speed = (2 + abs(math.sin(pygame.time.get_ticks() / 1000)) + font.size("A")[0] / 50) * 1.5



    with lock:
        # Render and scroll headlines
        for i in range(len(scrolling_data) - 1, -1, -1):  # Iterate in reverse for safe removal
            headline, x_position = scrolling_data[i]
            text = font.render(headline, True, white)
            text_rect = text.get_rect()
            text_rect.x = x_position
            text_rect.y = (screen_height - text_rect.height) // 2
            screen.blit(text, text_rect)

            # Move the headline left
            scrolling_data[i] = (headline, x_position - speed)

            # Remove if off-screen
            if x_position + text_rect.width < 0:
                scrolling_data.pop(i)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

# End the background thread
running = False
