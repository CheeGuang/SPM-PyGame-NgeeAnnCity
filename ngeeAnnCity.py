import pygame
import random
import sys
import csv
import os

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 850
GRID_SIZE = 20  # Changed grid size to 20x20
CELL_SIZE = 30
TITLE_FONT = pygame.font.SysFont("Arial", 40)
BUTTON_FONT = pygame.font.SysFont("Arial", 30)
GAME_FONT = pygame.font.SysFont("Arial", 20)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)
BLUE = (173, 216, 230)
GREEN = (144, 238, 144)
BUILDINGS = ['Residential', 'Industry', 'Commercial', 'Park', 'Road']
BUILDING_SYMBOLS = {'Residential': 'R', 'Industry': 'I', 'Commercial': 'C', 'Park': 'O', 'Road': '*'}
BACKGROUND_COLOR = BLUE
GRID_COLOR = BLACK
CELL_COLOR = WHITE
MARGIN_LEFT = 50
MARGIN_TOP = 200  # 2x margin top
MARGIN_BOTTOM = 50
MARGIN_RIGHT = 250
TEXT_MARGIN_RIGHT = 20
TEXT_PADDING_LEFT = 20
TEXT_PADDING_TOP = 10

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Ngee Ann City")

# Functions to draw text
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

def draw_left_aligned_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(topleft=(x, y))
    surface.blit(text_obj, text_rect)

def draw_centered_text(text, font, color, surface, rect):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=rect.center)
    surface.blit(text_obj, text_rect)

# Calculate points for the grid
def calculate_points(grid):
    points = 0
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if grid[row][col] == 'R':
                points += calculate_residential_points(grid, row, col)
            elif grid[row][col] == 'I':
                points += calculate_industry_points(grid, row, col)
            elif grid[row][col] == 'C':
                points += calculate_commercial_points(grid, row, col)
            elif grid[row][col] == 'O':
                points += calculate_park_points(grid, row, col)
            elif grid[row][col] == '*':
                points += calculate_road_points(grid, row, col)
    return points

# Calculate points for Residential buildings
def calculate_residential_points(grid, row, col):
    points = 0
    adjacents = [(row-1, col), (row+1, col), (row, col-1), (row, col+1)]
    adjacent_to_industry = False
    for r, c in adjacents:
        if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE:
            if grid[r][c] == 'I':
                adjacent_to_industry = True
                points = 1  # Maximum 1 point if adjacent to Industry
    if not adjacent_to_industry:
        for r, c in adjacents:
            if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE:
                if grid[r][c] == 'R' or grid[r][c] == 'C':
                    points += 1
                elif grid[r][c] == 'O':
                    points += 2
    return points

# Calculate points for Industry buildings
def calculate_industry_points(grid, row, col):
    points = 0
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if grid[r][c] == 'I':
                points += 1
    return points

# Calculate points for Commercial buildings
def calculate_commercial_points(grid, row, col):
    points = 0
    adjacents = [(row-1, col), (row+1, col), (row, col-1), (row, col+1)]
    for r, c in adjacents:
        if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE:
            if grid[r][c] == 'C':
                points += 1
    return points

# Calculate points for Park buildings
def calculate_park_points(grid, row, col):
    points = 0
    adjacents = [(row-1, col), (row+1, col), (row, col-1), (row, col+1)]
    for r, c in adjacents:
        if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE:
            if grid[r][c] == 'O':
                points += 1
    return points

# Calculate points for Road buildings
def calculate_road_points(grid, row, col):
    points = 0
    for c in range(GRID_SIZE):
        if grid[row][c] == '*':
            points += 1
    return points

# Generate coin for Commercial next to Residential
def generate_coins_for_commercial(grid, row, col):
    coins = 0
    adjacents = [(row-1, col), (row+1, col), (row, col-1), (row, col+1)]
    for r, c in adjacents:
        if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE:
            if grid[r][c] == 'R':
                coins += 1
    return coins

# Check if a cell is adjacent to an existing building
def is_adjacent_to_existing_building(grid, row, col):
    adjacents = [(row-1, col), (row+1, col), (row, col-1), (row, col+1)]
    for r, c in adjacents:
        if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE and (grid[r][c] is not None and grid[r][c] != ''):
            return True
    return False

# Save game state to CSV
def save_game(grid, coins, turn, score):
    with open('NgeeAnnCity_Arcade_SavedGame.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Grid', 'Coins', 'Turn', 'Score'])
        for row in grid:
            writer.writerow(row)
        writer.writerow([coins, turn, score])

