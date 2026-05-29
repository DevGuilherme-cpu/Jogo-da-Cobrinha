import numpy as np
import pygame
import random
import sys
import math

pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=512)

#  TEMAS VISUAIS
TEMAS = {
    "Selva": {
        "fundo":         (34,  85,  34),
        "grade":         (40, 100,  40),
        "parede":        (180, 30,  30),
        "parede_brilho": (220, 60,  60),
        "cobra":         (50, 205,  50),
        "cobra_sombra":  (30, 140,  30),
        "cobra_brilho":  (120, 240, 120),
        "pontos":        (255, 230,  80),
    },
    "Noite": {
        "fundo":         (10,  10,  30),
        "grade":         (20,  20,  50),
        "parede":        (80,   0, 160),
        "parede_brilho": (140,  0, 255),
        "cobra":         (0,  200, 255),
        "cobra_sombra":  (0,  100, 180),
        "cobra_brilho":  (150, 240, 255),
        "pontos":        (255, 200,  50),
    },
    "Deserto": {
        "fundo":         (180, 140,  60),
        "grade":         (190, 155,  75),
        "parede":        (160,  60,   0),
        "parede_brilho": (220, 100,  20),
        "cobra":         (255, 200,   0),
        "cobra_sombra":  (180, 130,   0),
        "cobra_brilho":  (255, 240, 150),
        "pontos":        (255, 255, 255),
    },
    "Gelo": {
        "fundo":         (180, 220, 240),
        "grade":         (160, 210, 235),
        "parede":        (0,   80, 160),
        "parede_brilho": (0,  140, 220),
        "cobra":         (255, 255, 255),
        "cobra_sombra":  (150, 200, 230),
        "cobra_brilho":  (220, 240, 255),
        "pontos":        (0,   60, 140),
    },
}

#  PERSONAGENS
PERSONAGENS = ["Cobra", "Lagarta", "Dragão", "Alien"]

#  DIFICULDADES
DIFICULDADES = {
    "Fácil":   {"velocidade": 8,  "obstaculos": 0},
    "Médio":   {"velocidade": 12, "obstaculos": 3},
    "Difícil": {"velocidade": 17, "obstaculos": 6},
    "Insano":  {"velocidade": 24, "obstaculos": 10},
}

#  JANELA / CONSTANTES
ESPESSURA_PAREDE = 10
LARGURA = 640
ALTURA = 480
TAMANHO_BLOCO = 20

AREA_X1 = ESPESSURA_PAREDE
AREA_Y1 = ESPESSURA_PAREDE
AREA_X2 = LARGURA - ESPESSURA_PAREDE
AREA_Y2 = ALTURA - ESPESSURA_PAREDE
AREA_LARGURA = AREA_X2 - AREA_X1
AREA_ALTURA = AREA_Y2 - AREA_Y1

# TELA REAL e SUPERFÍCIE VIRTUAL
tela = pygame.display.set_mode((LARGURA, ALTURA), pygame.RESIZABLE)
superficie_jogo = pygame.Surface((LARGURA, ALTURA))

relogio = pygame.time.Clock()
pygame.display.set_caption("🐍 Cobrinha Supreme")

fonte_titulo = pygame.font.SysFont("bahnschrift", 48, bold=True)
fonte_grande = pygame.font.SysFont("bahnschrift", 32, bold=True)
fonte_media = pygame.font.SysFont("bahnschrift", 22)
fonte_pequena = pygame.font.SysFont("bahnschrift", 17)

#  IMAGENS


