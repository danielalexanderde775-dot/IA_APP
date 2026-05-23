import math

# Guardar trayectoria del dedo índice
trayectoria = []

def detectar_movimiento(x, y):
    global trayectoria

    # Guardar punto
    trayectoria.append((x, y))

    # Limitar historial
    if len(trayectoria) > 15:
        trayectoria.pop(0)

    # Necesitamos suficientes puntos
    if len(trayectoria) < 10:
        return None

    # Movimiento total
    dx = trayectoria[-1][0] - trayectoria[0][0]
    dy = trayectoria[-1][1] - trayectoria[0][1]

    # -------- DETECCIÓN J --------
    # Movimiento curvo hacia abajo
    if dy > 0.1 and abs(dx) > 0.05:
        return "J"

    # -------- DETECCIÓN Z --------
    cambios = 0

    for i in range(1, len(trayectoria)-1):
        prev_x = trayectoria[i-1][0]
        curr_x = trayectoria[i][0]
        next_x = trayectoria[i+1][0]

        if (curr_x > prev_x and curr_x > next_x) or \
           (curr_x < prev_x and curr_x < next_x):
            cambios += 1

    if cambios >= 2:
        return "Z"

    return None