# Load game state from CSV
def load_game():
    if os.path.exists('NgeeAnnCity_Arcade_SavedGame.csv'):
        with open('NgeeAnnCity_Arcade_SavedGame.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            grid = []
            for i in range(GRID_SIZE):
                row = next(reader, None)
                if row is None:
                    return None, None, None, None
                # Convert 'None' strings to actual None values
                grid.append([None if cell == 'None' else cell for cell in row])
            coins, turn, score = map(int, next(reader))
            return grid, coins, turn, score
    return None, None, None, None

# Save leaderboard to CSV
def save_leaderboard(name, score):
    # Prevent CSV injection
    name = name.replace("=", "").replace("+", "").replace("-", "").replace("@", "")
    with open('NgeeAnnCity_Arcade_Leaderboard.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([name, score])

# Clear saved game
def clear_saved_game():
    if os.path.exists('NgeeAnnCity_Arcade_SavedGame.csv'):
        os.remove('NgeeAnnCity_Arcade_SavedGame.csv')

# Prompt for player name
def prompt_player_name():
    pygame.display.update()
    screen.fill(BACKGROUND_COLOR)
    draw_text('Enter your name:', BUTTON_FONT, BLACK, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40)
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
        draw_text('Enter your name:', BUTTON_FONT, BLACK, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40)
        draw_text(name, BUTTON_FONT, BLACK, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10)
        pygame.display.update()

# Display leaderboard
def display_leaderboard():
    while True:
        screen.fill(BACKGROUND_COLOR)
        draw_text('Leaderboard - Arcade Mode', TITLE_FONT, BLACK, screen, SCREEN_WIDTH // 2, 50)
        
        if os.path.exists('NgeeAnnCity_Arcade_Leaderboard.csv'):
            leaderboard = []
            with open('NgeeAnnCity_Arcade_Leaderboard.csv', 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    leaderboard.append((row[0], int(row[1])))
            leaderboard.sort(key=lambda x: x[1], reverse=True)  # Sort by score in descending order
            y_offset = 100
            for i, (name, score) in enumerate(leaderboard[:10]):  # Display top 10
                draw_text(f'{i + 1}. {name}: {score}', BUTTON_FONT, BLACK, screen, SCREEN_WIDTH // 2, y_offset)
                y_offset += 40
        else:
            draw_text('No leaderboard data available.', BUTTON_FONT, BLACK, screen, SCREEN_WIDTH // 2, 100)
        
        draw_text('Press B to go back to main menu', BUTTON_FONT, BLACK, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 40)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    return

        pygame.display.update()

# Main Menu with buttons
def main_menu():
    while True:
        screen.fill(BACKGROUND_COLOR)
        draw_text('Ngee Ann City', TITLE_FONT, BLACK, screen, SCREEN_WIDTH // 2, 50)

        button_width = 300
        button_height = 50

        play_button = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, 150, button_width, button_height)
        leaderboard_button = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, 220, button_width, button_height)
        exit_button = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, 290, button_width, button_height)

        pygame.draw.rect(screen, WHITE, play_button, border_radius=6)
        pygame.draw.rect(screen, WHITE, leaderboard_button, border_radius=6)
        pygame.draw.rect(screen, WHITE, exit_button, border_radius=6)
        pygame.draw.rect(screen, BLACK, play_button, 1, border_radius=6)
        pygame.draw.rect(screen, BLACK, leaderboard_button, 1, border_radius=6)
        pygame.draw.rect(screen, BLACK, exit_button, 1, border_radius=6)

        draw_centered_text('Play', BUTTON_FONT, BLACK, screen, play_button)
        draw_centered_text('Leaderboard', BUTTON_FONT, BLACK, screen, leaderboard_button)
        draw_centered_text('Exit', BUTTON_FONT, BLACK, screen, exit_button)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    play_menu()
                elif leaderboard_button.collidepoint(event.pos):
                    display_leaderboard()
                elif exit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

# Play Menu with buttons
def play_menu():
    while True:
        screen.fill(BACKGROUND_COLOR)
        draw_text('Play Mode', TITLE_FONT, BLACK, screen, SCREEN_WIDTH // 2, 50)

        button_width = 300
        button_height = 50

        arcade_mode_button = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, 150, button_width, button_height)
        free_play_button = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, 220, button_width, button_height)
        back_button = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, 290, button_width, button_height)

        pygame.draw.rect(screen, WHITE, arcade_mode_button, border_radius=6)
        pygame.draw.rect(screen, WHITE, free_play_button, border_radius=6)
        pygame.draw.rect(screen, WHITE, back_button, border_radius=6)
        pygame.draw.rect(screen, BLACK, arcade_mode_button, 1, border_radius=6)
        pygame.draw.rect(screen, BLACK, free_play_button, 1, border_radius=6)
        pygame.draw.rect(screen, BLACK, back_button, 1, border_radius=6)

        draw_centered_text('Arcade Mode', BUTTON_FONT, BLACK, screen, arcade_mode_button)
        draw_centered_text('Free Play', BUTTON_FONT, BLACK, screen, free_play_button)
        draw_centered_text('Back', BUTTON_FONT, BLACK, screen, back_button)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if arcade_mode_button.collidepoint(event.pos):
                    arcade_menu()
                elif free_play_button.collidepoint(event.pos):
                    free_play_menu()
                elif back_button.collidepoint(event.pos):
                    return

        pygame.display.update()

# Arcade Menu with buttons
def arcade_menu():
    while True:
        screen.fill(BACKGROUND_COLOR)
        draw_text('Arcade Mode', TITLE_FONT, BLACK, screen, SCREEN_WIDTH // 2, 50)

        button_width = 300
        button_height = 50

        load_saved_game_button = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, 150, button_width, button_height)
        start_new_button = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, 220, button_width, button_height)
        back_button = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, 290, button_width, button_height)

        pygame.draw.rect(screen, WHITE, load_saved_game_button, border_radius=6)
        pygame.draw.rect(screen, WHITE, start_new_button, border_radius=6)
        pygame.draw.rect(screen, WHITE, back_button, border_radius=6)
        pygame.draw.rect(screen, BLACK, load_saved_game_button, 1, border_radius=6)
        pygame.draw.rect(screen, BLACK, start_new_button, 1, border_radius=6)
        pygame.draw.rect(screen, BLACK, back_button, 1, border_radius=6)

        draw_centered_text('Load Saved Game', BUTTON_FONT, BLACK, screen, load_saved_game_button)
        draw_centered_text('Start New', BUTTON_FONT, BLACK, screen, start_new_button)
        draw_centered_text('Back', BUTTON_FONT, BLACK, screen, back_button)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if load_saved_game_button.collidepoint(event.pos):
                    grid, coins, turn, score = load_game()
                    if grid is not None:
                        print(f"Loaded game: coins={coins}, turn={turn}, score={score}")
                        arcade_game(grid, coins, turn, score)
                    else:
                        draw_text('No saved game found. Please start a new game.', BUTTON_FONT, BLACK, screen, SCREEN_WIDTH // 2, 360)
                        pygame.display.update()
                        pygame.time.wait(2000)
                elif start_new_button.collidepoint(event.pos):
                    arcade_game()
                elif back_button.collidepoint(event.pos):
                    return

        pygame.display.update()

# Free Play Menu with buttons
def free_play_menu():
    while True:
        screen.fill(BACKGROUND_COLOR)
        draw_text('Free Play Mode', TITLE_FONT, BLACK, screen, SCREEN_WIDTH // 2, 50)

        button_width = 300
        button_height = 50

        load_saved_game_button = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, 150, button_width, button_height)
        start_new_button = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, 220, button_width, button_height)
        back_button = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, 290, button_width, button_height)

        pygame.draw.rect(screen, WHITE, load_saved_game_button, border_radius=6)
        pygame.draw.rect(screen, WHITE, start_new_button, border_radius=6)
        pygame.draw.rect(screen, WHITE, back_button, border_radius=6)
        pygame.draw.rect(screen, BLACK, load_saved_game_button, 1, border_radius=6)
        pygame.draw.rect(screen, BLACK, start_new_button, 1, border_radius=6)
        pygame.draw.rect(screen, BLACK, back_button, 1, border_radius=6)

        draw_centered_text('Load Saved Game', BUTTON_FONT, BLACK, screen, load_saved_game_button)
        draw_centered_text('Start New', BUTTON_FONT, BLACK, screen, start_new_button)
        draw_centered_text('Back', BUTTON_FONT, BLACK, screen, back_button)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if load_saved_game_button.collidepoint(event.pos):
                    grid, coins, turn, score = load_game()
                    if grid is not None:
                        arcade_game(grid, coins, turn, score)
                    else:
                        draw_text('No saved game found. Please start a new game.', BUTTON_FONT, BLACK, screen, SCREEN_WIDTH // 2, 360)
                        pygame.display.update()
                        pygame.time.wait(2000)
                elif start_new_button.collidepoint(event.pos):
                    arcade_game()
                elif back_button.collidepoint(event.pos):
                    return

        pygame.display.update()

# Arcade Game Mode
def arcade_game(grid=None, coins=None, turn=None, score=None):
    if grid is None:
        grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    if coins is None:
        coins = 16
    if turn is None:
        turn = 0
    if score is None:
        score = 0
    demolish_mode = False
    buildings = random.sample(BUILDINGS, 2)
    first_turn = (turn == 0)
    selected_building = None
    animation_frame = 0
    illegal_placement = False

    def draw_grid():
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                rect = pygame.Rect(col * CELL_SIZE + MARGIN_LEFT, row * CELL_SIZE + MARGIN_TOP, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, GRID_COLOR, rect, 1)
                pygame.draw.rect(screen, CELL_COLOR, rect.inflate(-1, -1))
                if grid[row][col]:
                    draw_centered_text(grid[row][col], GAME_FONT, BLACK, screen, rect)

    def draw_rules():
        rules_x = SCREEN_WIDTH - MARGIN_RIGHT + TEXT_MARGIN_RIGHT + 50
        rules_y = MARGIN_TOP
        draw_text("Legend", BUTTON_FONT, BLACK, screen, rules_x, rules_y)
        legend_y = rules_y + 40
        for building, symbol in BUILDING_SYMBOLS.items():
            draw_text(f'{building}: {symbol}', GAME_FONT, BLACK, screen, rules_x, legend_y)
            legend_y += 20

        draw_text("Points System", BUTTON_FONT, BLACK, screen, rules_x, legend_y + 20)
        legend_y += 60
        draw_text("Residential:", GAME_FONT, BLACK, screen, rules_x, legend_y)
        draw_text("1 pt if adjacent to Industry", GAME_FONT, BLACK, screen, rules_x, legend_y + 20)
        draw_text("Otherwise:", GAME_FONT, BLACK, screen, rules_x, legend_y + 40)
        draw_text("+1 pt each adjacent R/C", GAME_FONT, BLACK, screen, rules_x, legend_y + 60)
        draw_text("+2 pts each adjacent Park", GAME_FONT, BLACK, screen, rules_x, legend_y + 80)
        draw_text("Industry:", GAME_FONT, BLACK, screen, rules_x, legend_y + 120)
        draw_text("1 pt each Industry in city", GAME_FONT, BLACK, screen, rules_x, legend_y + 140)
        draw_text("+1 coin each adjacent R", GAME_FONT, BLACK, screen, rules_x, legend_y + 160)
        draw_text("Commercial:", GAME_FONT, BLACK, screen, rules_x, legend_y + 200)
        draw_text("1 pt each adjacent Commercial", GAME_FONT, BLACK, screen, rules_x, legend_y + 220)
        draw_text("+1 coin each adjacent Residential", GAME_FONT, BLACK, screen, rules_x, legend_y + 240)
        draw_text("Park:", GAME_FONT, BLACK, screen, rules_x, legend_y + 280)
        draw_text("1 pt each adjacent Park", GAME_FONT, BLACK, screen, rules_x, legend_y + 300)
        draw_text("Road:", GAME_FONT, BLACK, screen, rules_x, legend_y + 340)
        draw_text("1 pt each connected road", GAME_FONT, BLACK, screen, rules_x, legend_y + 360)
        draw_text("in the same row", GAME_FONT, BLACK, screen, rules_x, legend_y + 380)

    while True:
        screen.fill(BACKGROUND_COLOR)
        draw_text(f'Turn: {turn}    Coins: {coins}    Score: {score}', GAME_FONT, BLACK, screen, SCREEN_WIDTH // 2, 20)
        
        draw_grid()
        draw_rules()

        if demolish_mode:
            draw_left_aligned_text('Demolish Mode: Click on a building to remove it', GAME_FONT, BLACK, screen, 20, 60)
            draw_left_aligned_text('Press D to return to building mode', GAME_FONT, BLACK, screen, 20, 80)
        else:
            draw_left_aligned_text(f'Choose a building: {BUILDINGS[BUILDINGS.index(buildings[0])]}, {BUILDING_SYMBOLS[buildings[0]]} (1) or {BUILDINGS[BUILDINGS.index(buildings[1])]}, {BUILDING_SYMBOLS[buildings[1]]} (2)', GAME_FONT, BLACK, screen, 20, 60)
            draw_left_aligned_text('Press D to toggle Demolish Mode', GAME_FONT, BLACK, screen, 20, 80)
            draw_left_aligned_text('Press M to return to Main Menu', GAME_FONT, BLACK, screen, 20, 100)
            if selected_building:
                draw_left_aligned_text(f'Building {selected_building}. Click on grid to place.', GAME_FONT, BLACK, screen, 20, 130)

        if illegal_placement:
            draw_left_aligned_text("Illegal placement. Try again.", GAME_FONT, BLACK, screen, 20, 160)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    save_game(grid, coins, turn, score)
                    return
                if event.key == pygame.K_d:
                    demolish_mode = not demolish_mode
                    illegal_placement = False

                if not demolish_mode and coins > 0:
                    if event.key == pygame.K_1:
                        selected_building = buildings[0]
                    elif event.key == pygame.K_2:
                        selected_building = buildings[1]

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                col = (x - MARGIN_LEFT) // CELL_SIZE
                row = (y - MARGIN_TOP) // CELL_SIZE
                if 0 <= col < GRID_SIZE and 0 <= row < GRID_SIZE:
                    if demolish_mode and grid[row][col] is not None:
                        # Check if there is more than one building on the board
                        building_count = sum([1 for r in range(GRID_SIZE) for c in range(GRID_SIZE) if grid[r][c] is not None])
                        if building_count > 1:
                            grid[row][col] = None
                            turn += 1
                            score = calculate_points(grid)
                            illegal_placement = False
                            demolish_mode = False
                    elif not demolish_mode and (grid[row][col] is None or grid[row][col] == '') and selected_building:
                        if first_turn or is_adjacent_to_existing_building(grid, row, col):
                            grid[row][col] = BUILDING_SYMBOLS[selected_building]
                            coins -= 1
                            if selected_building == 'Commercial':
                                coins += generate_coins_for_commercial(grid, row, col)
                            turn += 1
                            new_score = calculate_points(grid)
                            save_game(grid, coins, turn, score)
                            buildings = random.sample(BUILDINGS, 2)  # Randomize new buildings for the next turn
                            first_turn = False
                            selected_building = None
                            animation_frame = 30
                            illegal_placement = False

                            # Log points calculation details
                            point_difference = new_score - score
                            print(f"Turn {turn}:")
                            if point_difference > 0:
                                for r in range(GRID_SIZE):
                                    for c in range(GRID_SIZE):
                                        if grid[r][c] == 'R':
                                            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                                                nr, nc = r + dr, c + dc
                                                if 0 <= nr < GRID_SIZE and 0 <= nc < GRID_SIZE:
                                                    if grid[nr][nc] == 'R':
                                                        print("+1 Point for Residential adjacent Residential")
                                                    elif grid[nr][nc] == 'C':
                                                        print("+1 Point for Residential adjacent Commercial")
                                                    elif grid[nr][nc] == 'O':
                                                        print("+2 Points for Residential adjacent Park")
                                        elif grid[r][c] == 'I':
                                            print("+1 Point for each Industry in city")
                                        elif grid[r][c] == 'C':
                                            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                                                nr, nc = r + dr, c + dc
                                                if 0 <= nr < GRID_SIZE and 0 <= nc < GRID_SIZE:
                                                    if grid[nr][nc] == 'C':
                                                        print("+1 Point for Commercial adjacent Commercial")
                                        elif grid[r][c] == 'O':
                                            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                                                nr, nc = r + dr, c + dc
                                                if 0 <= nr < GRID_SIZE and 0 <= nc < GRID_SIZE:
                                                    if grid[nr][nc] == 'O':
                                                        print("+1 Point for Park adjacent Park")
                                        elif grid[r][c] == '*':
                                            for nc in range(GRID_SIZE):
                                                if grid[r][nc] == '*':
                                                    print("+1 Point for each connected Road in the same row")
                            score = new_score

        # Simple animation for score increase
        if animation_frame > 0:
            animation_frame -= 1
            draw_text('+', GAME_FONT, BLACK, screen, SCREEN_WIDTH // 2 + 50, 20)

        pygame.display.update()

        if coins <= 0 or turn >= 16:
            name = prompt_player_name()
            save_leaderboard(name, score)
            clear_saved_game()  # Clear the saved game after the game ends
            break




if __name__ == "__main__":
    main_menu()
