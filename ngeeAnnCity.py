import pygame
import random
import sys
import csv
import os

# Initialize Pygame
pygame.init()
pygame.mixer.init()  # Initialize mixer for sound

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 850
GRID_SIZE_ARCADE = 20  # Arcade Mode Grid Size
CELL_SIZE = 25
TITLE_FONT = pygame.font.SysFont("Arial", 40)
MENU_TITLE_FONT = pygame.font.SysFont("Arial", 120)
BUTTON_FONT = pygame.font.SysFont("Arial", 30)
GAME_FONT = pygame.font.SysFont("Arial", 20)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)
BLUE = (173, 216, 230)
GREEN = (144, 238, 144)
BUILDINGS = ['Residential', 'Industry', 'Commercial', 'Park', 'Road']
BUILDING_SYMBOLS = {'Residential': 'R', 'Industry': 'I', 'Commercial': 'C', 'Park': 'O', 'Road': '*'}
BACKGROUND_COLOR = (25, 25, 25)
GRID_COLOR = BLACK
CELL_COLOR = WHITE
MARGIN_LEFT = 50
MARGIN_TOP = 200
MARGIN_BOTTOM = 50
MARGIN_RIGHT = 250
TEXT_MARGIN_RIGHT = 20
TEXT_PADDING_LEFT = 20
TEXT_PADDING_TOP = 10

# Load sound effects
pygame.mixer.music.load('./MenuSoundtrack.mp3')
pygame.mixer.music.set_volume(0.6)  # Set volume to 60%
pygame.mixer.music.play(-1)  # -1 means the music will loop indefinitely
mouse_click_sound = pygame.mixer.Sound('./MouseClick.mp3')


# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Ngee Ann City")

# Function to draw buttons and handle hover effect
def draw_button_with_hover(button, text, font, color, hover_color, surface):
    mouse_pos = pygame.mouse.get_pos()
    if button.collidepoint(mouse_pos):
        pygame.draw.rect(surface, hover_color, button, border_radius=8)
    else:
        pygame.draw.rect(surface, color, button, border_radius=8)
    pygame.draw.rect(surface, BLACK, button, 1, border_radius=8)
    draw_centered_text(text, font, BLACK, surface, button)

# Functions to load Ngee Ann Poly image
def load_background_image(path):
    return pygame.image.load(path)

def draw_background_image(image, surface):
    surface.blit(image, (0, 0))

# Functions to draw text
def draw_text(text, font, color, surface, x, y):
    # Draw centered text
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

def draw_left_aligned_text(text, font, color, surface, x, y):
    # Draw left-aligned text
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(topleft=(x, y))
    surface.blit(text_obj, text_rect)

def draw_centered_text(text, font, color, surface, rect):
    # Draw centered text within a given rectangle
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=rect.center)
    surface.blit(text_obj, text_rect)

# Prompt for player name
def prompt_player_name():
    # Prompt the player to enter their name
    pygame.display.update()
    screen.fill(BACKGROUND_COLOR)
    draw_text('Enter your name:', BUTTON_FONT, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40)
    pygame.display.update()
    name = ""
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return name
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    name += event.unicode
        screen.fill(BACKGROUND_COLOR)
        draw_text('Enter your name:', BUTTON_FONT, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40)
        draw_text(name, BUTTON_FONT, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10)
        pygame.display.update()

