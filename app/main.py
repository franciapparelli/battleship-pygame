import pygame
from sys import exit
from funciones import *
from collections import namedtuple

WIDTH, HEIGHT = 1600, 900
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Naval Battle")

LIGHT_BLUE = (135, 206, 235)
BLACK = (0, 0, 0)
LETTERS = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]

FPS = 60

crew_img = pygame.image.load("images/crew2.png")
rect = crew_img.get_rect()
rect.center = WIDTH // 2, HEIGHT // 2

START_BUTTON = pygame.image.load("images/start.png")
rect_start = START_BUTTON.get_rect()
rect_start.center = WIDTH // 2, HEIGHT // 1.3

BULLET = pygame.image.load("images/bullet.png")

pygame.mixer.pre_init(20000)
pygame.mixer.init()
HIT_SOUND = pygame.mixer.Sound("images/hit.wav")
MISS_SOUND = pygame.mixer.Sound("images/miss.wav")
WIN_SOUND = pygame.mixer.Sound("images/winning.wav")

# we use the sizes to draw as well as to do our "steps" in the loops.
GRID_NODE_WIDTH = WIDTH // 25
GRID_NODE_HEIGHT = WIDTH // 25

winner = None


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
            elif item == "O":
                create_crew(x, y, (255, 255, 255))
                SCREEN.blit(BULLET, (x + GRID_NODE_WIDTH / 5, y + GRID_NODE_HEIGHT / 5))
            elif item == "T":
                create_crew(x, y, (0, 255, 0))
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
        x = (
            WIDTH // 16 - 25 + WIDTH // 2
        )  # for every row we start at the left of the screen again
        label = myfont.render(str(counter), 1, BLACK)
        counter += 1
        SCREEN.blit(label, (x, y))
        x = WIDTH // 16 + WIDTH // 2
        for item in row:
            if item == "-":
                create_crew(x, y, (255, 255, 255))
            elif item == "T":
                create_crew(x, y, (255, 0, 0))
            elif item == "F":
                create_crew(x, y, (255, 255, 255))
                SCREEN.blit(BULLET, (x + GRID_NODE_WIDTH / 5, y + GRID_NODE_HEIGHT / 5))
            elif item == "O":
                create_crew(x, y, (255, 255, 255))
                SCREEN.blit(BULLET, (x + GRID_NODE_WIDTH / 5, y + GRID_NODE_HEIGHT / 5))
            else:
                create_crew(x, y, (255, 255, 255))
                SCREEN.blit(BULLET, (x + GRID_NODE_WIDTH / 5, y + GRID_NODE_HEIGHT / 5))

            x += GRID_NODE_WIDTH  # for every item/number in that row we move one "step" to the right
        y += GRID_NODE_HEIGHT  # for every new row we move one "step" downwards


def validate_ship_placement(matrix):
    counter = 0
    for row in matrix:
        for item in row:
            if item == "B":
                counter += 1
    if counter != 12:
        return False
    return True


def computer_attacking(matrix, computer_counter):
    row = random.randint(0, 8)
    column = random.randint(0, 8)

    while matrix[row][column] == "F" or matrix[row][column] == "O":
        row = random.randint(0, 8)
        column = random.randint(0, 8)

    if matrix[row][column] == "B":
        matrix[row][column] = "F"
        pygame.mixer.Sound.play(HIT_SOUND)
        computer_counter += 1  # Increment the computer_counter
    else:
        matrix[row][column] = "O"
        pygame.mixer.Sound.play(MISS_SOUND)

    return matrix, computer_counter  # Return the updated computer_counter


Message = namedtuple("Message", ["text", "position", "frames"])


def create_message(text, position):
    return Message(text, position, 0)


def update_messages(messages):
    return [msg._replace(frames=msg.frames + 1) for msg in messages]


def add_message(messages, message):
    return messages + [message]


def remove_message(messages, message):
    return [msg for msg in messages if msg != message]


def render_message(screen, message, font):
    text_surface = font.render(message.text, True, (255, 255, 255))
    screen.blit(text_surface, message.position)


def display_winner(winner):
    font = pygame.font.SysFont("monospace", 60)
    text = font.render(f"{winner} wins!", True, (0, 0, 0))
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    pygame.draw.rect(SCREEN, (255, 255, 255), text_rect)
    SCREEN.blit(text, text_rect)
    pygame.display.update()


