import random
import os
import pygame

crew_member = pygame.image.load(os.path.join("images", "crew_member.png"))

# Funcion para inicilizar matrices que luego seran modificadas para mostrar por consola
def inicializar_matriz():
    matriz = [
    ["-", "-", "-", "-", "-", "-", "-", "-", "-"],
    ["-", "-", "-", "-", "-", "-", "-", "-", "-"],
    ["-", "-", "-", "-", "-", "-", "-", "-", "-"],
    ["-", "-", "-", "-", "-", "-", "-", "-", "-"],
    ["-", "-", "-", "-", "-", "-", "-", "-", "-"],
    ["-", "-", "-", "-", "-", "-", "-", "-", "-"],
    ["-", "-", "-", "-", "-", "-", "-", "-", "-"],
    ["-", "-", "-", "-", "-", "-", "-", "-", "-"],
    ["-", "-", "-", "-", "-", "-", "-", "-", "-"]
    ]
    return matriz

# Funcion para generar los barcos de la computadora
def inicializar_matriz_computadora():
    matriz = inicializar_matriz()

    # Logica para colocar los barcos
    n = 4
    es_valido = False
    while n > 0:
        if n == 2 or n == 1:
            m = n + 1
        else:
            m = n
        
        while es_valido is False:
            posicion_barco = random.randint(0, 1) # 0 para vertical, 1 para horizontal
            fila = random.randint(0, 8 - m)
            columna = random.randint(0, 9 - m)
            es_valido = validar_barcos_computadora(posicion_barco, fila, columna, matriz, m)
        
        if posicion_barco == 0:
            for i in range(m):
                 matriz[fila + i][columna] = "X"   
        else:
            for i in range(m): 
                matriz[fila][columna + i] = "X" 
        n -= 1           
    return matriz  

# Funcion de validacion de los barcos de la computadora antes que se coloquen
def validar_barcos_computadora(posicion_barco, fila, columna, matriz, m):
    if posicion_barco == 0:
        for i in range(m):
            if matriz[fila + i][columna] == "X":
                return False

    else:
        for i in range(m):
            if matriz[fila][columna + i] == "X":  
                return False
    return True

# Funcion para mostrar los tablero por consola
def mostrar_tablero(matriz):
    cadena = ""
    cadena += "  A B C D E F G H I"
    contador = 0
    for fila in matriz:
        cadena += '\n' + str(contador) + " "
        int(contador)
        contador += 1 
        for valor in fila:
            cadena += valor + " "
    return cadena    

# Funcion para separar las coordenadas ( "A1 A4" --> ["A1", "A4"] )
def separar_coordenadas(cadena):
    espacio = 0
    coordenadas_separadas = [""]
    for i in range(len(cadena)):
        if cadena[i] == " ": # Detecta un espacio e inicializa otro indice en la lista
            espacio += 1
            coordenadas_separadas.append("")
        else:
            coordenadas_separadas[espacio] += cadena[i] 
    return coordenadas_separadas

# Funcion para que el usuario coloque sus barcos
def solicitar_barcos():
    matriz_jugador = inicializar_matriz() # INICIALIZAMOS LA MATRIZ DEL USUARIO
    barco1 = input("Ingrese las coordenadas iniciales y finales para colocar su barco (Ejemplo: A1 A4) '\n' Barco 1 (4 celdas):")
    barco1 = separar_coordenadas(barco1)
    while colocar_barco(barco1, matriz_jugador, 4) is None:
        print("Las coordenadas ingresadas no son válidas!!") 
        barco1 = input("Ingrese las coordenadas iniciales y finales para colocar su barco (Ejemplo: A1 A4) '\n' Barco 1 (4 celdas):")
        barco1 = separar_coordenadas(barco1)
    print("Barcos colocados correctamente.")

    barco2 = input("Ingrese las coordenadas iniciales y finales para colocar su barco (Ejemplo: A1 A4) '\n' Barco 2 (3 celdas):")
    barco2 = separar_coordenadas(barco2)
    while colocar_barco(barco2, matriz_jugador, 3) is None:
        print("Las coordenadas ingresadas no son válidas!!") 
        barco2 = input("Ingrese las coordenadas iniciales y finales para colocar su barco (Ejemplo: A1 A4) '\n' Barco 2 (3 celdas):")
        barco2 = separar_coordenadas(barco2)
    

    barco3 = input("Ingrese las coordenadas iniciales y finales para colocar su barco (Ejemplo: A1 A4) '\n' Barco 3 (3 celdas):")
    barco3 = separar_coordenadas(barco3)
    while colocar_barco(barco3, matriz_jugador, 3) is None:
        print("Las coordenadas ingresadas no son válidas!!") 
        barco3 = input("Ingrese las coordenadas iniciales y finales para colocar su barco (Ejemplo: A1 A4) '\n' Barco 3 (3 celdas):")
        barco3 = separar_coordenadas(barco3)
    

    barco4 = input("Ingrese las coordenadas iniciales y finales para colocar su barco (Ejemplo: A1 A4) '\n' Barco 4 (2 celdas):")
    barco4 = separar_coordenadas(barco4)
    while colocar_barco(barco4, matriz_jugador, 2) is None:
        print("Las coordenadas ingresadas no son válidas!!") 
        barco4 = input("Ingrese las coordenadas iniciales y finales para colocar su barco (Ejemplo: A1 A4) '\n' Barco 4 (2 celdas):")
        barco4 = separar_coordenadas(barco4)
    

    return matriz_jugador

