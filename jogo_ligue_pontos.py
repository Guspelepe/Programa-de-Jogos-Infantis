import tkinter as tk
import math

def criar_jogo_ligue_pontos(janela):
    jogo = JogoLiguePontos(janela)
    return jogo

class JogoLiguePontos:
    def __init__(self, janela):
        self.janela = janela
        self.janela.configure(bg="#FFF9C4")

        frame_topo = tk.Frame(janela, bg="#FFF9C4")
        frame_topo.pack(pady=5)

        tk.Button(frame_topo, text="🔙 Voltar ao Menu", font=("Arial", 10),
                  bg="#FFC107", command=self.voltar).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_topo, text="Próximo Desenho ➡️", font=("Arial", 10),
                  bg="#81C784", command=self.proximo_desenho).pack(side=tk.LEFT, padx=5)

        self.status_label = tk.Label(janela, text="", font=("Arial", 14), bg="#FFF9C4", fg="#33691E")
        self.status_label.pack(pady=5)

        self.canvas = tk.Canvas(janela, width=600, height=450, bg="white", highlightthickness=2)
        self.canvas.pack(pady=10)

        self.desenhos = [
            {
                "nome": "Borboleta",
                "pontos": [(300,100), (200,180), (120,300), (180,380), (300,320), (420,380), (480,300), (400,180)],
                "final": self.desenhar_borboleta
            },
            {
                "nome": "Gato",
                "pontos": [(200,120), (160,180), (180,250), (250,280), (350,280), (420,250), (440,180), (400,120), (300,80)],
                "final": self.desenhar_gato
            },
            {
                "nome": "Cachorro",
                "pontos": [(180,150), (140,200), (160,260), (220,300), (300,300), (380,260), (400,200), (360,150), (300,130)],
                "final": self.desenhar_cachorro
            },
            {
                "nome": "Árvore",
                "pontos": [(300,60), (220,160), (380,160), (340,240), (380,320), (220,320)],
                "final": self.desenhar_arvore
            },
            {
                "nome": "Pinguim",
                "pontos": [(300,80), (250,130), (220,200), (230,280), (280,340), (320,340), (370,280), (380,200), (350,130)],
                "final": self.desenhar_pinguim
            }
        ]

        self.indice_atual = 0
        self.carregar_desenho()

        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_motion)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

        self.arrastando = False
        self.linha_temp = None
        self.ponto_inicio = None

    def voltar(self):
        self.janela.destroy()

    def carregar_desenho(self):
        self.dados = self.desenhos[self.indice_atual]
        self.pontos = self.dados["pontos"]
        self.total_pontos = len(self.pontos)
        self.conexoes = []
        self.proximo_ponto = 1
        self.finalizado = False
        self.redesenhar()

    def proximo_desenho(self):
        self.indice_atual = (self.indice_atual + 1) % len(self.desenhos)
        self.carregar_desenho()

    def ponto_mais_proximo(self, x, y, raio=15):
        for i, (px, py) in enumerate(self.pontos):
            if math.hypot(px - x, py - y) <= raio:
                return i
        return None

    def on_press(self, event):
        if self.finalizado:
            return
        idx = self.ponto_mais_proximo(event.x, event.y)
        if idx is None:
            return
        if idx == self.proximo_ponto - 1:
            self.arrastando = True
            self.ponto_inicio = idx
            self.linha_temp = None
        elif idx == self.proximo_ponto:
            self.adicionar_conexao(self.proximo_ponto - 1, self.proximo_ponto)
            self.arrastando = False

    def on_motion(self, event):
        if not self.arrastando or self.finalizado:
            return
        if self.linha_temp:
            self.canvas.delete(self.linha_temp)
        x1, y1 = self.pontos[self.ponto_inicio]
        self.linha_temp = self.canvas.create_line(x1, y1, event.x, event.y,
                                                  fill="gray", width=3, dash=(5,3))

    def on_release(self, event):
        if not self.arrastando or self.finalizado:
            return
        self.arrastando = False
        if self.linha_temp:
            self.canvas.delete(self.linha_temp)
            self.linha_temp = None
        idx_proximo = self.proximo_ponto
        if idx_proximo < self.total_pontos:
            px, py = self.pontos[idx_proximo]
            if math.hypot(event.x - px, event.y - py) <= 15:
                self.adicionar_conexao(self.ponto_inicio, idx_proximo)

    def adicionar_conexao(self, i, j):
        self.conexoes.append((i, j))
        self.proximo_ponto += 1
        self.redesenhar()
        if self.proximo_ponto >= self.total_pontos:
            self.finalizar()

    def finalizar(self):
        self.finalizado = True
        self.redesenhar()
        self.status_label.config(text=f"{self.dados['nome']} completo! 🎉")

    def redesenhar(self):
        self.canvas.delete("all")
        for (i, j) in self.conexoes:
            x1, y1 = self.pontos[i]
            x2, y2 = self.pontos[j]
            self.canvas.create_line(x1, y1, x2, y2, fill="black", width=3)
        if self.finalizado:
            self.dados["final"]()
            return
        for i, (x, y) in enumerate(self.pontos):
            numero = i + 1
            if i == self.proximo_ponto - 1 and not self.finalizado:
                cor_borda = "gold"
                largura_borda = 4
            else:
                cor_borda = "black"
                largura_borda = 2
            self.canvas.create_oval(x-12, y-12, x+12, y+12,
                                    fill="white", outline=cor_borda, width=largura_borda)
            self.canvas.create_text(x, y, text=str(numero), font=("Arial", 12, "bold"))
        if self.proximo_ponto < self.total_pontos:
            self.status_label.config(text=f"Ligue o ponto {self.proximo_ponto} ao ponto {self.proximo_ponto+1}")
        else:
            self.status_label.config(text="Último ponto! Ligue para terminar.")

    # Métodos de desenho final
    def desenhar_borboleta(self):
        c = self.canvas
        pts = self.pontos
        c.create_polygon(pts[0], pts[1], pts[2], pts[3], fill="#FFB74D", outline="black", width=2)
        c.create_polygon(pts[0], pts[7], pts[6], pts[5], pts[4], fill="#FFB74D", outline="black", width=2)
        c.create_line(pts[0], pts[3], fill="#5D4037", width=6)
        c.create_line(pts[0][0], pts[0][1], pts[0][0]-40, pts[0][1]-50, fill="#5D4037", width=3, smooth=True)
        c.create_line(pts[0][0], pts[0][1], pts[0][0]+40, pts[0][1]-50, fill="#5D4037", width=3, smooth=True)

    def desenhar_gato(self):
        c = self.canvas
        pts = self.pontos
        c.create_polygon(pts[0][0], pts[0][1], pts[1][0], pts[1][1], pts[2][0], pts[2][1],
                         fill="#FFCCBC", outline="black", width=2)
        c.create_polygon(pts[7][0], pts[7][1], pts[6][0], pts[6][1], pts[8][0], pts[8][1],
                         fill="#FFCCBC", outline="black", width=2)
        c.create_oval(150, 150, 450, 300, fill="#FFCCBC", outline="black", width=2)
        c.create_oval(230, 190, 270, 230, fill="white", outline="black")
        c.create_oval(330, 190, 370, 230, fill="white", outline="black")
        c.create_oval(250, 210, 260, 220, fill="black")
        c.create_oval(350, 210, 360, 220, fill="black")
        c.create_polygon(285, 240, 315, 240, 300, 255, fill="pink", outline="black")
        c.create_arc(260, 240, 340, 280, start=0, extent=-180, style="arc", outline="black", width=2)

    def desenhar_cachorro(self):
        c = self.canvas
        pts = self.pontos
        c.create_oval(100, 120, 200, 260, fill="#8D6E63", outline="black", width=2)
        c.create_oval(400, 120, 500, 260, fill="#8D6E63", outline="black", width=2)
        c.create_oval(140, 130, 460, 320, fill="#A1887F", outline="black", width=2)
        c.create_oval(220, 240, 380, 330, fill="#D7CCC8", outline="black", width=2)
        c.create_oval(200, 200, 240, 240, fill="white", outline="black")
        c.create_oval(360, 200, 400, 240, fill="white", outline="black")
        c.create_oval(220, 220, 230, 230, fill="black")
        c.create_oval(380, 220, 390, 230, fill="black")
        c.create_oval(280, 270, 320, 300, fill="black")
        c.create_polygon(290, 300, 310, 300, 300, 330, fill="red", outline="black")

    def desenhar_arvore(self):
        c = self.canvas
        pts = self.pontos
        c.create_rectangle(270, 240, 330, 380, fill="#795548", outline="black", width=2)
        c.create_polygon(pts[0], pts[1], pts[2], fill="#4CAF50", outline="black", width=2)
        c.create_oval(200, 100, 400, 250, fill="#66BB6A", outline="black", width=2)
        c.create_oval(180, 140, 420, 230, fill="#81C784", outline="black", width=2)

    def desenhar_pinguim(self):
        c = self.canvas
        pts = self.pontos
        c.create_oval(200, 150, 400, 380, fill="black", outline="black", width=2)
        c.create_oval(230, 220, 370, 360, fill="white", outline="white")
        c.create_oval(240, 70, 360, 200, fill="black", outline="black", width=2)
        c.create_oval(260, 110, 290, 140, fill="white", outline="black")
        c.create_oval(310, 110, 340, 140, fill="white", outline="black")
        c.create_oval(275, 125, 280, 130, fill="black")
        c.create_oval(325, 125, 330, 130, fill="black")
        c.create_polygon(280, 150, 320, 150, 300, 180, fill="orange", outline="black")
        c.create_polygon(250, 380, 230, 410, 270, 410, fill="orange", outline="black")
        c.create_polygon(350, 380, 330, 410, 370, 410, fill="orange", outline="black")