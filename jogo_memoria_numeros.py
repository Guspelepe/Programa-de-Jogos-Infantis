import tkinter as tk
import random

class JogoMemoriaNumeros:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Jogo da Memória - Números e Quantidades")
        self.janela.geometry("800x650")
        self.janela.configure(bg="#E8F5E9")
        self.janela.resizable(False, False)

        # Frame superior
        frame_topo = tk.Frame(janela, bg="#E8F5E9")
        frame_topo.pack(pady=10)
        tk.Button(frame_topo, text="🔙 Voltar ao Menu", font=("Arial", 10),
                  bg="#FFC107", command=self.voltar).pack(side=tk.LEFT, padx=5)
        self.lbl_mensagem = tk.Label(frame_topo, text="Encontre os pares: número e quantidade",
                                     font=("Arial", 14), bg="#E8F5E9", fg="#2E7D32")
        self.lbl_mensagem.pack(side=tk.LEFT, padx=20)

        # Frame para as cartas
        self.frame_cartas = tk.Frame(janela, bg="#E8F5E9")
        self.frame_cartas.pack(pady=20)

        self.borboleta = "🦋"

        # Gera pares de 1 a 6
        self.pares_base = []
        for i in range(1, 7):
            qtd_formatada = self.formatar_quantidade(i)
            self.pares_base.append((str(i), qtd_formatada))

        self.cartas = []
        self.valores = []
        self.viradas = []
        self.pares_encontrados = 0
        self.carta_virada_idx = None
        self.aguardando = False

        self.criar_tabuleiro()
        self.janela.protocol("WM_DELETE_WINDOW", self.voltar)

    def formatar_quantidade(self, n):
        """Organiza as borboletas em até 2 por linha, como um dado."""
        emojis = [self.borboleta] * n
        linhas = []
        for i in range(0, n, 2):
            linha = ' '.join(emojis[i:i+2])
            linhas.append(linha)
        return '\n'.join(linhas)

    def voltar(self):
        self.janela.destroy()

    def criar_tabuleiro(self):
        for widget in self.frame_cartas.winfo_children():
            widget.destroy()

        self.cartas = []
        self.valores = []
        self.viradas = []
        self.pares_encontrados = 0
        self.carta_virada_idx = None
        self.aguardando = False

        valores_embaralhar = []
        for num, qtd in self.pares_base:
            valores_embaralhar.append(num)
            valores_embaralhar.append(qtd)
        random.shuffle(valores_embaralhar)

        self.valores = valores_embaralhar
        self.viradas = [False] * len(self.valores)

        # Botões maiores para comportar múltiplas linhas
        for i, valor in enumerate(self.valores):
            btn = tk.Button(self.frame_cartas, text="?", font=("Arial", 18, "bold"),
                            width=8, height=4,   # altura extra para linhas
                            bg="#81C784", fg="white", activebackground="#66BB6A",
                            relief="raised", bd=4,
                            command=lambda idx=i: self.virar_carta(idx))
            btn.grid(row=i // 4, column=i % 4, padx=10, pady=10)
            self.cartas.append(btn)

        self.lbl_mensagem.config(text="Encontre os pares: número e quantidade")
        # Remove botão "Jogar Novamente" se existir
        for widget in self.janela.winfo_children():
            if isinstance(widget, tk.Button) and widget.cget("text") == "Jogar Novamente":
                widget.destroy()

    def virar_carta(self, idx):
        if self.aguardando:
            return
        if self.viradas[idx]:
            return

        if self.carta_virada_idx is not None and self.carta_virada_idx != idx:
            self.mostrar_carta(idx)
            self.aguardando = True
            self.janela.after(800, self.verificar_par, self.carta_virada_idx, idx)
            self.carta_virada_idx = None
        else:
            if self.carta_virada_idx is not None:
                pass
            self.carta_virada_idx = idx
            self.mostrar_carta(idx)

    def mostrar_carta(self, idx):
        valor = self.valores[idx]
        self.cartas[idx].config(text=valor, bg="#FFF176", fg="black")

    def esconder_carta(self, idx):
        self.cartas[idx].config(text="?", bg="#81C784", fg="white")

    def verificar_par(self, idx1, idx2):
        valor1 = self.valores[idx1]
        valor2 = self.valores[idx2]
        par_encontrado = False
        for num, qtd in self.pares_base:
            if (valor1 == num and valor2 == qtd) or (valor1 == qtd and valor2 == num):
                par_encontrado = True
                break

        if par_encontrado:
            self.viradas[idx1] = True
            self.viradas[idx2] = True
            self.cartas[idx1].config(bg="#A5D6A7", state="disabled", relief="sunken")
            self.cartas[idx2].config(bg="#A5D6A7", state="disabled", relief="sunken")
            self.pares_encontrados += 1
            if self.pares_encontrados == len(self.pares_base):
                self.lbl_mensagem.config(text="🎉 Parabéns! Você encontrou todos os pares!")
                tk.Button(self.janela, text="Jogar Novamente", font=("Arial", 12),
                          bg="#4CAF50", fg="white", command=self.criar_tabuleiro).pack(pady=10)
        else:
            self.esconder_carta(idx1)
            self.esconder_carta(idx2)

        self.aguardando = False