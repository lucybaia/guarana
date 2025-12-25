import tkinter as tk
from tkinter import messagebox

class GuaranaPet:
    def __init__(self, root):
        self.root = root
        self.root.title("Guaraná - O Mico Dev 🦁")
        self.root.geometry("320x450")
        self.root.resizable(False, False)
        
        # Cores da Selva
        self.colors = {
            "bg": "#fcf5e5",       # Creme suave (fundo)
            "highlight": "#ffb74d", # Laranja Mico
            "green": "#66bb6a",    # Verde natureza
            "dark": "#4e342e",     # Marrom tronco
            "blue": "#42a5f5"      # Azul céu
        }
        
        self.root.configure(bg=self.colors["bg"])

        # --- Estados Iniciais ---
        self.vigor = 100       # Antiga Energia
        self.fome = 0          # Fome
        self.frutas = 0        # Antigo XP (Moeda de troca)
        self.em_aventura = False # Antigo is_working

        # --- Interface (UI) ---
        
        # Cabeçalho
        tk.Label(root, text="Guaraná 🦁", font=("Helvetica", 16, "bold"), 
                 bg=self.colors["bg"], fg=self.colors["dark"]).pack(pady=10)

        # Área do Mico (Onde vai a imagem depois)
        self.pet_display = tk.Label(root, text="🐒", font=("Arial", 60), 
                                    bg=self.colors["bg"], fg=self.colors["highlight"])
        self.pet_display.pack(pady=10)
        
        self.lbl_status_text = tk.Label(root, text="O mico está observando...", 
                                        font=("Arial", 10, "italic"), bg=self.colors["bg"])
        self.lbl_status_text.pack(pady=5)

        # Painel de Status (Card)
        self.status_frame = tk.Frame(root, bg="#fff3e0", bd=2, relief="groove")
        self.status_frame.pack(pady=15, padx=20, fill="x")

        self.lbl_vigor = tk.Label(self.status_frame, text=f"⚡ Vigor: {self.vigor}%", bg="#fff3e0", font=("Arial", 10))
        self.lbl_vigor.pack(anchor="w", padx=10, pady=2)
        
        self.lbl_fome = tk.Label(self.status_frame, text=f"🍌 Fome: {self.fome}%", bg="#fff3e0", font=("Arial", 10))
        self.lbl_fome.pack(anchor="w", padx=10, pady=2)

        self.lbl_frutas = tk.Label(self.status_frame, text=f"🥥 Frutas (XP): {self.frutas}", 
                                   bg="#fff3e0", fg=self.colors["dark"], font=("Arial", 11, "bold"))
        self.lbl_frutas.pack(pady=5)

        # Botões de Ação
        self.btn_frame = tk.Frame(root, bg=self.colors["bg"])
        self.btn_frame.pack(pady=20)

        # Botão Focar
        self.btn_work = tk.Button(self.btn_frame, text="Codar (25m)", command=self.explorar_codigo, 
                                  bg=self.colors["green"], fg="white", width=12, font=("Arial", 9, "bold"))
        self.btn_work.grid(row=0, column=0, padx=5)

        # Botão Comer
        self.btn_feed = tk.Button(self.btn_frame, text="Dar Banana", command=self.dar_banana, 
                                  bg=self.colors["highlight"], fg="white", width=10)
        self.btn_feed.grid(row=0, column=1, padx=5)

        # Botão Dormir
        self.btn_sleep = tk.Button(self.btn_frame, text="Rede", command=self.descansar_na_rede, 
                                   bg=self.colors["blue"], fg="white", width=8)
        self.btn_sleep.grid(row=0, column=2, padx=5)

        # Inicia o Ciclo da Natureza
        self.atualizar_ciclo()

    # --- Lógica da Selva ---
    def atualizar_ciclo(self):
        """Atualiza os status passivamente a cada 3 segundos"""
        if not self.em_aventura:
            self.vigor = max(0, self.vigor - 1)
            self.fome = min(100, self.fome + 2)
            
            # Mudança de Humor Visual
            if self.fome > 70:
                self.pet_display.config(text="🦁💢") # Mico bravo/com fome
                self.lbl_status_text.config(text="Guaraná precisa de bananas!")
            elif self.vigor < 20:
                self.pet_display.config(text="🦁💤") # Mico com sono
                self.lbl_status_text.config(text="Guaraná está exausto...")
            else:
                self.pet_display.config(text="🐒") # Mico normal
                self.lbl_status_text.config(text="Pronto para o código!")

        self.refresh_ui()
        
        #