# Save leaderboard to CSV
def save_leaderboard(name, score):
    # Save the player's name and score to the leaderboard CSV file
    # Prevent CSV injection
    name = name.replace("=", "").replace("+", "").replace("-", "").replace("@", "")
    with open('NgeeAnnCity_Arcade_Leaderboard.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([name, score])

# Clear saved game for Arcade mode
def clear_saved_game_arcade():
    # Delete the saved game file for Arcade mode if it exists
    if os.path.exists('NgeeAnnCity_Arcade_SavedGame.csv'):
        os.remove('NgeeAnnCity_Arcade_SavedGame.csv')

# Clear saved game for Arcade mode
def clear_saved_game_free_play():
    # Delete the saved game file for Arcade mode if it exists
    if os.path.exists('NgeeAnnCity_FreePlay_SavedGame.csv'):
        os.remove('NgeeAnnCity_FreePlay_SavedGame.csv')

# Display leaderboard
def display_leaderboard():
    # Display the leaderboard on the screen
    displaying = True
    while displaying:
        screen.fill(BACKGROUND_COLOR)
        draw_text('Leaderboard - Arcade Mode', TITLE_FONT, WHITE, screen, SCREEN_WIDTH // 2, 50)
        
        if os.path.exists('NgeeAnnCity_Arcade_Leaderboard.csv'):
            # Load and display the top 10 scores from the leaderboard CSV file
            leaderboard = []
            with open('NgeeAnnCity_Arcade_Leaderboard.csv', 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    leaderboard.append((row[0], int(row[1])))
            leaderboard.sort(key=lambda x: x[1], reverse=True)  # Sort by score in descending order
            y_offset = 100
            for i, (name, score) in enumerate(leaderboard[:10]):  # Display top 10
                draw_text(f'{i + 1}. {name}: {score}', BUTTON_FONT, WHITE, screen, SCREEN_WIDTH // 2, y_offset)
                y_offset += 40
        else:
            draw_text('No leaderboard data available.', BUTTON_FONT, WHITE, screen, SCREEN_WIDTH // 2, 100)
        
        draw_text('Press B to go back to main menu', BUTTON_FONT, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 40)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    displaying = False

        pygame.display.update()

    screen.fill(BACKGROUND_COLOR)  # Clear the screen to remove lingering text
    pygame.display.update()
    return
        
# Arcade Mode Functions
def calculate_points_arcade(grid, restricted_residential):
    points = 0
    for row in range(GRID_SIZE_ARCADE):
        for col in range(GRID_SIZE_ARCADE):
            cell = grid[row][col]
            if cell == 'R':
                points += calculate_residential_points_arcade(grid, row, col, restricted_residential)
            elif cell == 'I':
                points += calculate_industry_points_arcade(grid, row, col)
            elif cell == 'C':
                points += calculate_commercial_points_arcade(grid, row, col)
            elif cell == 'O':
                points += calculate_park_points_arcade(grid, row, col)
            elif cell == '*':
                points += calculate_road_points_arcade(grid, row, col)
    return points

def calculate_residential_points_arcade(grid, row, col, restricted_residential):
    if restricted_residential.get((row, col), False):
        return 0  # If this Residential building is restricted, it can't gain or lose points

    points = 0
    adjacents = [(row-1, col), (row+1, col), (row, col-1), (row, col+1)]
    adjacent_to_industry = False
    for r, c in adjacents:
        if 0 <= r < GRID_SIZE_ARCADE and 0 <= c < GRID_SIZE_ARCADE:
            if grid[r][c] == 'I':
                adjacent_to_industry = True
                restricted_residential[(row, col)] = True  # Mark this Residential building as restricted
                break

    if adjacent_to_industry:
        return 1

    for r, c in adjacents:
        if 0 <= r < GRID_SIZE_ARCADE and 0 <= c < GRID_SIZE_ARCADE:
            if grid[r][c] == 'R':
                if any(0 <= rr < GRID_SIZE_ARCADE and 0 <= rc < GRID_SIZE_ARCADE and grid[rr][rc] == 'I' for rr, rc in [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]):
                    points += 1
                else:
                    points += 2
            elif grid[r][c] == 'C':
                points += 1
            elif grid[r][c] == 'O':
                points += 2

    return points

def calculate_industry_points_arcade(grid, row, col):
    points = 1
    adjacents = [(row-1, col), (row+1, col), (row, col-1), (row, col+1)]
    for r, c in adjacents:
        if 0 <= r < GRID_SIZE_ARCADE and 0 <= c < GRID_SIZE_ARCADE:
            if grid[r][c] == 'R':
                residential_adjacents = [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]
                skip_residential = False
                for rr, rc in residential_adjacents:
                    if (rr != row or rc != col) and 0 <= rr < GRID_SIZE_ARCADE and 0 <= rc < GRID_SIZE_ARCADE and grid[rr][rc] == 'I':
                        skip_residential = True
                        break
                if not skip_residential:
                    points += 1
    return points

def calculate_commercial_points_arcade(grid, row, col):
    points = 0
    adjacents = [(row-1, col), (row+1, col), (row, col-1), (row, col+1)]
    for r, c in adjacents:
        if 0 <= r < GRID_SIZE_ARCADE and 0 <= c < GRID_SIZE_ARCADE:
            if grid[r][c] == 'R':
                residential_adjacents = [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]
                skip_residential = False
                for rr, rc in residential_adjacents:
                    if 0 <= rr < GRID_SIZE_ARCADE and 0 <= rc < GRID_SIZE_ARCADE and grid[rr][rc] == 'I':
                        skip_residential = True
                        break
                if not skip_residential:
                    points += 1  # No points for adjacent Residential
            elif grid[r][c] == 'C':
                points += 2
    return points

def calculate_park_points_arcade(grid, row, col):
    points = 0
    adjacents = [(row-1, col), (row+1, col), (row, col-1), (row, col+1)]
    for r, c in adjacents:
        if 0 <= r < GRID_SIZE_ARCADE and 0 <= c < GRID_SIZE_ARCADE:
            if grid[r][c] == 'R':
                residential_adjacents = [(r-1, c), (r+1, c), (r, col-1), (r, col+1)]
                skip_residential = False
                for rr, rc in residential_adjacents:
                    if 0 <= rr < GRID_SIZE_ARCADE and 0 <= rc < GRID_SIZE_ARCADE and grid[rr][rc] == 'I':
                        skip_residential = True
                        break
                if not skip_residential:
                    points += 2
            elif grid[r][c] == 'O':
                points += 2
    return points

def calculate_road_points_arcade(grid, row, col):
    # Calculate points for a road
    points = 0
    adjacents = [(row-1, col), (row+1, col), (row, col-1), (row, col+1)]
    for r, c in adjacents:
        if 0 <= r < GRID_SIZE_ARCADE and 0 <= c < GRID_SIZE_ARCADE:
            if grid[r][c] == '*':
                points += 2  # Gain 2 points for each adjacent road
    return points

def generate_coins_for_commercial_arcade(grid, row, col):
    # Generate coins for a commercial building
    coins = 0
    adjacents = [(row-1, col), (row+1, col), (row, col-1), (row, col+1)]
    for r, c in adjacents:
        if 0 <= r < GRID_SIZE_ARCADE and 0 <= c < GRID_SIZE_ARCADE:
            if grid[r][c] == 'R':
                coins += 1
    return coins

def generate_coins_for_industry_arcade(grid, row, col):
    # Generate coins for an industry building
    coins = 0
    adjacents = [(row-1, col), (row+1, col), (row, col-1), (row, col+1)]
    for r, c in adjacents:
        if 0 <= r < GRID_SIZE_ARCADE and 0 <= c < GRID_SIZE_ARCADE:
            if grid[r][c] == 'R':
                coins += 1
    return coins

def is_adjacent_to_existing_building_arcade(grid, row, col):
    # Check if a cell is adjacent to an existing building
    adjacents = [(row-1, col), (row+1, col), (row, col-1), (row, col+1)]
    for r, c in adjacents:
        if 0 <= r < GRID_SIZE_ARCADE and 0 <= c < GRID_SIZE_ARCADE and (grid[r][c] is not None and grid[r][c] != ''):
            return True
    return False

def save_game_arcade(grid, coins, turn, score, restricted_residential):
    # Save the current game state to a CSV file for Arcade mode
    with open('NgeeAnnCity_Arcade_SavedGame.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Grid', 'Coins', 'Turn', 'Score', 'RestrictedResidential'])
        for row in grid:
            writer.writerow(row)
        writer.writerow([coins, turn, score])
        for key, value in restricted_residential.items():
            writer.writerow([key[0], key[1], value])

def load_game_arcade():
    # Load the saved game state from a CSV file for Arcade mode
    if os.path.exists('NgeeAnnCity_Arcade_SavedGame.csv'):
        with open('NgeeAnnCity_Arcade_SavedGame.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            grid = []
            for i in range(GRID_SIZE_ARCADE):
                row = next(reader, None)
                if row is None:
                    return None, None, None, None, None
                grid.append([None if cell == 'None' else cell for cell in row])
            coins, turn, score = map(int, next(reader))
            restricted_residential = {}
            for row in reader:
                restricted_residential[(int(row[0]), int(row[1]))] = row[2] == 'True'
            return grid, coins, turn, score, restricted_residential
    return None, None, None, None, None

# Free Play Mode Functions
def calculate_points_free_play(grid, restricted_residential):
    points = 0
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == 'R':
                points += calculate_residential_points_free_play(grid, row, col, restricted_residential)
            elif grid[row][col] == 'I':
                points += calculate_industry_points_free_play(grid, row, col)
            elif grid[row][col] == 'C':
                points += calculate_commercial_points_free_play(grid, row, col)
            elif grid[row][col] == 'O':
                points += calculate_park_points_free_play(grid, row, col)
            elif grid[row][col] == '*':
                points += calculate_road_points_free_play(grid, row, col)
    return points

def calculate_residential_points_free_play(grid, row, col, restricted_residential):
    if restricted_residential.get((row, col), False):
        return 0  # If this Residential building is restricted, it can't gain or lose points

    points = 0
    adjacents = [(row-1, col), (row+1, col), (row, col-1), (row, col+1)]
    adjacent_to_industry = False
    for r, c in adjacents:
        if 0 <= r < len(grid) and 0 <= c < len(grid[0]):
            if grid[r][c] == 'I':
                adjacent_to_industry = True
                restricted_residential[(row, col)] = True  # Mark this Residential building as restricted
                break

    if adjacent_to_industry:
        return 1

    for r, c in adjacents:
        if 0 <= r < len(grid) and 0 <= c < len(grid[0]):
            if grid[r][c] == 'R':
                if any(0 <= rr < len(grid) and 0 <= rc < len(grid[0]) and grid[rr][rc] == 'I' for rr, rc in [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]):
                    points += 1
                else:
                    points += 2
            elif grid[r][c] == 'C':
                points += 1
            elif grid[r][c] == 'O':
                points += 2

    return points

def calculate_industry_points_free_play(grid, row, col):
    points = 1
    adjacents = [(row-1, col), (row+1, col), (row, col-1), (row, col+1)]
    for r, c in adjacents:
        if 0 <= r < len(grid) and 0 <= c < len(grid[0]):
            if grid[r][c] == 'R':
                residential_adjacents = [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]
                skip_residential = False
                for rr, rc in residential_adjacents:
                    if (rr != row or rc != col) and 0 <= rr < len(grid) and 0 <= rc < len(grid[0]) and grid[rr][rc] == 'I':
                        skip_residential = True
                        break
                if not skip_residential:
                    points += 1
    return points

def calculate_commercial_points_free_play(grid, row, col):
    points = 0
    adjacents = [(row-1, col), (row+1, col), (row, col-1), (row, col+1)]
    for r, c in adjacents:
        if 0 <= r < len(grid) and 0 <= c < len(grid[0]):
            if grid[r][c] == 'R':
                residential_adjacents = [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]
                skip_residential = False
                for rr, rc in residential_adjacents:
                    if 0 <= rr < len(grid) and 0 <= rc < len(grid[0]) and grid[rr][rc] == 'I':
                        skip_residential = True
                        break
                if not skip_residential:
                    points += 1  # No points for adjacent Residential
            elif grid[r][c] == 'C':
                points += 2
    return points

def calculate_park_points_free_play(grid, row, col):
    points = 0
    adjacents = [(row-1, col), (row+1, col), (row, col-1), (row, col+1)]
    for r, c in adjacents:
        if 0 <= r < len(grid) and 0 <= c < len(grid[0]):
            if grid[r][c] == 'R':
                residential_adjacents = [(r-1, c), (r+1, c), (r, col-1), (r, col+1)]
                skip_residential = False
                for rr, rc in residential_adjacents:
                    if 0 <= rr < len(grid) and 0 <= rc < len(grid[0]) and grid[rr][rc] == 'I':
                        skip_residential = True
                        break
                if not skip_residential:
                    points += 2
            elif grid[r][c] == 'O':
                points += 2
    return points

def calculate_road_points_free_play(grid, row, col):
    # Calculate points for a road
    points = 0
    adjacents = [(row-1, col), (row+1, col), (row, col-1), (row, col+1)]
    for r, c in adjacents:
        if 0 <= r < len(grid) and 0 <= c < len(grid[0]):
            if grid[r][c] == '*':
                points += 2  # Gain 2 points for each adjacent road
    return points

def generate_coins_for_commercial_free_play(grid, row, col):
    # Generate coins for a commercial building
    coins = 0
    adjacents = [(row-1, col), (row+1, col), (row, col-1), (row, col+1)]
    for r, c in adjacents:
        if 0 <= r < len(grid) and 0 <= c < len(grid[0]):
            if grid[r][c] == 'R':
                coins += 1
    return coins

def generate_coins_for_industry_free_play(grid, row, col):
    # Generate coins for an industry building
    coins = 0
    adjacents = [(row-1, col), (row+1, col), (row, col-1), (row, col+1)]
    for r, c in adjacents:
        if 0 <= r < len(grid) and 0 <= c < len(grid[0]):
            if grid[r][c] == 'R':
                coins += 1
    return coins

def is_adjacent_to_existing_building_free_play(grid, row, col):
    # Check if a cell is adjacent to an existing building
    adjacents = [(row-1, col), (row+1, col), (row, col-1), (row, col+1)]
    for r, c in adjacents:
        if 0 <= r < len(grid) and 0 <= c < len(grid[0]) and (grid[r][c] is not None and grid[r][c] != ''):
            return True
    return False

def expand_grid(grid, new_size):
    # Expand the grid to a new size, centered on the existing grid
    new_grid = [[None for _ in range(new_size)] for _ in range(new_size)]
    old_size = len(grid)
    offset = (new_size - old_size) // 2
    for row in range(old_size):
        for col in range(old_size):
            new_grid[row][col] = grid[row][col]
    return new_grid

def save_game_free_play(grid, coins, turn, score, restricted_residential, expansion_count):
    # Save the current game state to a CSV file for Free Play mode
    with open('NgeeAnnCity_FreePlay_SavedGame.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Grid', 'Coins', 'Turn', 'Score', 'RestrictedResidential', 'ExpansionCount'])
        for row in grid:
            writer.writerow(row)
        writer.writerow([coins, turn, score, expansion_count])
        for key, value in restricted_residential.items():
            writer.writerow([key[0], key[1], value])

def load_game_free_play():
    # Load the saved game state from a CSV file for Free Play mode
    if os.path.exists('NgeeAnnCity_FreePlay_SavedGame.csv'):
        with open('NgeeAnnCity_FreePlay_SavedGame.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            grid = []
            row = next(reader, None)
            while row and len(row) > 0 and not row[0].isdigit():
                grid.append([None if cell == 'None' else cell for cell in row])
                row = next(reader, None)
            if row:
                coins, turn, score, expansion_count = map(int, row)
                restricted_residential = {}
                for row in reader:
                    restricted_residential[(int(row[0]), int(row[1]))] = row[2] == 'True'
                return grid, coins, turn, score, restricted_residential, expansion_count
    return None, None, None, None, None, 0

# Main Menu with buttons
def main_menu():
    background_image = load_background_image('./Background.png')  # Replace 'background.jpg' with your image file path

    while True:
        screen.fill(BLACK)  # Fill the screen with black color
        draw_background_image(background_image, screen)  # Draw the background image

        button_width = 400
        button_height = 70

        play_button = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, 450, button_width, button_height)
        leaderboard_button = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, 535, button_width, button_height)
        settings_button = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, 620, button_width, button_height)  # New Settings Button
        exit_button = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, 705, button_width, button_height)

        draw_button_with_hover(play_button, 'Play', BUTTON_FONT, WHITE, GREY, screen)
        draw_button_with_hover(leaderboard_button, 'Leaderboard', BUTTON_FONT, WHITE, GREY, screen)
        draw_button_with_hover(settings_button, 'Settings', BUTTON_FONT, WHITE, GREY, screen)  # Draw Settings Button
        draw_button_with_hover(exit_button, 'Exit', BUTTON_FONT, WHITE, GREY, screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_click_sound.play()
                if play_button.collidepoint(event.pos):
                    play_menu()
                elif leaderboard_button.collidepoint(event.pos):
                    display_leaderboard()
                elif settings_button.collidepoint(event.pos):  # Handle Settings Button Click
                    settings_menu()
                elif exit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
# Settings Menu with buttons
def settings_menu():
    background_image = load_background_image('./MenuBackground.png')  # Replace with your image file path

    while True:
        screen.fill(BLACK)  # Fill the screen with black color
        draw_background_image(background_image, screen)

        draw_text('Settings', MENU_TITLE_FONT, WHITE, screen, SCREEN_WIDTH // 2, 200)

        button_width = 400
        button_height = 70

        mute_button = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, 450, button_width, button_height)
        back_button = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, 535, button_width, button_height)

        draw_button_with_hover(mute_button, 'Mute/Unmute Music', BUTTON_FONT, WHITE, GREY, screen)
        draw_button_with_hover(back_button, 'Back', BUTTON_FONT, WHITE, GREY, screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_click_sound.play()
                if mute_button.collidepoint(event.pos):
                    if pygame.mixer.music.get_volume() > 0:
                        pygame.mixer.music.set_volume(0)
                    else:
                        pygame.mixer.music.set_volume(0.6)  # Set to your desired volume level
                elif back_button.collidepoint(event.pos):
                    return

        pygame.display.update()

# Play Menu with buttons
def play_menu():
    background_image = load_background_image('./MenuBackground.png')  # Replace 'background.jpg' with your image file path

    while True:
        screen.fill(BLACK)  # Fill the screen with black color
        draw_background_image(background_image, screen)

        draw_text('Play', MENU_TITLE_FONT, WHITE, screen, SCREEN_WIDTH // 2, 200)

        button_width = 400
        button_height = 70

        arcade_mode_button = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, 450, button_width, button_height)
        free_play_button = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, 535, button_width, button_height)
        back_button = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, 620, button_width, button_height)

        draw_button_with_hover(arcade_mode_button, 'Arcade Mode', BUTTON_FONT, WHITE, GREY, screen)
        draw_button_with_hover(free_play_button, 'Free Play', BUTTON_FONT, WHITE, GREY, screen)
        draw_button_with_hover(back_button, 'Back', BUTTON_FONT, WHITE, GREY, screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_click_sound.play()
                if arcade_mode_button.collidepoint(event.pos):
                    arcade_menu()
                elif free_play_button.collidepoint(event.pos):
                    free_play_menu()
                elif back_button.collidepoint(event.pos):
                    return

        pygame.display.update()

# Arcade Menu with buttons
def arcade_menu():
    background_image = load_background_image('./MenuBackground.png')  # Replace 'background.jpg' with your image file path

    while True:
        screen.fill(BLACK)  # Fill the screen with black color
        draw_background_image(background_image, screen)
        
        draw_text('Arcade Mode', MENU_TITLE_FONT, WHITE, screen, SCREEN_WIDTH // 2, 200)

        button_width = 400
        button_height = 70

        load_saved_game_button = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, 450, button_width, button_height)
        start_new_button = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, 535, button_width, button_height)
        back_button = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, 620, button_width, button_height)

        draw_button_with_hover(load_saved_game_button, 'Load Saved Game', BUTTON_FONT, WHITE, GREY, screen)
        draw_button_with_hover(start_new_button, 'Start New', BUTTON_FONT, WHITE, GREY, screen)
        draw_button_with_hover(back_button, 'Back', BUTTON_FONT, WHITE, GREY, screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_click_sound.play()
                if load_saved_game_button.collidepoint(event.pos):
                    grid, coins, turn, score, restricted_residential = load_game_arcade()
                    if grid is not None:
                        arcade_game(grid, coins, turn, score, restricted_residential)
                    else:
                        draw_text('No saved game found. Please start a new game.', BUTTON_FONT, WHITE, screen, SCREEN_WIDTH // 2, 360)
                        pygame.display.update()
                        pygame.time.wait(2000)
                elif start_new_button.collidepoint(event.pos):
                    arcade_game()
                elif back_button.collidepoint(event.pos):
                    return

        pygame.display.update()

# Free Play Menu with buttons
def free_play_menu():
    background_image = load_background_image('./MenuBackground.png')  # Replace 'background.jpg' with your image file path

    while True:
        screen.fill(BLACK)  # Fill the screen with black color
        draw_background_image(background_image, screen)
        
        draw_text('Free Play Mode', MENU_TITLE_FONT, WHITE, screen, SCREEN_WIDTH // 2, 200)

        button_width = 400
        button_height = 70

        load_saved_game_button = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, 450, button_width, button_height)
        start_new_button = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, 535, button_width, button_height)
        back_button = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, 620, button_width, button_height)

        draw_button_with_hover(load_saved_game_button, 'Load Saved Game', BUTTON_FONT, WHITE, GREY, screen)
        draw_button_with_hover(start_new_button, 'Start New', BUTTON_FONT, WHITE, GREY, screen)
        draw_button_with_hover(back_button, 'Back', BUTTON_FONT, WHITE, GREY, screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_click_sound.play()
                if load_saved_game_button.collidepoint(event.pos):
                    grid, coins, turn, score, restricted_residential, expansion_count = load_game_free_play()
                    if grid is not None:
                        free_play_game(grid, coins, turn, score, restricted_residential, expansion_count)
                    else:
                        draw_text('No saved game found. Please start a new game.', BUTTON_FONT, WHITE, screen, SCREEN_WIDTH // 2, 360)
                        pygame.display.update()
                        pygame.time.wait(2000)
                elif start_new_button.collidepoint(event.pos):
                    free_play_game()
                elif back_button.collidepoint(event.pos):
                    return

        pygame.display.update()

def arcade_game(grid=None, coins=None, turn=None, score=None, restricted_residential=None):
    pygame.mixer.music.load('./GameSoundtrack.mp3')
    pygame.mixer.music.set_volume(0.6)  # Set volume to 60%
    pygame.mixer.music.play(-1)  # -1 means the music will loop indefinitely

    if grid is None:
        grid = [[None for _ in range(GRID_SIZE_ARCADE)] for _ in range(GRID_SIZE_ARCADE)]
    if coins is None:
        coins = 16
    if turn is None:
        turn = 0
    if score is None:
        score = 0
    if restricted_residential is None:
        restricted_residential = {}
    demolish_mode = False
    buildings = random.sample(BUILDINGS, 2)
    first_turn = (turn == 0)
    selected_building = None
    animation_frame = 0
    illegal_placement = False

    def draw_grid():
        for row in range(GRID_SIZE_ARCADE):
            for col in range(GRID_SIZE_ARCADE):
                rect = pygame.Rect(col * CELL_SIZE + MARGIN_LEFT, row * CELL_SIZE + MARGIN_TOP, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, GRID_COLOR, rect, 1)
                pygame.draw.rect(screen, CELL_COLOR, rect.inflate(-1, -1))
                if grid[row][col]:
                    draw_centered_text(grid[row][col], GAME_FONT, BLACK, screen, rect)

    def draw_rules():
        rules_x = SCREEN_WIDTH - MARGIN_RIGHT + TEXT_MARGIN_RIGHT + 50
        rules_y = MARGIN_TOP
        draw_text("Legend", BUTTON_FONT, WHITE, screen, rules_x, rules_y)
        legend_y = rules_y + 40
        for building, symbol in BUILDING_SYMBOLS.items():
            draw_text(f'{building}: {symbol}', GAME_FONT, WHITE, screen, rules_x, legend_y)
            legend_y += 20

        draw_text("Points System", BUTTON_FONT, WHITE, screen, rules_x, legend_y + 20)
        legend_y += 60
        draw_text("Residential:", GAME_FONT, WHITE, screen, rules_x, legend_y)
        draw_text("1 pt if adjacent to Industry", GAME_FONT, WHITE, screen, rules_x, legend_y + 20)
        draw_text("Otherwise:", GAME_FONT, WHITE, screen, rules_x, legend_y + 40)
        draw_text("+1 pt each adjacent R/C", GAME_FONT, WHITE, screen, rules_x, legend_y + 60)
        draw_text("+2 pts each adjacent Park", GAME_FONT, WHITE, screen, rules_x, legend_y + 80)
        draw_text("Industry:", GAME_FONT, WHITE, screen, rules_x, legend_y + 120)
        draw_text("1 pt each Industry in city", GAME_FONT, WHITE, screen, rules_x, legend_y + 140)
        draw_text("+1 coin each adjacent R", GAME_FONT, WHITE, screen, rules_x, legend_y + 160)
        draw_text("Commercial:", GAME_FONT, WHITE, screen, rules_x, legend_y + 200)
        draw_text("1 pt each adjacent Commercial", GAME_FONT, WHITE, screen, rules_x, legend_y + 220)
        draw_text("+1 coin each adjacent Residential", GAME_FONT, WHITE, screen, rules_x, legend_y + 240)
        draw_text("Park:", GAME_FONT, WHITE, screen, rules_x, legend_y + 280)
        draw_text("1 pt each adjacent Park", GAME_FONT, WHITE, screen, rules_x, legend_y + 300)
        draw_text("Road:", GAME_FONT, WHITE, screen, rules_x, legend_y + 340)
        draw_text("1 pt each connected road", GAME_FONT, WHITE, screen, rules_x, legend_y + 360)
        draw_text("in the same row", GAME_FONT, WHITE, screen, rules_x, legend_y + 380)

    def update_score_and_coins(row, col, operation):
        nonlocal score, coins
        building = grid[row][col]
        points = 0
        coins_gained = 0

        if building == 'R':
            points = calculate_residential_points_arcade(grid, row, col, restricted_residential)
        elif building == 'I':
            points = calculate_industry_points_arcade(grid, row, col)
            coins_gained = generate_coins_for_industry_arcade(grid, row, col)
        elif building == 'C':
            points = calculate_commercial_points_arcade(grid, row, col)
            coins_gained = generate_coins_for_commercial_arcade(grid, row, col)
        elif building == 'O':
            points = calculate_park_points_arcade(grid, row, col)
        elif building == '*':
            points = calculate_road_points_arcade(grid, row, col)

        if operation == 'add':
            score += points
            coins += coins_gained
        elif operation == 'remove':
            score -= points
            coins -= coins_gained
    
    while True:
        screen.fill(BACKGROUND_COLOR)
        draw_text(f'Turn: {turn}    Coins: {coins}    Score: {score}', GAME_FONT, WHITE, screen, SCREEN_WIDTH // 2, 20)

        draw_grid()
        draw_rules()

        if demolish_mode:
            draw_left_aligned_text('Demolish Mode: Click on a building to remove it', GAME_FONT, WHITE, screen, 20, 60)
            draw_left_aligned_text('Press D to return to building mode', GAME_FONT, WHITE, screen, 20, 80)
        else:
            draw_left_aligned_text(f'Choose a building: {BUILDINGS[BUILDINGS.index(buildings[0])]}, {BUILDING_SYMBOLS[buildings[0]]} (1) or {BUILDINGS[BUILDINGS.index(buildings[1])]}, {BUILDING_SYMBOLS[buildings[1]]} (2)', GAME_FONT, WHITE, screen, 20, 60)
            draw_left_aligned_text('Press D to toggle Demolish Mode', GAME_FONT, WHITE, screen, 20, 80)
            draw_left_aligned_text('Press M to return to Main Menu', GAME_FONT, WHITE, screen, 20, 100)
            if selected_building:
                draw_left_aligned_text(f'Building {selected_building}. Click on grid to place.', GAME_FONT, WHITE, screen, 20, 130)

        if illegal_placement:
            draw_left_aligned_text("Illegal placement. Try again.", GAME_FONT, WHITE, screen, 20, 160)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    save_game_arcade(grid, coins, turn, score, restricted_residential)
                    pygame.mixer.music.load('./MenuSoundtrack.mp3')
                    pygame.mixer.music.set_volume(0.6)  # Set volume to 60%
                    pygame.mixer.music.play(-1)  # -1 means the music will loop indefinitely
                    return
                if event.key == pygame.K_d:
                    demolish_mode = not demolish_mode
                    illegal_placement = False

                if not demolish_mode and coins > 0:
                    if event.key == pygame.K_1:
                        selected_building = buildings[0]
                    elif event.key == pygame.K_2:
                        selected_building = buildings[1]

            if event.type == pygame.MOUSEBUTTONUP:
                x, y = event.pos
                col = (x - MARGIN_LEFT) // CELL_SIZE
                row = (y - MARGIN_TOP) // CELL_SIZE
                if 0 <= col < GRID_SIZE_ARCADE and 0 <= row < GRID_SIZE_ARCADE:
                    if demolish_mode and grid[row][col] is not None:
                        update_score_and_coins(row, col, 'remove')
                        grid[row][col] = None
                        coins -= 1
                        turn += 1
                        illegal_placement = False
                        demolish_mode = False
                    elif not demolish_mode and (grid[row][col] is None or grid[row][col] == '') and selected_building:
                        if first_turn or is_adjacent_to_existing_building_arcade(grid, row, col):
                            grid[row][col] = BUILDING_SYMBOLS[selected_building]
                            coins -= 1
                            turn += 1
                            update_score_and_coins(row, col, 'add')
                            save_game_arcade(grid, coins, turn, score, restricted_residential)
                            buildings = random.sample(BUILDINGS, 2)
                            first_turn = False
                            selected_building = None
                            animation_frame = 30
                            illegal_placement = False

        if animation_frame > 0:
            animation_frame -= 1
            draw_text('+', GAME_FONT, WHITE, screen, SCREEN_WIDTH // 2 + 50, 20)

        pygame.display.update()

        if coins <= 0 or turn >= 16:
            name = prompt_player_name()
            save_leaderboard(name, score)
            clear_saved_game_arcade()
            pygame.mixer.music.load('./MenuSoundtrack.mp3')
            pygame.mixer.music.set_volume(0.6)  # Set volume to 60%
            pygame.mixer.music.play(-1)  # -1 means the music will loop indefinitely
            break

def free_play_game(grid=None, coins=None, turn=None, score=None, restricted_residential=None, expansion_count=0):
    pygame.mixer.music.load('./GameSoundtrack.mp3')
    pygame.mixer.music.set_volume(0.6)  # Set volume to 60%
    pygame.mixer.music.play(-1)  # -1 means the music will loop indefinitely
    if grid is None:
        grid = [[None for _ in range(5)] for _ in range(5)]
    if coins is None:
        coins = 0
    if turn is None:
        turn = 0
    if score is None:
        score = 0
    if restricted_residential is None:
        restricted_residential = {}
    demolish_mode = False
    selected_building = None
    animation_frame = 0
    illegal_placement = False
    first_turn = (turn == 0)  # Check if it's the first turn

    def draw_grid():
        # Draw the game grid for Free Play mode
        grid_size = len(grid)
        for row in range(grid_size):
            for col in range(grid_size):
                rect = pygame.Rect(col * CELL_SIZE + MARGIN_LEFT, row * CELL_SIZE + MARGIN_TOP, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, GRID_COLOR, rect, 1)
                pygame.draw.rect(screen, CELL_COLOR, rect.inflate(-1, -1))
                if grid[row][col]:
                    draw_centered_text(grid[row][col], GAME_FONT, BLACK, screen, rect)

    def draw_rules():
        # Draw the rules and legend for Free Play mode
        rules_x = SCREEN_WIDTH - MARGIN_RIGHT + TEXT_MARGIN_RIGHT + 50
        rules_y = MARGIN_TOP
        draw_text("Legend", BUTTON_FONT, WHITE, screen, rules_x, rules_y)
        legend_y = rules_y + 40
        for building, symbol in BUILDING_SYMBOLS.items():
            draw_text(f'{building}: {symbol}', GAME_FONT, WHITE, screen, rules_x, legend_y)
            legend_y += 20

        draw_text("Points System", BUTTON_FONT, WHITE, screen, rules_x, legend_y + 20)
        legend_y += 60
        draw_text("Residential:", GAME_FONT, WHITE, screen, rules_x, legend_y)
        draw_text("1 pt if adjacent to Industry", GAME_FONT, WHITE, screen, rules_x, legend_y + 20)
        draw_text("Otherwise:", GAME_FONT, WHITE, screen, rules_x, legend_y + 40)
        draw_text("+1 pt each adjacent R/C", GAME_FONT, WHITE, screen, rules_x, legend_y + 60)
        draw_text("+2 pts each adjacent Park", GAME_FONT, WHITE, screen, rules_x, legend_y + 80)
        draw_text("Industry:", GAME_FONT, WHITE, screen, rules_x, legend_y + 120)
        draw_text("1 pt each Industry in city", GAME_FONT, WHITE, screen, rules_x, legend_y + 140)
        draw_text("+1 coin each adjacent R", GAME_FONT, WHITE, screen, rules_x, legend_y + 160)
        draw_text("Commercial:", GAME_FONT, WHITE, screen, rules_x, legend_y + 200)
        draw_text("1 pt each adjacent Commercial", GAME_FONT, WHITE, screen, rules_x, legend_y + 220)
        draw_text("+1 coin each adjacent Residential", GAME_FONT, WHITE, screen, rules_x, legend_y + 240)
        draw_text("Park:", GAME_FONT, WHITE, screen, rules_x, legend_y + 280)
        draw_text("1 pt each adjacent Park", GAME_FONT, WHITE, screen, rules_x, legend_y + 300)
        draw_text("Road:", GAME_FONT, WHITE, screen, rules_x, legend_y + 340)
        draw_text("1 pt each connected road", GAME_FONT, WHITE, screen, rules_x, legend_y + 360)
        draw_text("in the same row", GAME_FONT, WHITE, screen, rules_x, legend_y + 380)
    
    def update_score_and_coins_free_play(row, col, operation):
        nonlocal score, coins
        building = grid[row][col]
        points = 0
        coins_gained = 0

        if building == 'R':
            points = calculate_residential_points_free_play(grid, row, col, restricted_residential)
        elif building == 'I':
            points = calculate_industry_points_free_play(grid, row, col)
            coins_gained = generate_coins_for_industry_free_play(grid, row, col)
        elif building == 'C':
            points = calculate_commercial_points_free_play(grid, row, col)
            coins_gained = generate_coins_for_commercial_free_play(grid, row, col)
        elif building == 'O':
            points = calculate_park_points_free_play(grid, row, col)
        elif building == '*':
            points = calculate_road_points_free_play(grid, row, col)

        if operation == 'add':
            score += points
            coins += coins_gained
        elif operation == 'remove':
            score -= points
            coins -= coins_gained

    while True:
        screen.fill(BACKGROUND_COLOR)
        draw_text(f'Turn: {turn}    Coins: {coins}    Score: {score}', GAME_FONT, WHITE, screen, SCREEN_WIDTH // 2, 20)

        draw_grid()
        draw_rules()

        if demolish_mode:
            draw_left_aligned_text('Demolish Mode: Click on a building to remove it', GAME_FONT, WHITE, screen, 20, 60)
            draw_left_aligned_text('Press D to return to building mode', GAME_FONT, WHITE, screen, 20, 80)
        else:
            draw_left_aligned_text(f'Choose a building: Residential (R) (1), Industry (I) (2), Commercial (C) (3), Park (O) (4), Road (*) (5)', GAME_FONT, WHITE, screen, 20, 60)
            draw_left_aligned_text('Press D to toggle Demolish Mode', GAME_FONT, WHITE, screen, 20, 80)
            draw_left_aligned_text('Press M to return to Main Menu', GAME_FONT, WHITE, screen, 20, 100)
            if selected_building:
                draw_left_aligned_text(f'Building {selected_building}. Click on grid to place.', GAME_FONT, WHITE, screen, 20, 130)

        if illegal_placement:
            draw_left_aligned_text("Illegal placement. Try again.", GAME_FONT, WHITE, screen, 20, 160)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    save_game_free_play(grid, coins, turn, score, restricted_residential, expansion_count)
                    pygame.mixer.music.load('./MenuSoundtrack.mp3')
                    pygame.mixer.music.set_volume(0.6)  # Set volume to 60%
                    pygame.mixer.music.play(-1)  # -1 means the music will loop indefinitely
                    return
                if event.key == pygame.K_d:
                    demolish_mode = not demolish_mode
                    illegal_placement = False

                if not demolish_mode:
                    if event.key == pygame.K_1:
                        selected_building = 'Residential'
                    elif event.key == pygame.K_2:
                        selected_building = 'Industry'
                    elif event.key == pygame.K_3:
                        selected_building = 'Commercial'
                    elif event.key == pygame.K_4:
                        selected_building = 'Park'
                    elif event.key == pygame.K_5:
                        selected_building = 'Road'

            if event.type == pygame.MOUSEBUTTONUP:
                x, y = event.pos
                col = (x - MARGIN_LEFT) // CELL_SIZE
                row = (y - MARGIN_TOP) // CELL_SIZE
                if 0 <= col < len(grid) and 0 <= row < len(grid):
                    if demolish_mode and grid[row][col] is not None:
                        update_score_and_coins_free_play(row, col, 'remove')
                        grid[row][col] = None
                        turn += 1
                        illegal_placement = False
                        demolish_mode = False
                    elif not demolish_mode and (grid[row][col] is None or grid[row][col] == '') and selected_building:
                        if first_turn or is_adjacent_to_existing_building_free_play(grid, row, col):
                            grid[row][col] = BUILDING_SYMBOLS[selected_building]
                            turn += 1
                            update_score_and_coins_free_play(row, col, 'add')
                            save_game_free_play(grid, coins, turn, score, restricted_residential, expansion_count)
                            selected_building = None
                            animation_frame = 30
                            illegal_placement = False
                            first_turn = False  # Set first_turn to False after placing the first building

                            if col == len(grid[0]) - 1 or row == len(grid) - 1:
                                if expansion_count < 2:
                                    new_size = len(grid) + 10
                                    grid = expand_grid(grid, new_size)
                                    expansion_count += 1
                        else:
                            illegal_placement = True

        if animation_frame > 0:
            animation_frame -= 1
            draw_text('+', GAME_FONT, WHITE, screen, SCREEN_WIDTH // 2 + 50, 20)

        pygame.display.update()
        
        # Check end-game condition
        if all((cell is not None and cell is not '') for row in grid for cell in row):
            end_game_screen(score, coins)
            pygame.mixer.music.load('./MenuSoundtrack.mp3')
            pygame.mixer.music.set_volume(0.6)  # Set volume to 60%
            pygame.mixer.music.play(-1)  # -1 means the music will loop indefinitely
            break


def end_game_screen(score, coins):
    # Display the end-game screen
    while True:
        screen.fill(BACKGROUND_COLOR)
        draw_text('Game Over!', TITLE_FONT, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)
        draw_text(f'Total Points: {score}', BUTTON_FONT, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        draw_text(f'Total Coins: {coins}', BUTTON_FONT, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40)
        draw_text('Press M to return to Main Menu', BUTTON_FONT, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)

        clear_saved_game_free_play()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:

                    main_menu()
                    return

        pygame.display.update()


if __name__ == "__main__":
    main_menu()

