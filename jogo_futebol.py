# jogo_futebol.py
import tkinter as tk
import math
import random
import time

class JogoFutebol:
    def __init__(self, janela, callback_voltar):
        self.janela = janela
        self.janela.title("Futebol - Arrasta e Chuta")
        self.janela.geometry("900x600")  # um pouco maior para a plateia
        self.janela.configure(bg="#1B5E20")
        self.janela.resizable(True, True)
        self.callback_voltar = callback_voltar
        self.fullscreen = False

        # Frame principal para centralizar o canvas
        self.frame_principal = tk.Frame(janela, bg="#1B5E20")
        self.frame_principal.pack(fill=tk.BOTH, expand=True)

        # Botões superiores
        self.frame_topo = tk.Frame(self.frame_principal, bg="#1B5E20")
        self.frame_topo.pack(pady=5)
        tk.Button(self.frame_topo, text="🔙 Voltar ao Menu", font=("Arial", 12),
                  bg="#FFC107", command=self.voltar).pack(side=tk.LEFT, padx=5)
        tk.Button(self.frame_topo, text="🖥️ Tela Cheia", font=("Arial", 12),
                  bg="#FF9800", command=self.toggle_fullscreen).pack(side=tk.LEFT, padx=5)

        # Canvas centralizado
        self.canvas = tk.Canvas(self.frame_principal, width=800, height=500, bg="#4CAF50", highlightthickness=0)
        self.canvas.pack(pady=10)

        # Dimensões do campo (fixas, relativas ao canvas de 800x500)
        self.LIMITE_ESQ = 40
        self.LIMITE_DIR = 760
        self.LIMITE_SUP = 40
        self.LIMITE_INF = 460

        self.bola = {
            "x": 400, "y": 250, "raio": 12,
            "vx": 0, "vy": 0,
            "arrastando": False,
            "drag_start_x": 0, "drag_start_y": 0
        }

        self.goleiro = {
            "x": 700, "y": 190,
            "largura": 20, "altura": 80,
            "vy": 2.0,
            "min_y": self.LIMITE_SUP,
            "max_y": self.LIMITE_INF - 80
        }

        self.gols_jogador = 0
        self.gols_inimigo = 0
        self.estado = "parado"
        self.mouse_x = 0
        self.mouse_y = 0

        # Confetes
        self.confetes = []

        self.canvas.bind("<ButtonPress-1>", self.on_mouse_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_move)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_release)

        # Atalho F11 para tela cheia
        self.janela.bind("<F11>", lambda e: self.toggle_fullscreen())

        self.atualizar()

    def voltar(self):
        self.janela.destroy()
        self.callback_voltar()

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        self.janela.attributes('-fullscreen', self.fullscreen)
        if not self.fullscreen:
            self.janela.geometry("900x600")

    def on_mouse_press(self, event):
        self.mouse_x, self.mouse_y = event.x, event.y
        if self.estado != "arrastando":
            dist = math.hypot(event.x - self.bola["x"], event.y - self.bola["y"])
            if dist <= self.bola["raio"] + 8:
                self.bola["arrastando"] = True
                self.estado = "arrastando"
                self.bola["vx"], self.bola["vy"] = 0, 0
                self.bola["drag_start_x"] = self.bola["x"]
                self.bola["drag_start_y"] = self.bola["y"]

    def on_mouse_move(self, event):
        self.mouse_x, self.mouse_y = event.x, event.y

    def on_mouse_release(self, event):
        if self.bola["arrastando"]:
            dx = self.bola["drag_start_x"] - self.mouse_x
            dy = self.bola["drag_start_y"] - self.mouse_y
            dist = math.hypot(dx, dy)
            if dist > 5:
                forca = dist * 0.12
                nx, ny = dx / dist, dy / dist
                self.bola["vx"] = nx * forca
                self.bola["vy"] = ny * forca
                self.estado = "movendo"
            else:
                self.estado = "parado"
            self.bola["arrastando"] = False

    def gol_jogador(self):
        self.gols_jogador += 1
        self.aumentar_velocidade_goleiro()
        if self.gols_jogador % 3 == 0:
            self.aumentar_tamanho_goleiro()
        self.criar_confetes("jogador")
        self.resetar_bola()

    def gol_inimigo(self):
        self.gols_inimigo += 1
        self.aumentar_velocidade_goleiro()
        self.criar_confetes("inimigo")
        self.resetar_bola()

    def criar_confetes(self, lado):
        # Cria uma explosão de confetes na lateral do gol
        if lado == "jogador":
            x_centro = self.LIMITE_DIR
        else:
            x_centro = self.LIMITE_ESQ
        for _ in range(50):
            self.confetes.append({
                "x": x_centro,
                "y": random.uniform(self.LIMITE_SUP, self.LIMITE_INF),
                "vx": random.uniform(-150, 150) * (1 if lado == "jogador" else -1),
                "vy": random.uniform(-200, -50),
                "cor": random.choice(["red", "yellow", "blue", "lime", "cyan", "magenta", "orange"]),
                "vida": random.uniform(0.8, 1.5)
            })

    def atualizar_confetes(self, delta_t):
        for confete in self.confetes:
            confete["vy"] += 300 * delta_t  # gravidade
            confete["x"] += confete["vx"] * delta_t
            confete["y"] += confete["vy"] * delta_t
            confete["vida"] -= delta_t
        self.confetes = [c for c in self.confetes if c["vida"] > 0]

    def mover_goleiro(self):
        self.goleiro["y"] += self.goleiro["vy"]
        if self.goleiro["y"] <= self.goleiro["min_y"] or self.goleiro["y"] >= self.goleiro["max_y"]:
            self.goleiro["vy"] *= -1
            self.goleiro["y"] = max(self.goleiro["min_y"], min(self.goleiro["max_y"], self.goleiro["y"]))

    def mover_bola(self):
        if self.estado != "movendo":
            return

        self.bola["vx"] *= 0.985
        self.bola["vy"] *= 0.985

        self.bola["x"] += self.bola["vx"]
        self.bola["y"] += self.bola["vy"]

        if abs(self.bola["vx"]) < 0.05 and abs(self.bola["vy"]) < 0.05:
            self.bola["vx"], self.bola["vy"] = 0, 0
            self.estado = "parado"

        if self.bola["y"] - self.bola["raio"] < self.LIMITE_SUP:
            self.bola["y"] = self.LIMITE_SUP + self.bola["raio"]
            self.bola["vy"] *= -1
        elif self.bola["y"] + self.bola["raio"] > self.LIMITE_INF:
            self.bola["y"] = self.LIMITE_INF - self.bola["raio"]
            self.bola["vy"] *= -1

        if self.bola["x"] - self.bola["raio"] < self.LIMITE_ESQ:
            self.gol_inimigo()
            return

        if self.bola["x"] + self.bola["raio"] > self.LIMITE_DIR:
            self.gol_jogador()
            return

        if self.colisao_bola_goleiro():
            self.bola["vx"] *= -1
            self.bola["vy"] += random.uniform(-1, 1)
            if self.bola["vx"] > 0:
                self.bola["x"] = self.goleiro["x"] + self.goleiro["largura"] + self.bola["raio"]
            else:
                self.bola["x"] = self.goleiro["x"] - self.bola["raio"]

    def colisao_bola_goleiro(self):
        rx, ry = self.goleiro["x"], self.goleiro["y"]
        rw, rh = self.goleiro["largura"], self.goleiro["altura"]
        cx, cy = self.bola["x"], self.bola["y"]
        px = max(rx, min(cx, rx + rw))
        py = max(ry, min(cy, ry + rh))
        dist = math.hypot(cx - px, cy - py)
        return dist <= self.bola["raio"]

    def resetar_bola(self):
        self.bola["x"], self.bola["y"] = 400, 250
        self.bola["vx"], self.bola["vy"] = 0, 0
        self.estado = "parado"

    def aumentar_velocidade_goleiro(self):
        self.goleiro["vy"] *= 1.15

    def aumentar_tamanho_goleiro(self):
        self.goleiro["altura"] += 10
        self.goleiro["largura"] += 5
        self.goleiro["max_y"] = self.LIMITE_INF - self.goleiro["altura"]

    def atualizar(self):
        self.mover_goleiro()
        self.mover_bola()
        self.atualizar_confetes(0.016)  # ~60 fps
        self.desenhar()
        self.janela.after(16, self.atualizar)

    def desenhar(self):
        self.canvas.delete("all")

        # Fundo do campo (gramado)
        self.canvas.create_rectangle(
            self.LIMITE_ESQ, self.LIMITE_SUP, self.LIMITE_DIR, self.LIMITE_INF,
            fill="#2E7D32", outline="white", width=3
        )

        # Linhas do campo
        self.canvas.create_line(400, self.LIMITE_SUP, 400, self.LIMITE_INF, fill="white", width=2)
        self.canvas.create_oval(350, 200, 450, 300, outline="white", width=3)
        # Área do goleiro (pequena área)
        self.canvas.create_rectangle(self.LIMITE_DIR-80, 170, self.LIMITE_DIR, 330, outline="white", width=2)
        self.canvas.create_rectangle(self.LIMITE_ESQ, 170, self.LIMITE_ESQ+80, 330, outline="white", width=2)
        # Traves (gols)
        self.canvas.create_line(self.LIMITE_DIR, 180, self.LIMITE_DIR, 320, fill="white", width=5)
        self.canvas.create_line(self.LIMITE_ESQ, 180, self.LIMITE_ESQ, 320, fill="white", width=5)

        # Plateia (torcida)
        self.desenhar_plateia()

        # Goleiro (desenho detalhado)
        self.desenhar_goleiro()

        # Bola
        self.desenhar_bola()

        # Linha de mira
        if self.bola["arrastando"]:
            sx, sy = self.bola["drag_start_x"], self.bola["drag_start_y"]
            self.canvas.create_line(sx, sy, self.mouse_x, self.mouse_y, fill="yellow", width=3, dash=(6,4))
            dx, dy = sx - self.mouse_x, sy - self.mouse_y
            ang = math.atan2(dy, dx)
            ponta_x = sx - 15*math.cos(ang)
            ponta_y = sy - 15*math.sin(ang)
            self.canvas.create_line(sx, sy, ponta_x, ponta_y, fill="yellow", width=4, arrow="last")

        # Confetes
        for confete in self.confetes:
            self.canvas.create_rectangle(confete["x"]-3, confete["y"]-3,
                                        confete["x"]+3, confete["y"]+3,
                                        fill=confete["cor"], outline="")

        # Placar
        self.canvas.create_text(400, 20, text=f"Você {self.gols_jogador} x {self.gols_inimigo} Inimigo",
                                font=("Comic Sans MS", 18, "bold"), fill="white")
        self.canvas.create_text(60, 20, text="Seu gol ➔", fill="white", font=("Arial", 10))
        self.canvas.create_text(740, 20, text="Gol deles", fill="white", font=("Arial", 10))

    def desenhar_plateia(self):
        # Desenha espectadores nas bordas superior e inferior
        cores_roupa = ["#E57373", "#64B5F6", "#81C784", "#FFB74D", "#BA68C8", "#4DD0E1"]
        for i in range(0, 800, 20):
            # Superior
            self.canvas.create_oval(i, 5, i+10, 15, fill=random.choice(cores_roupa), outline="black")
            self.canvas.create_oval(i+2, 2, i+8, 8, fill="#FFCC80")  # cabeça
            # Inferior
            self.canvas.create_oval(i, 465, i+10, 475, fill=random.choice(cores_roupa), outline="black")
            self.canvas.create_oval(i+2, 462, i+8, 468, fill="#FFCC80")

        # Laterais (esquerda e direita) com espaço reduzido, alguns espectadores
        for j in range(40, 460, 20):
            self.canvas.create_oval(5, j, 15, j+10, fill=random.choice(cores_roupa), outline="black")
            self.canvas.create_oval(2, j+2, 8, j+8, fill="#FFCC80")
            self.canvas.create_oval(785, j, 795, j+10, fill=random.choice(cores_roupa), outline="black")
            self.canvas.create_oval(792, j+2, 798, j+8, fill="#FFCC80")

    def desenhar_goleiro(self):
        gx, gy = self.goleiro["x"], self.goleiro["y"]
        gw, gh = self.goleiro["largura"], self.goleiro["altura"]
        centro_x = gx + gw/2
        # Corpo (camisa)
        self.canvas.create_rectangle(gx, gy+10, gx+gw, gy+gh, fill="#E53935", outline="black", width=2)
        # Cabeça
        self.canvas.create_oval(centro_x-10, gy-5, centro_x+10, gy+15, fill="#FFCC80", outline="black", width=2)
        # Cabelo
        self.canvas.create_arc(centro_x-10, gy-5, centro_x+10, gy+5, start=0, extent=180, fill="#5D4037")
        # Olhos
        self.canvas.create_oval(centro_x-5, gy+2, centro_x-2, gy+5, fill="white")
        self.canvas.create_oval(centro_x+2, gy+2, centro_x+5, gy+5, fill="white")
        self.canvas.create_oval(centro_x-4, gy+3, centro_x-3, gy+4, fill="black")
        self.canvas.create_oval(centro_x+3, gy+3, centro_x+4, gy+4, fill="black")
        # Luvas (braços esticados)
        self.canvas.create_rectangle(gx-8, gy+15, gx, gy+35, fill="#FFCC80", outline="black")
        self.canvas.create_rectangle(gx+gw, gy+15, gx+gw+8, gy+35, fill="#FFCC80", outline="black")
        # Chuteiras
        self.canvas.create_rectangle(gx+2, gy+gh-5, gx+8, gy+gh, fill="black")
        self.canvas.create_rectangle(gx+gw-8, gy+gh-5, gx+gw-2, gy+gh, fill="black")

    def desenhar_bola(self):
        bx, by, br = self.bola["x"], self.bola["y"], self.bola["raio"]
        # Círculo principal branco
        self.canvas.create_oval(bx-br, by-br, bx+br, by+br, fill="white", outline="black", width=2)
        # Pentágonos pretos (estilo futebol)
        # Desenho simplificado de gomos
        for ang in [0, 72, 144, 216, 288]:
            rad = math.radians(ang)
            px = bx + br*0.6*math.cos(rad)
            py = by + br*0.6*math.sin(rad)
            self.canvas.create_polygon(
                px, py,
                px+5, py-5,
                px+8, py,
                px+5, py+5,
                px, py+5,
                fill="black"
            )
        # Centro preto
        self.canvas.create_oval(bx-4, by-4, bx+4, by+4, fill="black")