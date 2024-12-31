import pygame
import requests
from bs4 import BeautifulSoup
import schedule
import time

# Function to scrape headlines
def get_headlines():
    url = "https://www.nbcsports.com/fantasy/basketball/player-news"
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    return [headline.get_text(strip=True) for headline in soup.find_all('div', class_='PlayerNewsPost-headline')]

# Update headlines function for schedule
def update_headlines():
    global scrolling_headlines, x_positions, displayed_headlines
    new_headlines = get_headlines()
    for headline in new_headlines:
        if headline not in displayed_headlines:
            scrolling_headlines.extend([headline] * 3)  # Add new headline repeated 3 times
            current_x = x_positions[-1] + font.size(scrolling_headlines[-1])[0] + text_gap
            x_positions.extend([current_x + i * (font.size(headline)[0] + text_gap) for i in range(3)])

# Initialize pygame
pygame.init()

# Screen setup
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

# Initialize headlines
scrolling_headlines = get_headlines() * 3  # Repeat each headline 3 times
x_positions = []
current_x = screen_width
for headline in scrolling_headlines:
    x_positions.append(current_x)
    current_x += font.size(headline)[0] + text_gap

# Dictionary to track displayed counts
displayed_headlines = {headline: 0 for headline in set(scrolling_headlines)}

# Schedule the task to run X minutes
schedule.every(4).minute.do(update_headlines)

# Main loop
running = True
while running:
    screen.fill(black)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Run scheduled tasks
    schedule.run_pending()

    # Display headlines and update positions
    for i, headline in enumerate(list(scrolling_headlines)):  # Use a copy to safely modify the list
        text = font.render(headline, True, white)
        text_rect = text.get_rect()
        text_rect.x = x_positions[i]
        text_rect.y = (screen_height - text_rect.height) // 2
        screen.blit(text, text_rect)

        # Move headline left
        x_positions[i] -= speed

        # Reset position when a headline scrolls off screen
        if x_positions[i] < -text_rect.width:
            displayed_headlines[headline] += 1
            if displayed_headlines[headline] >= 3:
                # Remove headline and update positions
                scrolling_headlines.pop(i)
                x_positions.pop(i)
                continue
            # Place the headline at the end of the last one
            last_visible_index = (i - 1) % len(scrolling_headlines)
            x_positions[i] = x_positions[last_visible_index] + font.size(scrolling_headlines[last_visible_index])[0] + text_gap

    pygame.display.flip()
    clock.tick(60)

pygame.quit()


