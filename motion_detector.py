trayectoria = []

def detectar_movimiento(x, y):
    global trayectoria

    trayectoria.append((x, y))

    # Mantener historial
    if len(trayectoria) > 20:
        trayectoria.pop(0)

    # Esperar suficientes puntos
    if len(trayectoria) < 15:
        return None

    # Movimiento total
    dx = trayectoria[-1][0] - trayectoria[0][0]
    dy = trayectoria[-1][1] - trayectoria[0][1]

    # =========================
    # DETECCIÓN J
    # =========================
    # Movimiento hacia abajo + curva leve
    if dy > 0.15 and abs(dx) > 0.08:
        trayectoria.clear()
        return "J"

    # =========================
    # DETECCIÓN Z
    # =========================

    cambios = 0

    for i in range(2, len(trayectoria)-2):

        x1 = trayectoria[i-1][0]
        x2 = trayectoria[i][0]
        x3 = trayectoria[i+1][0]

        # Detectar cambio REAL de dirección
        if (x2 > x1 and x2 > x3) or \
           (x2 < x1 and x2 < x3):
            cambios += 1

    # Necesita MUCHOS cambios
    if cambios >= 4 and abs(dx) > 0.20:
        trayectoria.clear()
        return "Z"

    return None