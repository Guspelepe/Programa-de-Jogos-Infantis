import tkinter as tk
from tkinter import font

# Importação dos jogos
from jogo_futebol import JogoFutebol
from jogo_ligue_pontos import JogoLiguePontos
from jogo_nave import JogoNave
from jogo_memoria_numeros import JogoMemoriaNumeros
from jogo_damas import JogoDamas


class MenuPrincipal:
    def __init__(self, root):
        self.root = root
        self.root.title("🎮 Meu GCompris - Jogos Infantis")

        # Maximiza a janela (tela cheia com barra de título)
        try:
            self.root.state('zoomed')   # Windows
        except:
            try:
                self.root.attributes('-zoomed', True)  # Linux
            except:
                self.root.geometry("1024x768")   # fallback

        # Cor de fundo suave e alegre (Azul Céu)
        self.BG_COLOR = "#E0F7FA"
        self.root.configure(bg=self.BG_COLOR)
        self.root.resizable(True, True)

        # Configuração de Fontes
        self.titulo_fonte = font.Font(family="Comic Sans MS", size=32, weight="bold")
        self.subtitulo_fonte = font.Font(family="Comic Sans MS", size=16)
        self.botao_fonte = font.Font(family="Comic Sans MS", size=18, weight="bold")

        self.criar_interface()

    def criar_interface(self):
        # --- CABEÇALHO ---
        frame_cabecalho = tk.Frame(self.root, bg=self.BG_COLOR)
        frame_cabecalho.pack(pady=(30, 10))

        # Título principal
        tk.Label(
            frame_cabecalho, 
            text="GCOMPRIS", 
            font=self.titulo_fonte,
            bg=self.BG_COLOR, 
            fg="#006064"
        ).pack()

        # Subtítulo amigável
        tk.Label(
            frame_cabecalho, 
            text="Escolha um jogo para começar!", 
            font=self.subtitulo_fonte,
            bg=self.BG_COLOR, 
            fg="#00838F"
        ).pack(pady=5)

        # --- ÁREA DOS JOGOS (GRADE DE CARDS) ---
        frame_jogos = tk.Frame(self.root, bg=self.BG_COLOR)
        frame_jogos.pack(expand=True, pady=20)

        # Lista de jogos com: Texto, Comando, Cor Normal, Cor de Hover (mouse em cima)
        jogos_info = [
            ("⚽ Futebol", self.abrir_futebol, "#4CAF50", "#45a049"),          # Verde
            ("🔢 Ligue os Pontos", self.abrir_ligue_pontos, "#FF9800", "#e68a00"), # Laranja
            ("🚀 Nave Espacial", self.abrir_nave, "#9C27B0", "#8e24aa"),     # Roxo
            ("🧠 Memória Números", self.abrir_memoria_numeros, "#E91E63", "#d81b60"), # Rosa
            ("♟️ Damas", self.abrir_damas, "#00BCD4", "#00acc1")             # Ciano
        ]

        # Organizando em uma grade de 3 colunas (estilo tablet)
        colunas = 3
        for index, (texto, comando, cor_base, cor_hover) in enumerate(jogos_info):
            linha = index // colunas
            coluna = index % colunas

            self.criar_card_jogo(frame_jogos, texto, comando, cor_base, cor_hover, linha, coluna)

        # --- RODAPÉ ---
        frame_rodape = tk.Frame(self.root, bg=self.BG_COLOR)
        frame_rodape.pack(side="bottom", fill="x", pady=15)

        tk.Label(
            frame_rodape, 
            text="🎈 Desenvolvido com carinho para crianças • GCompris Simplificado",
            font=("Comic Sans MS", 11, "italic"), 
            bg=self.BG_COLOR, 
            fg="#006064"
        ).pack()

    def criar_card_jogo(self, parent, texto, comando, cor_base, cor_hover, linha, coluna):
        """ Cria um botão colorido e interativo no estilo card """
        
        # Frame container para simular uma margem/espaco agradável
        card_frame = tk.Frame(parent, bg=self.BG_COLOR, padx=15, pady=15)
        card_frame.grid(row=linha, column=coluna)

        btn = tk.Button(
            card_frame,
            text=texto,
            font=self.botao_fonte,
            bg=cor_base,
            fg="white",
            activebackground=cor_hover,
            activeforeground="white",
            relief="flat",
            bd=0,
            width=18,
            height=2,
            cursor="hand2",
            command=comando
        )
        btn.pack(ipady=10, ipadx=10)

        # Animação ao passar o mouse por cima (Hover)
        def on_enter(e):
            btn.config(bg=cor_hover)

        def on_leave(e):
            btn.config(bg=cor_base)

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

    # ---- Métodos para abrir cada jogo ----
    def abrir_futebol(self):
        self.root.withdraw()
        janela = tk.Toplevel(self.root)
        JogoFutebol(janela, self.voltar_menu)
        janela.protocol("WM_DELETE_WINDOW", lambda: self.fechar_jogo(janela))

    def abrir_ligue_pontos(self):
        janela = tk.Toplevel(self.root)
        janela.title("Ligue os Pontos")
        janela.geometry("700x600")
        janela.configure(bg="#FFF9C4")
        JogoLiguePontos(janela)

    def abrir_nave(self):
        janela = tk.Toplevel(self.root)
        janela.protocol("WM_DELETE_WINDOW", lambda: self.fechar_jogo(janela))
        JogoNave(janela)

    def abrir_memoria_numeros(self):
        janela = tk.Toplevel(self.root)
        janela.title("Memória com Números")
        janela.geometry("700x600")
        janela.configure(bg="#E8F5E9")
        JogoMemoriaNumeros(janela)

    def abrir_damas(self):
        janela = tk.Toplevel(self.root)
        janela.protocol("WM_DELETE_WINDOW", lambda: self.fechar_jogo(janela))
        JogoDamas(janela)

    def voltar_menu(self):
        self.root.deiconify()

    def fechar_jogo(self, janela):
        janela.destroy()
        self.voltar_menu()


if __name__ == "__main__":
    root = tk.Tk()
    app = MenuPrincipal(root)
    root.mainloop()