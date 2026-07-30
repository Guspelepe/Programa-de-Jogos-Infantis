import tkinter as tk
import math
import random

class JogoFutebol:
    def __init__(self, janela, callback_voltar):
        self.janela = janela
        self.janela.title("⚽ Futebol - Arrasta e Chuta")
        self.janela.geometry("900x600")  
        self.janela.configure(bg="#2E7D32") # Verde estádio mais agradável
        self.janela.resizable(True, True)
        self.callback_voltar = callback_voltar
        self.fullscreen = False

        # Frame principal
        self.frame_principal = tk.Frame(janela, bg="#2E7D32")
        self.frame_principal.pack(fill=tk.BOTH, expand=True)

        # Botões superiores (Estilo Moderno)
        self.frame_topo = tk.Frame(self.frame_principal, bg="#2E7D32")
        self.frame_topo.pack(pady=10)
        
        btn_voltar = tk.Button(self.frame_topo, text="🔙 Voltar ao Menu", font=("Comic Sans MS", 12, "bold"),
                               bg="#FF5252", fg="white", activebackground="#FF1744", 
                               relief="flat", cursor="hand2", command=self.voltar)
        btn_voltar.pack(side=tk.LEFT, padx=10, ipadx=10, ipady=5)
        
        btn_tela = tk.Button(self.frame_topo, text="🖥️ Tela Cheia", font=("Comic Sans MS", 12, "bold"),
                             bg="#FFCA28", fg="#333333", activebackground="#FFB300", 
                             relief="flat", cursor="hand2", command=self.toggle_fullscreen)
        btn_tela.pack(side=tk.LEFT, padx=10, ipadx=10, ipady=5)

        # Canvas centralizado
        self.canvas = tk.Canvas(self.frame_principal, width=800, height=500, bg="#4CAF50", highlightthickness=0)
        self.canvas.pack(pady=5)

        # Dimensões do campo (fixas, relativas ao canvas de 800x500)
        self.LIMITE_ESQ = 50
        self.LIMITE_DIR = 750
        self.LIMITE_SUP = 50
        self.LIMITE_INF = 450

        self.bola = {
            "x": 400, "y": 250, "raio": 14,
            "vx": 0, "vy": 0,
            "arrastando": False,
            "drag_start_x": 0, "drag_start_y": 0
        }

        self.goleiro = {
            "x": 700, "y": 210,
            "largura": 25, "altura": 80,
            "vy": 2.5,
            "min_y": self.LIMITE_SUP,
            "max_y": self.LIMITE_INF - 80
        }

        self.gols_jogador = 0
        self.gols_inimigo = 0
        self.estado = "parado"
        self.mouse_x = 0
        self.mouse_y = 0

        self.confetes = []
        self.torcedores = [] # Lista para guardar as cores fixas da plateia

        self.canvas.bind("<ButtonPress-1>", self.on_mouse_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_move)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_release)

        # Atalho F11 para tela cheia
        self.janela.bind("<F11>", lambda e: self.toggle_fullscreen())

        self.gerar_plateia() # Sorteia as cores APENAS UMA VEZ
        self.atualizar()

    def voltar(self):
        self.janela.destroy()
        self.callback_voltar()

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        self.janela.attributes('-fullscreen', self.fullscreen)
        if not self.fullscreen:
            self.janela.geometry("900x600")

    def gerar_plateia(self):
        """ Cria a plateia com cores sorteadas que não vão mais piscar """
        cores_roupa = ["#E57373", "#64B5F6", "#81C784", "#FFB74D", "#BA68C8", "#4DD0E1", "#FFF176"]
        
        # Superior e Inferior
        for i in range(0, 800, 20):
            self.torcedores.append({"x": i, "y": 5, "cor": random.choice(cores_roupa), "tipo": "sup"})
            self.torcedores.append({"x": i, "y": 475, "cor": random.choice(cores_roupa), "tipo": "inf"})
            
        # Laterais
        for j in range(40, 460, 20):
            self.torcedores.append({"x": 5, "y": j, "cor": random.choice(cores_roupa), "tipo": "esq"})
            self.torcedores.append({"x": 780, "y": j, "cor": random.choice(cores_roupa), "tipo": "dir"})

    def on_mouse_press(self, event):
        self.mouse_x, self.mouse_y = event.x, event.y
        if self.estado != "arrastando":
            dist = math.hypot(event.x - self.bola["x"], event.y - self.bola["y"])
            if dist <= self.bola["raio"] + 15: # Área de clique um pouco maior para facilitar
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
        x_centro = self.LIMITE_DIR if lado == "jogador" else self.LIMITE_ESQ
        for _ in range(60):
            self.confetes.append({
                "x": x_centro,
                "y": random.uniform(self.LIMITE_SUP, self.LIMITE_INF),
                "vx": random.uniform(-200, 200) * (1 if lado == "jogador" else -1),
                "vy": random.uniform(-250, -50),
                "cor": random.choice(["red", "yellow", "blue", "lime", "cyan", "magenta", "orange", "white"]),
                "vida": random.uniform(0.8, 1.8)
            })

    def atualizar_confetes(self, delta_t):
        for confete in self.confetes:
            confete["vy"] += 350 * delta_t  
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

        # Colisão com as paredes de cima e baixo
        if self.bola["y"] - self.bola["raio"] < self.LIMITE_SUP:
            self.bola["y"] = self.LIMITE_SUP + self.bola["raio"]
            self.bola["vy"] *= -1
        elif self.bola["y"] + self.bola["raio"] > self.LIMITE_INF:
            self.bola["y"] = self.LIMITE_INF - self.bola["raio"]
            self.bola["vy"] *= -1

        # Gols
        if self.bola["x"] - self.bola["raio"] < self.LIMITE_ESQ:
            self.gol_inimigo()
            return
        if self.bola["x"] + self.bola["raio"] > self.LIMITE_DIR:
            self.gol_jogador()
            return

        # Colisão Goleiro
        if self.colisao_bola_goleiro():
            self.bola["vx"] *= -1
            self.bola["vy"] += random.uniform(-2, 2)
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
        self.goleiro["max_y"] = self.LIMITE_INF - self.goleiro["altura"]

    def atualizar(self):
        self.mover_goleiro()
        self.mover_bola()
        self.atualizar_confetes(0.016)
        self.desenhar()
        self.janela.after(16, self.atualizar)

    def desenhar(self):
        self.canvas.delete("all")

        # 1. Fundo do estádio (Bancadas)
        self.canvas.create_rectangle(0, 0, 800, 500, fill="#5D4037", outline="")

        # 2. Desenhar Plateia Fixa
        for t in self.torcedores:
            x, y = t["x"], t["y"]
            self.canvas.create_oval(x, y, x+12, y+12, fill=t["cor"], outline="#3E2723")
            if t["tipo"] == "sup":
                self.canvas.create_oval(x+3, y+8, x+9, y+14, fill="#FFCC80", outline="")
            elif t["tipo"] == "inf":
                self.canvas.create_oval(x+3, y-2, x+9, y+4, fill="#FFCC80", outline="")
            elif t["tipo"] == "esq":
                self.canvas.create_oval(x+8, y+3, x+14, y+9, fill="#FFCC80", outline="")
            elif t["tipo"] == "dir":
                self.canvas.create_oval(x-2, y+3, x+4, y+9, fill="#FFCC80", outline="")

        # 3. Gramado com Listras (Mowed Grass Effect)
        largura_listra = 50
        for i in range(self.LIMITE_ESQ, self.LIMITE_DIR, largura_listra):
            cor = "#4CAF50" if (i // largura_listra) % 2 == 0 else "#43A047"
            self.canvas.create_rectangle(i, self.LIMITE_SUP, min(i + largura_listra, self.LIMITE_DIR), self.LIMITE_INF, fill=cor, outline="")
        
        # Borda do campo
        self.canvas.create_rectangle(self.LIMITE_ESQ, self.LIMITE_SUP, self.LIMITE_DIR, self.LIMITE_INF, outline="white", width=4)

        # 4. Marcações do Campo
        meio_campo = (self.LIMITE_ESQ + self.LIMITE_DIR) / 2
        self.canvas.create_line(meio_campo, self.LIMITE_SUP, meio_campo, self.LIMITE_INF, fill="white", width=4)
        self.canvas.create_oval(meio_campo-50, 200, meio_campo+50, 300, outline="white", width=4)
        self.canvas.create_oval(meio_campo-6, 244, meio_campo+6, 256, fill="white") # Centro
        
        # Pequena área e Redes (Hachurado)
        # Esquerda
        self.canvas.create_rectangle(self.LIMITE_ESQ, 170, self.LIMITE_ESQ+70, 330, outline="white", width=3)
        for i in range(170, 330, 15):
            self.canvas.create_line(self.LIMITE_ESQ-20, i, self.LIMITE_ESQ, i, fill="#BDBDBD", width=1)
        # Direita
        self.canvas.create_rectangle(self.LIMITE_DIR-70, 170, self.LIMITE_DIR, 330, outline="white", width=3)
        for i in range(170, 330, 15):
            self.canvas.create_line(self.LIMITE_DIR, i, self.LIMITE_DIR+20, i, fill="#BDBDBD", width=1)

        # Traves 
        self.canvas.create_line(self.LIMITE_DIR, 170, self.LIMITE_DIR, 330, fill="#FFEB3B", width=6)
        self.canvas.create_line(self.LIMITE_ESQ, 170, self.LIMITE_ESQ, 330, fill="#FFEB3B", width=6)

        # 5. Goleiro 
        self.desenhar_goleiro()

        # 6. Bola
        self.desenhar_bola()

        # 7. Linha de mira (Estilingue)
        if self.bola["arrastando"]:
            sx, sy = self.bola["drag_start_x"], self.bola["drag_start_y"]
            self.canvas.create_line(sx, sy, self.mouse_x, self.mouse_y, fill="#FFEB3B", width=4, dash=(5,3))
            dx, dy = sx - self.mouse_x, sy - self.mouse_y
            ang = math.atan2(dy, dx)
            ponta_x = sx - 20*math.cos(ang)
            ponta_y = sy - 20*math.sin(ang)
            self.canvas.create_line(sx, sy, ponta_x, ponta_y, fill="#FF5252", width=5, arrow="last")

        # 8. Confetes
        for c in self.confetes:
            self.canvas.create_rectangle(c["x"]-4, c["y"]-4, c["x"]+4, c["y"]+4, fill=c["cor"], outline="")

        # 9. Placar Super Destaque
        self.canvas.create_rectangle(250, 10, 550, 50, fill="#212121", outline="#FFCA28", width=3)
        self.canvas.create_text(400, 30, text=f"👦 Você {self.gols_jogador} x {self.gols_inimigo} Robô 🤖",
                                font=("Comic Sans MS", 16, "bold"), fill="white")
        
        self.canvas.create_text(110, 30, text="◀ Seu Gol", font=("Comic Sans MS", 12, "bold"), fill="#FFEB3B")
        self.canvas.create_text(690, 30, text="Gol Deles ▶", font=("Comic Sans MS", 12, "bold"), fill="#FFEB3B")

    def desenhar_goleiro(self):
        gx, gy = self.goleiro["x"], self.goleiro["y"]
        gw, gh = self.goleiro["largura"], self.goleiro["altura"]
        centro_x = gx + gw/2
        
        # Sombra
        self.canvas.create_oval(gx-5, gy+gh-5, gx+gw+5, gy+gh+5, fill="#2E7D32", outline="")
        
        # Corpo
        self.canvas.create_rectangle(gx, gy+15, gx+gw, gy+gh-10, fill="#D32F2F", outline="#B71C1C", width=2)
        # Cabeça
        self.canvas.create_oval(centro_x-12, gy-5, centro_x+12, gy+19, fill="#FFCC80", outline="#EF6C00", width=2)
        # Olhos
        self.canvas.create_oval(centro_x-6, gy+4, centro_x-2, gy+8, fill="white")
        self.canvas.create_oval(centro_x+2, gy+4, centro_x+6, gy+8, fill="white")
        self.canvas.create_oval(centro_x-5, gy+5, centro_x-3, gy+7, fill="black")
        self.canvas.create_oval(centro_x+3, gy+5, centro_x+5, gy+7, fill="black")
        # Luvas Grandes
        self.canvas.create_oval(gx-12, gy+20, gx, gy+35, fill="#E0E0E0", outline="#9E9E9E", width=2)
        self.canvas.create_oval(gx+gw, gy+20, gx+gw+12, gy+35, fill="#E0E0E0", outline="#9E9E9E", width=2)
        # Chuteiras
        self.canvas.create_rectangle(gx, gy+gh-10, gx+10, gy+gh, fill="#111111")
        self.canvas.create_rectangle(gx+gw-10, gy+gh-10, gx+gw, gy+gh, fill="#111111")

    def desenhar_bola(self):
        bx, by, br = self.bola["x"], self.bola["y"], self.bola["raio"]
        # Sombra da bola
        self.canvas.create_oval(bx-br, by+br-5, bx+br, by+br+5, fill="#2E7D32", outline="")
        
        # Bola branca
        self.canvas.create_oval(bx-br, by-br, bx+br, by+br, fill="white", outline="#424242", width=2)
        
        # Gomos da bola (mais organizados)
        self.canvas.create_oval(bx-4, by-4, bx+4, by+4, fill="#212121")
        for ang in [30, 90, 150, 210, 270, 330]:
            rad = math.radians(ang)
            px1 = bx + br*0.4 * math.cos(rad)
            py1 = by + br*0.4 * math.sin(rad)
            px2 = bx + br*0.9 * math.cos(rad)
            py2 = by + br*0.9 * math.sin(rad)
            self.canvas.create_line(px1, py1, px2, py2, fill="#212121", width=2)