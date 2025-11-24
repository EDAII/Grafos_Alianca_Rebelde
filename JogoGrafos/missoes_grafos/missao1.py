import tkinter as tk
from tkinter import ttk
from collections import deque

from algoritmos_grafos.bfs import bfs_levels


class Missao1:
    """
    Missão 1: Sinal de Socorro – Busca em Largura (BFS)
    """
    def __init__(self, root, game_manager, content_frame):
        self.root = root
        self.game_manager = game_manager
        self.base_content_frame = content_frame

        
        self.graph = {
            "Base": ["A", "B"],
            "A": ["Base", "C", "D"],
            "B": ["Base", "E"],
            "C": ["A"],
            "D": ["A", "F"],
            "E": ["B", "F"],
            "F": ["D", "E"]
        }
        self.start_node = "Base"

        self.queue = deque()
        self.visited = set()
        self.level = {}
        self.current = None

        # Componentes gráficos
        self.canvas = None
        self.lbl_queue = None
        self.lbl_visited = None
        self.lbl_levels = None
        self.lbl_status = None
        self.btn_next = None

        self.node_positions = {}
        self.node_items = {}

        self._carregar_estilos()

    def _carregar_estilos(self):
        
        try:
            self.cor_fundo = self.game_manager.bg_color_dark
            self.cor_texto = self.game_manager.fg_color_light
            self.cor_titulo = self.game_manager.title_color_accent
            self.font_titulo = self.game_manager.header_font_obj
            self.font_narrativa = self.game_manager.narrative_font_obj
            self.font_subtitulo = self.game_manager.small_bold_font_obj
        except AttributeError:
            
            self.cor_fundo = "#000000"
            self.cor_texto = "#f5f5f5"
            self.cor_titulo = "#FF4AB7"
            self.font_titulo = ("Arial", 20, "bold")
            self.font_narrativa = ("Arial", 12)
            self.font_subtitulo = ("Arial", 10, "bold")

    def _limpar_frame(self):
        for w in self.base_content_frame.winfo_children():
            w.destroy()

    

    def iniciar_missao_contexto(self, image_to_display=None):
       
        self._limpar_frame()

        tk.Label(
            self.base_content_frame,
            text="Missão 1: Sinal de Socorro – Busca em Largura (BFS)",
            font=self.font_titulo,
            fg=self.cor_titulo,
            bg=self.cor_fundo
        ).pack(pady=(10, 6))

        if image_to_display:
            tk.Label(
                self.base_content_frame,
                image=image_to_display,
                bg=self.cor_fundo
            ).pack(pady=(8, 10))

        contexto = (
            "Centro de Comando Rebelde: captamos um sinal de socorro vindo da Orla Externa.\n"
            "Os mapas estelares foram corrompidos pelo Império e precisamos reconstruir as rotas.\n\n"
            "Sua tarefa é percorrer os sistemas em ondas, a partir da Base Rebelde, usando o algoritmo "
            "de Busca em Largura (BFS).\n\n"
            "Descubra quais sistemas estão em cada nível de distância e identifique, ao final, "
            "a origem do sinal. Que a Força guie seus passos."
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
            text="Iniciar Missão",
            command=self._iniciar_missao,
            style="Accent.Dark.TButton"
        ).pack(pady=10)

    

    def _iniciar_missao(self):
        self._resetar_bfs()
        self._montar_tela_bfs()

    def _resetar_bfs(self):
        self.queue.clear()
        self.visited.clear()
        self.level.clear()
        self.current = None

        # Estado inicial do BFS
        self.visited.add(self.start_node)
        self.level[self.start_node] = 0
        self.queue.append(self.start_node)

    def _montar_tela_bfs(self):
        self._limpar_frame()

        tk.Label(
            self.base_content_frame,
            text="Missão 1: Sinal de Socorro – BFS",
            font=self.font_titulo,
            fg=self.cor_titulo,
            bg=self.cor_fundo
        ).pack(pady=(8, 2))

        narrativa = (
            "Você está na Base Rebelde. Cada sistema estelar é um nó do grafo, e as rotas "
            "hiperespaciais são suas ligações.\n\n"
            "Use a Busca em Largura (BFS) para explorar os sistemas em camadas: primeiro os mais "
            "próximos, depois os mais distantes.\n\n"
            "Acompanhe a fila, os visitados e os níveis de distância enquanto o algoritmo avança."
        )
        tk.Label(
            self.base_content_frame,
            text=narrativa,
            wraplength=820,
            justify=tk.LEFT,
            font=self.font_narrativa,
            fg=self.cor_texto,
            bg=self.cor_fundo
        ).pack(pady=(4, 10), padx=18)

        main = tk.Frame(self.base_content_frame, bg=self.cor_fundo)
        main.pack(fill=tk.BOTH, expand=True, padx=10, pady=8)

        left = tk.Frame(main, bg=self.cor_fundo, width=340)
        left.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left.pack_propagate(False)

        right = tk.Frame(main, bg=self.cor_fundo)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Labels de estado
        self.lbl_queue = tk.Label(
            left,
            text=f"Fila: {list(self.queue)}",
            font=self.font_subtitulo,
            fg=self.cor_texto,
            bg=self.cor_fundo
        )
        self.lbl_visited = tk.Label(
            left,
            text=f"Visitados: {list(self.visited)}",
            font=self.font_subtitulo,
            fg=self.cor_texto,
            bg=self.cor_fundo
        )
        self.lbl_levels = tk.Label(
            left,
            text=f"Níveis: {self.level}",
            font=self.font_subtitulo,
            fg=self.cor_texto,
            bg=self.cor_fundo,
            wraplength=320,
            justify=tk.LEFT
        )
        self.lbl_status = tk.Label(
            left,
            text=(
                "BFS iniciado a partir da Base.\n"
                "Clique em 'Próximo passo' para explorar o próximo sistema."
            ),
            font=self.font_narrativa,
            fg="#ffd54a",
            bg=self.cor_fundo,
            wraplength=320,
            justify=tk.LEFT
        )

        self.lbl_queue.pack(anchor="w", pady=(8, 2))
        self.lbl_visited.pack(anchor="w", pady=2)
        self.lbl_levels.pack(anchor="w", pady=2)
        self.lbl_status.pack(anchor="w", pady=(8, 10))

        # Botões de controle
        controls = tk.Frame(left, bg=self.cor_fundo)
        controls.pack(fill=tk.X, pady=(6, 2))

        self.btn_next = ttk.Button(
            controls,
            text="Próximo passo",
            command=self._proximo_passo
        )
        self.btn_next.pack(side=tk.LEFT, padx=4, pady=2)

        ttk.Button(
            controls,
            text="Reiniciar missão",
            command=self._iniciar_missao
        ).pack(side=tk.LEFT, padx=4, pady=2)

        ttk.Button(
            left,
            text="Sair da Missão",
            command=self._sair,
            style="Dark.TButton"
        ).pack(fill=tk.X, pady=(10, 4))

        # Botão de concluir missão (habilita só no final)
        self.btn_concluir = ttk.Button(
            left,
            text="Concluir Missão",
            command=self._finalizar_missao,
            style="Accent.Dark.TButton",
            state="disabled"
        )
        self.btn_concluir.pack(fill=tk.X, pady=(4, 8))

        # Canvas do grafo
        self.canvas = tk.Canvas(right, bg=self.cor_fundo, highlightthickness=0, height=400)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self._desenhar_grafo()

    def _desenhar_grafo(self):
        if not self.canvas:
            return
        self.canvas.delete("all")

        # Posições fixas dos nós (ajuste como quiser)
        self.node_positions = {
            "Base": (350, 220),
            "A": (220, 120),
            "B": (220, 320),
            "C": (120, 60),
            "D": (120, 180),
            "E": (120, 360),
            "F": (80, 240),
        }

        # Desenhar arestas (não dirigidas)
        drawn_edges = set()
        for u, vizinhos in self.graph.items():
            x1, y1 = self.node_positions[u]
            for v in vizinhos:
                if (v, u) in drawn_edges:
                    continue
                x2, y2 = self.node_positions[v]
                self.canvas.create_line(x1, y1, x2, y2, fill="#555555")
                drawn_edges.add((u, v))

        # Desenhar nós
        self.node_items = {}
        for node, (x, y) in self.node_positions.items():
            r = 20

            # cor base
            fill = "#333333"
            outline = "#eeeeee"
            text_color = "#ffffff"

            if node == self.start_node:
                fill = "#b58900"  # destaque da base
            if node in self.visited:
                fill = "#005f87"  # visitados
            if node == self.current:
                fill = "#d33682"  # nó atual em processamento

            circle = self.canvas.create_oval(x - r, y - r, x + r, y + r,
                                             fill=fill, outline=outline, width=2)
            text = self.canvas.create_text(x, y, text=node, fill=text_color)
            self.node_items[node] = (circle, text)

    def _atualizar_labels(self):
        self.lbl_queue.config(text=f"Fila: {list(self.queue)}")
        self.lbl_visited.config(text=f"Visitados: {list(self.visited)}")
        self.lbl_levels.config(text=f"Níveis: {self.level}")

    def _proximo_passo(self):
        if not self.queue:
            self.lbl_status.config(
                text="BFS concluído! Todos os sistemas alcançáveis foram visitados."
            )
            self.btn_next.config(state="disabled")
            self.btn_concluir.config(state="normal")
            self.current = None
            self._desenhar_grafo()
            return

        # Pega o próximo da fila
        u = self.queue.popleft()
        self.current = u

        # Explora vizinhos
        for v in self.graph.get(u, []):
            if v not in self.visited:
                self.visited.add(v)
                self.level[v] = self.level[u] + 1
                self.queue.append(v)

        self.lbl_status.config(
            text=f"Processando sistema {u}. Vizinhos não visitados foram adicionados à fila."
        )
        self._atualizar_labels()
        self._desenhar_grafo()


    def _finalizar_missao(self):
       
        self._limpar_frame()

        tk.Label(
            self.base_content_frame,
            text="Missão Concluída!",
            font=self.font_titulo,
            fg="green",
            bg=self.cor_fundo
        ).pack(pady=(10, 8))

        resumo = (
            "Você percorreu a malha de sistemas da Orla Externa utilizando Busca em Largura.\n\n"
            "As distâncias foram mapeadas, e a Rebelião agora conhece quais sistemas estão "
            "a cada salto da Base.\n\n"
            "Com isso, podemos responder mais rapidamente aos sinais de socorro e esquivar "
            "dos bloqueios do Império."
        )
        tk.Label(
            self.base_content_frame,
            text=resumo,
            wraplength=760,
            justify=tk.CENTER,
            font=self.font_narrativa,
            fg=self.cor_texto,
            bg=self.cor_fundo
        ).pack(pady=10, padx=20)

        ttk.Button(
            self.base_content_frame,
            text="Continuar",
            command=self._encerrar_no_gm,
            style="Accent.Dark.TButton"
        ).pack(pady=16)

    def _encerrar_no_gm(self):
        self.game_manager.mission_completed("Missao1")

    def _sair(self):
        # Se quiser tratar "sair" como falha, você pode chamar mission_failed_options.
        # Aqui, vamos considerar como missão concluída para avançar o fluxo.
        self.game_manager.mission_completed("Missao1")

    def retry_mission(self):
        """
        Método extra caso o GameManager use mission_failed_options e precise
        de um 'Tentar Novamente'.
        """
        self._iniciar_missao()
