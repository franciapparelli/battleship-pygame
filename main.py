import pygame
from sys import exit
from funciones import * 

WIDTH, HEIGHT = 1280, 720
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Naval Battle")

LIGHT_BLUE = (135, 206, 235)
BLACK = (0, 0, 0)
LETTERS = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]

FPS = 60

def draw_window():
    SCREEN.fill(LIGHT_BLUE)
    pygame.draw.rect(SCREEN, (255, 0, 0), [640, 0, 2, 1280])

matrix = inicializar_matriz()
# we use the sizes to draw as well as to do our "steps" in the loops. 
grid_node_width = 30  
grid_node_height = 30

def createCrew(x, y, color):
    pygame.draw.rect(SCREEN, color, [x, y, grid_node_width, grid_node_height], 2)

def visualizeGrid(matrix):
    y = 115  # we start at the top of the screen
    x = 185
    myfont = pygame.font.SysFont("monospace", 30)
    for letter in LETTERS:
        label = myfont.render(letter, 2, BLACK)
        SCREEN.blit(label, (x, y - 30))
        x += grid_node_width
    counter = 0
    for row in matrix:
        x = 150 # for every row we start at the left of the screen again
        label = myfont.render(str(counter), 1, BLACK)
        counter += 1
        SCREEN.blit(label, (x, y))
        x = 180
        for item in row:
            if item == "-":
                createCrew(x, y, (255, 255, 255))
            else:
                createCrew(x, y, (0, 0, 0))

            x += grid_node_width # for ever item/number in that row we move one "step" to the right
        y += grid_node_height   # for every new row we move one "step" downwards


def main():
    pygame.init()
    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 1 representa el clic izquierdo del mouse
                    # Obtener la posición del clic del mouse
                    x, y = pygame.mouse.get_pos()
                    # Calcular la celda en la que se hizo clic
                    column_click = x // 30 - 6
                    row_click = y // 30 - 4
                    print(f"Se hizo clic en la celda ({row_click}, {column_click})")
                    matrix[row_click][column_click] = "T"

        draw_window()               
        visualizeGrid(matrix)
        pygame.display.update()

    

if __name__ == '__main__':
    main()


    