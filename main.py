import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import os

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue") 

class GuaranaPet:
    def __init__(self, root):
        self.root = root
        self.root.title("Guaraná - O Mico Dev")
        self.root.geometry("380x640")
        self.root.resizable(False, False)

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
            else:
                print("Arquivo de fonte não encontrado em assets.")
        except Exception as e:
            print(f"Erro ao carregar fonte: {e}")

        self.colors = {
            "bg":       "#F4F6D8",
            "frame":    "#E3D08C",
            "text":     "#3B2820",
            "white":    "#FFFFFF",
            "timer":    "#BC5636",
            "disabled": "#8D6E63"
        }

        self.root.configure(fg_color=self.colors["bg"])

        self.POMODORO_TIME = 25 * 60 
        self.tempo_restante = 0
        self.timer_running = False
        self.vigor_inicial_foco = 100

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

        self.img_idle   = load_and_resize(os.path.join(assets_folder, "mico_idle.png"))
        self.img_work   = load_and_resize(os.path.join(assets_folder, "mico_work.png"))
        self.img_sleep  = load_and_resize(os.path.join(assets_folder, "mico_sleep.png"))
        self.img_tired  = load_and_resize(os.path.join(assets_folder, "mico_tired.png"))
        self.img_hungry = load_and_resize(os.path.join(assets_folder, "mico_hungry.png"))
        
        btn_size = (110, 50)
        self.btn_img_focar    = load_and_resize(os.path.join(assets_folder, "foia_focar.png"), size=btn_size)
        self.btn_img_focar_h  = load_and_resize(os.path.join(assets_folder, "foia_focar_h.png"), size=btn_size)
        self.btn_img_comer    = load_and_resize(os.path.join(assets_folder, "foia_comer.png"), size=btn_size)
        self.btn_img_comer_h  = load_and_resize(os.path.join(assets_folder, "foia_comer_h.png"), size=btn_size)
        self.btn_img_zzz      = load_and_resize(os.path.join(assets_folder, "foia_zzz.png"), size=btn_size)
        self.btn_img_zzz_h    = load_and_resize(os.path.join(assets_folder, "foia_zzz_h.png"), size=btn_size)

        if not all([self.img_idle, self.img_work, self.img_sleep, self.img_tired, self.img_hungry]):
            self.images_loaded = False
            print("Aviso: Algumas imagens do mico não foram carregadas")

        self.vigor = 100
        self.fome = 0
        self.frutas = 0
        self.em_aventura = False
        self.dormindo = False
        self.timer_mode = None
        self.cycle_running = False

        self.lbl_title = ctk.CTkLabel(root, text="Guaraná 🦁", 
                                      font=(self.custom_font, 32, "bold"),
                                      text_color=self.colors["text"])
        self.lbl_title.pack(pady=(15, 5))

        self.pet_display = ctk.CTkLabel(root, text="")
        
        if self.images_loaded and self.img_idle:
            self.pet_display.configure(image=self.img_idle)
        else:
            self.pet_display.configure(text="🐒", font=("Arial", 80))
            
        self.pet_display.pack(pady=8)
        
        self.lbl_status_text = ctk.CTkLabel(root, text="O mico está observando...", 
                                            font=("Verdana", 11), 
                                            text_color=self.colors["text"])
        self.lbl_status_text.pack(pady=5)

        self.lbl_timer = ctk.CTkLabel(root, text="", 
                                      font=(self.custom_font, 28, "bold"), 
                                      text_color=self.colors["timer"])
        self.lbl_timer.pack(pady=5)

        self.status_frame = ctk.CTkFrame(root, fg_color=self.colors["frame"], corner_radius=20)
        self.status_frame.pack(pady=10, padx=20, fill="x")

        inner_frame = ctk.CTkFrame(self.status_frame, fg_color="transparent")
        inner_frame.pack(pady=10, padx=15)

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

        self.lbl_frutas = ctk.CTkLabel(inner_frame, text=f"🍌 Frutas: {self.frutas}", 
                                       font=(self.custom_font, 13, "bold"), 
                                       text_color="#E65100")
        self.lbl_frutas.pack(pady=(10, 5))

        self.btn_frame = ctk.CTkFrame(root, fg_color="transparent")
        self.btn_frame.pack(pady=15)

        self.btn_work = ctk.CTkButton(self.btn_frame, text="", 
                                      command=self.explorar_codigo,
                                      image=self.btn_img_focar,
                                      fg_color="transparent", 
                                      hover_color=None,
                                      width=110, height=50)
        self.btn_work.grid(row=0, column=0, padx=5)
        self.btn_work.bind("<Enter>", lambda e: self.on_hover(self.btn_work, self.btn_img_focar_h))
        self.btn_work.bind("<Leave>", lambda e: self.on_leave(self.btn_work, self.btn_img_focar))

        self.btn_feed = ctk.CTkButton(self.btn_frame, text="", 
                                      command=self.dar_banana,
                                      image=self.btn_img_comer,
                                      fg_color="transparent", 
                                      hover_color=None,
                                      width=110, height=50)
        self.btn_feed.grid(row=0, column=1, padx=5)
        self.btn_feed.bind("<Enter>", lambda e: self.on_hover(self.btn_feed, self.btn_img_comer_h))
        self.btn_feed.bind("<Leave>", lambda e: self.on_leave(self.btn_feed, self.btn_img_comer))

        self.btn_sleep = ctk.CTkButton(self.btn_frame, text="", 
                                       command=self.descansar_na_rede,
                                       image=self.btn_img_zzz,
                                       fg_color="transparent", 
                                       hover_color=None,
                                       width=110, height=50)
        self.btn_sleep.grid(row=0, column=2, padx=5)
        self.btn_sleep.bind("<Enter>", lambda e: self.on_hover(self.btn_sleep, self.btn_img_zzz_h))
        self.btn_sleep.bind("<Leave>", lambda e: self.on_leave(self.btn_sleep, self.btn_img_zzz))

    def on_hover(self, btn, img):
        if btn.cget("state") != "disabled":
            btn.configure(image=img)

    def on_leave(self, btn, img):
        if btn.cget("state") != "disabled":
            btn.configure(image=img)

    def atualizar_humor_visual(self):
        if not self.images_loaded:
            return
            
        if self.dormindo:
            if self.img_sleep:
                self.pet_display.configure(image=self.img_sleep)
        elif self.em_aventura:
            if self.tempo_restante <= 5 * 60 and self.img_tired:
                self.pet_display.configure(image=self.img_tired)
            elif self.img_work:
                self.pet_display.configure(image=self.img_work)
        elif self.fome >= 90:
            if self.img_hungry:
                self.pet_display.configure(image=self.img_hungry)
        elif self.vigor < 30:
            if self.img_tired:
                self.pet_display.configure(image=self.img_tired)
        else:
            if self.img_idle:
                self.pet_display.configure(image=self.img_idle)

    def atualizar_ciclo_vida(self):
        if not self.em_aventura and not self.dormindo:
            self.vigor = max(0, self.vigor - 1)
            self.fome = min(100, self.fome + 2)
            
            self.atualizar_humor_visual()
            
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
        self.vigor_inicial_foco = self.vigor
        self.alternar_botoes("disabled")
        self.timer_mode = "focus"

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
            
            if self.timer_mode == "focus":
                tempo_decorrido = self.POMODORO_TIME - self.tempo_restante
                porcentagem_completa = tempo_decorrido / self.POMODORO_TIME
                vigor_perdido = int(100 * porcentagem_completa)
                self.vigor = max(0, self.vigor_inicial_foco - vigor_perdido)
                
                self.atualizar_humor_visual()
                
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
        self.fome += 10
        self.alternar_botoes("normal")
        
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
        
        self.atualizar_humor_visual()
        
        self.lbl_status_text.configure(text="Acordou! Pronto pra codar 💪")
        self.root.bell()
        self.refresh_ui()

    def dar_banana(self):
        custo = 10
        if self.frutas >= custo:
            self.fome = max(0, self.fome - 20)
            self.frutas -= custo
            
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
        
        self.atualizar_humor_visual()
            
        self.lbl_status_text.configure(text="Zzz... Dormindo")
        self.tempo_restante = 15 * 60
        self.contagem_regressiva()

if __name__ == "__main__":
    root = ctk.CTk()
    app = GuaranaPet(root)
    root.mainloop()