import pygame
from sys import exit
from funciones import *

WIDTH, HEIGHT = 1600, 900
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Naval Battle")

LIGHT_BLUE = (135, 206, 235)
BLACK = (0, 0, 0)
LETTERS = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]

FPS = 60
CREW_IMG = pygame.image.load("images/crew2.png")
rect = CREW_IMG.get_rect()
rect.center = WIDTH // 2, HEIGHT // 2
START_BUTTON = pygame.image.load("images/start.png")
rect_start = START_BUTTON.get_rect()
rect_start.center = WIDTH // 2, HEIGHT // 1.3

# we use the sizes to draw as well as to do our "steps" in the loops.
GRID_NODE_WIDTH = WIDTH // 25
GRID_NODE_HEIGHT = WIDTH // 25


def draw_window():
    SCREEN.fill(LIGHT_BLUE)
    pygame.draw.rect(SCREEN, (255, 0, 0), [WIDTH / 2, 0, 2, WIDTH])


def create_crew(x, y, color):
    pygame.draw.rect(SCREEN, color, [x, y, GRID_NODE_WIDTH, GRID_NODE_HEIGHT], 2)


def visualize_grid_player(matrix):
    y = HEIGHT // 8  # we start at the top of the screen
    x = WIDTH // 16 + 14
    myfont = pygame.font.SysFont("monospace", 30)
    for letter in LETTERS:
        label = myfont.render(letter, 2, BLACK)
        SCREEN.blit(label, (x, y - 30))
        x += GRID_NODE_WIDTH
    counter = 0
    for row in matrix:
        x = WIDTH // 16 - 25  # for every row we start at the left of the screen again
        label = myfont.render(str(counter), 1, BLACK)
        counter += 1
        SCREEN.blit(label, (x, y))
        x = WIDTH // 16
        for item in row:
            if item == "-":
                create_crew(x, y, (255, 255, 255))
            elif item == "H":
                create_crew(x, y, (0, 255, 0))
            elif item == "F":
                create_crew(x, y, (255, 0, 0))
            else:
                create_crew(x, y, (0, 0, 0))

            x += GRID_NODE_WIDTH  # for every item/number in that row we move one "step" to the right
        y += GRID_NODE_HEIGHT  # for every new row we move one "step" downwards


def visualize_grid_computer(matrix):
    y = HEIGHT // 8  # we start at the top of the screen
    x = WIDTH // 16 + 14 + WIDTH // 2
    myfont = pygame.font.SysFont("monospace", 30)
    for letter in LETTERS:
        label = myfont.render(letter, 2, BLACK)
        SCREEN.blit(label, (x, y - 30))
        x += GRID_NODE_WIDTH
    counter = 0
    for row in matrix:
        x = WIDTH // 16 - 25 + WIDTH // 2 # for every row we start at the left of the screen again
        label = myfont.render(str(counter), 1, BLACK)
        counter += 1
        SCREEN.blit(label, (x, y))
        x = WIDTH // 16 + WIDTH // 2
        for item in row:
            if item == "-":
                create_crew(x, y, (255, 255, 255))
            elif item == "H":
                create_crew(x, y, (0, 255, 0))
            elif item == "F":
                create_crew(x, y, (255, 0, 0))
            else:
                create_crew(x, y, (0, 0, 0))

            x += GRID_NODE_WIDTH  # for every item/number in that row we move one "step" to the right
        y += GRID_NODE_HEIGHT  # for every new row we move one "step" downwards

"""
def validate_ship_placement(matrix):
    # Define the ship sizes and their counts
    ship_sizes = {'Aircraft Carrier': 5, 'Battleship': 4, 'Cruiser': 3, 'Submarine': 3, 'Destroyer': 2}
    ship_counts = {ship: 0 for ship in ship_sizes}

    # Iterate through the matrix to validate ship placement
    for row in range(9):
        for col in range(9):
            cell = matrix[row][col]

            # If the cell contains a ship, check its placement
            if cell == "H":
                # Check horizontally for consecutive ships
                if col + 1 < 9 and matrix[row][col + 1] == "H":
                    return False  # Two ships are adjacent horizontally
                # Check vertically for consecutive ships
                if row + 1 < 9 and matrix[row + 1][col] == "H":
                    return False  # Two ships are adjacent vertically

                # Determine the ship's size
                ship_size = 1
                if col + 1 < 9 and matrix[row][col + 1] == "H":
                    # If the ship continues horizontally, calculate its size
                    for i in range(col + 1, 9):
                        if matrix[row][i] == "H":
                            ship_size += 1
                        else:
                            break

                elif row + 1 < 9 and matrix[row + 1][col] == "H":
                    # If the ship continues vertically, calculate its size
                    for i in range(row + 1, 9):
                        if matrix[i][col] == "H":
                            ship_size += 1
                        else:
                            break

                # Check if the ship size matches a valid ship size
                if ship_size not in ship_sizes.values():
                    return False  # Invalid ship size

                # Increment the count of the corresponding ship
                for ship, size in ship_sizes.items():
                    if size == ship_size:
                        ship_counts[ship] += 1

    # Check if the correct number of each ship is placed
    for ship, count in ship_counts.items():
        if count != 1:  # In a standard game, there should be one of each type of ship
            return False

    # All checks passed, ship placement is valid
    return True
"""


