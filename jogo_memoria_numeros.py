import tkinter as tk
import random

class JogoMemoriaNumeros:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Jogo da Memória - Números e Quantidades")
        self.janela.geometry("800x680")
        self.janela.configure(bg="#E8F5E9")
        self.janela.resizable(False, False)

        # --- BARRA SUPERIOR ---
        frame_topo = tk.Frame(janela, bg="#E8F5E9")
        frame_topo.pack(pady=10)
        
        tk.Button(frame_topo, text="🔙 Voltar ao Menu", font=("Comic Sans MS", 10, "bold"),
                  bg="#FF5252", fg="white", activebackground="#FF1744", relief="flat",
                  cursor="hand2", command=self.voltar).pack(side=tk.LEFT, padx=10, ipadx=5)
        
        self.lbl_mensagem = tk.Label(frame_topo, text="Encontre os pares: o número e suas borboletas 🦋",
                                     font=("Comic Sans MS", 14, "bold"), bg="#E8F5E9", fg="#2E7D32")
        self.lbl_mensagem.pack(side=tk.LEFT, padx=20)

        # Frame para as cartas (Grid 3x4 = 12 cartas)
        self.frame_cartas = tk.Frame(janela, bg="#E8F5E9")
        self.frame_cartas.pack(pady=15)

        self.borboleta = "🦋"

        # Gera pares de 1 a 6
        self.pares_base = []
        for i in range(1, 7):
            self.pares_base.append((str(i), i)) # Guardamos o número e a contagem real

        self.cartas = []
        self.valores = []
        self.viradas = []
        self.pares_encontrados = 0
        self.carta_virada_idx = None
        self.aguardando = False
        
        # Controle de animação de virada
        self.animando_idx = None
        self.etapa_animacao = 0

        self.criar_tabuleiro()
        self.janela.protocol("WM_DELETE_WINDOW", self.voltar)

    def formatar_quantidade(self, n):
        """Organiza as borboletas perfeitamente em linhas para caber na carta."""
        emojis = [self.borboleta] * n
        linhas = []
        # Agrupa em até 3 por linha dependendo do tamanho para ficar harmonioso
        limite_por_linha = 3 if n > 4 else 2
        for i in range(0, n, limite_por_linha):
            linha = ' '.join(emojis[i:i+limite_por_linha])
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
            valores_embaralhar.append(("numero", num))
            valores_embaralhar.append(("qtd", qtd))
            
        random.shuffle(valores_embaralhar)

        self.valores = valores_embaralhar
        self.viradas = [False] * len(self.valores)

        # Criação dos botões em grid de 3 linhas por 4 colunas
        for i, (tipo, val) in enumerate(self.valores):
            btn = tk.Button(self.frame_cartas, text="❓", font=("Comic Sans MS", 22, "bold"),
                            width=6, height=3,  
                            bg="#81C784", fg="white", activebackground="#66BB6A",
                            relief="raised", bd=4, cursor="hand2",
                            command=lambda idx=i: self.clicar_carta(idx))
            btn.grid(row=i // 4, column=i % 4, padx=12, pady=12)
            self.cartas.append(btn)

        self.lbl_mensagem.config(text="Encontre os pares: o número e suas borboletas 🦋", fg="#2E7D32")
        
        # Remove botão "Jogar Novamente" se já existir
        for widget in self.janela.winfo_children():
            if isinstance(widget, tk.Button) and widget.cget("text") == "Jogar Novamente 🔄":
                widget.destroy()

    def clicar_carta(self, idx):
        if self.aguardando: return
        if self.viradas[idx]: return
        if self.carta_virada_idx == idx: return

        # Inicia a animação de virar para mostrar a carta
        self.animar_virada(idx, "mostrar", 0)

    def animar_virada(self, idx, acao, passo):
        """Cria o efeito visual de rotação 3D encolhendo e expandindo o botão"""
        larguras = [6, 4, 2, 1, 2, 4, 6] # Simula o giro horizontal
        
        if passo < len(larguras):
            self.cartas[idx].config(width=larguras[passo])
            
            # Na metade do giro, altera o texto/conteúdo
            if passo == 3:
                if acao == "mostrar":
                    tipo, val = self.valores[idx]
                    if tipo == "numero":
                        self.cartas[idx].config(text=str(val), font=("Comic Sans MS", 26, "bold"), bg="#FFF59D", fg="#E65100")
                    else:
                        texto_qtd = self.formatar_quantidade(val)
                        # Fonte ajustada para caber perfeitamente os emojis
                        self.cartas[idx].config(text=texto_qtd, font=("Comic Sans MS", 14, "bold"), bg="#E1F5FE", fg="#01579B")
                else:
                    self.cartas[idx].config(text="❓", font=("Comic Sans MS", 22, "bold"), bg="#81C784", fg="white")
            
            self.janela.after(25, lambda: self.animar_virada(idx, acao, passo + 1))
        else:
            # Fim da animação desta carta
            if acao == "mostrar":
                self.processar_carta_revelada(idx)

    def processar_carta_revelada(self, idx):
        if self.carta_virada_idx is None:
            self.carta_virada_idx = idx
        else:
            idx1 = self.carta_virada_idx
            idx2 = idx
            self.carta_virada_idx = None
            self.aguardando = True

            # Verifica se formam par
            if self.verificar_par_logica(idx1, idx2):
                self.viradas[idx1] = True
                self.viradas[idx2] = True
                self.cartas[idx1].config(bg="#C8E6C9", state="disabled", relief="sunken")
                self.cartas[idx2].config(bg="#C8E6C9", state="disabled", relief="sunken")
                self.pares_encontrados += 1
                self.aguardando = False

                if self.pares_encontrados == len(self.pares_base):
                    self.lbl_mensagem.config(text="🎉 Parabéns! Você encontrou todos os pares!", fg="#1B5E20")
                    tk.Button(self.janela, text="Jogar Novamente 🔄", font=("Comic Sans MS", 13, "bold"),
                              bg="#4CAF50", fg="white", activebackground="#388E3C", relief="raised",
                              cursor="hand2", command=self.criar_tabuleiro).pack(pady=5)
            else:
                # Se errar, espera um instante e desvira as duas com animação
                self.janela.after(900, lambda: self.esconder_par(idx1, idx2))

    def verificar_par_logica(self, idx1, idx2):
        tipo1, val1 = self.valores[idx1]
        tipo2, val2 = self.valores[idx2]
        
        # Um deve ser número e o outro quantidade, e os valores numéricos devem coincidir
        if tipo1 != tipo2 and str(val1) == str(val2):
            return True
        return False

    def esconder_par(self, idx1, idx2):
        self.animar_virada(idx1, "esconder", 0)
        self.animar_virada(idx2, "esconder", 0)
        self.aguardando = False