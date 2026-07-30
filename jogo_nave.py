import tkinter as tk
import math
import random

class JogoNave:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("🚀 Nave Espacial - Gravidade Extrema")
        self.janela.geometry("800x600")
        self.janela.configure(bg="#0B0C10") # Preto mais espacial/profundo
        self.janela.resizable(False, False)

        # --- BARRA SUPERIOR ---
        frame_topo = tk.Frame(janela, bg="#0B0C10")
        frame_topo.pack(pady=10)
        
        tk.Button(frame_topo, text="🔙 Voltar ao Menu", font=("Comic Sans MS", 10, "bold"),
                  bg="#FF5252", fg="white", activebackground="#FF1744", relief="flat",
                  cursor="hand2", command=self.voltar).pack(side=tk.LEFT, padx=10, ipadx=5)
        
        self.lbl_status = tk.Label(frame_topo, text="Use ⬅️ ➡️ para resistir à gravidade!",
                                   font=("Comic Sans MS", 14, "bold"), fg="#4FC3F7", bg="#0B0C10")
        self.lbl_status.pack(side=tk.LEFT, padx=20)

        # --- CANVAS DO JOGO ---
        self.canvas = tk.Canvas(janela, width=800, height=550, bg="#000000", highlightthickness=0)
        self.canvas.pack()
        self.canvas.focus_set()

        self.W = 800
        self.H = 550

        # Nave (centro vertical)
        self.nave = {
            "x": self.W / 2,
            "y": self.H / 2,
            "vx": 0,
            "raio": 18
        }

        # Sistema de Estrelas Animadas
        self.estrelas = []
        self.gerar_estrelas()

        self.planeta = None
        self.criar_novo_planeta()

        # Gravidade extrema
        self.gravidade_base = 200000
        self.aumento_dificuldade_intervalo = 6000  # ms (a cada 6s)

        self.teclas = set()
        self.jogo_rodando = True
        self.contador_animacao = 0 # Para animar o fogo do motor

        self.canvas.bind("<KeyPress>", self.on_key_press)
        self.canvas.bind("<KeyRelease>", self.on_key_release)

        self.ultimo_aumento = self.agora()
        self.loop()

    def voltar(self):
        self.jogo_rodando = False
        self.janela.destroy()

    def agora(self):
        return self.janela.tk.call("clock", "milliseconds") if self.janela.winfo_exists() else 0

    def on_key_press(self, event):
        self.teclas.add(event.keysym)
        return "break"

    def on_key_release(self, event):
        self.teclas.discard(event.keysym)
        return "break"

    def gerar_estrelas(self):
        """ Cria um campo de estrelas com profundidade (parallax) """
        cores = ["#FFFFFF", "#B3E5FC", "#FFF9C4", "#CFD8DC"]
        for _ in range(120):
            self.estrelas.append({
                "x": random.randint(0, self.W),
                "y": random.randint(0, self.H),
                "r": random.choice([1, 1, 2, 3]), # Estrelas maiores e menores
                "vy": random.uniform(1.0, 5.0),   # Velocidades diferentes dão a ilusão de 3D
                "cor": random.choice(cores)
            })

    def criar_novo_planeta(self):
        lado = random.choice(["esquerda", "direita"])
        raio = random.randint(300, 400)
        
        if lado == "esquerda":
            x = -raio * 0.5   
        else:
            x = self.W + raio * 0.5

        y = -random.randint(50, 150)
        massa = raio / 50.0   
        cor = random.choice(["#E91E63", "#9C27B0", "#3F51B5", "#FF9800", "#F44336", "#00BCD4"])
        
        # Gerar crateras fixas para este planeta (não vão mais piscar!)
        crateras = []
        for _ in range(random.randint(8, 15)):
            ang = random.uniform(0, math.pi * 2)
            dist = random.uniform(0, raio * 0.75) # Mantém as crateras dentro do planeta
            crateras.append({
                "dx": math.cos(ang) * dist,
                "dy": math.sin(ang) * dist,
                "r": random.randint(15, int(raio * 0.2))
            })

        self.planeta = {
            "x": x, "y": y,
            "raio": raio,
            "massa": massa,
            "cor": cor,
            "vy": random.uniform(80, 120),
            "crateras": crateras
        }

    def loop(self):
        if not self.jogo_rodando:
            return

        agora = self.agora()
        delta_t = 0.016
        self.contador_animacao += 1

        # Atualiza estrelas
        for estrela in self.estrelas:
            estrela["y"] += estrela["vy"]
            if estrela["y"] > self.H:
                estrela["y"] = 0
                estrela["x"] = random.randint(0, self.W)

        # Movimento do jogador
        aceleracao = 900   
        if "Left" in self.teclas:
            self.nave["vx"] -= aceleracao * delta_t
        if "Right" in self.teclas:
            self.nave["vx"] += aceleracao * delta_t

        self.nave["vx"] *= 0.85   # Atrito no vácuo simulado (para o jogo ter controle)

        if self.planeta:
            dx = self.planeta["x"] - self.nave["x"]
            dy = self.planeta["y"] - self.nave["y"]
            dist = math.hypot(dx, dy)
            if dist < 1:
                dist = 1

            # Força gravitacional
            G = self.gravidade_base
            forca = G * self.planeta["massa"] / (dist ** 1.2)
            self.nave["vx"] += (dx / dist) * forca * delta_t

            # Movimento do planeta
            self.planeta["y"] += self.planeta["vy"] * delta_t

            # Colisão
            if dist < self.nave["raio"] + self.planeta["raio"] - 10: # Margem de respiro
                self.game_over()
                return

            if self.planeta["y"] - self.planeta["raio"] > self.H:
                self.criar_novo_planeta()

        # Nave saiu da tela completamente
        if self.nave["x"] < -self.nave["raio"] * 2 or self.nave["x"] > self.W + self.nave["raio"] * 2:
            self.game_over()
            return

        self.nave["x"] += self.nave["vx"] * delta_t

        # Aumenta dificuldade
        if agora - self.ultimo_aumento > self.aumento_dificuldade_intervalo:
            self.gravidade_base += 3000
            self.ultimo_aumento = agora
            if self.planeta:
                self.planeta["vy"] += 30   

        self.desenhar()
        self.janela.after(16, self.loop)

    def game_over(self):
        self.jogo_rodando = False
        self.desenhar()
        
        # Painel de Game Over Escuro
        self.canvas.create_rectangle(200, 200, 600, 350, fill="#1A237E", outline="#3949AB", width=4)
        
        self.canvas.create_text(self.W/2, self.H/2 - 20, text="GAME OVER",
                               font=("Comic Sans MS", 48, "bold"), fill="#FF5252")
        self.canvas.create_text(self.W/2, self.H/2 + 40,
                               text="A gravidade te engoliu! 🌌",
                               font=("Comic Sans MS", 18, "bold"), fill="white")
        self.lbl_status.config(text="Você virou poeira estelar! 💥", fg="#FF5252")

    def desenhar(self):
        self.canvas.delete("all")

        # 1. Desenhar Fundo Estrelado
        for e in self.estrelas:
            x, y, r = e["x"], e["y"], e["r"]
            self.canvas.create_oval(x, y, x+r, y+r, fill=e["cor"], outline="")

        # 2. Desenhar Planeta e Feixe de Gravidade
        if self.planeta:
            p = self.planeta
            px, py, pr = p["x"], p["y"], p["raio"]
            
            # Raio Trator (Linha de Gravidade)
            dx = px - self.nave["x"]
            dy = py - self.nave["y"]
            dist = math.hypot(dx, dy)
            if dist > 0:
                self.canvas.create_line(self.nave["x"], self.nave["y"], px, py,
                                        fill="#B388FF", dash=(15, 10), width=3) # Roxo neon

            # Planeta (Base)
            self.canvas.create_oval(px-pr, py-pr, px+pr, py+pr, fill=p["cor"], outline="#FFFFFF", width=3)
            
            # Crateras do Planeta
            for cr in p["crateras"]:
                cx = px + cr["dx"]
                cy = py + cr["dy"]
                cr_r = cr["r"]
                self.canvas.create_oval(cx-cr_r, cy-cr_r, cx+cr_r, cy+cr_r, fill="", outline="#000000", width=2)

        # 3. Desenhar a Nave
        nx, ny = self.nave["x"], self.nave["y"]
        
        # Animação do fogo do propulsor (pisca rápido)
        if self.contador_animacao % 4 < 2:
            tamanho_fogo = 25
            cor_fundo = "#FFEB3B" # Amarelo
        else:
            tamanho_fogo = 15
            cor_fundo = "#FF9800" # Laranja
            
        # Fogo central
        self.canvas.create_polygon(nx-8, ny+10, nx+8, ny+10, nx, ny+tamanho_fogo, fill=cor_fundo, outline="")

        # Corpo principal da nave (Asas delta)
        self.canvas.create_polygon(nx, ny-25, nx-20, ny+15, nx, ny+5, nx+20, ny+15,
                                   fill="#E0E0E0", outline="#9E9E9E", width=2)
        
        # Bico e asas em destaque
        self.canvas.create_polygon(nx, ny-25, nx-5, ny-5, nx+5, ny-5, fill="#D32F2F", outline="")
        
        # Cockpit (Vidro azul central)
        self.canvas.create_oval(nx-4, ny-8, nx+4, ny+2, fill="#81D4FA", outline="#0277BD")

        # 4. Placar Flutuante
        self.canvas.create_text(80, 20, text=f"Força G: {self.gravidade_base}",
                               font=("Comic Sans MS", 12, "bold"), fill="#00E676")
        if self.planeta:
            self.canvas.create_text(80, 45, text=f"Massa: {int(self.planeta['massa']*100)}",
                                   font=("Comic Sans MS", 12, "bold"), fill="#FFCA28")