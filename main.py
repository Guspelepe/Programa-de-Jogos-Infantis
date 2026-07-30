# main.py
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
        self.root.title("Meu GCompris")

        # Maximiza a janela (tela cheia com barra de título)
        try:
            self.root.state('zoomed')   # Windows
        except:
            try:
                self.root.attributes('-zoomed', True)  # Linux
            except:
                self.root.geometry("1024x768")   # fallback

        self.root.configure(bg="#E0F7FA")
        self.root.resizable(True, True)   # permite redimensionar se necessário

        titulo_fonte = font.Font(family="Comic Sans MS", size=28, weight="bold")
        botao_fonte = font.Font(family="Comic Sans MS", size=18)

        tk.Label(
            self.root, text="🎮 Escolha um Jogo", font=titulo_fonte,
            bg="#E0F7FA", fg="#006064"
        ).pack(pady=40)

        frame_botoes = tk.Frame(self.root, bg="#E0F7FA")
        frame_botoes.pack(expand=True)

        # Botões para cada jogo
        botoes = [
            ("⚽ Futebol", self.abrir_futebol),
            ("🔢 Ligue os Pontos", self.abrir_ligue_pontos),
            ("🚀 Nave Espacial", self.abrir_nave),
            ("🧠 Memória Números", self.abrir_memoria_numeros),
            ("♟️ Damas", self.abrir_damas)          
        ]

        for texto, comando in botoes:
            tk.Button(
                frame_botoes, text=texto, font=botao_fonte,
                width=20, height=2, bg="#4DD0E1", fg="white",
                activebackground="#00BCD4", relief="raised", bd=5,
                command=comando
            ).pack(pady=10)

        tk.Label(
            self.root, text="Desenvolvido para a disciplina • GCompris simplificado",
            font=("Arial", 10), bg="#E0F7FA", fg="#006064"
        ).pack(side="bottom", pady=10)

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