# Funcion para colocar los barcos del usuario
def colocar_barco(barco, matriz, n_barco):
    # Validacion
    columnas_validas = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]
    filas_validas = ["0", "1", "2", "3", "4", "5", "6", "7", "8"]
    if len(barco) != 2:
        return None
    for i in barco:
        contador = 0
        if len(i) != 2:
            return None
        for j in i:
            if contador % 2 == 0:
                if j not in columnas_validas:
                    return None
            else:
                if j not in filas_validas:
                    return None
            contador += 1
    
    primer_coordenada = barco[0]
    ultima_coordenada = barco[1]
    columna_primer_coordenada = primer_coordenada[0]
    columna_ultima_coordenada = ultima_coordenada[0]
    columna_primer_coordenada = ord(columna_primer_coordenada) - 65
    columna_ultima_coordenada = ord(columna_ultima_coordenada) - 65
    fila_primer_coordenada = int(primer_coordenada[1])
    fila_ultima_coordenada = int(ultima_coordenada[1])
    barco_vertical = False

    if columna_primer_coordenada == columna_ultima_coordenada:
        barco_vertical = True
    if barco_vertical:
        for i in range(n_barco):
            if matriz[fila_primer_coordenada + i][columna_primer_coordenada] != "X" and fila_ultima_coordenada - fila_primer_coordenada == n_barco - 1:
                matriz[fila_primer_coordenada + i][columna_primer_coordenada] = "X"
            else:
                return None    
    else:
        for i in range(n_barco):
            if matriz[fila_primer_coordenada][columna_primer_coordenada + i] != "X" and columna_ultima_coordenada - columna_primer_coordenada == n_barco - 1:  
                matriz[fila_primer_coordenada][columna_primer_coordenada + i] = "X" 
            else:
                return None           
    return matriz  

# Funcion del ataque del jugador
def ataque_jugador(matriz_visible, matriz_computadora, contador):
    coordenadas_ataque = input("Ingrese las coordenadas para atacar (Ejemplo: A1): ")
    while coordenadas_ataque[0] not in ["A", "B", "C", "D", "E", "F", "G", "H", "I"] or coordenadas_ataque[1] not in ["0", "1", "2", "3", "4", "5", "6", "7", "8"] or len(coordenadas_ataque) != 2:
        coordenadas_ataque = input("Coordenadas no validas. Ingrese nuevamente las coordenadas para atacar (Ejemplo: A1): ")
        columna_coordenadas = ord(coordenadas_ataque[0]) - 65
        fila_coordenadas = int(coordenadas_ataque[1])
    columna_coordenadas = ord(coordenadas_ataque[0]) - 65
    fila_coordenadas = int(coordenadas_ataque[1])
    if matriz_computadora[fila_coordenadas][columna_coordenadas] == "X":
        matriz_visible[fila_coordenadas][columna_coordenadas] = "T"
        matriz_computadora[fila_coordenadas][columna_coordenadas] = "T"
        contador += 1
        print("Acertaste! Has impactado en un barco enemigo.")
    else:
        if matriz_computadora[fila_coordenadas][columna_coordenadas] == "T":
            print("Ya habias disparado ahi, perdiste el turno!")
        else:
            matriz_visible[fila_coordenadas][columna_coordenadas] = "O"
            print("Fallaste! No has impactado en un barco enemigo.")
    print(mostrar_tablero(matriz_visible))
    return contador

# Funcion del ataque de la computadora
def ataque_computadora(matriz, contador_computadora):
    fila = random.randint (0 , 8)
    columna = random.randint (0 , 8)
    
    while matriz [fila][columna] != "T" and matriz [fila][columna] != "O":
        fila = random.randint (0 , 8)
        columna = random.randint (0 , 8)
        if matriz [fila][columna] == "X":
            matriz [fila][columna] = "T"
            contador_computadora += 1
            print("La computadora ha tocado tu barco")
        else:
            matriz [fila][columna] = "O"
            print("La computadora ha fallado a tu barco")
        print(mostrar_tablero(matriz))
    return contador_computadora