import tkinter as tk
from tkinter import ttk, messagebox
import os
from PIL import Image, ImageTk 
import random

from algoritmos_grafos.bipartite_check import is_bipartite_check

class Missao4:
    """
    Missão 4: Negociação de Alianças (Grafo Bipartido)
    """
    def __init__(self, root, game_manager, content_frame):
        self.root = root
        self.game_manager = game_manager
        self.base_content_frame = content_frame

        self.graph = {
            "A": ["B", "H"], "B": ["A", "C"], "C": ["B", "D"], 
            "D": ["C", "E"], "E": ["D", "F"], "F": ["E", "G"],
            "G": ["F", "H"], "H": ["G", "A"]
        }
        self.start_node = "A"
        self.is_bipartite_solution, self.solution_colors, _ = is_bipartite_check(self.graph, self.start_node)
        
        self.current_colors = {node: 0 for node in self.graph} 
        self.message = "Aliança inicializada. Comece a colorir o planeta A!"
        
        self._carregar_estilos()

    def _carregar_estilos(self):
        try:
            self.cor_fundo = self.game_manager.bg_color_dark
            self.cor_texto = self.game_manager.fg_color_light
            self.cor_titulo = self.game_manager.title_color_accent
            self.font_titulo = self.game_manager.header_font_obj
            self.font_narrativa = self.game_manager.narrative_font_obj
            self.font_subtitulo = self.game_manager.small_bold_font_obj
            self.cor_grupo1 = "#0000FF" # Azul (Rebeldes)
            self.cor_grupo2 = "#FF0000" # Vermelho (Neutros/Aliados)
            self.cor_conflito = "#FFFF00"
            self.cor_sucesso = "#00FF00"
        except AttributeError:
            self.cor_fundo = "black"
            self.cor_texto = "white"
            self.cor_titulo = "#FF00E6"
            self.font_titulo = ("Arial", 20, "bold")
            self.font_narrativa = ("Arial", 12)
            self.font_subtitulo = ("Arial", 10, "bold")
            self.cor_grupo1 = "#0000FF"
            self.cor_grupo2 = "#FF0000"
            self.cor_conflito = "#FFFF00"
            self.cor_sucesso = "#00FF00"

    def _limpar_frame(self):
        for w in self.base_content_frame.winfo_children():
            w.destroy()

    def iniciar_missao_contexto(self, image_to_display=None):
        self._limpar_frame()

        try:
            image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "img", "missao4_grafos.png") 
            img = Image.open(image_path)
            img = img.resize((380, 250), Image.Resampling.LANCZOS) 
            self.tk_image = ImageTk.PhotoImage(img) 
            img_label = tk.Label(self.base_content_frame, image=self.tk_image, bg=self.cor_fundo)
            img_label.pack(pady=10)
        except (FileNotFoundError, NameError):
            tk.Label(self.base_content_frame, text="(AVISO: Imagem missao4_grafos.png não carregada)", fg=self.cor_conflito, bg=self.cor_fundo).pack(pady=5)

        tk.Label(
            self.base_content_frame,
            text="Missão 4: Negociação de Alianças (Grafo Bipartido)",
            font=self.font_titulo,
            fg=self.cor_titulo,
            bg=self.cor_fundo
        ).pack(pady=(10, 6))

        contexto = (
            "**Princesa Leia:** Precisamos formar uma aliança planetária unida. No entanto, alguns planetas são inimigos naturais (Grafo Bipartido). "
            "Só podemos aceitar uma aliança se o conjunto puder ser dividido em dois grupos (G1 e G2) onde **NÃO HÁ arestas (ligações) DENTRO do mesmo grupo**.\n\n"
            "**Sua Tarefa:** Use a coloração para dividir os planetas. Cor **Azul (Grupo Rebelde)** e Cor **Vermelha (Grupo Neutro)**. Se houver um conflito de cor entre vizinhos, a aliança é instável."
        )
        tk.Label(
            self.base_content_frame,
            text=contexto,
            wraplength=800,
            justify=tk.LEFT,
            font=self.font_narrativa,
            fg=self.cor_texto,
            bg=self.cor_fundo
        ).pack(pady=(6, 14), padx=20)

        ttk.Button(
            self.base_content_frame,
            text="Iniciar Negociação",
            command=self._iniciar_missao,
            style="Accent.Dark.TButton"
        ).pack(pady=10)

    def _iniciar_missao(self):
        self.current_colors = {node: 0 for node in self.graph.keys()}
        self.current_colors[self.start_node] = 1 
        self.message = f"Iniciando: Planeta {self.start_node} é o Grupo Rebelde (Azul)."
        self._montar_tela_missao()

    def _montar_tela_missao(self):
        self._limpar_frame()

        tk.Label(self.base_content_frame, text="Coloração Bipartida", font=self.font_titulo, fg=self.cor_titulo, bg=self.cor_fundo).pack(pady=(8, 2))

        main = tk.Frame(self.base_content_frame, bg=self.cor_fundo)
        main.pack(fill=tk.BOTH, expand=True, padx=10, pady=8)

        left = tk.Frame(main, bg=self.cor_fundo, width=340)
        left.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left.pack_propagate(False)

        right = tk.Frame(main, bg=self.cor_fundo)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.lbl_status = tk.Label(left, text=self.message, font=self.font_narrativa, fg=self.cor_texto, bg=self.cor_fundo, wraplength=300, justify=tk.LEFT)
        self.lbl_status.pack(anchor="w", pady=(8, 10))
        
        ttk.Button(left, text="Ajuda / Conceitos", command=self._mostrar_conceito_ajuda).pack(fill=tk.X, pady=5)
        
        tk.Label(left, text="Colorir Planeta:", font=self.font_subtitulo, fg=self.cor_texto, bg=self.cor_fundo).pack(anchor="w", pady=(5, 0))
        
        for node in self.graph.keys():
            if self.current_colors[node] == 0: 
                frame = tk.Frame(left, bg=self.cor_fundo)
                frame.pack(fill=tk.X, pady=2)
                
                tk.Label(frame, text=f"Planeta {node}:", bg=self.cor_fundo, fg=self.cor_texto).pack(side=tk.LEFT)
                
                ttk.Button(frame, text="Azul (Grupo 1)", command=lambda n=node: self._colorir(n, 1)).pack(side=tk.LEFT, padx=5)
                ttk.Button(frame, text="Vermelho (Grupo 2)", command=lambda n=node: self._colorir(n, 2)).pack(side=tk.LEFT, padx=5)
        
        if all(c != 0 for c in self.current_colors.values()) and 3 not in self.current_colors.values():
             ttk.Button(left, text="CONCLUIR ALIANÇA", command=self._finalizar_missao, style="Accent.Dark.TButton").pack(fill=tk.X, pady=15)


        self.canvas = tk.Canvas(right, bg=self.cor_fundo, highlightthickness=0, height=400)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self._desenhar_grafo()
        
    def _mostrar_conceito_ajuda(self):
        messagebox.showinfo(
            "Protocolos de Ajuda (Grafo Bipartido)",
            "Conceito: Um grafo é Bipartido se seus nós puderem ser divididos em dois grupos (Azul e Vermelho) de forma que NENHUM nó do mesmo grupo esteja conectado diretamente.\n\nSua tarefa é garantir que vizinhos SEMPRE tenham cores diferentes."
        )


    def _colorir(self, node, color_id):
        self.current_colors[node] = color_id
        
        conflito_detectado = False
        for neighbor in self.graph[node]:
            if self.current_colors.get(neighbor) == color_id:
                self.message = f"CONFLITO CRÍTICO! Planeta {node} (Cor {color_id}) é inimigo de {neighbor} (Mesma Cor). Aliança Instável!"
                self.current_colors[node] = 3
                self.lbl_status.config(fg=self.cor_conflito)
                conflito_detectado = True
                break

        if not conflito_detectado:
            self.message = f"Planeta {node} alocado ao Grupo {color_id}. Estabilidade mantida."
            self.lbl_status.config(fg=self.cor_texto)

        if 3 in self.current_colors.values():
             self._finalizar_missao()
             return

        self._montar_tela_missao()

    def _desenhar_grafo(self):
        if not self.canvas: return
        self.canvas.delete("all")
        

        pos = {"A": (200 + 150, 50), "B": (350 + 150, 150), "C": (350 + 150, 300), 
               "D": (200 + 150, 400), "E": (50 + 150, 300), "F": (50 + 150, 150),
               "G": (450 + 150, 220), "H": (0 + 150, 220)} 

        for u, neighbors in self.graph.items():
            x1, y1 = pos.get(u, (0,0))
            for v in neighbors:
                x2, y2 = pos.get(v, (0,0))
                self.canvas.create_line(x1, y1, x2, y2, fill="#777777", width=2)
        
        r = 20
        for node, (x, y) in pos.items():
            color_id = self.current_colors.get(node, 0)
            fill = "#333333"
            outline = "#eeeeee"
            
            if color_id == 1:
                fill = self.cor_grupo1
            elif color_id == 2:
                fill = self.cor_grupo2
            elif color_id == 3: # Conflito
                fill = self.cor_conflito
                outline = self.cor_conflito
                
            self.canvas.create_oval(x - r, y - r, x + r, y + r, fill=fill, outline=outline, width=3)
            self.canvas.create_text(x, y, text=node, fill=self.cor_texto, font=("Arial", 10, "bold"))

    def _finalizar_missao(self):
        if all(c != 0 for c in self.current_colors.values()) and 3 not in self.current_colors.values():
            self.game_manager.mission_completed("Missao4")
        else:
            self.game_manager.mission_failed_options(
                self,
                "Falha na Aliança",
                "Houve conflitos de cor ou a coloração não foi concluída. A aliança é instável e o Império aproveitou. Tente reorganizar a coloração para um novo diagnóstico."
            )

    def retry_mission(self):
        self._iniciar_missao()