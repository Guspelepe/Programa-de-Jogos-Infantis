import tkinter as tk
import math

class JogoLiguePontos:
    def __init__(self, janela):
        self.janela = janela
        self.janela.configure(bg="#FFF9C4") # Amarelo pastel suave

        # --- BARRA SUPERIOR ---
        frame_topo = tk.Frame(janela, bg="#FFF9C4")
        frame_topo.pack(pady=15)

        tk.Button(frame_topo, text="🔙 Voltar ao Menu", font=("Comic Sans MS", 12, "bold"),
                  bg="#FF5252", fg="white", activebackground="#FF1744", relief="flat",
                  cursor="hand2", command=self.voltar).pack(side=tk.LEFT, padx=10, ipadx=10)
        
        tk.Button(frame_topo, text="Próximo Desenho ➡️", font=("Comic Sans MS", 12, "bold"),
                  bg="#4CAF50", fg="white", activebackground="#43A047", relief="flat",
                  cursor="hand2", command=self.proximo_desenho).pack(side=tk.LEFT, padx=10, ipadx=10)

        # Texto de Instrução/Status
        self.status_label = tk.Label(janela, text="", font=("Comic Sans MS", 16, "bold"), 
                                     bg="#FFF9C4", fg="#E65100")
        self.status_label.pack(pady=5)

        # Canvas onde o desenho acontece
        self.canvas = tk.Canvas(janela, width=650, height=450, bg="white", highlightthickness=3, highlightbackground="#FFCC80")
        self.canvas.pack(pady=10)

        # --- BANCO DE DESENHOS ---
        # Agora os pontos formam exatamenta a silhueta do desenho!
        self.desenhos = [
            {
                "nome": "Borboleta",
                "pontos": [(325, 80), (250, 60), (120, 150), (200, 250), (120, 380), 
                           (250, 400), (325, 320), (400, 400), (530, 380), (450, 250), 
                           (530, 150), (400, 60)],
                "final": self.desenhar_borboleta
            },
            {
                "nome": "Gatinho",
                "pontos": [(325, 380), (200, 350), (150, 250), (180, 120), (250, 150), 
                           (325, 130), (400, 150), (470, 120), (500, 250), (450, 350)],
                "final": self.desenhar_gato
            },
            {
                "nome": "Árvore",
                "pontos": [(380, 400), (380, 300), (480, 280), (550, 200), (450, 100), 
                           (325, 60), (200, 100), (100, 200), (170, 280), (270, 300), 
                           (270, 400)],
                "final": self.desenhar_arvore
            },
            {
                "nome": "Pinguim",
                "pontos": [(325, 60), (230, 120), (180, 220), (200, 350), (250, 400), 
                           (400, 400), (450, 350), (470, 220), (420, 120)],
                "final": self.desenhar_pinguim
            },
            {
                "nome": "Cachorrinho",
                "pontos": [(325, 120), (250, 120), (150, 200), (180, 320), (250, 280), 
                           (280, 380), (370, 380), (400, 280), (470, 320), (500, 200), 
                           (400, 120)],
                "final": self.desenhar_cachorro
            }
        ]

        self.indice_atual = 0
        self.arrastando = False
        self.linha_temp = None
        self.ponto_inicio = None
        
        # Binds do Mouse
        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_motion)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

        self.carregar_desenho()

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

    def ponto_mais_proximo(self, x, y, raio=25): # Raio maior para facilitar o clique
        for i, (px, py) in enumerate(self.pontos):
            if math.hypot(px - x, py - y) <= raio:
                return i
        return None

    def on_press(self, event):
        if self.finalizado: return
        
        idx = self.ponto_mais_proximo(event.x, event.y)
        if idx is None: return
        
        if idx == self.proximo_ponto - 1:
            self.arrastando = True
            self.ponto_inicio = idx
            self.linha_temp = None

    def on_motion(self, event):
        if not self.arrastando or self.finalizado: return
        
        if self.linha_temp:
            self.canvas.delete(self.linha_temp)
            
        x1, y1 = self.pontos[self.ponto_inicio]
        self.linha_temp = self.canvas.create_line(x1, y1, event.x, event.y,
                                                  fill="#BDBDBD", width=4, dash=(10, 5))

    def on_release(self, event):
        if not self.arrastando or self.finalizado: return
        self.arrastando = False
        
        if self.linha_temp:
            self.canvas.delete(self.linha_temp)
            self.linha_temp = None
            
        idx = self.ponto_mais_proximo(event.x, event.y)
        
        # Se for o último ponto, liga de volta no primeiro (0) para fechar o desenho
        alvo_correto = 0 if self.proximo_ponto == self.total_pontos else self.proximo_ponto

        if idx == alvo_correto:
            self.adicionar_conexao(self.ponto_inicio, idx)

    def adicionar_conexao(self, i, j):
        self.conexoes.append((i, j))
        self.proximo_ponto += 1
        
        if self.proximo_ponto > self.total_pontos:
            self.finalizar()
        else:
            self.redesenhar()

    def finalizar(self):
        self.finalizado = True
        self.redesenhar()
        self.status_label.config(text=f"Parabéns! Você desenhou: {self.dados['nome']}! 🎉", fg="#2E7D32")

    def redesenhar(self):
        self.canvas.delete("all")
        
        # Se terminou, desenha a arte preenchida por cima
        if self.finalizado:
            self.dados["final"]()
            return
            
        # Linhas já conectadas
        for (i, j) in self.conexoes:
            x1, y1 = self.pontos[i]
            x2, y2 = self.pontos[j]
            self.canvas.create_line(x1, y1, x2, y2, fill="#424242", width=4)
            
        # Bolinhas (Pontos)
        for i, (x, y) in enumerate(self.pontos):
            numero = i + 1
            # Destaca a bolinha que a criança precisa clicar agora
            if i == self.proximo_ponto - 1:
                cor_fundo = "#FFEB3B"  # Amarelo chamativo
                cor_borda = "#F57F17"
                largura_borda = 4
                tamanho = 18
            else:
                cor_fundo = "white"
                cor_borda = "#757575"
                largura_borda = 2
                tamanho = 15
                
            self.canvas.create_oval(x-tamanho, y-tamanho, x+tamanho, y+tamanho,
                                    fill=cor_fundo, outline=cor_borda, width=largura_borda)
            self.canvas.create_text(x, y, text=str(numero), font=("Comic Sans MS", 12, "bold"))
            
        # Atualiza a mensagem na tela
        if self.proximo_ponto <= self.total_pontos:
            alvo = 1 if self.proximo_ponto == self.total_pontos else self.proximo_ponto + 1
            self.status_label.config(text=f"Ligue o ponto {self.proximo_ponto} ao ponto {alvo} ✏️", fg="#E65100")

    # ==========================================
    # MÉTODOS DE DESENHO FINAL (Com preenchimento)
    # ==========================================
    def preencher_poligono(self, cor_fundo, cor_borda):
        """ Função auxiliar para preencher a silhueta ligada pelos pontos """
        flat_pontos = [coord for ponto in self.pontos for coord in ponto]
        self.canvas.create_polygon(*flat_pontos, fill=cor_fundo, outline=cor_borda, width=4)

    def desenhar_borboleta(self):
        self.preencher_poligono("#CE93D8", "#6A1B9A") # Silhueta Roxo claro
        c = self.canvas
        # Corpo e antenas
        c.create_oval(310, 100, 340, 350, fill="#5D4037", outline="#3E2723", width=2)
        c.create_line(315, 120, 270, 50, fill="#5D4037", width=4, smooth=True)
        c.create_line(335, 120, 380, 50, fill="#5D4037", width=4, smooth=True)
        # Detalhes nas asas
        c.create_oval(180, 150, 240, 210, fill="#F48FB1", outline="")
        c.create_oval(410, 150, 470, 210, fill="#F48FB1", outline="")

    def desenhar_gato(self):
        self.preencher_poligono("#FFCC80", "#E65100") # Silhueta Laranja (Gato rajado)
        c = self.canvas
        # Olhos
        c.create_oval(250, 200, 300, 250, fill="white", outline="black", width=2)
        c.create_oval(350, 200, 400, 250, fill="white", outline="black", width=2)
        c.create_oval(270, 220, 290, 240, fill="black")
        c.create_oval(360, 220, 380, 240, fill="black")
        # Focinho
        c.create_polygon(310, 270, 340, 270, 325, 290, fill="pink", outline="black", width=2)
        # Bigodes
        c.create_line(300, 280, 200, 260, width=2)
        c.create_line(300, 290, 200, 300, width=2)
        c.create_line(350, 280, 450, 260, width=2)
        c.create_line(350, 290, 450, 300, width=2)

    def desenhar_arvore(self):
        # Para a árvore, desenhamos o tronco atrás primeiro
        self.canvas.create_rectangle(300, 300, 350, 450, fill="#795548", outline="#4E342E", width=3)
        self.preencher_poligono("#81C784", "#2E7D32") # Silhueta Verde (Copas)
        # Algumas maçãs
        self.canvas.create_oval(250, 150, 280, 180, fill="red", outline="darkred", width=2)
        self.canvas.create_oval(350, 100, 380, 130, fill="red", outline="darkred", width=2)
        self.canvas.create_oval(420, 220, 450, 250, fill="red", outline="darkred", width=2)

    def desenhar_pinguim(self):
        self.preencher_poligono("#212121", "black") # Corpo preto
        c = self.canvas
        # Barriga branca
        c.create_oval(240, 150, 410, 380, fill="white", outline="")
        # Olhos
        c.create_oval(280, 120, 310, 150, fill="white", outline="black")
        c.create_oval(340, 120, 370, 150, fill="white", outline="black")
        c.create_oval(290, 130, 300, 140, fill="black")
        c.create_oval(350, 130, 360, 140, fill="black")
        # Bico e patas
        c.create_polygon(310, 160, 340, 160, 325, 190, fill="orange", outline="black")
        c.create_oval(230, 380, 280, 410, fill="orange", outline="black", width=2)
        c.create_oval(370, 380, 420, 410, fill="orange", outline="black", width=2)

    def desenhar_cachorro(self):
        self.preencher_poligono("#A1887F", "#4E342E") # Corpo marrom
        c = self.canvas
        # Mancha no olho
        c.create_oval(240, 170, 310, 240, fill="#D7CCC8", outline="")
        # Olhos
        c.create_oval(260, 190, 290, 220, fill="white", outline="black")
        c.create_oval(360, 190, 390, 220, fill="white", outline="black")
        c.create_oval(270, 200, 280, 210, fill="black")
        c.create_oval(370, 200, 380, 210, fill="black")
        # Focinho
        c.create_oval(300, 260, 350, 300, fill="black")
        # Língua
        c.create_path = c.create_polygon(315, 300, 335, 300, 335, 330, 325, 340, 315, 330, fill="#EF9A9A", outline="black")