import os
import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (255, 255, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Create the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Krazy Colors")

# Colors
colors = {
    "Red": (255, 0, 0),
    "Green": (0, 255, 0),
    "Blue": (0, 0, 255),
    "Yellow": (255, 255, 0),
}

color_keys = list(colors.keys())
current_color_name, current_color = random.choice(list(colors.items()))

font = pygame.font.Font(None, 36)
result_font = pygame.font.Font(None, 48)
current_color_font = pygame.font.Font(None, 72)

points = 0

def draw_rounded_rect(surface, rect, color, corner_radius):
    pygame.draw.rect(surface, color, rect.inflate(-2 * corner_radius, 0))
    pygame.draw.rect(surface, color, rect.inflate(0, -2 * corner_radius))

    pygame.draw.circle(surface, color, (rect.topleft[0] + corner_radius, rect.topleft[1] + corner_radius), corner_radius)
    pygame.draw.circle(surface, color, (rect.topright[0] - corner_radius, rect.topright[1] + corner_radius), corner_radius)
    pygame.draw.circle(surface, color, (rect.bottomleft[0] + corner_radius, rect.bottomleft[1] - corner_radius), corner_radius)
    pygame.draw.circle(surface, color, (rect.bottomright[0] - corner_radius, rect.bottomright[1] - corner_radius), corner_radius)


def draw_color_boxes():
    box_width = 150
    box_height = 150
    box_margin = 30
    corner_radius = 25

    for i, color_name in enumerate(displayed_colors):
        color = colors[color_name]
        box_x = (WIDTH - (4 * box_width + 3 * box_margin)) // 2 + i * (box_width + box_margin)
        box_y = HEIGHT // 2 - box_height // 2
        rect = pygame.Rect(box_x, box_y, box_width, box_height)
        draw_rounded_rect(screen, rect, color, corner_radius)

def draw_message(screen, text, font, color, bg_color, pos):
    message_text = font.render(text, True, color)
    message_rect = message_text.get_rect(center=pos)
    pygame.draw.rect(screen, bg_color, message_rect.inflate(10, 10))
    screen.blit(message_text, message_rect)

def draw_score_streak(screen):
    streak_text = font.render(f"Streak: {streak}", True, BLACK)
    streak_rect = streak_text.get_rect(topleft=(10, 10))
    screen.blit(streak_text, streak_rect)

def get_clicked_box(x, y):
    box_width = 150
    box_height = 150
    box_margin = 30

    for i in range(4):
        box_x = (WIDTH - (4 * box_width + 3 * box_margin)) // 2 + i * (box_width + box_margin)
        box_y = HEIGHT // 2 - box_height // 2
        rect = pygame.Rect(box_x, box_y, box_width, box_height)

        if rect.collidepoint(x, y):
            return i
    return None

def get_new_colors():
    new_colors = random.sample(color_keys, 4)
    if current_color_name not in new_colors:
        new_colors[random.randint(0,3)] = current_color_name
    return new_colors

def update_result_message(message, duration):
    global result_message, result_message_timer
    result_message = message
    result_message_timer = duration

def update_score_change_indicator(message, duration):
    global score_change_message, score_change_message_timer
    score_change_message = message
    score_change_message_timer = duration

displayed_colors = get_new_colors()
result_message = ""
result_message_timer = 0
score_change_message = ""
score_change_message_timer = 0
streak = 0

running = True
while running:
    screen.fill(BACKGROUND_COLOR)

    draw_color_boxes()

    current_color_text = current_color_font.render(f"Press the {current_color_name} button", True, BLACK)
    current_color_rect = current_color_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
    screen.blit(current_color_text, current_color_rect)

    points_text = font.render(f"Points: {points}", True, BLACK)
    points_rect = points_text.get_rect(topleft=(WIDTH - points_text.get_width() - 10, 10))
    screen.blit(points_text, points_rect)

    if result_message_timer > 0:
        draw_message(screen, result_message, result_font, WHITE, BLACK, (WIDTH // 2, HEIGHT // 2 + 150))
        result_message_timer -= 1

    if score_change_message_timer > 0:
        score_change_text = font.render(score_change_message, True, BLACK)
        screen.blit(score_change_text, (WIDTH // 2 + points_text.get_width() // 2 + 10, 10 + points_text.get_height()))
        score_change_message_timer -= 1

    draw_score_streak(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and result_message_timer <= 0:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            box_index = get_clicked_box(mouse_x, mouse_y)
            if box_index is not None:
                if displayed_colors[box_index] == current_color_name:
                    update_result_message("Correct!", 200)
                    points += 100
                    streak += 1
                    update_score_change_indicator("+100", 200)
                    current_color_name, current_color = random.choice(list(colors.items()))
                    displayed_colors = get_new_colors()
                elif box_index is not None:
                    update_result_message("Incorrect. Try again!", 200)
                    points -= 50
                    if points < 0:
                        points = 0
                    streak = 0
                    update_score_change_indicator("-50", 200)

    pygame.display.update()

# Quit Pygame
pygame.quit()