def main():
    pygame.init()
    clock = pygame.time.Clock()
    running = True
    player_matrix = inicializar_matriz()
    computer_matrix = inicializar_matriz_computadora()
    visible_computer_matrix = inicializar_matriz()
    moving = False
    ships_placing_phase = True
    attacking_phase = False

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and ships_placing_phase:
                if event.button == 1:  # 1 representa el clic izquierdo del mouse
                    if rect.collidepoint(event.pos):
                        moving = True
                    if rect_start.collidepoint(event.pos):
                        # if validate_ship_placement(player_matrix):
                        #     ships_placing_phase = False
                        ships_placing_phase = False
                        attacking_phase = True
                        START_BUTTON.fill((255,255,255,0))

            elif event.type == pygame.MOUSEBUTTONUP and ships_placing_phase:
                moving = False
                first_pos_x, first_pos_y = rect.midleft
                second_pos_x, second_pos_y = rect.midright
                first_node_x = (first_pos_x - (WIDTH // 16)) // GRID_NODE_WIDTH
                first_node_y = (first_pos_y - (HEIGHT // 8)) // GRID_NODE_HEIGHT
                second_node_x = (second_pos_x - (WIDTH // 16)) // GRID_NODE_WIDTH
                second_node_y = (second_pos_y - (HEIGHT // 8)) // GRID_NODE_HEIGHT
            elif event.type == pygame.MOUSEMOTION and moving and ships_placing_phase:
                rect.move_ip(event.rel)
                first_pos_x, first_pos_y = rect.topleft
                second_pos_x, second_pos_y = rect.bottomright
                first_node_x = (first_pos_x - (WIDTH // 16)) // GRID_NODE_WIDTH
                first_node_y = (first_pos_y - (HEIGHT // 8)) // GRID_NODE_HEIGHT
                second_node_x = (second_pos_x - (WIDTH // 16)) // GRID_NODE_WIDTH
                second_node_y = (second_pos_y - (HEIGHT // 8)) // GRID_NODE_HEIGHT
                for row in range(9):
                    for item in range(9):
                        if (row == first_node_y and item == first_node_x) or (
                            row == second_node_y and item == second_node_x
                        ):
                            if (
                                first_node_x <= 8
                                and first_node_x >= 0
                                and first_node_y <= 8
                                and first_node_y >= 0
                                and first_node_x == second_node_x
                                or first_node_y == second_node_y
                                and second_node_x - first_node_x == 1
                            ):
                                player_matrix[row][item] = "H"
                            else:
                                player_matrix[row][item] = "F"
                        else:
                            player_matrix[row][item] = "-"
            elif event.type == pygame.MOUSEBUTTONDOWN and attacking_phase:
                player_attacking_phase = True
                computer_attacking_phase = False
                if event.button == 1:  # 1 representa el clic izquierdo del mouse
                    # Obtener la posición del clic del mouse
                    x, y = pygame.mouse.get_pos()

                    # Calcular la celda en la que se hizo clic  
                    column_click = (x - (WIDTH // 16 + WIDTH // 2)) // GRID_NODE_WIDTH
                    row_click = (y - (HEIGHT // 8)) // GRID_NODE_HEIGHT
                    if (
                        row_click <= 8
                        and row_click >= 0
                        and column_click <= 8
                        and column_click >= 0
                    ):
                        if player_attacking_phase:
                            if computer_matrix[row_click][column_click] == "X":
                                visible_computer_matrix[row_click][column_click] = "T"
                        else:
                            computer_matrix[row_click][column_click] = "T"

        draw_window()
        visualize_grid_player(player_matrix)
        visualize_grid_computer(visible_computer_matrix)
        SCREEN.blit(CREW_IMG, rect)
        SCREEN.blit(START_BUTTON, rect_start)
        pygame.draw.rect(SCREEN, BLACK, rect, 2)
        pygame.display.update()


if __name__ == "__main__":
    main()