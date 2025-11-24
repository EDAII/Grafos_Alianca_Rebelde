import tkinter as tk
from tkinter import ttk, messagebox
import os
from PIL import Image, ImageTk 
from collections import deque
import random

from algoritmos_grafos.dfs_recursion import get_dfs_path

class Missao3:
    """
    Missão 3: Infiltração na Base (DFS)
    """
    def __init__(self, root, game_manager, content_frame):
        self.root = root
        self.game_manager = game_manager
        self.base_content_frame = content_frame

        self.graph = {
            "Núcleo": ["A", "B"], "A": ["C", "D"], "B": ["E"],
            "C": ["F"], "D": ["G"], "E": ["H"], "F": [], "G": [], "H": []
        }
        self.start_node = "Núcleo"
        self.visited = set()
        self.path = []
        self.dfs_path_solution, _ = get_dfs_path(self.graph, self.start_node)
        self.current_index = 0
        self.current_node = None
        self.is_finished = False
        
        self._carregar_estilos()

    def _carregar_estilos(self):
        try:
            self.cor_fundo = self.game_manager.bg_color_dark
            self.cor_texto = self.game_manager.fg_color_light
            self.cor_titulo = self.game_manager.title_color_accent
            self.font_titulo = self.game_manager.header_font_obj
            self.font_narrativa = self.game_manager.narrative_font_obj
            self.font_subtitulo = self.game_manager.small_bold_font_obj
            self.cor_alerta = "#FF4500"
            self.cor_sucesso = "#00FF00"
            self.cor_backtrack = "#00FFFF" # Ciano
        except AttributeError:
            self.cor_fundo = "black"
            self.cor_texto = "white"
            self.cor_titulo = "#FF00E6"
            self.font_titulo = ("Arial", 20, "bold")
            self.font_narrativa = ("Arial", 12)
            self.font_subtitulo = ("Arial", 10, "bold")
            self.cor_alerta = "#FF4500"
            self.cor_sucesso = "#00FF00"
            self.cor_backtrack = "#00FFFF"

    def _limpar_frame(self):
        for w in self.base_content_frame.winfo_children():
            w.destroy()

    def iniciar_missao_contexto(self, image_to_display=None):
        self._limpar_frame()

        try:
            image_path = os.path.join("JogoGrafos", "img", "missao3_grafos.png") 
            img = Image.open(image_path)
            img = img.resize((380, 250), Image.Resampling.LANCZOS) 
            self.tk_image = ImageTk.PhotoImage(img) 
            img_label = tk.Label(self.base_content_frame, image=self.tk_image, bg=self.cor_fundo)
            img_label.pack(pady=10)
        except (FileNotFoundError, NameError):
            tk.Label(self.base_content_frame, text="(Imagem missao3_grafos.png não carregada)", fg=self.cor_alerta, bg=self.cor_fundo).pack(pady=5)


        tk.Label(
            self.base_content_frame,
            text="Missão 3: Infiltração na Base (Busca em Profundidade)",
            font=self.font_titulo,
            fg=self.cor_titulo,
            bg=self.cor_fundo
        ).pack(pady=(10, 6))

        contexto = (
            "**Comandante Ackbar:** É uma armadilha! Precisamos plantar o explosivo no núcleo imperial. "
            "Os túneis de ventilação formam um grafo complexo. Sua tarefa é usar o **DFS (Busca em Profundidade)** para encontrar o caminho, explorando cada túnel até o fim.\n\n"
            "**Foco:** Observe o **Backtracking**. Quando você chegar a um beco sem saída (uma folha), o algoritmo deve **RECUAR** (retornar da recursão) para o último ponto de decisão."
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
            text="Iniciar Infiltração",
            command=self._iniciar_missao,
            style="Accent.Dark.TButton"
        ).pack(pady=10)

    def _iniciar_missao(self):
        self._resetar_dfs()
        self._montar_tela_missao()

    def _resetar_dfs(self):
        self.visited.clear()
        self.path.clear()
        self.is_finished = False
        self.current_index = 0
        self.current_node = self.start_node
        _, self.path_solution = get_dfs_path(self.graph, self.start_node)
        self.visited.add(self.start_node)

    def _montar_tela_missao(self):
        self._limpar_frame()

        tk.Label(self.base_content_frame, text="Busca em Profundidade (DFS)", font=self.font_titulo, fg=self.cor_titulo, bg=self.cor_fundo).pack(pady=(8, 2))

        main = tk.Frame(self.base_content_frame, bg=self.cor_fundo)
        main.pack(fill=tk.BOTH, expand=True, padx=10, pady=8)

        left = tk.Frame(main, bg=self.cor_fundo, width=340)
        left.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left.pack_propagate(False)

        right = tk.Frame(main, bg=self.cor_fundo)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.lbl_path = tk.Label(left, text=f"Caminho Atual: {list(self.visited)}", font=self.font_subtitulo, fg=self.cor_texto, bg=self.cor_fundo, wraplength=300, justify=tk.LEFT)
        self.lbl_status = tk.Label(left, text="Iniciando no Núcleo. Explorar em profundidade!", font=self.font_narrativa, fg=self.cor_titulo, bg=self.cor_fundo, wraplength=300, justify=tk.LEFT)
        
        self.lbl_path.pack(anchor="w", pady=(8, 2))
        self.lbl_status.pack(anchor="w", pady=(8, 10))
        
        self.btn_next = ttk.Button(left, text="Próximo Passo (Recursão)", command=self._proximo_passo)
        self.btn_next.pack(fill=tk.X, pady=(10, 4))
        
        self.canvas = tk.Canvas(right, bg=self.cor_fundo, highlightthickness=0, height=400)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self._desenhar_grafo()

    def _proximo_passo(self):
        if self.current_index >= len(self.path_solution):
            self.lbl_status.config(text="DFS concluído. O caminho de infiltração foi mapeado!", fg=self.cor_sucesso)
            self.btn_next.config(state="disabled")
            ttk.Button(self.base_content_frame, text="Concluir Missão", command=self._finalizar_missao, style="Accent.Dark.TButton").pack(pady=20)
            return

        next_node = self.path_solution[self.current_index]
        prev_node = self.path_solution[self.current_index - 1] if self.current_index > 0 else None
        
        self.current_node = next_node
        
        if next_node not in self.visited:
            self.visited.add(next_node)
            self.lbl_status.config(text=f"Avançando: {prev_node} -> {next_node}. Recursão (Entrando em Profundidade)!", fg=self.cor_titulo)
        elif next_node == prev_node:

             self.lbl_status.config(text=f"*** RECUO TÁTICO ***: Backtracking! Saindo da recursão (Pilha vazia).", fg=self.cor_alerta)
        else:
             self.lbl_status.config(text=f"Retornando: {prev_node} -> {next_node}. Backtracking!", fg=self.cor_backtrack)

        self.current_index += 1

        
        self.lbl_path.config(text=f"Caminho de Visita: {self.path_solution[:self.current_index]}")
        self._desenhar_grafo()

    def _desenhar_grafo(self):
        if not self.canvas: return
        self.canvas.delete("all")
        
        pos = {"Núcleo": (350, 50), "A": (250, 150), "B": (450, 150), 
               "C": (150, 250), "D": (350, 250), "E": (550, 250),
               "F": (150, 350), "G": (350, 350), "H": (550, 350)}
        
        for u, neighbors in self.graph.items():
            x1, y1 = pos[u]
            for v in neighbors:
                x2, y2 = pos[v]
                self.canvas.create_line(x1, y1, x2, y2, fill="#555555", width=2)
        
        # Desenhar nós
        r = 20
        for node, (x, y) in pos.items():
            fill = "#333333"
            outline = "#eeeeee"
            text_color = "#ffffff"
            
            if node == self.start_node:
                outline = self.cor_titulo
            if node in self.visited:
                fill = "#005f87"
            if node == self.current_node:
                fill = self.cor_alerta
                
            self.canvas.create_oval(x - r, y - r, x + r, y + r, fill=fill, outline=outline, width=3)
            self.canvas.create_text(x, y, text=node, fill=text_color, font=("Arial", 10, "bold"))

    def _finalizar_missao(self):
        self.game_manager.mission_completed("Missao3")
    
    def retry_mission(self):
        self._iniciar_missao()