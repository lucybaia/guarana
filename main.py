import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import os

# --- Configuração Global de Tema ---
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue") 

class GuaranaPet:
    def __init__(self, root):
        self.root = root
        self.root.title("Guaraná - O Mico Dev")
        self.root.geometry("380x640")
        self.root.resizable(False, False)

        # --- CARREGANDO FONTE PERSONALIZADA ---
        base_folder = os.path.dirname(__file__)
        assets_folder = os.path.join(base_folder, 'assets')
        font_path = os.path.join(assets_folder, "Jost-VariableFont_wght.ttf")
        
        self.custom_font = "Verdana"
        try:
            if os.path.exists(font_path):
                ctk.FontManager.load_font(font_path)
                try:
                    import tkinter.font as tkfont
                    families = list(tkfont.families())
                    found = None
                    for f in families:
                        if f.lower().startswith("jost"):
                            found = f
                            break
                    if found:
                        self.custom_font = found
                    else:
                        self.custom_font = "Jost"
                    print(f"Fonte carregada: {font_path} -> {self.custom_font}")
                except Exception:
                    self.custom_font = "Jost"
                    print(f"Fonte carregada mas não foi possível listar famílias; usando {self.custom_font}")
            else:
                print("Arquivo de fonte não encontrado em assets.")
        except Exception as e:
            print(f"Erro ao carregar fonte: {e}")
        
        # --- Paleta de Cores "Kawaii/Pastel" ---
        self.colors = {
            "bg":       "#FFF8E7",
            "frame":    "#FFECB3",
            "text":     "#5D4037",
            "green":    "#A5D6A7",
            "green_h":  "#81C784",
            "pink":     "#F48FB1",
            "pink_h":   "#F06292",
            "blue":     "#90CAF9",
            "blue_h":   "#64B5F6",
            "timer":    "#EF5350"
        }
        
        self.root.configure(fg_color=self.colors["bg"])

        # --- CONFIGURAÇÕES DO POMODORO ---
        self.POMODORO_TIME = 25 * 60 
        self.tempo_restante = 0
        self.timer_running = False
        self.vigor_inicial_foco = 100  # Guarda vigor no início do foco

        # --- CARREGANDO AS IMAGENS ---
        self.images_loaded = True

        def load_and_resize(path, size=(180, 180)):
            try:
                from PIL import Image
                pil_img = Image.open(path).convert("RGBA")
                pil_img.thumbnail(size, Image.LANCZOS)
                return ctk.CTkImage(light_image=pil_img, size=size)
            except ImportError:
                try:
                    img = tk.PhotoImage(file=path)
                    w = img.width()
                    h = img.height()
                    factor = max(1, int(max(w / size[0], h / size[1])))
                    if factor > 1:
                        try:
                            img = img.subsample(factor, factor)
                        except Exception:
                            pass
                    return img
                except Exception as e:
                    print(f"Erro imagem (fallback): {e}")
                    return None
            except Exception as e:
                print(f"Erro imagem: {e}")
                return None

        # Carrega todas as imagens incluindo as novas
        self.img_idle   = load_and_resize(os.path.join(assets_folder, "mico_idle.png"))
        self.img_work   = load_and_resize(os.path.join(assets_folder, "mico_work.png"))
        self.img_sleep  = load_and_resize(os.path.join(assets_folder, "mico_sleep.png"))
        self.img_tired  = load_and_resize(os.path.join(assets_folder, "mico_tired.png"))
        self.img_hungry = load_and_resize(os.path.join(assets_folder, "mico_hungry.png"))
        
        if not all([self.img_idle, self.img_work, self.img_sleep, self.img_tired, self.img_hungry]):
            self.images_loaded = False
            print("Aviso: Algumas imagens não foram carregadas")

        # --- Estados Iniciais ---
        self.vigor = 100
        self.fome = 0
        self.frutas = 0
        self.em_aventura = False
        self.dormindo = False
        self.timer_mode = None
        self.cycle_running = False

        # --- INTERFACE (UI) ---
        
        # 1. Título
        self.lbl_title = ctk.CTkLabel(root, text="Guaraná 🦁", 
                  font=(self.custom_font, 32, "bold"),
                          text_color=self.colors["text"])
        self.lbl_title.pack(pady=(15, 5))

        # 2. Área do Mico
        self.pet_display = ctk.CTkLabel(root, text="")
        
        if self.images_loaded and self.img_idle:
            self.pet_display.configure(image=self.img_idle)
        else:
            self.pet_display.configure(text="🐒", font=("Arial", 80))
            
        self.pet_display.pack(pady=8)
        
        # Texto de Status
        self.lbl_status_text = ctk.CTkLabel(root, text="O mico está observando...", 
                                            font=("Verdana", 11), 
                                            text_color=self.colors["text"])
        self.lbl_status_text.pack(pady=5)

        # 3. Timer
        self.lbl_timer = ctk.CTkLabel(root, text="", 
                  font=(self.custom_font, 28, "bold"), 
                          text_color=self.colors["timer"])
        self.lbl_timer.pack(pady=5)

        # 4. Painel de Status
        self.status_frame = ctk.CTkFrame(root, fg_color=self.colors["frame"], corner_radius=20)
        self.status_frame.pack(pady=10, padx=20, fill="x")

        inner_frame = ctk.CTkFrame(self.status_frame, fg_color="transparent")
        inner_frame.pack(pady=10, padx=15)

        # VIGOR - Label e Barra na mesma linha
        vigor_container = ctk.CTkFrame(inner_frame, fg_color="transparent")
        vigor_container.pack(fill="x", pady=5)
        
        self.lbl_vigor = ctk.CTkLabel(vigor_container, text=f"⚡ Vigor: {self.vigor}%", 
                  font=(self.custom_font, 11, "bold"), 
                          text_color=self.colors["text"],
                          width=120, anchor="w")
        self.lbl_vigor.pack(side="left", padx=(0, 10))
        
        self.pb_vigor = ctk.CTkProgressBar(vigor_container, width=180)
        self.pb_vigor.set(self.vigor / 100)
        self.pb_vigor.pack(side="left")

        # FOME - Label e Barra na mesma linha
        fome_container = ctk.CTkFrame(inner_frame, fg_color="transparent")
        fome_container.pack(fill="x", pady=5)
        
        self.lbl_fome = ctk.CTkLabel(fome_container, text=f"🍌 Fome: {self.fome}%", 
                 font=(self.custom_font, 11, "bold"), 
                         text_color=self.colors["text"],
                         width=120, anchor="w")
        self.lbl_fome.pack(side="left", padx=(0, 10))
        
        self.pb_fome = ctk.CTkProgressBar(fome_container, width=180)
        self.pb_fome.set(self.fome / 100)
        self.pb_fome.pack(side="left")

        # FRUTAS
        self.lbl_frutas = ctk.CTkLabel(inner_frame, text=f"🍌 Frutas: {self.frutas}", 
                   font=(self.custom_font, 13, "bold"), 
                           text_color="#E65100")
        self.lbl_frutas.pack(pady=(10, 5))

        # 5. Botões
        self.btn_frame = ctk.CTkFrame(root, fg_color="transparent")
        self.btn_frame.pack(pady=15)

        self.btn_work = ctk.CTkButton(self.btn_frame, text="Focar 🍌", 
                                      command=self.explorar_codigo,
                                      fg_color=self.colors["green"], 
                                      hover_color=self.colors["green_h"],
                                      text_color="white", 
                                      font=("Verdana", 11, "bold"),
                                      corner_radius=30, width=100, height=38)
        self.btn_work.grid(row=0, column=0, padx=8)

        self.btn_feed = ctk.CTkButton(self.btn_frame, text="Comer 🍌", 
                                      command=self.dar_banana,
                                      fg_color=self.colors["pink"], 
                                      hover_color=self.colors["pink_h"],
                                      text_color="white", 
                                      font=("Verdana", 11, "bold"),
                                      corner_radius=30, width=90, height=38)
        self.btn_feed.grid(row=0, column=1, padx=8)

        self.btn_sleep = ctk.CTkButton(self.btn_frame, text="Zzz... 💤", 
                                       command=self.descansar_na_rede,
                                       fg_color=self.colors["blue"], 
                                       hover_color=self.colors["blue_h"],
                                       text_color="white", 
                                       font=("Verdana", 11, "bold"),
                                       corner_radius=30, width=90, height=38)
        self.btn_sleep.grid(row=0, column=2, padx=8)

        # A lógica (ciclo de vida) será iniciada quando o usuário apertar 'Focar'

    def atualizar_humor_visual(self):
        """Atualiza a imagem do mico baseado no estado atual"""
        if not self.images_loaded:
            return
            
        # Prioridade: Dormindo > Aventura > Fome > Cansado > Idle
        if self.dormindo:
            if self.img_sleep:
                self.pet_display.configure(image=self.img_sleep)
        elif self.em_aventura:
            # Durante aventura: cansado nos últimos 5 minutos
            if self.tempo_restante <= 5 * 60 and self.img_tired:
                self.pet_display.configure(image=self.img_tired)
            elif self.img_work:
                self.pet_display.configure(image=self.img_work)
        elif self.fome >= 90:
            # Com muita fome
            if self.img_hungry:
                self.pet_display.configure(image=self.img_hungry)
        elif self.vigor < 30:
            # Muito cansado
            if self.img_tired:
                self.pet_display.configure(image=self.img_tired)
        else:
            # Estado normal
            if self.img_idle:
                self.pet_display.configure(image=self.img_idle)

    def atualizar_ciclo_vida(self):
        # Não atualiza stats durante aventura ou sono
        if not self.em_aventura and not self.dormindo:
            self.vigor = max(0, self.vigor - 1)
            self.fome = min(100, self.fome + 2)
            
            # Atualiza visual baseado no estado
            self.atualizar_humor_visual()
            
            # Atualiza texto de status
            if self.fome >= 90:
                self.lbl_status_text.configure(text="FOME EXTREMA!!! 🍌💢")
            elif self.fome > 70:
                self.lbl_status_text.configure(text="Tô com fome... 😕")
            elif self.vigor < 30:
                self.lbl_status_text.configure(text="Cansado demais... 😴")
            elif self.vigor < 50:
                self.lbl_status_text.configure(text="Meio cansado...")
            else:
                self.lbl_status_text.configure(text="Só observando...")

        self.refresh_ui()
        
        if self.fome >= 100:
            messagebox.showerror("Ah não!", "Guaraná fugiu para procurar comida na floresta!")
            self.root.destroy()
        else:
            self.root.after(3000, self.atualizar_ciclo_vida)

    def refresh_ui(self):
        self.lbl_vigor.configure(text=f"⚡ Vigor: {self.vigor}%")
        self.lbl_fome.configure(text=f"🍌 Fome: {self.fome}%")
        self.lbl_frutas.configure(text=f"🥥 Frutas: {self.frutas}")
        try:
            self.pb_vigor.set(max(0.0, min(1.0, self.vigor / 100)))
            self.pb_fome.set(max(0.0, min(1.0, self.fome / 100)))
        except Exception:
            pass

    def alternar_botoes(self, estado):
        self.btn_work.configure(state=estado)
        self.btn_feed.configure(state=estado)
        self.btn_sleep.configure(state=estado)

    def explorar_codigo(self):
        if self.vigor < 15:
            messagebox.showwarning("Cansado", "Mico precisa de descanso antes!")
            return
        
        self.em_aventura = True
        self.vigor_inicial_foco = self.vigor  # Guarda vigor inicial
        self.alternar_botoes("disabled")
        self.timer_mode = "focus"

        # Inicia o ciclo de vida se ainda não estiver rodando
        if not getattr(self, "cycle_running", False):
            self.cycle_running = True
            self.atualizar_ciclo_vida()
        
        if self.images_loaded and self.img_work:
            self.pet_display.configure(image=self.img_work)
        else:
            self.pet_display.configure(text="👨‍💻")
            
        self.lbl_status_text.configure(text="Focando! Shhh...")
        self.tempo_restante = self.POMODORO_TIME
        self.contagem_regressiva()

    def contagem_regressiva(self):
        if self.tempo_restante > 0:
            mins, secs = divmod(self.tempo_restante, 60)
            self.lbl_timer.configure(text=f"{mins:02d}:{secs:02d}")
            
            # Durante o foco: diminui vigor proporcionalmente
            if self.timer_mode == "focus":
                # Calcula quanto de vigor gastar (20 pontos ao longo de 25 min)
                tempo_decorrido = self.POMODORO_TIME - self.tempo_restante
                porcentagem_completa = tempo_decorrido / self.POMODORO_TIME
                vigor_perdido = int(20 * porcentagem_completa)
                self.vigor = max(0, self.vigor_inicial_foco - vigor_perdido)
                
                # Atualiza visual (mostra cansado nos últimos 5 min)
                self.atualizar_humor_visual()
                
                # Atualiza texto nos últimos minutos
                if self.tempo_restante <= 5 * 60:
                    self.lbl_status_text.configure(text="Quase lá... mas cansado 😮‍💨")
                
                self.refresh_ui()
            
            self.tempo_restante -= 1
            self.root.after(1000, self.contagem_regressiva)
        else:
            if self.timer_mode == "focus":
                self.fim_da_aventura()
            elif self.timer_mode == "sleep":
                self.fim_do_sono()
            else:
                self.lbl_timer.configure(text="00:00")

    def fim_da_aventura(self):
        self.em_aventura = False
        self.lbl_timer.configure(text="00:00")
        self.frutas += 25
        # Vigor já foi diminuído durante a contagem
        self.fome += 10
        self.alternar_botoes("normal")
        
        # Atualiza visual baseado no estado final
        self.atualizar_humor_visual()
        
        self.lbl_status_text.configure(text="Bom trabalho! +25 Frutas")
        self.root.bell()
        self.refresh_ui()

    def fim_do_sono(self):
        self.dormindo = False
        self.timer_mode = None
        self.lbl_timer.configure(text="00:00")
        self.vigor = 100
        self.alternar_botoes("normal")
        
        # Volta ao estado normal
        self.atualizar_humor_visual()
        
        self.lbl_status_text.configure(text="Acordou! Pronto pra codar 💪")
        self.root.bell()
        self.refresh_ui()

    def dar_banana(self):
        custo = 10
        if self.frutas >= custo:
            self.fome = max(0, self.fome - 20)
            self.frutas -= custo
            
            # Atualiza visual (pode sair do estado com fome)
            self.atualizar_humor_visual()
            
            self.lbl_status_text.configure(text="Nhac! Delícia. 😋")
            self.refresh_ui()
            self.root.after(1500, lambda: self.lbl_status_text.configure(text="Feliz!"))
        else:
            messagebox.showinfo("Sem frutas", "Trabalhe (Focar) para ganhar frutas!")

    def descansar_na_rede(self):
        self.dormindo = True
        self.timer_mode = "sleep"
        self.alternar_botoes("disabled")
        
        # Define visual de sono
        self.atualizar_humor_visual()
            
        self.lbl_status_text.configure(text="Zzz... Dormindo")
        self.tempo_restante = 15 * 60
        self.contagem_regressiva()

if __name__ == "__main__":
    root = ctk.CTk()
    app = GuaranaPet(root)
    root.mainloop()