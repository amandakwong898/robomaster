import pygame
import random
import json

# Initialize Pygame
pygame.init()

# Set the screen size
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Create the actors
tagger = pygame.Rect(50, 50, 50, 50)
chased = pygame.Rect(SCREEN_WIDTH - 100, SCREEN_HEIGHT - 100, 50, 50)

# Set the initial direction for the chased actor
chased_dx = 2
chased_dy = 2

# Set the initial direction for the tagger actor
tagger_dx = 3
tagger_dy = 3

# Set the initial score
score = 0

# Set the font and size for the score display
font = pygame.font.SysFont(None, 48)

# Set the initial color for the score display
score_color = (0, 0, 0)

# Set the initial position for the score display
score_x = SCREEN_WIDTH // 2
score_y = 10

# Set the initial collision state to False
collision_occurred = False

# Create lists to store instructions for each actor
chased_instructions = []
tagger_instructions = []

# Main game loop
done = False
while not done:
    # --- Event Processing ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # --- Game Logic ---
    # Move the chased actor
    chased.x += chased_dx
    chased.y += chased_dy

    # If the chased actor hits a wall, reverse direction
    if chased.left < 0 or chased.right > SCREEN_WIDTH:
        chased_dx *= -1
    if chased.top < 0 or chased.bottom > SCREEN_HEIGHT:
        chased_dy *= -1

    # Move the tagger actor
    tagger.x += tagger_dx
    tagger.y += tagger_dy

    # If the tagger actor hits a wall, reverse direction
    if tagger.left < 0 or tagger.right > SCREEN_WIDTH:
        tagger_dx *= -1
    if tagger.top < 0 or tagger.bottom > SCREEN_HEIGHT:
        tagger_dy *= -1

    # Check for collision between the actors
    if chased.colliderect(tagger):
        if not collision_occurred:
            score += 1
            collision_occurred = True
            # Add instructions for each actor
            chased_instructions.append({"command": "move", "direction": "forward", "distance": 1})
            tagger_instructions.append({"command": "turn", "direction": "clockwise", "angle": 90})
    else:
        collision_occurred = False
    # print("Score:", score)
    collision_occurred = False

    # --- Drawing ---
    # Clear the screen
    screen.fill((255, 255, 255))

    # Draw the actors
    pygame.draw.rect(screen, (0, 255, 0), tagger)
    pygame.draw.rect(screen, (255, 0, 0), chased)

    # Draw the score on the screen
    font = pygame.font.Font(None, 36)
    score_text = font.render("Score: " + str(score), True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    # Update the screen
    pygame.display.flip()

    # --- FPS Limit ---
    pygame.time.Clock().tick(60)

# Close the Pygame window
pygame.quit()

# Convert the instruction lists to a JSON object
json_data = {
    "instructions": [
        {"tagger": tagger_instructions},
        {"chased": chased_instructions}
    ]
}

# Write the JSON data to a file
with open("instructions.json", "w") as f:
    json.dump(json_data, f)
