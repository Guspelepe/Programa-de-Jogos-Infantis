import tkinter as tk
import math
import random

class JogoNave:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Nave Espacial - Gravidade Extrema")
        self.janela.geometry("800x600")
        self.janela.configure(bg="black")
        self.janela.resizable(False, False)

        frame_topo = tk.Frame(janela, bg="black")
        frame_topo.pack(pady=5)
        tk.Button(frame_topo, text="🔙 Voltar ao Menu", font=("Arial", 10),
                  bg="#FFC107", command=self.voltar).pack(side=tk.LEFT, padx=5)
        self.lbl_status = tk.Label(frame_topo, text="Use ← → para resistir à gravidade!",
                                   font=("Arial", 14), fg="white", bg="black")
        self.lbl_status.pack(side=tk.LEFT, padx=20)

        self.canvas = tk.Canvas(janela, width=800, height=550, bg="black", highlightthickness=0)
        self.canvas.pack()
        self.canvas.focus_set()

        self.W = 800
        self.H = 550

        # Nave (centro vertical)
        self.nave = {
            "x": self.W / 2,
            "y": self.H / 2,
            "vx": 0,
            "raio": 15
        }

        self.planeta = None
        self.criar_novo_planeta()

        # Gravidade extrema
        self.gravidade_base = 200000
        self.aumento_dificuldade_intervalo = 6000  # ms (a cada 6s)

        self.teclas = set()
        self.jogo_rodando = True

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

    def criar_novo_planeta(self):
        lado = random.choice(["esquerda", "direita"])
        raio = random.randint(300, 400)
        if lado == "esquerda":
            x = -raio * 0.5   # metade pra fora
        else:
            x = self.W + raio * 0.5

        y = -random.randint(50, 150)
        massa = raio / 50.0   # massa proporcional, bem alta
        cor = random.choice(["#E91E63", "#9C27B0", "#3F51B5", "#FF9800", "#F44336"])
        self.planeta = {
            "x": x,
            "y": y,
            "raio": raio,
            "massa": massa,
            "cor": cor,
            "vy": random.uniform(80, 120)   # desce rápido
        }

    def loop(self):
        if not self.jogo_rodando:
            return

        agora = self.agora()
        delta_t = 0.016

        # Movimento do jogador (apenas horizontal)
        aceleracao = 900   # ainda responsiva, mas a gravidade é muito maior
        if "Left" in self.teclas:
            self.nave["vx"] -= aceleracao * delta_t
        if "Right" in self.teclas:
            self.nave["vx"] += aceleracao * delta_t

        self.nave["vx"] *= 0.85   # atrito mínimo para parar rapidamente

        if self.planeta:
            dx = self.planeta["x"] - self.nave["x"]
            dy = self.planeta["y"] - self.nave["y"]
            dist = math.hypot(dx, dy)
            if dist < 1:
                dist = 1

            # Força gravitacional brutal
            G = self.gravidade_base
            forca = G * self.planeta["massa"] / (dist ** 1.2)
            self.nave["vx"] += (dx / dist) * forca * delta_t

            # Movimento do planeta
            self.planeta["y"] += self.planeta["vy"] * delta_t

            # Colisão
            if dist < self.nave["raio"] + self.planeta["raio"]:
                self.game_over()
                return

            if self.planeta["y"] - self.planeta["raio"] > self.H:
                self.criar_novo_planeta()

        # Nave saiu da tela completamente
        if self.nave["x"] < -self.nave["raio"] * 2 or self.nave["x"] > self.W + self.nave["raio"] * 2:
            self.game_over()
            return

        self.nave["x"] += self.nave["vx"] * delta_t

        # Aumenta dificuldade periodicamente
        if agora - self.ultimo_aumento > self.aumento_dificuldade_intervalo:
            self.gravidade_base += 3000
            self.ultimo_aumento = agora
            if self.planeta:
                self.planeta["vy"] += 30   # planetas descem ainda mais rápido

        self.desenhar()
        self.janela.after(16, self.loop)

    def game_over(self):
        self.jogo_rodando = False
        self.desenhar()
        self.canvas.create_text(self.W/2, self.H/2, text="GAME OVER",
                               font=("Arial", 48, "bold"), fill="red")
        self.canvas.create_text(self.W/2, self.H/2 + 50,
                               text="A gravidade te engoliu!",
                               font=("Arial", 18), fill="white")
        self.lbl_status.config(text="Você perdeu! 😞")

    def desenhar(self):
        self.canvas.delete("all")

        # Fundo estrelado
        for i in range(100):
            x = (i * 37 + 11) % self.W
            y = (i * 53 + 7) % self.H
            self.canvas.create_oval(x, y, x+1, y+1, fill="white", outline="")

        if self.planeta:
            p = self.planeta
            x, y, r = p["x"], p["y"], p["raio"]
            self.canvas.create_oval(x-r, y-r, x+r, y+r, fill=p["cor"], outline="white", width=3)
            for _ in range(6):
                cx = x + random.randint(-int(r*0.6), int(r*0.6))
                cy = y + random.randint(-int(r*0.6), int(r*0.6))
                cr = random.randint(15, 30)
                self.canvas.create_oval(cx-cr, cy-cr, cx+cr, cy+cr,
                                        fill="", outline="white", width=1)

            dx = p["x"] - self.nave["x"]
            dy = p["y"] - self.nave["y"]
            dist = math.hypot(dx, dy)
            if dist > 0:
                self.canvas.create_line(self.nave["x"], self.nave["y"],
                                        p["x"], p["y"],
                                        fill="gray", dash=(3,6), width=2)

        # Nave
        nx, ny = self.nave["x"], self.nave["y"]
        r = self.nave["raio"]
        self.canvas.create_polygon(nx, ny-r, nx-r, ny+r, nx+r, ny+r,
                                   fill="cyan", outline="white", width=2)
        self.canvas.create_polygon(nx-r, ny+r, nx-5, ny+r+10,
                                   nx+5, ny+r+10, nx+r, ny+r,
                                   fill="orange", outline="white")

        self.canvas.create_text(60, 20, text=f"Gravidade: {self.gravidade_base}",
                               font=("Arial", 12), fill="yellow")
        if self.planeta:
            self.canvas.create_text(60, 40, text=f"Planeta: {self.planeta['raio']}px",
                                   font=("Arial", 12), fill="yellow")