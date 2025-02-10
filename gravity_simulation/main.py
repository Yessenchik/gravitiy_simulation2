import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gravity Simulation with Football Image")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SUN_COLOR = (255, 223, 0)
CLOUD_COLOR = (240, 240, 240)
EARTH_COLOR = (0, 128, 0)
MOON_COLOR = (192, 192, 192)
MARS_COLOR = (188, 39, 50)
JUPITER_COLOR = (210, 105, 30)
SUN_GROUND_COLOR = (255, 200, 0)

# Fonts
font = pygame.font.SysFont("Arial", 20)

# Gravity on planets (m/s^2)
PLANETS = {
    "Earth": 9.8,
    "Moon": 1.62,
    "Mars": 3.71,
    "Jupiter": 24.79,
    "Sun": 274,
}

# Coefficient of restitution
RESTITUTION = 0.7

# Load the football image
football_img = pygame.image.load('football.png').convert_alpha()
football_img = pygame.transform.scale(football_img, (40, 40))  # Scale the image
football_rect = football_img.get_rect()

# Function to draw clouds for Earth
def draw_clouds():
    # Updated cloud positions to be slightly lower than the Sun
    cloud_positions = [(120, 130), (250, 150), (500, 130)]
    for pos in cloud_positions:
        x, y = pos
        pygame.draw.circle(screen, CLOUD_COLOR, (x, y), 30)
        pygame.draw.circle(screen, CLOUD_COLOR, (x + 30, y + 10), 40)
        pygame.draw.circle(screen, CLOUD_COLOR, (x - 30, y + 10), 40)
        pygame.draw.circle(screen, CLOUD_COLOR, (x + 15, y - 20), 30)

# Function to draw the Sun in the top-left corner
def draw_sun():
    pygame.draw.circle(screen, SUN_COLOR, (80, 80), 50)

# Function to draw the environment
def draw_environment(planet):
    if planet == "Earth":
        screen.fill((135, 206, 250))  # Sky blue background
        pygame.draw.rect(screen, EARTH_COLOR, (0, HEIGHT - 50, WIDTH, 50))  # Ground
        draw_sun()
        draw_clouds()
    elif planet == "Moon":
        screen.fill((25, 25, 112))  # Dark blue background (space)
        pygame.draw.rect(screen, MOON_COLOR, (0, HEIGHT - 50, WIDTH, 50))  # Ground
        draw_sun()
    elif planet == "Mars":
        screen.fill((250, 128, 114))  # Light red background
        pygame.draw.rect(screen, MARS_COLOR, (0, HEIGHT - 50, WIDTH, 50))  # Ground
        draw_sun()
    elif planet == "Jupiter":
        screen.fill((255, 228, 196))  # Beige background
        pygame.draw.rect(screen, JUPITER_COLOR, (0, HEIGHT - 50, WIDTH, 50))  # Ground
        draw_sun()
    elif planet == "Sun":
        screen.fill((255, 140, 0))  # Bright orange background
        pygame.draw.rect(screen, SUN_GROUND_COLOR, (0, HEIGHT - 50, WIDTH, 50))  # Sun ground

# Function to draw the football
def draw_football(x, y):
    football_rect.center = (x, y)
    screen.blit(football_img, football_rect)

def main():
    running = True
    selected_planet = "Earth"
    ball_x, ball_y = WIDTH // 2, 50  # Starting position of the ball
    ball_velocity = 0  # Initial velocity
    initial_height = 2  # Default height in meters
    gravity = PLANETS[selected_planet]  # Gravitational acceleration
    pixels_per_meter = 50  # Scale for height (1 meter = 50 pixels)
    is_falling = False

    while running:
        draw_environment(selected_planet)  # Draw the current planet's background

        # Adjust text for clarity
        text_color = WHITE if selected_planet == "Moon" else BLACK
        instructions = [
            f"Press UP/DOWN to change height (h = {initial_height:.1f}m).",
            "Press LEFT/RIGHT to select planet. SPACE to drop ball."
        ]
        for i, line in enumerate(instructions):
            text = font.render(line, True, text_color)
            screen.blit(text, (10, 10 + i * 20))

        # Display selected planet and gravity
        planet_info = font.render(
            f"Selected Planet: {selected_planet} (g = {gravity} m/s^2)", True, text_color
        )
        screen.blit(planet_info, (10, 60))

        # Simulate physics
        if is_falling:
            ball_velocity += gravity * (1 / 60)  # Gravity increases velocity
            ball_y += ball_velocity * pixels_per_meter / 60  # Update position

            # Check for ground collision
            if ball_y >= HEIGHT - football_rect.height // 2 - 50:  # 50 = ground height
                ball_y = HEIGHT - football_rect.height // 2 - 50  # Place ball on the ground
                ball_velocity = -ball_velocity * RESTITUTION  # Reverse velocity with energy loss

                # Stop bouncing if the velocity is too small
                if abs(ball_velocity) < 1:
                    is_falling = False
                    ball_velocity = 0
                    initial_height = 0

        # Update the ball's height to correspond with adjustments
        if not is_falling:
            ball_y = HEIGHT - int(initial_height * pixels_per_meter) - 50 - football_rect.height // 2

        # Draw the football
        draw_football(ball_x, int(ball_y))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    initial_height = min(initial_height + 0.1, 10)  # Max height 10m
                elif event.key == pygame.K_DOWN:
                    initial_height = max(initial_height - 0.1, 0.1)  # Min height 0.1m
                elif event.key == pygame.K_RIGHT:
                    planet_keys = list(PLANETS.keys())
                    selected_index = planet_keys.index(selected_planet)
                    selected_planet = planet_keys[(selected_index + 1) % len(PLANETS)]
                    gravity = PLANETS[selected_planet]
                elif event.key == pygame.K_LEFT:
                    planet_keys = list(PLANETS.keys())
                    selected_index = planet_keys.index(selected_planet)
                    selected_planet = planet_keys[(selected_index - 1) % len(PLANETS)]
                    gravity = PLANETS[selected_planet]
                elif event.key == pygame.K_SPACE:
                    is_falling = True
                    ball_velocity = 0  # Reset velocity

        # Display height and velocity
        if is_falling:
            height_above_ground = (HEIGHT - football_rect.height // 2 - 50 - ball_y) / pixels_per_meter
            height_text = font.render(
                f"Height above ground: {max(height_above_ground, 0):.2f} m", True, text_color
            )
            screen.blit(height_text, (10, 90))
            velocity_text = font.render(
                f"Velocity: {ball_velocity:.2f} m/s", True, text_color
            )
            screen.blit(velocity_text, (10, 110))

        pygame.display.flip()
        pygame.time.Clock().tick(60)  # 60 FPS

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()