def criar_cabeca(personagem, cor_cobra, cor_sombra):
    surf = pygame.Surface((TAMANHO_BLOCO, TAMANHO_BLOCO), pygame.SRCALPHA)
    B = TAMANHO_BLOCO
    cx, cy = B // 2, B // 2

    if personagem == "Lagarta":
        pygame.draw.circle(surf, cor_sombra, (cx, cy), B//2)
        pygame.draw.circle(surf, (200, 230, 80), (cx, cy), B//2 - 2)
        pygame.draw.circle(surf, (0, 0, 0), (cx-3, cy-3), 2)
        pygame.draw.circle(surf, (0, 0, 0), (cx+3, cy-3), 2)
        pygame.draw.line(surf, (100, 180, 0), (cx-3, 1), (cx-5, -2), 1)
        pygame.draw.line(surf, (100, 180, 0), (cx+3, 1), (cx+5, -2), 1)

    elif personagem == "Dragão":
        pts = [(cx, 0), (B, cy+4), (cx+2, B), (cx-2, B), (0, cy+4)]
        pygame.draw.polygon(surf, cor_sombra, pts)
        pts2 = [(cx, 2), (B-2, cy+4), (cx+1, B-2), (cx-1, B-2), (2, cy+4)]
        pygame.draw.polygon(surf, (255, 80, 0), pts2)
        pygame.draw.circle(surf, (255, 220, 0), (cx-3, cy-1), 2)
        pygame.draw.circle(surf, (255, 220, 0), (cx+3, cy-1), 2)

    elif personagem == "Alien":
        pygame.draw.rect(surf, cor_sombra, (1, 3, B-2, B-4), border_radius=4)
        pygame.draw.rect(surf, (0, 200, 100),
                         (2, 4, B-4, B-6), border_radius=3)
        for ex, ey in [(3, 6), (B-5, 6), (cx-1, 5)]:
            pygame.draw.circle(surf, (200, 255, 0), (ex, ey), 2)
        for ax in [2, 5, B-6, B-3]:
            pygame.draw.line(surf, (0, 180, 80), (ax, B-4), (ax, B), 1)

    else:
        pygame.draw.circle(surf, cor_sombra, (cx, cy), B//2)
        pygame.draw.circle(surf, cor_cobra, (cx, cy), B//2 - 2)
        pygame.draw.circle(surf, (255, 255, 255), (cx-3, cy-2), 3)
        pygame.draw.circle(surf, (255, 255, 255), (cx+3, cy-2), 3)
        pygame.draw.circle(surf, (0, 0, 0), (cx-3, cy-2), 1)
        pygame.draw.circle(surf, (0, 0, 0), (cx+3, cy-2), 1)
        pygame.draw.line(surf, (220, 50, 50), (cx, cy+3), (cx+3, cy+5), 2)

    return surf


def criar_comida():
    surf = pygame.Surface((TAMANHO_BLOCO, TAMANHO_BLOCO), pygame.SRCALPHA)
    B = TAMANHO_BLOCO
    pygame.draw.circle(surf, (200, 0, 0), (B//2, B//2+1), B//2-1)
    pygame.draw.circle(surf, (230, 50, 50), (B//2-2, B//2-2), B//4)
    pygame.draw.line(surf, (80, 160, 0), (B//2+1, 2), (B//2+3, -1), 2)
    return surf


#  SOM PROCEDURAL
def gerar_som(freq=440, duracao=0.08, volume=0.3, forma="square"):
    sample_rate = 44100
    n = int(sample_rate * duracao)
    t = np.linspace(0, duracao, n, False)
    if forma == "square":
        onda = np.sign(np.sin(2 * np.pi * freq * t))
    elif forma == "triangle":
        onda = 2 * np.abs(2 * (t * freq - np.floor(t * freq + 0.5))) - 1
    else:
        onda = np.sin(2 * np.pi * freq * t)
    fade = np.linspace(1, 0, n)
    onda = (onda * fade * volume * 32767).astype(np.int16)
    stereo = np.column_stack([onda, onda])
    return pygame.sndarray.make_sound(stereo)


try:
    SOM_COMER = gerar_som(freq=600, duracao=0.10, volume=0.4, forma="square")
    SOM_MORTE = gerar_som(freq=150, duracao=0.35, volume=0.5, forma="triangle")
    SOM_NIVEL = gerar_som(freq=880, duracao=0.20, volume=0.4, forma="sine")
    SONS_OK = True
except Exception:
    SONS_OK = False


def tocar(som):
    if SONS_OK:
        try:
            som.play()
        except:
            pass


#  PARTÍCULAS
particulas = []

def adicionar_particulas(x, y, cor):
    for _ in range(10):
        angulo = random.uniform(0, 2*math.pi)
        vel = random.uniform(1, 4)
        particulas.append({
            "x": x + TAMANHO_BLOCO//2,
            "y": y + TAMANHO_BLOCO//2,
            "vx": math.cos(angulo)*vel,
            "vy": math.sin(angulo)*vel,
            "vida": 20,
            "cor": cor,
            "raio": random.randint(2, 5),
        })


def atualizar_particulas():
    mortas = []
    for p in particulas:
        p["x"] += p["vx"]
        p["y"] += p["vy"]
        p["vida"] -= 1
        p["vy"] += 0.15
        alpha = int(255 * p["vida"] / 20)
        r, g, b = p["cor"]
        pygame.draw.circle(superficie_jogo, (min(r, 255), min(g, 255), min(b, 255)),
                           (int(p["x"]), int(p["y"])), p["raio"])
        if p["vida"] <= 0:
            mortas.append(p)
    for p in mortas:
        particulas.remove(p)


#  ANIMAÇÕES CARTOON
anim_morte = {"ativo": False, "timer": 0, "x": 0, "y": 0, "angulo_estrela": 0}
anim_comer = {"ativo": False, "timer": 0, "x": 0, "y": 0, "escala": 1.0}

DURACAO_ANIM_MORTE = 90
DURACAO_ANIM_COMER = 40


def desenhar_estrelas_tontas(x, y, angulo, num_estrelas=5):
    raio = TAMANHO_BLOCO * 1.8
    cx = x + TAMANHO_BLOCO // 2
    cy = y + TAMANHO_BLOCO // 2
    for i in range(num_estrelas):
        a = math.radians(angulo + i * (360 / num_estrelas))
        sx = int(cx + math.cos(a) * raio)
        sy = int(cy + math.sin(a) * raio)
        for j in range(5):
            a1 = math.radians(j * 72 - 90)
            a2 = math.radians(j * 72 + 36 - 90)
            p1 = (sx + int(math.cos(a1)*5), sy + int(math.sin(a1)*5))
            p2 = (sx + int(math.cos(a2)*2), sy + int(math.sin(a2)*2))
            p3 = (sx + int(math.cos(math.radians(j*72+72-90))*5),
                  sy + int(math.sin(math.radians(j*72+72-90))*5))
            pygame.draw.polygon(superficie_jogo, (255, 230, 0), [p1, p2, p3])
        pygame.draw.circle(superficie_jogo, (255, 200, 0), (sx, sy), 2)


def desenhar_olhos_tontos(x, y):
    cx = x + TAMANHO_BLOCO // 2
    cy = y + TAMANHO_BLOCO // 2
    for ox, oy in [(-4, -3), (4, -3)]:
        ex, ey = cx + ox, cy + oy
        pygame.draw.circle(superficie_jogo, (255, 255, 255), (ex, ey), 4)
        pygame.draw.circle(superficie_jogo, (0, 0, 0), (ex, ey), 4, 1)
        pygame.draw.circle(superficie_jogo, (0, 0, 0), (ex + 1, ey), 2, 1)
        pygame.draw.circle(superficie_jogo, (0, 0, 0), (ex - 1, ey), 2, 1)


def desenhar_anim_comer(x, y, timer):
    progresso = timer / DURACAO_ANIM_COMER
    alpha = int(255 * min(1.0, progresso * 4) * max(0, 1 - (progresso - 0.5) * 2))
    fy = y - int(30 * (1 - progresso))
    escala = 1.0 + 0.5 * math.sin(progresso * math.pi)

    textos = ["NOM!", "😋", "+1"]
    txt_str = textos[min(int(timer / 15), 2)]
    txt_surf = fonte_media.render(txt_str, True, (255, 220, 50))
    w = int(txt_surf.get_width() * escala)
    h = int(txt_surf.get_height() * escala)
    if w > 0 and h > 0:
        txt_surf = pygame.transform.scale(txt_surf, (w, h))
        txt_surf.set_alpha(max(0, alpha))
        cx = x + TAMANHO_BLOCO // 2
        superficie_jogo.blit(txt_surf, txt_surf.get_rect(center=(cx, fy)))

    num_raios = 8
    for i in range(num_raios):
        a = math.radians(i * (360 / num_raios) + timer * 8)
        r1 = TAMANHO_BLOCO
        r2 = TAMANHO_BLOCO + int(8 * escala)
        cx2 = x + TAMANHO_BLOCO // 2
        cy2 = y + TAMANHO_BLOCO // 2
        px1 = int(cx2 + math.cos(a) * r1)
        py1 = int(cy2 + math.sin(a) * r1)
        px2 = int(cx2 + math.cos(a) * r2)
        py2 = int(cy2 + math.sin(a) * r2)
        pygame.draw.line(superficie_jogo, (255, 220, 50), (px1, py1), (px2, py2), 2)

#  RECORDES
recordes = {d: 0 for d in DIFICULDADES}

#  FUNÇÕES AUXILIARES DE DESENHO
def desenhar_grade(tema):
    for x in range(AREA_X1, AREA_X2, TAMANHO_BLOCO):
        pygame.draw.line(
            superficie_jogo, tema["grade"], (x, AREA_Y1), (x, AREA_Y2))
    for y in range(AREA_Y1, AREA_Y2, TAMANHO_BLOCO):
        pygame.draw.line(
            superficie_jogo, tema["grade"], (AREA_X1, y), (AREA_X2, y))


def desenhar_paredes(tema):
    EP = ESPESSURA_PAREDE
    pygame.draw.rect(superficie_jogo, tema["parede"], (0, 0, LARGURA, EP))
    pygame.draw.rect(
        superficie_jogo, tema["parede"], (0, ALTURA-EP, LARGURA, EP))
    pygame.draw.rect(superficie_jogo, tema["parede"], (0, 0, EP, ALTURA))
    pygame.draw.rect(
        superficie_jogo, tema["parede"], (LARGURA-EP, 0, EP, ALTURA))
    pygame.draw.rect(
        superficie_jogo, tema["parede_brilho"], (0, 0, LARGURA, EP), 2)
    pygame.draw.rect(
        superficie_jogo, tema["parede_brilho"], (0, ALTURA-EP, LARGURA, EP), 2)
    pygame.draw.rect(
        superficie_jogo, tema["parede_brilho"], (0, 0, EP, ALTURA), 2)
    pygame.draw.rect(
        superficie_jogo, tema["parede_brilho"], (LARGURA-EP, 0, EP, ALTURA), 2)


def desenhar_obstaculos(obstaculos, tema):
    for ox, oy in obstaculos:
        pygame.draw.rect(
            superficie_jogo, tema["parede"], (ox, oy, TAMANHO_BLOCO, TAMANHO_BLOCO), border_radius=3)
        pygame.draw.rect(superficie_jogo, tema["parede_brilho"], (
            ox, oy, TAMANHO_BLOCO, TAMANHO_BLOCO), 2, border_radius=3)


def desenhar_segmento(x, y, tema):
    cx = x + TAMANHO_BLOCO // 2
    cy = y + TAMANHO_BLOCO // 2
    r = TAMANHO_BLOCO // 2
    pygame.draw.circle(superficie_jogo, tema["cobra_sombra"], (cx, cy), r)
    pygame.draw.circle(superficie_jogo, tema["cobra"],        (cx, cy), r-2)
    pygame.draw.circle(
        superficie_jogo, tema["cobra_brilho"], (cx-2, cy-2), max(2, r//3))


def desenhar_cobra(lista_cobra, direcao, img_cabeca, tema):
    for bloco in lista_cobra[:-1]:
        desenhar_segmento(bloco[0], bloco[1], tema)
    if lista_cobra:
        cab = lista_cobra[-1]
        angulos = {"direita": 0, "esquerda": 180, "cima": 270, "baixo": 90}
        img_rot = pygame.transform.rotate(img_cabeca, angulos.get(direcao, 0))
        superficie_jogo.blit(img_rot, [cab[0], cab[1]])


def texto_centro(msg, cor, y, fonte=None):
    f = fonte or fonte_media
    s = f.render(msg, True, cor)
    r = s.get_rect(center=(LARGURA//2, y))
    superficie_jogo.blit(s, r)

# --- FUNÇÃO DE REDIMENSIONAMENTO PROPORCIONAL ---
def calcular_escala_e_posicao(tamanho_tela_real, tamanho_superficie):
    escala_x = tamanho_tela_real[0] / tamanho_superficie[0]
    escala_y = tamanho_tela_real[1] / tamanho_superficie[1]
    escala = min(escala_x, escala_y)

    novo_w = int(tamanho_superficie[0] * escala)
    novo_h = int(tamanho_superficie[1] * escala)

    offset_x = (tamanho_tela_real[0] - novo_w) // 2
    offset_y = (tamanho_tela_real[1] - novo_h) // 2

    return escala, (novo_w, novo_h), (offset_x, offset_y)


def mapear_mouse(pos_mouse_real):
    escala, novo_tamanho, offset = calcular_escala_e_posicao(
        tela.get_size(), superficie_jogo.get_size())

    x_sem_offset = pos_mouse_real[0] - offset[0]
    y_sem_offset = pos_mouse_real[1] - offset[1]

    virtual_x = int(x_sem_offset / escala)
    virtual_y = int(y_sem_offset / escala)

    return virtual_x, virtual_y


def renderizar_na_tela_real():
    tela.fill((0, 0, 0))
    escala, novo_tamanho, offset = calcular_escala_e_posicao(
        tela.get_size(), superficie_jogo.get_size())

    tela_escalada = pygame.transform.scale(superficie_jogo, novo_tamanho)
    tela.blit(tela_escalada, offset)
    pygame.display.flip()

#  TELA GAME OVER ESTILO GTA
def tela_game_over(superficie_jogo, tema, dificuldade_nome, pontuacao, novo_recorde):
    global tela

    fonte_gta_grande = pygame.font.SysFont("impact", 64)
    fonte_gta_media  = pygame.font.SysFont("impact", 28)
    fonte_gta_small  = pygame.font.SysFont("bahnschrift", 18)

    snapshot = superficie_jogo.copy()

    opcoes = ["[ C ]  TENTAR DE NOVO", "[ M ]  MENU PRINCIPAL", "[ S ]  SAIR"]
    opcao_sel = 0

    tick = 0
    FADE_DURACAO = 80

    while True:
        tick += 1
        progresso_fade = min(1.0, tick / FADE_DURACAO)

        superficie_jogo.blit(snapshot, (0, 0))

        escuro = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
        alpha_escuro = int(180 * progresso_fade)
        escuro.fill((0, 0, 0, alpha_escuro))
        superficie_jogo.blit(escuro, (0, 0))

        faixa_h = int(90 * progresso_fade)
        if faixa_h > 0:
            pygame.draw.rect(superficie_jogo, (180, 0, 0),
                             (0, 0, LARGURA, faixa_h))
            pygame.draw.rect(superficie_jogo, (220, 20, 20),
                             (0, faixa_h - 3, LARGURA, 3))

        base_h = int(50 * progresso_fade)
        if base_h > 0:
            pygame.draw.rect(superficie_jogo, (10, 10, 10),
                             (0, ALTURA - base_h, LARGURA, base_h))

        # --- AJUSTE NAS POSIÇÕES Y ---
        if progresso_fade > 0.4:
            alpha_txt = int(255 * min(1.0, (progresso_fade - 0.4) / 0.6))

            titulo_shadow = fonte_gta_grande.render(
                "VOCÊ MORREU", True, (80, 0, 0))
            titulo_shadow.set_alpha(alpha_txt)
            r_sh = titulo_shadow.get_rect(
                center=(LARGURA//2 + 4, ALTURA//2 - 90 + 4))
            superficie_jogo.blit(titulo_shadow, r_sh)

            titulo_surf = fonte_gta_grande.render(
                "VOCÊ MORREU", True, (255, 255, 255))
            titulo_surf.set_alpha(alpha_txt)
            r_t = titulo_surf.get_rect(center=(LARGURA//2, ALTURA//2 - 90))
            superficie_jogo.blit(titulo_surf, r_t)

            sep_w = int((LARGURA - 100) *
                        min(1.0, (progresso_fade - 0.5) / 0.5))
            if sep_w > 0:
                pygame.draw.rect(superficie_jogo, (200, 0, 0),
                                 (50, ALTURA//2 - 45, sep_w, 3))

        if progresso_fade > 0.6:
            alpha_info = int(255 * min(1.0, (progresso_fade - 0.6) / 0.4))

            # Ajustado para ALTURA//2 - 10
            pts_surf = fonte_gta_media.render(
                f"PONTUAÇÃO:  {pontuacao}", True, (220, 220, 220))
            pts_surf.set_alpha(alpha_info)
            superficie_jogo.blit(pts_surf, pts_surf.get_rect(
                center=(LARGURA//2, ALTURA//2 - 10)))

            rec_cor = (255, 200, 0) if novo_recorde else (160, 160, 160)
            rec_txt = "★  NOVO RECORDE!  ★" if novo_recorde else f"RECORDE:  {recordes[dificuldade_nome]}"
            rec_surf = fonte_gta_media.render(rec_txt, True, rec_cor)
            rec_surf.set_alpha(alpha_info)
            superficie_jogo.blit(rec_surf, rec_surf.get_rect(
                center=(LARGURA//2, ALTURA//2 + 30)))

        if progresso_fade >= 1.0:
            pulse = abs(math.sin(tick * 0.06))
            for i, op in enumerate(opcoes):
                # Ajustado para iniciar em ALTURA//2 + 80
                cy_op = ALTURA//2 + 80 + i * 32
                sel = (i == opcao_sel)
                cor_txt = (255, int(220 * pulse),
                           0) if sel else (180, 180, 180)
                prefix = "▶ " if sel else "   "
                op_surf = fonte_gta_small.render(prefix + op, True, cor_txt)
                superficie_jogo.blit(op_surf, op_surf.get_rect(
                    center=(LARGURA//2, cy_op)))

        renderizar_na_tela_real()
        relogio.tick(60)

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.VIDEORESIZE:
                tela = pygame.display.set_mode((ev.w, ev.h), pygame.RESIZABLE)
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_UP:
                    opcao_sel = (opcao_sel - 1) % len(opcoes)
                elif ev.key == pygame.K_DOWN:
                    opcao_sel = (opcao_sel + 1) % len(opcoes)
                elif ev.key in (pygame.K_RETURN, pygame.K_SPACE) and progresso_fade >= 1.0:
                    return ["continuar", "menu", "sair"][opcao_sel]
                elif ev.key == pygame.K_c:
                    return "continuar"
                elif ev.key == pygame.K_m:
                    return "menu"
                elif ev.key == pygame.K_s:
                    pygame.quit()
                    sys.exit()

#  MENU PRINCIPAL ANIMADO
def menu_principal():
    global tela
    tema_idx = 0
    personagem_idx = 0
    dificuldade_idx = 1
    nomes_temas = list(TEMAS.keys())
    nomes_dif = list(DIFICULDADES.keys())
    tick = 0

    deco_cobra = [[LARGURA//2 + i*TAMANHO_BLOCO,
                   AREA_Y1 + TAMANHO_BLOCO] for i in range(8)]
    deco_dir = "esquerda"
    deco_dx, deco_dy = -TAMANHO_BLOCO, 0
    deco_tick = 0
    deco_comprimento = 12

    particulas_menu = []

    def spawn_particula_menu(tema):
        particulas_menu.append({
            "x": random.randint(AREA_X1, AREA_X2),
            "y": random.randint(AREA_Y1, AREA_Y2),
            "vx": random.uniform(-0.4, 0.4),
            "vy": random.uniform(-0.6, -0.2),
            "vida": random.randint(60, 120),
            "vida_max": 120,
            "raio": random.randint(2, 4),
            "cor": tema["cobra_brilho"],
        })

    estrelas = [(random.randint(AREA_X1, AREA_X2), random.randint(AREA_Y1, AREA_Y2),
                 random.randint(1, 3)) for _ in range(40)]

    fade_entrada = 255

    while True:
        tick += 1
        tema_nome = nomes_temas[tema_idx]
        tema = TEMAS[tema_nome]

        superficie_jogo.fill(tema["fundo"])

        grade_surf = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
        for gx in range(AREA_X1, AREA_X2, TAMANHO_BLOCO):
            pygame.draw.line(
                grade_surf, (*tema["grade"], 80), (gx, AREA_Y1), (gx, AREA_Y2))
        for gy in range(AREA_Y1, AREA_Y2, TAMANHO_BLOCO):
            pygame.draw.line(
                grade_surf, (*tema["grade"], 80), (AREA_X1, gy), (AREA_X2, gy))
        superficie_jogo.blit(grade_surf, (0, 0))

        for (ex, ey, er) in estrelas:
            brilho = int(120 + 80 * math.sin(tick * 0.03 + ex * 0.1))
            pygame.draw.circle(
                superficie_jogo, (brilho, brilho, brilho), (ex, ey), er)

        if tick % 6 == 0:
            spawn_particula_menu(tema)
        mortas_m = []
        for pm in particulas_menu:
            pm["x"] += pm["vx"]
            pm["y"] += pm["vy"]
            pm["vida"] -= 1
            if pm["vida"] <= 0:
                mortas_m.append(pm)
                continue
            a = int(200 * pm["vida"] / pm["vida_max"])
            r, g, b = pm["cor"]
            s_p = pygame.Surface((pm["raio"]*2, pm["raio"]*2), pygame.SRCALPHA)
            pygame.draw.circle(s_p, (r, g, b, a),
                               (pm["raio"], pm["raio"]), pm["raio"])
            superficie_jogo.blit(
                s_p, (int(pm["x"]) - pm["raio"], int(pm["y"]) - pm["raio"]))
        for pm in mortas_m:
            particulas_menu.remove(pm)

        deco_tick += 1
        if deco_tick % 8 == 0:
            nx = deco_cobra[-1][0] + deco_dx
            ny = deco_cobra[-1][1] + deco_dy
            margem = TAMANHO_BLOCO * 2
            if nx < AREA_X1 + margem:
                deco_dy = TAMANHO_BLOCO if deco_dy >= 0 else -TAMANHO_BLOCO
                deco_dx = TAMANHO_BLOCO
                deco_dy = 0
                deco_dir = "direita"
            elif nx >= AREA_X2 - margem:
                deco_dx = -TAMANHO_BLOCO
                deco_dy = 0
                deco_dir = "esquerda"
            if ny < AREA_Y1 + margem:
                deco_dx = 0
                deco_dy = TAMANHO_BLOCO
                deco_dir = "baixo"
            elif ny >= AREA_Y2 - margem:
                deco_dx = 0
                deco_dy = -TAMANHO_BLOCO
                deco_dir = "cima"
            nx = max(AREA_X1, min(nx, AREA_X2 - TAMANHO_BLOCO))
            ny = max(AREA_Y1, min(ny, AREA_Y2 - TAMANHO_BLOCO))
            deco_cobra.append([nx, ny])
            if len(deco_cobra) > deco_comprimento:
                deco_cobra.pop(0)

        for idx_b, bloco in enumerate(deco_cobra[:-1]):
            alpha_b = int(60 + 60 * idx_b / len(deco_cobra))
            r, g, b = tema["cobra"]
            s_b = pygame.Surface(
                (TAMANHO_BLOCO, TAMANHO_BLOCO), pygame.SRCALPHA)
            cx_b = TAMANHO_BLOCO//2
            cy_b = TAMANHO_BLOCO//2
            pygame.draw.circle(s_b, (r, g, b, alpha_b),
                               (cx_b, cy_b), TAMANHO_BLOCO//2 - 1)
            superficie_jogo.blit(s_b, bloco)

        if deco_cobra:
            img_deco = criar_cabeca(
                "Cobra", tema["cobra"], tema["cobra_sombra"])
            angulos_d = {"direita": 0, "esquerda": 180,
                         "cima": 270, "baixo": 90}
            img_deco_r = pygame.transform.rotate(
                img_deco, angulos_d.get(deco_dir, 0))
            deco_s = pygame.Surface(
                (TAMANHO_BLOCO, TAMANHO_BLOCO), pygame.SRCALPHA)
            deco_s.blit(img_deco_r, (0, 0))
            deco_s.set_alpha(100)
            superficie_jogo.blit(deco_s, deco_cobra[-1])

        painel = pygame.Surface((480, 350), pygame.SRCALPHA)
        painel.fill((0, 0, 0, 140))
        superficie_jogo.blit(painel, (LARGURA//2 - 240, 95))
        pygame.draw.rect(superficie_jogo, (*tema["cobra"], 180),
                         (LARGURA//2 - 240, 95, 480, 350), 2, border_radius=6)

        pulso = 1.0 + 0.025 * math.sin(tick * 0.07)
        t_sh = fonte_titulo.render("COBRINHA", True, (0, 0, 0))
        w_sh = int(t_sh.get_width() * pulso)
        h_sh = int(t_sh.get_height() * pulso)
        t_sh = pygame.transform.scale(t_sh, (w_sh, h_sh))
        superficie_jogo.blit(t_sh, t_sh.get_rect(
            center=(LARGURA//2 + 3, 58 + 3)))

        hue_r = int(180 + 75 * math.sin(tick * 0.04))
        hue_g = int(220 + 35 * math.sin(tick * 0.04 + 1))
        t_main = fonte_titulo.render("COBRINHA", True, (hue_r, hue_g, 60))
        w_m = int(t_main.get_width() * pulso)
        h_m = int(t_main.get_height() * pulso)
        t_main = pygame.transform.scale(t_main, (w_m, h_m))
        superficie_jogo.blit(t_main, t_main.get_rect(center=(LARGURA//2, 58)))

        wave = int(3 * math.sin(tick * 0.1))
        sub = fonte_pequena.render(
            "🐍  SUPREME EDITION  🐍", True, (200, 200, 200))
        superficie_jogo.blit(sub, sub.get_rect(center=(LARGURA//2, 95 + wave)))

        lbl_p = fonte_pequena.render("▸ PERSONAGEM", True, tema["pontos"])
        superficie_jogo.blit(lbl_p, (LARGURA//2 - 230, 112))
        for i, p in enumerate(PERSONAGENS):
            col = i % 2
            row = i // 2
            rx = 160 + col*180
            ry = 125 + row*38
            rect = pygame.Rect(rx, ry, 158, 32)
            sel = (i == personagem_idx)
            brilho_btn = int(40 * abs(math.sin(tick*0.06))) if sel else 0
            cor_f = tuple(min(255, c + brilho_btn)
                          for c in tema["cobra"]) if sel else (40, 40, 40)
            pygame.draw.rect(superficie_jogo, cor_f, rect, border_radius=6)
            pygame.draw.rect(superficie_jogo, tema["cobra"] if sel else (
                80, 80, 80), rect, 2, border_radius=6)
            txt_c = (0, 0, 0) if sel and tema_nome == "Gelo" else (
                255, 255, 255)
            s_p2 = fonte_media.render(("✓ " if sel else "  ") + p, True, txt_c)
            superficie_jogo.blit(s_p2, s_p2.get_rect(center=rect.center))

        pygame.draw.line(superficie_jogo, (*tema["cobra"], 120),
                         (LARGURA//2 - 220, 203), (LARGURA//2 + 220, 203), 1)

        lbl_t = fonte_pequena.render("▸ TEMA VISUAL", True, tema["pontos"])
        superficie_jogo.blit(lbl_t, (LARGURA//2 - 230, 210))
        for i, tn in enumerate(nomes_temas):
            col = i % 2
            row = i // 2
            rx = 160 + col*180
            ry = 222 + row*38
            rect = pygame.Rect(rx, ry, 158, 32)
            sel = (i == tema_idx)
            brilho_btn = int(40 * abs(math.sin(tick*0.06))) if sel else 0
            cor_f = tuple(min(255, c + brilho_btn)
                          for c in tema["cobra"]) if sel else (40, 40, 40)
            pygame.draw.rect(superficie_jogo, cor_f, rect, border_radius=6)
            pygame.draw.rect(superficie_jogo, tema["cobra"] if sel else (
                80, 80, 80), rect, 2, border_radius=6)
            txt_c = (0, 0, 0) if sel and tema_nome == "Gelo" else (
                255, 255, 255)
            s_t2 = fonte_media.render(
                ("✓ " if sel else "  ") + tn, True, txt_c)
            superficie_jogo.blit(s_t2, s_t2.get_rect(center=rect.center))

        pygame.draw.line(superficie_jogo, (*tema["cobra"], 120),
                         (LARGURA//2 - 220, 300), (LARGURA//2 + 220, 300), 1)

        lbl_d = fonte_pequena.render("▸ DIFICULDADE", True, tema["pontos"])
        superficie_jogo.blit(lbl_d, (LARGURA//2 - 230, 307))
        for i, d in enumerate(nomes_dif):
            rx = 48 + i * 138
            ry = 320
            rect = pygame.Rect(rx, ry, 128, 32)
            sel = (i == dificuldade_idx)
            brilho_btn = int(40 * abs(math.sin(tick*0.06))) if sel else 0
            cor_f = tuple(min(255, c + brilho_btn)
                          for c in tema["cobra"]) if sel else (40, 40, 40)
            pygame.draw.rect(superficie_jogo, cor_f, rect, border_radius=6)
            pygame.draw.rect(superficie_jogo, tema["cobra"] if sel else (
                80, 80, 80), rect, 2, border_radius=6)
            txt_c = (0, 0, 0) if sel and tema_nome == "Gelo" else (
                255, 255, 255)
            s_d2 = fonte_media.render(("✓ " if sel else "  ") + d, True, txt_c)
            superficie_jogo.blit(s_d2, s_d2.get_rect(center=rect.center))

        dif_nome = nomes_dif[dificuldade_idx]
        rec = recordes[dif_nome]
        rec_surf = fonte_pequena.render(
            f"🏆  Recorde em {dif_nome}:  {rec}", True, (255, 215, 0))
        superficie_jogo.blit(
            rec_surf, rec_surf.get_rect(center=(LARGURA//2, 364)))

        pulso_btn = 0.92 + 0.08 * abs(math.sin(tick * 0.09))
        btn_w = int(240 * pulso_btn)
        btn_h = int(36 * pulso_btn)
        btn_cor = (
            int(60 + 100 * abs(math.sin(tick * 0.07))),
            int(180 + 60 * abs(math.sin(tick * 0.07))),
            50
        )
        btn_rect = pygame.Rect(0, 0, btn_w, btn_h)
        btn_rect.center = (LARGURA//2, 400)
        pygame.draw.rect(superficie_jogo, btn_cor, btn_rect, border_radius=10)
        pygame.draw.rect(superficie_jogo, (255, 255, 255),
                         btn_rect, 2, border_radius=10)
        btn_txt = fonte_grande.render("▶  JOGAR", True, (0, 0, 0))
        superficie_jogo.blit(btn_txt, btn_txt.get_rect(center=btn_rect.center))

        tecla_txt = fonte_pequena.render(
            "ENTER ou clique para jogar  |  ESC para sair", True, (130, 130, 130))
        superficie_jogo.blit(
            tecla_txt, tecla_txt.get_rect(center=(LARGURA//2, 430)))

        desenhar_paredes(TEMAS[tema_nome])

        if fade_entrada > 0:
            fade_surf = pygame.Surface((LARGURA, ALTURA))
            fade_surf.fill((0, 0, 0))
            fade_surf.set_alpha(fade_entrada)
            superficie_jogo.blit(fade_surf, (0, 0))
            fade_entrada = max(0, fade_entrada - 6)

        renderizar_na_tela_real()
        relogio.tick(60)

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.VIDEORESIZE:
                tela = pygame.display.set_mode((ev.w, ev.h), pygame.RESIZABLE)
            if ev.type == pygame.KEYDOWN:
                if ev.key in (pygame.K_RETURN, pygame.K_SPACE):
                    return (nomes_temas[tema_idx], PERSONAGENS[personagem_idx], nomes_dif[dificuldade_idx])
                if ev.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                mx, my = mapear_mouse(ev.pos)

                for i, p in enumerate(PERSONAGENS):
                    col = i % 2
                    row = i//2
                    if pygame.Rect(160+col*180, 125+row*38, 158, 32).collidepoint(mx, my):
                        personagem_idx = i
                for i, tn in enumerate(nomes_temas):
                    col = i % 2
                    row = i//2
                    if pygame.Rect(160+col*180, 222+row*38, 158, 32).collidepoint(mx, my):
                        tema_idx = i
                for i in range(len(nomes_dif)):
                    if pygame.Rect(48+i*138, 320, 128, 32).collidepoint(mx, my):
                        dificuldade_idx = i
                if btn_rect.collidepoint(mx, my):
                    return (nomes_temas[tema_idx], PERSONAGENS[personagem_idx], nomes_dif[dificuldade_idx])

#  LOOP DO JOGO
def gerar_obstaculos(n, lista_cobra, comida_x, comida_y):
    cols = AREA_LARGURA // TAMANHO_BLOCO
    rows = AREA_ALTURA // TAMANHO_BLOCO
    obs = []
    tentativas = 0
    while len(obs) < n and tentativas < 500:
        tentativas += 1
        ox = random.randint(0, cols-1)*TAMANHO_BLOCO + AREA_X1
        oy = random.randint(0, rows-1)*TAMANHO_BLOCO + AREA_Y1
        if [ox, oy] in lista_cobra:
            continue
        if ox == comida_x and oy == comida_y:
            continue
        if abs(ox - lista_cobra[-1][0]) < TAMANHO_BLOCO*4 and \
           abs(oy - lista_cobra[-1][1]) < TAMANHO_BLOCO*4:
            continue
        obs.append((ox, oy))
    return obs


def loop_jogo(tema_nome, personagem, dificuldade_nome):
    global recordes, tela
    tema = TEMAS[tema_nome]
    cfg = DIFICULDADES[dificuldade_nome]
    velocidade = cfg["velocidade"]
    n_obs = cfg["obstaculos"]

    img_cabeca = criar_cabeca(personagem, tema["cobra"], tema["cobra_sombra"])
    img_comida = criar_comida()

    x = AREA_X1 + (AREA_LARGURA//2 // TAMANHO_BLOCO) * TAMANHO_BLOCO
    y = AREA_Y1 + (AREA_ALTURA // 2 // TAMANHO_BLOCO) * TAMANHO_BLOCO

    x_mudanca = 0
    y_mudanca = 0
    direcao = "direita"
    ultima_direcao = "direita"
    lista_cobra = [[x, y]]
    comprimento = 1

    def nova_comida():
        cols = AREA_LARGURA // TAMANHO_BLOCO
        rows = AREA_ALTURA // TAMANHO_BLOCO
        while True:
            cx = random.randint(0, cols-1)*TAMANHO_BLOCO + AREA_X1
            cy = random.randint(0, rows-1)*TAMANHO_BLOCO + AREA_Y1
            if [cx, cy] not in lista_cobra:
                return cx, cy

    comida_x, comida_y = nova_comida()
    obstaculos = gerar_obstaculos(n_obs, lista_cobra, comida_x, comida_y)

    particulas.clear()
    anim_comer["ativo"] = False
    anim_comer["timer"] = 0
    fim = False
    morreu = False

    while not fim:

        if morreu:
            pontuacao = comprimento - 1
            novo_recorde = pontuacao > recordes[dificuldade_nome]
            if novo_recorde:
                recordes[dificuldade_nome] = pontuacao

            acao = tela_game_over(superficie_jogo, tema,
                                  dificuldade_nome, pontuacao, novo_recorde)
            if acao == "continuar":
                loop_jogo(tema_nome, personagem, dificuldade_nome)
                return
            else:
                fim = True
            continue

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.VIDEORESIZE:
                tela = pygame.display.set_mode((ev.w, ev.h), pygame.RESIZABLE)

            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_LEFT and ultima_direcao != "direita":
                    x_mudanca = -TAMANHO_BLOCO
                    y_mudanca = 0
                    direcao = "esquerda"
                elif ev.key == pygame.K_RIGHT and ultima_direcao != "esquerda":
                    x_mudanca = TAMANHO_BLOCO
                    y_mudanca = 0
                    direcao = "direita"
                elif ev.key == pygame.K_UP and ultima_direcao != "baixo":
                    y_mudanca = -TAMANHO_BLOCO
                    x_mudanca = 0
                    direcao = "cima"
                elif ev.key == pygame.K_DOWN and ultima_direcao != "cima":
                    y_mudanca = TAMANHO_BLOCO
                    x_mudanca = 0
                    direcao = "baixo"
                elif ev.key == pygame.K_ESCAPE:
                    fim = True
                elif ev.key == pygame.K_a and ultima_direcao != "direita":
                    x_mudanca = -TAMANHO_BLOCO
                    y_mudanca = 0
                    direcao = "esquerda"
                elif ev.key == pygame.K_d and ultima_direcao != "esquerda":
                    x_mudanca = TAMANHO_BLOCO
                    y_mudanca = 0
                    direcao = "direita"
                elif ev.key == pygame.K_w and ultima_direcao != "baixo":
                    y_mudanca = -TAMANHO_BLOCO
                    x_mudanca = 0
                    direcao = "cima"
                elif ev.key == pygame.K_s and ultima_direcao != "cima":
                    y_mudanca = TAMANHO_BLOCO
                    x_mudanca = 0
                    direcao = "baixo"

        x += x_mudanca
        y += y_mudanca

        ultima_direcao = direcao

        bateu = False
        if x < AREA_X1 or x >= AREA_X2 or y < AREA_Y1 or y >= AREA_Y2:
            x = max(AREA_X1, min(x, AREA_X2 - TAMANHO_BLOCO))
            y = max(AREA_Y1, min(y, AREA_Y2 - TAMANHO_BLOCO))
            bateu = True

        cabeca = [x, y]
        lista_cobra.append(cabeca)
        if len(lista_cobra) > comprimento:
            del lista_cobra[0]

        if (x, y) in obstaculos:
            bateu = True

        if cabeca in lista_cobra[:-1]:
            bateu = True

        if bateu:
            tocar(SOM_MORTE)
            angulo_estrela = 0
            for t in range(1, DURACAO_ANIM_MORTE + 1):
                for ev in pygame.event.get():
                    if ev.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if ev.type == pygame.VIDEORESIZE:
                        tela = pygame.display.set_mode(
                            (ev.w, ev.h), pygame.RESIZABLE)

                angulo_estrela += 8
                tremor_x = x + int(math.sin(t * 1.5) * 5)
                tremor_y = y + int(math.cos(t * 2.1) * 4)

                superficie_jogo.fill(tema["fundo"])
                desenhar_grade(tema)
                desenhar_paredes(tema)
                desenhar_obstaculos(obstaculos, tema)
                superficie_jogo.blit(img_comida, [comida_x, comida_y])
                desenhar_cobra(lista_cobra, direcao, img_cabeca, tema)

                angulos = {"direita": 0, "esquerda": 180,
                           "cima": 270, "baixo": 90}
                img_rot = pygame.transform.rotate(
                    img_cabeca, angulos.get(direcao, 0))
                superficie_jogo.blit(img_rot, [tremor_x, tremor_y])
                desenhar_olhos_tontos(tremor_x, tremor_y)
                desenhar_estrelas_tontas(tremor_x, tremor_y, angulo_estrela)

                if t < 30:
                    txt = fonte_media.render("AU!!", True, (255, 80, 80))
                    superficie_jogo.blit(txt, txt.get_rect(
                        center=(tremor_x + TAMANHO_BLOCO//2, tremor_y - 22)))

                pontos_txt = fonte_media.render(
                    f"🍎 {comprimento-1}", True, tema["pontos"])
                superficie_jogo.blit(pontos_txt, (AREA_X1+5, AREA_Y1+4))
                dif_txt = fonte_pequena.render(
                    dificuldade_nome, True, (200, 200, 200))
                superficie_jogo.blit(
                    dif_txt, (LARGURA - dif_txt.get_width() - AREA_X1 - 5, AREA_Y1+5))

                renderizar_na_tela_real()
                relogio.tick(60)

            morreu = True
            continue

        superficie_jogo.fill(tema["fundo"])
        desenhar_grade(tema)
        desenhar_paredes(tema)
        desenhar_obstaculos(obstaculos, tema)
        superficie_jogo.blit(img_comida, [comida_x, comida_y])
        atualizar_particulas()
        desenhar_cobra(lista_cobra, direcao, img_cabeca, tema)

        if anim_comer["ativo"]:
            anim_comer["timer"] += 1
            desenhar_anim_comer(
                anim_comer["x"], anim_comer["y"], anim_comer["timer"])
            if anim_comer["timer"] >= DURACAO_ANIM_COMER:
                anim_comer["ativo"] = False

        pontos_txt = fonte_media.render(
            f"🍎 {comprimento-1}", True, tema["pontos"])
        superficie_jogo.blit(pontos_txt, (AREA_X1+5, AREA_Y1+4))
        dif_txt = fonte_pequena.render(dificuldade_nome, True, (200, 200, 200))
        superficie_jogo.blit(
            dif_txt, (LARGURA - dif_txt.get_width() - AREA_X1 - 5, AREA_Y1+5))

        renderizar_na_tela_real()

        if x == comida_x and y == comida_y:
            tocar(SOM_COMER)
            adicionar_particulas(comida_x, comida_y, (255, 80, 80))
            anim_comer["ativo"] = True
            anim_comer["timer"] = 0
            anim_comer["x"] = comida_x
            anim_comer["y"] = comida_y
            comprimento += 1
            comida_x, comida_y = nova_comida()
            if dificuldade_nome != "Fácil" and (comprimento-1) % 5 == 0 and comprimento > 1:
                tocar(SOM_NIVEL)
                novos = gerar_obstaculos(1, lista_cobra, comida_x, comida_y)
                obstaculos.extend(novos)

        relogio.tick(velocidade)


if __name__ == "__main__":
    while True:
        tema_nome, personagem, dificuldade = menu_principal()
        loop_jogo(tema_nome, personagem, dificuldade)
