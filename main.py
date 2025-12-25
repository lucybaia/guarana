import tkinter as tk
from tkinter import messagebox
import os
import math

class GuaranaPet:
    def __init__(self, root):
        self.root = root
        self.root.title("Guaraná - O Mico Dev 🦁")
        self.root.geometry("320x520") # Aumentei um pouco mais para caber o timer
        self.root.resizable(False, False)
        
        # Cores da Selva
        self.colors = {
            "bg": "#ffe5a9",       # Creme suave
            "highlight": "#ffb74d", # Laranja
            "green": "#66bb6a",    # Verde
            "dark": "#663c33",     # Marrom
            "blue": "#42a5f5",     # Azul
            "timer": "#d32f2f"     # Vermelho Pomodoro
        }
        
        self.root.configure(bg=self.colors["bg"])

        # --- CONFIGURAÇÕES DO POMODORO ---
        # Para testar rápido, mude para 10 segundos. Para usar real, coloque 1500 (25 min)
        self.POMODORO_TIME = 25 * 60  
        self.tempo_restante = 0
        self.timer_running = False

        # --- CARREGANDO AS IMAGENS (Seu código original de imagem) ---
        base_folder = os.path.dirname(__file__)
        assets_folder = os.path.join(base_folder, 'assets')

        self.images_loaded = True
        def load_and_resize(path, max_w=180, max_h=180):
            img = tk.PhotoImage(file=path)
            try:
                w = img.width()
                h = img.height()
            except Exception:
                return img
            if w > max_w or h > max_h:
                factor = max(1, math.ceil(max(w / max_w, h / max_h)))
                try:
                    return img.subsample(factor, factor)
                except Exception:
                    return img
            return img

        try:
            self.img_idle = load_and_resize(os.path.join(assets_folder, "mico_idle.png"))
            self.img_work = load_and_resize(os.path.join(assets_folder, "mico_work.png"))
            self.img_sleep = load_and_resize(os.path.join(assets_folder, "mico_sleep.png"))
        except Exception as e:
            print(f"Warning: failed to load images: {e}")
            self.images_loaded = False
            self.img_idle = self.img_work = self.img_sleep = None

        # --- Estados Iniciais ---
        self.vigor = 100
        self.fome = 0
        self.frutas = 0
        self.em_aventura = False

        # --- Interface (UI) ---
        
        # Cabeçalho
        tk.Label(root, text="Guaraná 🦁", font=("Helvetica", 16, "bold"), 
                 bg=self.colors["bg"], fg=self.colors["dark"]).pack(pady=(10, 0))

        # Área do Mico
        if self.images_loaded:
            self.pet_display = tk.Label(root, image=self.img_idle, bg=self.colors["bg"])
        else:
            self.pet_display = tk.Label(root, text="🐒", font=("Arial", 60), bg=self.colors["bg"], fg=self.colors["highlight"])
        self.pet_display.pack(pady=5)
        
        # Texto de Status
        self.lbl_status_text = tk.Label(root, text="O mico está observando...", 
                                        font=("Arial", 10, "italic"), bg=self.colors["bg"])
        self.lbl_status_text.pack(pady=2)

        # --- NOVO: Label do Timer ---
        self.lbl_timer = tk.Label(root, text="", font=("Courier New", 24, "bold"), 
                                  bg=self.colors["bg"], fg=self.colors["timer"])
        self.lbl_timer.pack(pady=5)

        # Painel de Status
        self.status_frame = tk.Frame(root, bg="#fff3e0", bd=2, relief="groove")
        self.status_frame.pack(pady=10, padx=20, fill="x")

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

        self.btn_work = tk.Button(self.btn_frame, text="Codar (25m)", command=self.explorar_codigo, 
                                  bg=self.colors["green"], fg="white", width=12, font=("Arial", 9, "bold"))
        self.btn_work.grid(row=0, column=0, padx=5)

        self.btn_feed = tk.Button(self.btn_frame, text="Dar Banana", command=self.dar_banana, 
                                  bg=self.colors["highlight"], fg="white", width=10)
        self.btn_feed.grid(row=0, column=1, padx=5)

        self.btn_sleep = tk.Button(self.btn_frame, text="Rede", command=self.descansar_na_rede, 
                                   bg=self.colors["blue"], fg="white", width=8)
        self.btn_sleep.grid(row=0, column=2, padx=5)

        # Inicia o Ciclo Passivo
        self.atualizar_ciclo_vida()

    # --- Lógica da Selva (Passiva) ---
    def atualizar_ciclo_vida(self):
        """Atualiza fome e vigor periodicamente se NÃO estiver trabalhando"""
        if not self.em_aventura:
            self.vigor = max(0, self.vigor - 1)
            self.fome = min(100, self.fome + 2)
            
            # Mudança Visual Automática
            if self.images_loaded:
                if self.vigor < 20:
                    self.pet_display.config(image=self.img_sleep)
                    self.lbl_status_text.config(text="Guaraná está caindo de sono...")
                else:
                    self.pet_display.config(image=self.img_idle)
                    if self.fome > 70:
                         self.lbl_status_text.config(text="Guaraná está com MUITA fome! 💢")
                    else:
                         self.lbl_status_text.config(text="Pronto para o código!")
            else:
                 # Fallback para emojis se imagem falhar
                 if self.vigor < 20: self.pet_display.config(text="💤")
                 else: self.pet_display.config(text="🐒")

        self.refresh_ui()
        
        # Verifica Game Over
        if self.fome >= 100:
            messagebox.showerror("Game Over", "Guaraná voltou para a floresta procurar comida!\n(Você perdeu)")
            self.root.destroy()
        else:
            # Chama essa função de novo daqui 3 segundos
            self.root.after(3000, self.atualizar_ciclo_vida)

    def refresh_ui(self):
        self.lbl_vigor.config(text=f"⚡ Vigor: {self.vigor}%")
        self.lbl_fome.config(text=f"🍌 Fome: {self.fome}%")
        self.lbl_frutas.config(text=f"🥥 Frutas (XP): {self.frutas}")

    def alternar_botoes(self, estado):
        """Ativa ou Desativa botões (tk.NORMAL ou tk.DISABLED)"""
        self.btn_work.config(state=estado)
        self.btn_feed.config(state=estado)
        self.btn_sleep.config(state=estado)

    # --- Lógica do Pomodoro ---
    def explorar_codigo(self):
        if self.vigor < 15:
            messagebox.showwarning("Exausto", "O mico está cansado demais para codar!")
            return
        
        # Inicia o modo foco
        self.em_aventura = True
        self.alternar_botoes(tk.DISABLED) # Bloqueia botões para focar
        
        if self.images_loaded:
            self.pet_display.config(image=self.img_work)
        else:
            self.pet_display.config(text="👨‍💻")
            
        self.lbl_status_text.config(text="Modo Foco ativado! Não pare agora.")
        self.root.title("Guaraná - Focando... 🍅")
        
        # Configura o tempo
        self.tempo_restante = self.POMODORO_TIME
        self.contagem_regressiva()

    def contagem_regressiva(self):
        if self.tempo_restante > 0:
            # Formata minutos:segundos
            mins, secs = divmod(self.tempo_restante, 60)
            self.lbl_timer.config(text=f"{mins:02d}:{secs:02d}")
            
            self.tempo_restante -= 1
            # Chama a si mesmo daqui 1000ms (1 segundo)
            self.root.after(1000, self.contagem_regressiva)
        else:
            self.fim_da_aventura()

    def fim_da_aventura(self):
        self.em_aventura = False
        self.lbl_timer.config(text="00:00") # Zera o timer visualmente
        
        # Recompensas
        self.frutas += 25
        self.vigor -= 20
        self.fome += 10
        
        # Retorna ao estado normal
        self.alternar_botoes(tk.NORMAL)
        
        if self.images_loaded:
            self.pet_display.config(image=self.img_idle)
        else:
            self.pet_display.config(text="🐒")
            
        self.lbl_status_text.config(text="Ciclo concluído! Bom trabalho.")
        self.root.title("Guaraná - O Mico Dev 🦁")
        
        # Toca um som de alerta do sistema
        self.root.bell()
        messagebox.showinfo("Pomodoro", "Ciclo concluído! Tire uma pausa.")
        
        self.refresh_ui()

    def dar_banana(self):
        custo = 10
        if self.frutas >= custo:
            self.fome = max(0, self.fome - 20)
            self.frutas -= custo
            self.lbl_status_text.config(text="Nham nham! Banana boa.")
            self.refresh_ui()
            # Limpa o texto depois de 2 seg
            self.root.after(2000, lambda: self.lbl_status_text.config(text="Guaraná está satisfeito."))
        else:
            messagebox.showinfo("Sem Frutas", "Você precisa codar mais para comprar bananas!")

    def descansar_na_rede(self):
        self.vigor = 100
        if self.images_loaded:
            self.pet_display.config(image=self.img_sleep)
        else:
            self.pet_display.config(text="💤")
            
        self.lbl_status_text.config(text="Zzz... Recarregando as baterias.")
        self.refresh_ui()
        
        # Bloqueia ações enquanto dorme (3 seg)
        self.alternar_botoes(tk.DISABLED)
        
        def acordar():
            self.alternar_botoes(tk.NORMAL)
            if self.images_loaded:
                self.pet_display.config(image=self.img_idle)
            else:
                self.pet_display.config(text="🐒")
            self.lbl_status_text.config(text="Guaraná acordou renovado!")

        self.root.after(3000, acordar)

if __name__ == "__main__":
    import traceback
    print("Iniciando Guaraná...")
    try:
        root = tk.Tk()
        app = GuaranaPet(root)
        try:
            root.lift()
            root.attributes('-topmost', True)
            root.after(100, lambda: root.attributes('-topmost', False))
        except Exception:
            pass
        root.mainloop()
    except Exception as e:
        print("Erro ao iniciar:")
        traceback.print_exc()