def main():
    pygame.init()
    clock = pygame.time.Clock()

    # Crew Boats Load
    crew2_img = pygame.image.load("images/crew2.png")
    rect2 = crew2_img.get_rect()
    rect2.center = WIDTH // 9, HEIGHT // 1.2

    crew3_img = pygame.image.load("images/crew3.png")
    rect3 = crew3_img.get_rect()
    rect3.center = WIDTH // 3, HEIGHT // 1.2

    crew3D_img = pygame.image.load("images/crew3.png")  # Second Boat of size 3
    rect3D = crew3D_img.get_rect()
    rect3D.center = WIDTH // 9, HEIGHT // 1.1

    crew4_img = pygame.image.load("images/crew4.png")
    rect4 = crew4_img.get_rect()
    rect4.center = WIDTH // 3, HEIGHT // 1.1

    player_matrix = inicializar_matriz()
    computer_matrix = inicializar_matriz_computadora()
    visible_computer_matrix = inicializar_matriz()
    moving = False
    moving2 = False
    moving3 = False
    moving3D = False
    moving4 = False
    ships_placing_phase = True
    attacking_phase = False
    player_attacking_phase = True
    computer_attacking_phase = False
    player_counter = 0
    computer_counter = 0
    messages = []
    running = True
    winner = None
    winner_display = False
    counter1_message = None
    counter2_message = None
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and ships_placing_phase:
                if event.button == 1:  # 1 representa el clic izquierdo del mouse
                    if rect2.collidepoint(event.pos):
                        moving = True
                        moving2 = True
                    if rect3.collidepoint(event.pos):
                        moving = True
                        moving3 = True
                    if rect3D.collidepoint(event.pos):
                        moving = True
                        moving3D = True
                    if rect4.collidepoint(event.pos):
                        moving = True
                        moving4 = True
                    if rect_start.collidepoint(event.pos):
                        if validate_ship_placement(player_matrix):
                            ships_placing_phase = False
                            attacking_phase = True
                            START_BUTTON.fill((255, 255, 255, 0))
                if event.button == 3:
                    if rect2.collidepoint(event.pos):
                        crew2_img = pygame.transform.rotate(crew2_img, 90)
                        rect2 = crew2_img.get_rect()
                        rect2.center = rect2.centerx, rect2.centery
                        rect2.move_ip(pygame.mouse.get_pos())
                    if rect3.collidepoint(event.pos):
                        crew3_img = pygame.transform.rotate(crew3_img, 90)
                        rect3 = crew3_img.get_rect()
                        rect3.center = rect3.centerx, rect3.centery
                        rect3.move_ip(pygame.mouse.get_pos())
                    if rect3D.collidepoint(event.pos):
                        crew3D_img = pygame.transform.rotate(crew3D_img, 90)
                        rect3D = crew3D_img.get_rect()
                        rect3D.center = rect3D.centerx, rect3D.centery
                        rect3D.move_ip(pygame.mouse.get_pos())
                    if rect4.collidepoint(event.pos):
                        crew4_img = pygame.transform.rotate(crew4_img, 90)
                        rect4 = crew4_img.get_rect()
                        rect4.center = rect4.centerx, rect4.centery
                        rect4.move_ip(pygame.mouse.get_pos())
            elif event.type == pygame.MOUSEBUTTONUP and ships_placing_phase:
                moving = False
                if moving2:
                    moving2 = False
                elif moving3:
                    moving3 = False
                elif moving3D:
                    moving3D = False
                elif moving4:
                    moving4 = False
                first_pos_x, first_pos_y = rect.midleft
                second_pos_x, second_pos_y = rect.midright
                first_node_x = (first_pos_x - (WIDTH // 16)) // GRID_NODE_WIDTH
                first_node_y = (first_pos_y - (HEIGHT // 8)) // GRID_NODE_HEIGHT
                second_node_x = (second_pos_x - (WIDTH // 16)) // GRID_NODE_WIDTH
                second_node_y = (second_pos_y - (HEIGHT // 8)) // GRID_NODE_HEIGHT
                for row in range(9):
                    for item in range(9):
                        if player_matrix[row][item] == "H":
                            player_matrix[row][item] = "B"

            elif event.type == pygame.MOUSEMOTION and moving and ships_placing_phase:
                if moving2:
                    rect2.move_ip(event.rel)
                    first_pos_x, first_pos_y = rect2.topleft
                    second_pos_x, second_pos_y = rect2.bottomright
                elif moving3:
                    rect3.move_ip(event.rel)
                    first_pos_x, first_pos_y = rect3.topleft
                    second_pos_x, second_pos_y = rect3.bottomright
                elif moving3D:
                    rect3D.move_ip(event.rel)
                    first_pos_x, first_pos_y = rect3D.topleft
                    second_pos_x, second_pos_y = rect3D.bottomright
                elif moving4:
                    rect4.move_ip(event.rel)
                    first_pos_x, first_pos_y = rect4.topleft
                    second_pos_x, second_pos_y = rect4.bottomright
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
                            ):
                                if moving2:
                                    if (
                                        second_node_x - first_node_x == 1
                                        or second_node_y - first_node_y == 1
                                    ):
                                        player_matrix[row][item] = "H"
                                    else:
                                        player_matrix[row][item] = "F"
                                elif moving3 or moving3D:
                                    if second_node_x - first_node_x == 2:
                                        player_matrix[row][item] = "H"
                                        if item != first_node_x:
                                            player_matrix[row][item - 1] = "H"
                                    elif second_node_y - first_node_y == 2:
                                        player_matrix[row][item] = "H"
                                        if row != first_node_y:
                                            player_matrix[row - 1][item] = "H"
                                    else:
                                        if second_node_x - first_node_x == 3:
                                            player_matrix[row][item] = "F"
                                            player_matrix[row][item - 1] = "F"
                                        if second_node_y - first_node_y == 3:
                                            player_matrix[row][item] = "F"
                                            player_matrix[row - 1][item] = "F"
                                elif moving4:
                                    if (
                                        second_node_x - first_node_x == 3
                                        and second_node_x < 9
                                        and second_node_x - 2 >= 0
                                    ):
                                        player_matrix[row][item] = "H"
                                        player_matrix[row][second_node_x - 1] = "H"
                                        player_matrix[row][second_node_x - 2] = "H"
                                    elif (
                                        second_node_y - first_node_y == 3
                                        and second_node_y < 9
                                        and second_node_y - 2 >= 0
                                    ):
                                        player_matrix[row][item] = "H"
                                        player_matrix[second_node_y - 1][item] = "H"
                                        player_matrix[second_node_y - 2][item] = "H"
                                    else:
                                        player_matrix[row][item] = "F"
                                else:
                                    player_matrix[row][item] = "F"
                        else:
                            if player_matrix[row][item] != "B":
                                player_matrix[row][item] = "-"

            elif event.type == pygame.MOUSEBUTTONDOWN and attacking_phase:
                if player_attacking_phase:
                    messages = remove_message(messages, counter1_message)
                    messages = remove_message(messages, counter2_message)
                    counter1_message = create_message(
                        f"Player Counter: {player_counter}", (10, 10)
                    )  # Display for 2 seconds (assuming 60 FPS)
                    counter2_message = create_message(
                        f"Computer Counter: {computer_counter}", (WIDTH - 350, 10)
                    )  # Display for 2 seconds (assuming 60 FPS)
                    messages = add_message(messages, counter1_message)
                    messages = add_message(messages, counter2_message)
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
                        if computer_matrix[row_click][column_click] == "X":
                            computer_matrix[row_click][column_click] = "T"
                            visible_computer_matrix[row_click][column_click] = "T"
                            pygame.mixer.Sound.play(HIT_SOUND)
                            player_counter += 1
                        elif computer_matrix[row_click][column_click] != "T":
                            visible_computer_matrix[row_click][column_click] = "O"
                            pygame.mixer.Sound.play(MISS_SOUND)
                        player_attacking_phase = False
                        if player_counter < 12:
                            row = random.randint(0, 8)
                            column = random.randint(0, 8)

                            while (
                                player_matrix[row][column] == "F"
                                or player_matrix[row][column] == "O"
                            ):
                                row = random.randint(0, 8)
                                column = random.randint(0, 8)

                            if player_matrix[row][column] == "B":
                                player_matrix[row][column] = "F"
                                pygame.mixer.Sound.play(HIT_SOUND)
                                computer_counter += 1  # Increment the computer_counter
                            else:
                                player_matrix[row][column] = "O"
                                pygame.mixer.Sound.play(MISS_SOUND)
                                player_attacking_phase = True
                        else:
                            running = False
        if player_counter == 12:
            winner = "Player"
            display_winner(winner)
            pygame.mixer.Sound.play(WIN_SOUND)
            pygame.time.wait(900)
            pygame.quit()
        elif computer_counter == 12:
            winner = "Computer"
            display_winner(winner)
            pygame.time.wait(5000)
            pygame.quit()

        draw_window()
        visualize_grid_player(player_matrix)
        visualize_grid_computer(visible_computer_matrix)
        SCREEN.blit(crew2_img, rect2)
        SCREEN.blit(crew3_img, rect3)
        SCREEN.blit(crew3D_img, rect3D)
        SCREEN.blit(crew4_img, rect4)
        SCREEN.blit(START_BUTTON, rect_start)
        myfont = pygame.font.SysFont("monospace", 30)
        for message in messages:
            render_message(SCREEN, message, myfont)
        pygame.display.update()
    SCREEN.fill(LIGHT_BLUE)
    SCREEN.blit(START_BUTTON, (WIDTH // 2, HEIGHT // 2))


if __name__ == "__main__":
    main()
