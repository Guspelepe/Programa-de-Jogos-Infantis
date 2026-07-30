import tkinter as tk
import random

class JogoDamas:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Damas")
        self.janela.geometry("520x580")
        self.janela.configure(bg="#FFE0B2")
        self.janela.resizable(False, False)

        frame_topo = tk.Frame(janela, bg="#FFE0B2")
        frame_topo.pack(pady=5)
        tk.Button(frame_topo, text="🔙 Voltar ao Menu", font=("Arial", 10),
                  bg="#FFC107", command=self.voltar).pack(side=tk.LEFT, padx=5)
        self.lbl_status = tk.Label(frame_topo, text="Sua vez (brancas)",
                                   font=("Arial", 14), bg="#FFE0B2", fg="#5D4037")
        self.lbl_status.pack(side=tk.LEFT, padx=20)

        self.canvas = tk.Canvas(janela, width=480, height=480, bg="#DEB887", highlightthickness=0)
        self.canvas.pack(pady=10)
        self.canvas.bind("<Button-1>", self.on_click)

        self.tamanho_casa = 60
        self.tabuleiro = [[0]*8 for _ in range(8)]
        self.inicializar_tabuleiro()

        self.selecionado = None
        self.movimentos_possiveis = []
        self.turno_do_jogador = True
        self.jogo_encerrado = False

        self.desenhar_tabuleiro()
        self.janela.protocol("WM_DELETE_WINDOW", self.voltar)

    def voltar(self):
        self.janela.destroy()

    def inicializar_tabuleiro(self):
        for i in range(8):
            for j in range(8):
                if (i + j) % 2 == 1:
                    if i < 3:
                        self.tabuleiro[i][j] = 2   # preta
                    elif i > 4:
                        self.tabuleiro[i][j] = 1   # branca

    def desenhar_tabuleiro(self):
        self.canvas.delete("all")
        for i in range(8):
            for j in range(8):
                x1 = j * self.tamanho_casa
                y1 = i * self.tamanho_casa
                x2 = x1 + self.tamanho_casa
                y2 = y1 + self.tamanho_casa
                cor = "#F5DEB3" if (i + j) % 2 == 0 else "#8B4513"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=cor, outline="")

                peca = self.tabuleiro[i][j]
                if peca != 0:
                    self.desenhar_peca(i, j, peca)

        if self.selecionado is not None:
            i, j = self.selecionado
            x = j * self.tamanho_casa + self.tamanho_casa//2
            y = i * self.tamanho_casa + self.tamanho_casa//2
            self.canvas.create_oval(x-25, y-25, x+25, y+25, outline="yellow", width=3)

            for (li, col) in self.movimentos_possiveis:
                cx = col * self.tamanho_casa + self.tamanho_casa//2
                cy = li * self.tamanho_casa + self.tamanho_casa//2
                self.canvas.create_oval(cx-10, cy-10, cx+10, cy+10, fill="lightgreen", outline="")

    def desenhar_peca(self, linha, coluna, tipo):
        x = coluna * self.tamanho_casa + self.tamanho_casa//2
        y = linha * self.tamanho_casa + self.tamanho_casa//2
        if tipo == 1:
            self.canvas.create_oval(x-20, y-20, x+20, y+20, fill="white", outline="gray", width=2)
        elif tipo == 2:
            self.canvas.create_oval(x-20, y-20, x+20, y+20, fill="black", outline="gray", width=2)
        elif tipo == 3:
            self.canvas.create_oval(x-20, y-20, x+20, y+20, fill="white", outline="gold", width=4)
            self.canvas.create_oval(x-12, y-12, x+12, y+12, fill="white", outline="gold", width=2)
        elif tipo == 4:
            self.canvas.create_oval(x-20, y-20, x+20, y+20, fill="black", outline="gold", width=4)
            self.canvas.create_oval(x-12, y-12, x+12, y+12, fill="black", outline="gold", width=2)

    def on_click(self, event):
        if self.jogo_encerrado or not self.turno_do_jogador:
            return

        coluna = event.x // self.tamanho_casa
        linha = event.y // self.tamanho_casa
        if linha < 0 or linha >= 8 or coluna < 0 or coluna >= 8:
            return

        if self.selecionado is None:
            if self.tabuleiro[linha][coluna] in (1, 3):
                self.selecionado = (linha, coluna)
                self.movimentos_possiveis = self.calcular_movimentos(linha, coluna, captura_obrigatoria=True)
                self.desenhar_tabuleiro()
        else:
            if (linha, coluna) in self.movimentos_possiveis:
                self.executar_movimento(self.selecionado, (linha, coluna))
                self.selecionado = None
                self.movimentos_possiveis = []
                self.desenhar_tabuleiro()
                self.verificar_fim_de_jogo()
                if not self.jogo_encerrado:
                    self.turno_do_jogador = False
                    self.lbl_status.config(text="Vez da IA (pretas)...")
                    self.janela.after(300, self.jogada_ia)
            else:
                if self.tabuleiro[linha][coluna] in (1, 3):
                    self.selecionado = (linha, coluna)
                    self.movimentos_possiveis = self.calcular_movimentos(linha, coluna, captura_obrigatoria=True)
                else:
                    self.selecionado = None
                    self.movimentos_possiveis = []
                self.desenhar_tabuleiro()

    def calcular_movimentos(self, linha, coluna, captura_obrigatoria=False):
        peca = self.tabuleiro[linha][coluna]
        if peca == 0:
            return []

        movimentos = []
        capturas = []

        if peca in (1, 2):
            direcoes = [(-1, -1), (-1, 1)] if peca == 1 else [(1, -1), (1, 1)]
        else:
            direcoes = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        for dx, dy in direcoes:
            nova_linha = linha + dx
            nova_coluna = coluna + dy
            if 0 <= nova_linha < 8 and 0 <= nova_coluna < 8 and self.tabuleiro[nova_linha][nova_coluna] == 0:
                movimentos.append((nova_linha, nova_coluna))

            salto_linha = linha + 2*dx
            salto_coluna = coluna + 2*dy
            meio_linha = linha + dx
            meio_coluna = coluna + dy
            if 0 <= salto_linha < 8 and 0 <= salto_coluna < 8 and self.tabuleiro[salto_linha][salto_coluna] == 0:
                peca_meio = self.tabuleiro[meio_linha][meio_coluna]
                if peca_meio != 0:
                    if (peca in (1,3) and peca_meio in (2,4)) or (peca in (2,4) and peca_meio in (1,3)):
                        capturas.append((salto_linha, salto_coluna))

        if captura_obrigatoria and capturas:
            return capturas
        return movimentos + capturas

    def executar_movimento(self, origem, destino):
        lin_orig, col_orig = origem
        lin_dest, col_dest = destino
        peca = self.tabuleiro[lin_orig][col_orig]
        self.tabuleiro[lin_orig][col_orig] = 0
        self.tabuleiro[lin_dest][col_dest] = peca

        if abs(lin_dest - lin_orig) == 2:
            meio_lin = (lin_orig + lin_dest) // 2
            meio_col = (col_orig + col_dest) // 2
            self.tabuleiro[meio_lin][meio_col] = 0

        if peca == 1 and lin_dest == 0:
            self.tabuleiro[lin_dest][col_dest] = 3
        elif peca == 2 and lin_dest == 7:
            self.tabuleiro[lin_dest][col_dest] = 4

    def jogada_ia(self):
        if self.jogo_encerrado:
            return

        # Coleta movimentos e capturas
        movimentos = []
        capturas = []
        for i in range(8):
            for j in range(8):
                if self.tabuleiro[i][j] in (2, 4):
                    destinos = self.calcular_movimentos(i, j, captura_obrigatoria=False)
                    for d in destinos:
                        if abs(d[0] - i) == 2:
                            capturas.append((i, j, d[0], d[1]))
                        else:
                            movimentos.append((i, j, d[0], d[1]))

        if capturas:
            # Escolhe aleatoriamente uma captura
            escolha = random.choice(capturas)
            origem = (escolha[0], escolha[1])
            destino = (escolha[2], escolha[3])
        elif movimentos:
            escolha = random.choice(movimentos)
            origem = (escolha[0], escolha[1])
            destino = (escolha[2], escolha[3])
        else:
            self.fim_de_jogo("Você venceu! IA não pode mais mover.")
            return

        self.executar_movimento(origem, destino)
        self.desenhar_tabuleiro()
        self.verificar_fim_de_jogo()

        if not self.jogo_encerrado:
            self.turno_do_jogador = True
            self.lbl_status.config(text="Sua vez (brancas)")
            if not self.tem_movimentos_validos(1):
                self.fim_de_jogo("IA venceu! Você não pode mais mover.")

    def tem_movimentos_validos(self, time):
        for i in range(8):
            for j in range(8):
                peca = self.tabuleiro[i][j]
                if (time == 1 and peca in (1,3)) or (time == 2 and peca in (2,4)):
                    if self.calcular_movimentos(i, j, captura_obrigatoria=True):
                        return True
        return False

    def verificar_fim_de_jogo(self):
        tem_brancas = any(1 in row or 3 in row for row in self.tabuleiro)
        tem_pretas = any(2 in row or 4 in row for row in self.tabuleiro)
        if not tem_brancas:
            self.fim_de_jogo("IA venceu! Você não tem mais peças.")
        elif not tem_pretas:
            self.fim_de_jogo("Você venceu! IA não tem mais peças.")

    def fim_de_jogo(self, mensagem):
        self.jogo_encerrado = True
        self.lbl_status.config(text=mensagem)
        tk.messagebox.showinfo("Fim de jogo", mensagem)