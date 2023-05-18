import pygame
import random

# Additional imports
import pygame.gfxdraw

# Initialize Pygame
pygame.init()

# Constants
WIDTH = 800
HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Colors
colors = {
    "Red": (255, 0, 0),
    "Green": (0, 255, 0),
    "Blue": (0, 0, 255),
    "Yellow": (255, 255, 0),
    "Purple": (128, 0, 128),
    "Cyan": (0, 255, 255),
    "Orange": (255, 165, 0),
    "Pink": (255, 105, 180),
}

color_keys = list(colors.keys())

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Color Learning Game")

# Fonts
font = pygame.font.Font(None, 36)
result_font = pygame.font.Font(None, 48)

# Game variables
points = 0
current_color_name, current_color = random.choice(list(colors.items()))

# Draw border around text
def draw_border(surface, rect, color, border_width):
    pygame.gfxdraw.rectangle(surface, rect, color)
    inner_rect = rect.inflate(-border_width, -border_width)
    pygame.gfxdraw.rectangle(surface, inner_rect, color)

# Draw message with a background
def draw_message(surface, message, font, color, bg_color, pos, padding=10):
    message_text = font.render(message, True, color)
    message_rect = message_text.get_rect()
    message_rect.topleft = pos
    bg_rect = message_rect.inflate(padding * 2, padding * 2)
    bg_rect.center = message_rect.center
    pygame.draw.rect(surface, bg_color, bg_rect)
    surface.blit(message_text, message_rect)

# Draw color boxes
def draw_color_boxes():
    box_width = 150
    box_height = 150
    margin = 30
    total_width = 2 * (box_width + margin)
    total_height = 2 * (box_height + margin)
    offset_x = (WIDTH - total_width) // 2
    offset_y = (HEIGHT - total_height) // 2 + 100
    for i, color_key in enumerate(displayed_colors):
        color = colors[color_key]
        x = offset_x + (i % 2) * (box_width + margin)
        y = offset_y + (i // 2) * (box_height + margin)
        pygame.draw.rect(screen, color, (x, y, box_width, box_height))

def get_clicked_box(mouse_x, mouse_y):
    box_width = 150
    box_height = 150
    margin = 30
    total_width = 2 * (box_width + margin)
    total_height = 2 * (box_height + margin)
    offset_x = (WIDTH - total_width) // 2
    offset_y = (HEIGHT - total_height) // 2 + 100
    if mouse_y >= offset_y and mouse_y <= offset_y + total_height:
        col = (mouse_x - offset_x) // (box_width + margin)
        row = (mouse_y - offset_y) // (box_height + margin)
        if 0 <= col < 2 and 0 <= row < 2:
            return row * 2 + col
    return None

def get_new_colors():
    new_colors = random.sample(color_keys, 4)
    if current_color_name not in new_colors:
        new_colors[random.randint(0, 3)] = current_color_name
    return new_colors

displayed_colors = get_new_colors()

result_message = ""
result_message_timer = 0

def update_result_message(message, duration):
    global result_message, result_message_timer
    result_message = message
    result_message_timer = duration

score_change_indicator = ""
score_change_timer = 0

def update_score_change_indicator(indicator, duration):
    global score_change_indicator, score_change_timer
    score_change_indicator = indicator
    score_change_timer = duration

# Main game loop
clock = pygame.time.Clock()
running = True
while running:
    dt = clock.tick(30)
    screen.fill(WHITE)

    # Display the color name
    color_text = font.render(current_color_name, True, BLACK)
    screen.blit(color_text, (WIDTH // 2 - color_text.get_width() // 2, HEIGHT // 4 - color_text.get_height() // 2))

    # Draw color boxes
    draw_color_boxes()

    # Draw points
    points_text = font.render(f"Points: {points}", True, BLACK)
    points_rect = points_text.get_rect(topright=(WIDTH - 10, 10))
    draw_border(screen, points_rect.inflate(10, 10), BLACK, 2)
    screen.blit(points_text, points_rect)

    # Display result message
    if result_message_timer > 0:
        result_message_timer -= dt
        if result_message == "Correct!":
            draw_message(screen, result_message, result_font, WHITE, (0, 128, 0), (WIDTH // 2 - 60, HEIGHT // 4 + 80))
        else:
            draw_message(screen, result_message, result_font, WHITE, (255, 0, 0), (WIDTH // 2 - 110, HEIGHT // 4 + 80))

    # Display score change indicator
    if score_change_timer > 0:
        score_change_timer -= dt
        score_change_text = result_font.render(score_change_indicator, True, BLACK)
        screen.blit(score_change_text, (WIDTH - points_text.get_width() - 10, 10 + points_text.get_height()))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            box_index = get_clicked_box(mouse_x, mouse_y)
            if box_index is not None and displayed_colors[box_index] == current_color_name:
                update_result_message("Correct!", 1000)
                points += 100
                update_score_change_indicator("+100", 1000)
                current_color_name, current_color = random.choice(list(colors.items()))
                displayed_colors = get_new_colors()
            elif box_index is not None:
                update_result_message("Incorrect. Try again!", 1000)
                points -= 50
                if points < 0:
                    points = 0
                update_score_change_indicator("-50", 1000)

    pygame.display.update()

# Quit Pygame
pygame.quit()
