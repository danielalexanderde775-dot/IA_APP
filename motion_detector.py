trayectoria = []

def detectar_movimiento(data):

    global trayectoria

    # -------- PUNTOS MANO --------
    indice_tip_x = data[24]
    indice_tip_y = data[25]

    indice_base_y = data[19]

    # =========================
    # SOLO FUNCIONA SI EL ÍNDICE
    # ESTÁ LEVANTADO
    # =========================
    indice_arriba = indice_tip_y < indice_base_y

    if not indice_arriba:
        trayectoria.clear()
        return None

    # Guardar trayectoria
    trayectoria.append((indice_tip_x, indice_tip_y))

    # Limitar historial
    if len(trayectoria) > 20:
        trayectoria.pop(0)

    # Esperar suficientes puntos
    if len(trayectoria) < 15:
        return None

    # Movimiento total
    dx = trayectoria[-1][0] - trayectoria[0][0]
    dy = trayectoria[-1][1] - trayectoria[0][1]

    # =========================
    # LETRA J
    # =========================
    if dy > 0.15 and abs(dx) > 0.08:
        trayectoria.clear()
        return "J"

    # =========================
    # LETRA Z
    # =========================
    cambios = 0

    for i in range(2, len(trayectoria)-2):

        x1 = trayectoria[i-1][0]
        x2 = trayectoria[i][0]
        x3 = trayectoria[i+1][0]

        if (x2 > x1 and x2 > x3) or \
           (x2 < x1 and x2 < x3):
            cambios += 1

    if cambios >= 4 and abs(dx) > 0.25:
        trayectoria.clear()
        return "Z"

    return None