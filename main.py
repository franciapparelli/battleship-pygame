import pygame
from sys import exit
from funciones import *

WIDTH, HEIGHT = 1920, 1080
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Naval Battle")

LIGHT_BLUE = (135, 206, 235)
BLACK = (0, 0, 0)
LETTERS = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]

FPS = 60
CREW_IMG = pygame.image.load("images/crew2.png")
rect = CREW_IMG.get_rect()
rect.center = 1280 // 2, 720 // 2

# we use the sizes to draw as well as to do our "steps" in the loops.
GRID_NODE_WIDTH = 60
GRID_NODE_HEIGHT = 60

ships_placing_phase = True
atacking_phase = False


def draw_window():
    SCREEN.fill(LIGHT_BLUE)
    pygame.draw.rect(SCREEN, (255, 0, 0), [WIDTH / 2, 0, 2, 1280])


def create_crew(x, y, color):
    pygame.draw.rect(SCREEN, color, [x, y, GRID_NODE_WIDTH, GRID_NODE_HEIGHT], 2)


def visualize_grid(matrix):
    y = 115  # we start at the top of the screen
    x = 100
    myfont = pygame.font.SysFont("monospace", 30)
    for letter in LETTERS:
        label = myfont.render(letter, 2, BLACK)
        SCREEN.blit(label, (x, y - 30))
        x += GRID_NODE_WIDTH
    counter = 0
    for row in matrix:
        x = 80  # for every row we start at the left of the screen again
        label = myfont.render(str(counter), 1, BLACK)
        counter += 1
        SCREEN.blit(label, (x, y))
        x = 100
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



def main():
    pygame.init()
    clock = pygame.time.Clock()
    running = True
    matrix = inicializar_matriz()
    moving = False
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
            elif event.type == pygame.MOUSEBUTTONUP and ships_placing_phase:
                moving = False
                first_pos_x, first_pos_y = rect.midleft
                second_pos_x, second_pos_y = rect.midright
                first_node_x = first_pos_x // GRID_NODE_WIDTH - 1
                first_node_y = first_pos_y // GRID_NODE_HEIGHT - 2
                second_node_x = second_pos_x // GRID_NODE_WIDTH - 2
                second_node_y = second_pos_y // GRID_NODE_HEIGHT -2
            elif event.type == pygame.MOUSEMOTION and moving and ships_placing_phase:
                rect.move_ip(event.rel)
                first_pos_x, first_pos_y = rect.topleft
                second_pos_x, second_pos_y = rect.bottomright
                first_node_x = first_pos_x // GRID_NODE_WIDTH - 1
                first_node_y = first_pos_y // GRID_NODE_HEIGHT - 2
                second_node_x = second_pos_x // GRID_NODE_WIDTH - 2
                second_node_y = second_pos_y // GRID_NODE_HEIGHT - 2
                for row in range(9):
                    for item in range(9):
                        if (row == first_node_y and item == first_node_x) or (
                            row == second_node_y and item == second_node_x
                            ):
                            if first_node_x <= 8 and first_node_x >= 0 and first_node_y <= 8 and first_node_y >= 0 and first_node_x == second_node_x or first_node_y == second_node_y:
                                matrix[row][item] = "H"
                            else:
                                matrix[row][item] = "F"
                        else:
                            matrix[row][item] = "-"
            elif event.type == pygame.MOUSEBUTTONDOWN and atacking_phase:
                if event.button == 1:  # 1 representa el clic izquierdo del mouse
                    # Obtener la posición del clic del mouse
                    x, y = pygame.mouse.get_pos()
                    # Calcular la celda en la que se hizo clic
                    column_click = x // 60 - 6
                    row_click = y // 60 - 4
                    if (
                    row_click <= 8
                    and row_click >= 0
                    and column_click <= 8
                    and column_click >= 0
                    ):
                        matrix[row_click][column_click] = "T"

        draw_window()
        visualize_grid(matrix)
        SCREEN.blit(CREW_IMG, rect)
        pygame.draw.rect(SCREEN, BLACK, rect, 2)
        pygame.display.update()

if __name__ == "__main__":
    main()