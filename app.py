import pygame
import requests
from bs4 import BeautifulSoup

# Scrape headlines
url = "https://www.nbcsports.com/fantasy/basketball/player-news"
response = requests.get(url)
response.raise_for_status()
soup = BeautifulSoup(response.text, 'html.parser')
headlines = [headline.get_text(strip=True) for headline in soup.find_all('div', class_='PlayerNewsPost-headline')]

# Prepare the scrolling list
scrolling_headlines = headlines * 3  # Repeat headlines three times

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
x_positions = []

# Initialize dictionary to track displayed headlines
displayed_headlines = {}

# Calculate initial x-positions with proper spacing
current_x = screen_width
for headline in scrolling_headlines:
    x_positions.append(current_x)
    current_x += font.size(headline)[0] + text_gap  # Add width of text + gap

# Main loop
running = True
while running:
    screen.fill(black)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Display headlines and update positions
    for i, headline in enumerate(scrolling_headlines):
        text = font.render(headline, True, white)
        text_rect = text.get_rect()
        text_rect.x = x_positions[i]
        text_rect.y = (screen_height - text_rect.height) // 2
        screen.blit(text, text_rect)

        # Update displayed count in dictionary
        if headline not in displayed_headlines:
            displayed_headlines[headline] = 1
        else:
            displayed_headlines[headline] += 1

        # If a headline has been displayed 3 times, remove it
        if displayed_headlines[headline] >= 3:
            # Remove the headline and adjust scrolling list
            displayed_headlines.pop(headline, None)
            scrolling_headlines = [h for h in scrolling_headlines if displayed_headlines.get(h, 0) < 3]

        # Move headline left
        x_positions[i] -= speed

        # Reset position when a headline scrolls off screen
        if x_positions[i] < -text_rect.width:
            # Place the headline at the end of the last one
            last_visible_index = (i - 1) % len(scrolling_headlines)
            x_positions[i] = x_positions[last_visible_index] + font.size(scrolling_headlines[last_visible_index])[0] + text_gap

    pygame.display.flip()
    clock.tick(60)

pygame.quit()


