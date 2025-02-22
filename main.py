import pygame
import sys
import math
import random

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Realistic Gravity Simulation")

# Fonts
font = pygame.font.SysFont("Arial", 20)

# Planet Environments
PLANETS = {
    "Earth": {"g": 9.8, "air_density": 1.225, "sky": (135, 206, 250), "ground": (0, 128, 0)},
    "Moon": {"g": 1.62, "air_density": 0, "sky": (25, 25, 112), "ground": (105, 105, 105)},
    "Mars": {"g": 3.71, "air_density": 0.02, "sky": (250, 128, 114), "ground": (139, 69, 19)},
    "Jupiter": {"g": 24.79, "air_density": 0.16, "sky": (255, 228, 196), "ground": (210, 105, 30)},
    "Sun": {"g": 274, "air_density": 0, "sky": (255, 140, 0), "ground": (255, 223, 0)}
}

# Physics Constants
RESTITUTION = 0.7
GROUND_FRICTION = 0.85
BALL_MASS = 0.43
BALL_RADIUS = 0.11
BALL_AREA = math.pi * BALL_RADIUS ** 2
BALL_DRAG_COEFFICIENT = 0.47

# Load the football image
football_img = pygame.image.load('football.png').convert_alpha()
football_img = pygame.transform.scale(football_img, (40, 40))
football_rect = football_img.get_rect()

# Store craters when Moon is selected
moon_craters = []


def generate_craters():
    """Generate craters only once when switching to the Moon."""
    global moon_craters
    moon_craters = [(random.randint(50, WIDTH - 50), HEIGHT - 50 + random.randint(5, 20), random.randint(10, 20)) for _
                    in range(6)]


def draw_sun():
    """Draw the Sun with sun rays."""
    pygame.draw.circle(screen, (255, 223, 0), (80, 80), 50)
    for i in range(12):
        angle = math.radians(i * 30)
        x1 = 80 + math.cos(angle) * 60
        y1 = 80 + math.sin(angle) * 60
        x2 = 80 + math.cos(angle) * 70
        y2 = 80 + math.sin(angle) * 70
        pygame.draw.line(screen, (255, 200, 0), (x1, y1), (x2, y2), 3)


def draw_clouds():
    """Draw fluffy clouds for Earth."""
    cloud_positions = [(120, 130), (250, 150), (500, 130)]
    for x, y in cloud_positions:
        pygame.draw.circle(screen, (240, 240, 240), (x, y), 30)
        pygame.draw.circle(screen, (240, 240, 240), (x + 30, y + 10), 40)
        pygame.draw.circle(screen, (240, 240, 240), (x - 30, y + 10), 40)
        pygame.draw.circle(screen, (240, 240, 240), (x + 15, y - 20), 30)


def draw_craters():
    """Draw pre-generated craters for the Moon surface."""
    for x, y, size in moon_craters:
        pygame.draw.circle(screen, (80, 80, 80), (x, y), size)


def draw_environment(planet):
    """Draw background and ground with planetary effects."""
    screen.fill(PLANETS[planet]["sky"])
    pygame.draw.rect(screen, PLANETS[planet]["ground"], (0, HEIGHT - 50, WIDTH, 50))

    if planet in ["Earth", "Mars", "Jupiter"]:
        draw_sun()

    if planet == "Earth":
        draw_clouds()

    if planet == "Moon":
        draw_craters()


def draw_football(x, y):
    """Draw football at given position."""
    football_rect.center = (x, y)
    screen.blit(football_img, football_rect)


def main():
    running = True
    selected_planet = "Earth"
    ball_x, ball_y = WIDTH // 2, 50
    ball_velocity = 0
    initial_height = 2
    gravity = PLANETS[selected_planet]["g"]
    pixels_per_meter = 50
    is_falling = False
    delta_t = 1 / 60

    while running:
        draw_environment(selected_planet)

        text_color = (255, 255, 255) if selected_planet == "Moon" else (0, 0, 0)
        instructions = [
            f"UP/DOWN: Change height (h = {initial_height:.1f}m)",
            "LEFT/RIGHT: Change planet | SPACE: Drop ball"
        ]
        for i, line in enumerate(instructions):
            screen.blit(font.render(line, True, text_color), (10, 10 + i * 20))

        screen.blit(font.render(f"Planet: {selected_planet} (g = {gravity} m/s²)", True, text_color), (10, 60))

        if is_falling:
            ball_velocity += gravity * delta_t
            ball_y += ball_velocity * pixels_per_meter * delta_t

            if ball_y >= HEIGHT - 50 - football_rect.height // 2:
                ball_y = HEIGHT - 50 - football_rect.height // 2
                ball_velocity = -ball_velocity * RESTITUTION
                if abs(ball_velocity) < 0.5:
                    is_falling = False
                    ball_velocity = 0
                    initial_height = 0
                else:
                    ball_velocity *= GROUND_FRICTION

        if not is_falling:
            ball_y = HEIGHT - int(initial_height * pixels_per_meter) - 50 - football_rect.height // 2

        draw_football(ball_x, int(ball_y))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    initial_height = min(initial_height + 0.1, 10)
                elif event.key == pygame.K_DOWN:
                    initial_height = max(initial_height - 0.1, 0.1)
                elif event.key == pygame.K_RIGHT:
                    planet_keys = list(PLANETS.keys())
                    new_planet = planet_keys[(planet_keys.index(selected_planet) + 1) % len(PLANETS)]
                    if new_planet == "Moon":
                        generate_craters()  # Generate craters when switching to the Moon
                    selected_planet = new_planet
                    gravity = PLANETS[selected_planet]["g"]
                elif event.key == pygame.K_LEFT:
                    planet_keys = list(PLANETS.keys())
                    new_planet = planet_keys[(planet_keys.index(selected_planet) - 1) % len(PLANETS)]
                    if new_planet == "Moon":
                        generate_craters()
                    selected_planet = new_planet
                    gravity = PLANETS[selected_planet]["g"]
                elif event.key == pygame.K_SPACE:
                    is_falling = True
                    ball_velocity = 0

        pygame.display.flip()
        pygame.time.Clock().tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()