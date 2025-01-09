import pygame
import requests
from bs4 import BeautifulSoup
import threading
import time

# URL to scrape headlines
url = "https://www.nbcsports.com/fantasy/basketball/player-news"

# Global variables
scrolling_headlines = []
x_positions = []
running = True

# Pygame setup
pygame.init()
screen_width = 800
screen_height = 100
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Scrolling Headlines")
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()

# Colors
black = (0, 0, 0)
white = (255, 255, 255)

# Scrolling variables
speed = 2
text_gap = 100  # Minimum space between consecutive headlines
seen_headlines = set()  # Track seen headlines to avoid duplicates

# Function to fetch updates from the website
def fetch_updates():
    global scrolling_headlines, x_positions
    while running:
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            new_headlines = [
                headline.get_text(strip=True)
                for headline in soup.find_all('div', class_='PlayerNewsPost-headline')
            ]

            # Add only new headlines to the stack if not already present
            for headline in new_headlines:
                if headline not in seen_headlines:
                    seen_headlines.add(headline)

            # Update the scrolling_headlines list
            all_headlines = list(seen_headlines)
            if all_headlines:
                scrolling_headlines.extend(all_headlines * 3)  # Repeat the entire list 3 times

            # Update x_positions based on the new scrolling_headlines
            if scrolling_headlines:
                current_x = x_positions[-1] + font.size(scrolling_headlines[-1])[0] + text_gap if x_positions else screen_width
                for headline in all_headlines * 3:
                    x_positions.append(current_x)
                    current_x += font.size(headline)[0] + text_gap

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

    # Display headlines and update positions if there are any
    if scrolling_headlines:
        for i in range(len(scrolling_headlines) - 1, -1, -1):  # Iterate in reverse to allow safe removal
            headline = scrolling_headlines[i]
            text = font.render(headline, True, white)
            text_rect = text.get_rect()
            text_rect.x = x_positions[i]
            text_rect.y = (screen_height - text_rect.height) // 2
            screen.blit(text, text_rect)

            # Move headline left
            x_positions[i] -= speed

            # Reset position when a headline scrolls off screen
            if x_positions[i] < -text_rect.width:
                scrolling_headlines.pop(i)
                x_positions.pop(i)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

# End the background thread
running = False
