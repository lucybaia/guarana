import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import os
from PIL import Image, ImageDraw

# Configurações Globais
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue") 

class GuaranaPet:
    def __init__(self, root):
        self.root = root
        self.root.title("Guaraná - O Mico Dev")
        self.root.geometry("460x750")
        self.root.resizable(False, False)

        # --- Configurações de Jogo ---
        self.POMODORO_TIME = 25 * 60  # 25 minutos
        self.SLEEP_TIME = 15 * 60     # 15 minutos
        
        self.tempo_restante = 0
        self.timer_mode = None        # 'focus' ou 'sleep'
        self.jogo_iniciado = False    # Trava: só começa a sentir fome depois do primeiro foco
        self.vigor_inicial_sessao = 100
        
        # Estados Iniciais do Pet
        self.vigor = 100
        self.fome = 0
        self.frutas = 0
        self.em_aventura = False
        self.dormindo = False
        
        # Variáveis de Imagem (para evitar Garbage Collection)
        self.current_display_image = None
        self.status_display_image = None

        # --- Paleta de Cores (Tema Selva) ---
        self.colors = {
            "bg":       "#F4F6D8",
            "frame":    "#E3D08C",
            "text":     "#3B2820",
            "white":    "#FFFFFF",
            "timer":    "#BC5636",
            "disabled": "#8D6E63"
        }
        self.root.configure(fg_color=self.colors["bg"])

        # 1. Carregar Recursos
        self._carregar_fontes()
        self._carregar_assets()

        # 2. Montar Interface
        self._configurar_ui()

        # 3. Iniciar Loop de Vida (ficará em espera até jogo_iniciado = True)
        self.atualizar_ciclo_vida()

    def _carregar_fontes(self):
        base_folder = os.path.dirname(__file__)
        assets_folder = os.path.join(base_folder, 'assets')
        font_path = os.path.join(assets_folder, "Jost-VariableFont_wght.ttf")
        
        self.custom_font = "Jost" # Fallback
        if os.path.exists(font_path):
            try:
                ctk.FontManager.load_font(font_path)
                import tkinter.font as tkfont
                families = list(tkfont.families())
                for f in families:
                    if "jost" in f.lower():
                        self.custom_font = f
                        break
                print(f"Fonte carregada: {self.custom_font}")
            except Exception as e:
                print(f"Erro ao carregar fonte: {e}")

    def _carregar_assets(self):
        """Carrega imagens usando PIL para manipulação avançada"""
        base_folder = os.path.dirname(__file__)
        self.assets_folder = os.path.join(base_folder, 'assets')
        self.images_loaded = True

        def load_pil(filename, size=None):
            try:
                path = os.path.join(self.assets_folder, filename)
                img = Image.open(path).convert("RGBA")
                if size:
                    img.thumbnail(size, Image.LANCZOS)
                return img
            except Exception as e:
                print(f"Erro ao carregar {filename}: {e}")
                return None

        # Sprites do Mico
        self.pil_mico_idle = load_pil("mico_idle.png", (220, 220))
        self.pil_mico_work = load_pil("mico_work.png", (220, 220))
        self.pil_mico_sleep = load_pil("mico_sleep.png", (220, 220))
        self.pil_mico_tired = load_pil("mico_tired.png", (220, 220))
        self.pil_mico_hungry = load_pil("mico_hungry.png", (220, 220))

        # Fundos
        self.pil_bg = load_pil("fundo.jpg", (420, 300))
        self.pil_status_bg = load_pil("fundobarra.png")
        if self.pil_status_bg:
            self.pil_status_bg = self.pil_status_bg.resize((380, 120), Image.LANCZOS)

        # Botões (Carrega PIL e converte para CTkImage)
        def load_ctk_btn(filename):
            pil = load_pil(filename, (110, 50))
            return ctk.CTkImage(light_image=pil, size=(110, 50)) if pil else None

        self.btn_img_focar    = load_ctk_btn("foia_focar.png")
        self.btn_img_focar_h  = load_ctk_btn("foia_focar_h.png")
        self.btn_img_comer    = load_ctk_btn("foia_comer.png")
        self.btn_img_comer_h  = load_ctk_btn("foia_comer_h.png")
        self.btn_img_zzz      = load_ctk_btn("foia_zzz.png")
        self.btn_img_zzz_h    = load_ctk_btn("foia_zzz_h.png")

        if not all([self.pil_mico_idle, self.pil_bg]):
            self.images_loaded = False
            print("AVISO: Assets essenciais não encontrados.")

    def _configurar_ui(self):
        # Título
        self.lbl_title = ctk.CTkLabel(self.root, text="Guaraná 🦁", 
                                      font=(self.custom_font, 36, "bold"),
                                      text_color=self.colors["text"])
        self.lbl_title.pack(pady=(10, 2))

        # Área do Pet (Frame transparente)
        self.pet_area = ctk.CTkFrame(self.root, fg_color="transparent", width=420, height=300)
        self.pet_area.pack(pady=4)
        
        self.pet_display = ctk.CTkLabel(self.pet_area, text="")
        self.pet_display.place(relx=0.5, rely=0.5, anchor="center")
        
        self.atualizar_visual_mico() # Estado inicial

        # Texto de Status
        self.lbl_status_text = ctk.CTkLabel(self.root, text="O mico está observando...", 
                                            font=("Rost", 21), 
                                            text_color=self.colors["text"])
        self.lbl_status_text.pack(pady=2)

        # Timer
        self.lbl_timer = ctk.CTkLabel(self.root, text="", 
                                      font=(self.custom_font, 28, "bold"), 
                                      text_color=self.colors["timer"])
        self.lbl_timer.pack(pady=2)

        # Frame de Status (Barras)
        self.status_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.status_frame.pack(pady=6, padx=20, fill="x")
        
        self.status_display = ctk.CTkLabel(self.status_frame, text="")
        self.status_display.pack()
        self.atualizar_visual_status()

        # Botões
        self.btn_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.btn_frame.pack(pady=8)

        self._criar_botao(0, self.btn_img_focar, self.btn_img_focar_h, self.explorar_codigo)
        self._criar_botao(1, self.btn_img_comer, self.btn_img_comer_h, self.dar_banana)
        self._criar_botao(2, self.btn_img_zzz, self.btn_img_zzz_h, self.descansar_na_rede)

    def _criar_botao(self, col, img_normal, img_hover, comando):
        btn = ctk.CTkButton(self.btn_frame, text="", command=comando,
                            image=img_normal, fg_color="transparent", hover_color=None,
                            width=110, height=50)
        btn.grid(row=0, column=col, padx=5)
        
        # Bindings para efeito hover
        btn.bind("<Enter>", lambda e: self._on_hover(btn, img_hover))
        btn.bind("<Leave>", lambda e: self._on_leave(btn, img_normal))
        
        # Salva referências para alternar estado depois
        if comando == self.explorar_codigo: self.btn_work = btn
        elif comando == self.dar_banana: self.btn_feed = btn
        elif comando == self.descansar_na_rede: self.btn_sleep = btn

    def _on_hover(self, btn, img):
        if btn.cget("state") != "disabled":
            btn.configure(image=img)

    def _on_leave(self, btn, img):
        if btn.cget("state") != "disabled":
            btn.configure(image=img)

    # --- LÓGICA DE COMPOSIÇÃO DE IMAGEM ---

    def compositar_mico_com_fundo(self, pil_mico):
        """Cola o mico em cima do fundo.jpg"""
        if not self.pil_bg or not pil_mico:
            return None
        try:
            composited = self.pil_bg.copy()
            x = (composited.width - pil_mico.width) // 2
            y = (composited.height - pil_mico.height) // 2
            composited.paste(pil_mico, (x, y), pil_mico)
            return ctk.CTkImage(light_image=composited, size=(420, 300))
        except Exception as e:
            print(f"Erro composição: {e}")
            return None

    def compositar_status_barras(self):
        """Desenha barras de progresso e texto sobre o png de status"""
        if not self.pil_status_bg:
            return None
        try:
            img = self.pil_status_bg.copy()
            draw = ImageDraw.Draw(img)
            
            padding_left = 20
            y_vigor = 20
            y_fome = 40
            bar_x = padding_left + 100
            bar_w = 200
            bar_h = 10
            text_color = (59, 40, 32, 255) # #3B2820
            
            def draw_stat(y, label, val, color):
                # Texto
                draw.text((padding_left, y), f"{label} {val}%", fill=text_color)
                # Contorno
                draw.rectangle([bar_x, y+5, bar_x + bar_w, y+5 + bar_h], outline=text_color, width=1)
                # Preenchimento
                fill_w = int(bar_w * (val / 100))
                if fill_w > 0:
                    draw.rectangle([bar_x, y+5, bar_x + fill_w, y+5 + bar_h], fill=color)

            draw_stat(y_vigor, "⚡ Vigor", self.vigor, (76, 175, 80, 255))  # Verde
            draw_stat(y_fome, "🍌 Fome", self.fome, (255, 152, 0, 255))   # Laranja
            
            # Texto Frutas (canto direito ou abaixo)
            draw.text((padding_left + 100, y_fome + 20), f"🥥 Frutas: {self.frutas}", fill=(200, 80, 0, 255))

            return ctk.CTkImage(light_image=img, size=(380, 120))
        except Exception as e:
            print(f"Erro barras: {e}")
            return None

    # --- ATUALIZAÇÕES VISUAIS ---

    def atualizar_visual_mico(self):
        if not self.images_loaded:
            self.pet_display.configure(text="🐒")
            return

        pil_target = self.pil_mico_idle

        if self.dormindo:
            pil_target = self.pil_mico_sleep
        elif self.em_aventura:
            if self.timer_mode == 'focus' and self.tempo_restante <= 5 * 60:
                pil_target = self.pil_mico_tired
            else:
                pil_target = self.pil_mico_work
        elif self.fome >= 90:
            pil_target = self.pil_mico_hungry
        elif self.vigor < 30:
            pil_target = self.pil_mico_tired

        tk_image = self.compositar_mico_com_fundo(pil_target)
        if tk_image:
            self.pet_display.configure(image=tk_image, text="")
            self.current_display_image = tk_image

    def atualizar_visual_status(self):
        tk_image = self.compositar_status_barras()
        if tk_image:
            self.status_display.configure(image=tk_image)
            self.status_display_image = tk_image

    def refresh_ui(self):
        self.atualizar_visual_status()
        self.atualizar_visual_mico()

    # --- LÓGICA DO JOGO E TIMER ---

    def atualizar_ciclo_vida(self):
        """Loop passivo: só roda se o jogo foi iniciado"""
        if not self.jogo_iniciado:
            return

        if not self.em_aventura and not self.dormindo:
            self.vigor = max(0, self.vigor - 1)
            self.fome = min(100, self.fome + 2)
            
            if self.fome >= 90:
                self.lbl_status_text.configure(text="FOME EXTREMA!!! 🍌💢")
            elif self.fome > 70:
                self.lbl_status_text.configure(text="Tô com fome... 😕")
            elif self.vigor < 30:
                self.lbl_status_text.configure(text="Cansado demais... 😴")
            else:
                self.lbl_status_text.configure(text="Só observando...")

            self.refresh_ui()

        if self.fome >= 100:
            messagebox.showerror("Game Over", "Guaraná fugiu para procurar comida na floresta!")
            self.root.destroy()
        else:
            self.root.after(3000, self.atualizar_ciclo_vida)

    def contagem_regressiva(self):
        """Loop ativo (Timer)"""
        if self.tempo_restante > 0:
            mins, secs = divmod(self.tempo_restante, 60)
            self.lbl_timer.configure(text=f"{mins:02d}:{secs:02d}")
            
            # --- Lógica Proporcional ---
            if self.timer_mode == "focus":
                # Vigor desce de 'vigor_inicial' até 0%
                fator = self.tempo_restante / self.POMODORO_TIME
                self.vigor = int(self.vigor_inicial_sessao * fator)
                
                if self.tempo_restante <= 5 * 60:
                    self.lbl_status_text.configure(text="Quase lá... (Cansando)")
                    self.atualizar_visual_mico()

            elif self.timer_mode == "sleep":
                # Vigor sobe de 'vigor_inicial' até 100%
                tempo_decorrido = self.SLEEP_TIME - self.tempo_restante
                pct_concluida = tempo_decorrido / self.SLEEP_TIME
                ganho_necessario = 100 - self.vigor_inicial_sessao
                self.vigor = int(self.vigor_inicial_sessao + (ganho_necessario * pct_concluida))

            self.refresh_ui()
            self.tempo_restante -= 1
            self.root.after(1000, self.contagem_regressiva)
        else:
            self.finalizar_timer()

    def finalizar_timer(self):
        self.lbl_timer.configure(text="00:00")
        
        if self.timer_mode == "focus":
            self.vigor = 0
            self.frutas += 25
            self.fome += 10
            self.lbl_status_text.configure(text="Ciclo Completo! +25 Frutas")
            self.em_aventura = False
            
        elif self.timer_mode == "sleep":
            self.vigor = 100
            self.lbl_status_text.configure(text="Energia renovada! (100%)")
            self.dormindo = False

        self.timer_mode = None
        self.alternar_botoes("normal")
        self.root.bell()
        self.refresh_ui()

    # --- AÇÕES DO USUÁRIO ---

    def alternar_botoes(self, estado):
        self.btn_work.configure(state=estado)
        self.btn_feed.configure(state=estado)
        self.btn_sleep.configure(state=estado)

    def explorar_codigo(self):
        if self.vigor <= 0:
             messagebox.showwarning("Exausto", "O mico está desmaiado de sono! Coloque ele na rede.")
             return

        # Inicia a "vida" do jogo se for a primeira vez
        if not self.jogo_iniciado:
            self.jogo_iniciado = True
            self.atualizar_ciclo_vida()

        self.em_aventura = True
        self.timer_mode = "focus"
        self.vigor_inicial_sessao = self.vigor # Salva para cálculo
        self.alternar_botoes("disabled")
        
        self.lbl_status_text.configure(text="Focando! Shhh...")
        self.tempo_restante = self.POMODORO_TIME
        self.atualizar_visual_mico()
        self.contagem_regressiva()

    def dar_banana(self):
        custo = 10
        if self.frutas >= custo:
            self.fome = max(0, self.fome - 20)
            self.frutas -= custo
            self.lbl_status_text.configure(text="Nhac! Delícia. 😋")
            self.refresh_ui()
            self.root.after(1500, lambda: self.lbl_status_text.configure(text="Feliz!"))
        else:
            messagebox.showinfo("Sem frutas", "Trabalhe (Focar) para ganhar frutas!")

    def descansar_na_rede(self):
        self.dormindo = True
        self.timer_mode = "sleep"
        self.vigor_inicial_sessao = self.vigor # Salva para cálculo
        self.alternar_botoes("disabled")
        
        self.lbl_status_text.configure(text="Zzz... Recuperando Vigor")
        self.tempo_restante = self.SLEEP_TIME
        self.atualizar_visual_mico()
        self.contagem_regressiva()

if __name__ == "__main__":
    root = ctk.CTk()
    app = GuaranaPet(root)
    root.mainloop()