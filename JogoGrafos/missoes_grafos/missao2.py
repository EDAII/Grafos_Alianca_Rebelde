# missao2.py - Fortemente Conectado (Grafo)
import tkinter as tk
from tkinter import ttk, messagebox
import os
from PIL import Image, ImageTk 
from collections import deque
import random

# Importa o algoritmo (assumindo que o strong_connect.py está na pasta correta)
from algoritmos_grafos.strong_connect import is_strongly_connected_component, get_transposed_graph, _bfs_check

class Missao2:
    """
    Missão 2: Estabilidade das Rotas – Fortemente Conectado (SCC)
    Simulação interativa passo a passo com validação estrita da decisão do jogador.
    """
    def __init__(self, root, game_manager, content_frame):
        self.root = root
        self.game_manager = game_manager
        self.base_content_frame = content_frame

        # Grafo de Desafio: NÃO Fortemente Conectado (Hoth isolado)
        self.graph_original = {
            "Tatooine": ["Naboo", "Coruscant"], "Naboo": ["Coruscant"], "Coruscant": ["Endor"], 
            "Endor": ["Dagobah"], "Dagobah": ["Tatooine", "Hoth"], "Hoth": ["Dagobah"]
        }
        self.start_node = "Tatooine"
        self.all_nodes = set(self.graph_original.keys())
        
        self.current_step = 0
        self.max_steps = 6 
        
        self.transposed_graph = get_transposed_graph(self.graph_original)
        self.is_scc_gabarito = self._is_scc_gabarito_calc() # Gabarito é False para este grafo
        
        self.status_message = "Pronto para iniciar o diagnóstico."
        self.graph_to_draw = self.graph_original
        self.visited_original = set()
        self.visited_transposed = set()
        self.is_connected = False
        
        self.bfs_queue = deque()
        self.bfs_visited = set()
        self.current_bfs_node = None
        self.levels = {} 
        
        self.btn_next = None
        self.next_command = "INICIAR"
        
        # Inicialização dos atributos de UI
        self.lbl_listas = None
        self.lbl_etapa = None
        self.lbl_fila = None
        self.lbl_status = None
        self.lbl_alcan = None
        self.lbl_graph_type = None
        self.controls_frame = None
        self.lbl_levels = None 

        self._carregar_estilos()
        
        self.conceitos = {
            "BUSCA EM LARGURA (BFS)": "Explora o grafo em camadas, usando uma FILA (FIFO) para garantir que os nós mais próximos (menor distância) sejam visitados primeiro. O nó inicial está na Camada 0.",
            "GRAFO REVERSO (G^T)": "Um grafo onde a direção de TODAS as arestas foi invertida. É essencial para verificar se há um caminho de VOLTA para o nó inicial, provando a conectividade.",
            "FORTEMENTE CONECTADO (SCC)": "Um conjunto de nós é SCC se, e somente se, todos os nós são alcançáveis a partir de um nó inicial no grafo original (G) E no grafo reverso (G^T).",
        }

    def _is_scc_gabarito_calc(self):
        """Calcula o resultado SCC real para usar como gabarito."""
        visited_orig = _bfs_check(self.graph_original, self.start_node)
        transposed_graph = get_transposed_graph(self.graph_original)
        visited_trans = _bfs_check(transposed_graph, self.start_node)
        
        return (len(visited_orig) == len(self.all_nodes)) and (len(visited_trans) == len(self.all_nodes))

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
            self.cor_dica = "#00FFFF"
            self.cor_processando = "#FFFF00"
        except AttributeError:
            self.cor_fundo = "black"
            self.cor_texto = "white"
            self.cor_titulo = "#FF00E6"
            self.font_titulo = ("Arial", 20, "bold")
            self.font_narrativa = ("Arial", 12)
            self.font_subtitulo = ("Arial", 10, "bold")
            self.cor_alerta = "#FF4500"
            self.cor_sucesso = "#00FF00"
            self.cor_dica = "#00FFFF"
            self.cor_processando = "#FFFF00"

    def _limpar_frame(self):
        for w in self.base_content_frame.winfo_children():
            w.destroy()
            
    def _resetar_estado_bfs(self):
        """Reinicia filas, visitados e níveis para um novo diagnóstico."""
        self.bfs_queue.clear()
        self.bfs_visited.clear()
        self.visited_original.clear()
        self.visited_transposed.clear()
        self.levels.clear()
        self.current_bfs_node = None
        self.graph_to_draw = self.graph_original
        self.current_graph = self.graph_original


    def iniciar_missao_contexto(self, image_to_display=None):
        self._limpar_frame()

        try:
            image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "img", "missao2_grafos.png")
            img = Image.open(image_path)
            img = img.resize((380, 250), Image.Resampling.LANCZOS) 
            self.tk_image = ImageTk.PhotoImage(img) 
            img_label = tk.Label(self.base_content_frame, image=self.tk_image, bg=self.cor_fundo)
            img_label.pack(pady=10)
        except (FileNotFoundError, NameError):
            tk.Label(self.base_content_frame, text="(AVISO: Imagem missao2_grafos.png não carregada)", fg=self.cor_alerta, bg=self.cor_fundo).pack(pady=5)

        tk.Label(
            self.base_content_frame,
            text="Missão 2: Estabilidade das Rotas (Fortemente Conectado)",
            font=self.font_titulo,
            fg=self.cor_titulo,
            bg=self.cor_fundo
        ).pack(pady=(10, 6))

        contexto = (
            "**Comandante Organa:** O Império sabotou os hiper-roteadores! Rotas unidirecionais significam que nossa frota pode ir, mas não voltar. "
            "A frota só está segura se o conjunto de sistemas for **Fortemente Conectado (SCC)**: garantindo o caminho de IDA e o caminho de VOLTA.\n\n"
            "**Procedimento:** Usaremos a lógica do Grafo Reverso e Duas BFS para diagnosticar a conectividade."
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
            text="Iniciar Diagnóstico",
            command=self._iniciar_diagnostico,
            style="Accent.Dark.TButton"
        ).pack(pady=10)

    def _iniciar_diagnostico(self):
        """Configura o estado inicial para a primeira BFS e monta a tela."""
        self._resetar_estado_bfs()
        
        self.current_step = 1
        
        # Estado inicial do BFS (Tatooine na Camada 0)
        self.bfs_queue.append(self.start_node)
        self.bfs_visited.add(self.start_node)
        self.visited_original.add(self.start_node)
        self.current_bfs_node = self.start_node
        self.levels[self.start_node] = 0
        
        self.status_message = "1. INÍCIO DA BFS DE IDA (G). Nó inicial (Tatooine) na fila."
        self.next_command = "AVANCAR_BFS"
        self._montar_tela_missao()

    def _formatar_listas(self, graph):
        """Formata as listas de adjacência para o painel lateral."""
        lines = []
        for node in sorted(graph.keys()):
            neighbors = " -> ".join(graph.get(node, []))
            if not neighbors:
                 neighbors = "(Nenhum Destino)"
            lines.append(f"{node}: {neighbors}")
        return "\n".join(lines)

    def _montar_tela_missao(self):
        self._limpar_frame()

        tk.Label(self.base_content_frame, text="Diagnóstico de Conectividade", font=self.font_titulo, fg=self.cor_titulo, bg=self.cor_fundo).pack(pady=(8, 2))

        main = tk.Frame(self.base_content_frame, bg=self.cor_fundo)
        main.pack(fill=tk.BOTH, expand=True, padx=10, pady=8)

        left = tk.Frame(main, bg=self.cor_fundo, width=340)
        left.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left.pack_propagate(False)

        right = tk.Frame(main, bg=self.cor_fundo)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # --- Sub-Painel de Listas de Adjacência (Topo da Direita) ---
        list_frame = tk.Frame(right, bg=self.cor_fundo)
        list_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(list_frame, text="LISTAS DE ADJACÊNCIA (ROTAS ATUAIS):", font=self.font_subtitulo, fg=self.cor_dica, bg=self.cor_fundo).pack(anchor="w")
        
        self.lbl_listas = tk.Label(list_frame, text=self._formatar_listas(self.graph_to_draw), font=("Arial", 9), fg=self.cor_texto, bg=self.cor_fundo, justify=tk.LEFT)
        self.lbl_listas.pack(anchor="w")

        # --- Elementos de Controle (Esquerda) ---
        self.lbl_etapa = tk.Label(left, text=f"ETAPA: {self.current_step} / 4", font=self.font_subtitulo, fg=self.cor_titulo, bg=self.cor_fundo)
        
        self.lbl_fila = tk.Label(left, text=f"FILA (Próximos a visitar): {list(self.bfs_queue)}", font=self.font_subtitulo, fg=self.cor_dica, bg=self.cor_fundo, wraplength=300, justify=tk.LEFT)
        self.lbl_levels = tk.Label(left, text=f"CAMADAS (Distância): {self.levels}", font=("Arial", 9), fg=self.cor_texto, bg=self.cor_fundo, wraplength=300, justify=tk.LEFT)

        self.lbl_status = tk.Label(left, text=self.status_message, font=self.font_narrativa, fg=self.cor_texto, bg=self.cor_fundo, wraplength=300, justify=tk.LEFT)
        self.lbl_graph_type = tk.Label(left, text="Grafo Atual: Original (G)", font=self.font_subtitulo, fg=self.cor_sucesso, bg=self.cor_fundo)
        
        visited_set = self.visited_transposed if self.current_step >= 3 else self.visited_original
        label_text = f"Sistemas Alcançados: {sorted(list(visited_set))}" if visited_set else "Sistemas Alcançados: {Nenhum}"
        self.lbl_alcan = tk.Label(left, text=label_text, font=self.font_subtitulo, fg=self.cor_texto, bg=self.cor_fundo, wraplength=300, justify=tk.LEFT)
        
        self.lbl_etapa.pack(anchor="w", pady=(8, 2))
        self.lbl_fila.pack(anchor="w", pady=2)
        self.lbl_levels.pack(anchor="w", pady=2)
        self.lbl_alcan.pack(anchor="w", pady=5)
        self.lbl_status.pack(anchor="w", pady=(8, 10))
        self.lbl_graph_type.pack(anchor="w", pady=5)
        
        # Área de botões de decisão
        self.controls_frame = tk.Frame(left, bg=self.cor_fundo)
        self.controls_frame.pack(fill=tk.X, pady=(10, 4))
        
        self.btn_next = ttk.Button(self.controls_frame, text="Iniciar Diagnóstico", command=self._proximo_passo)
        self.btn_next.pack(fill=tk.X)
        
        # Botão de Ajuda
        ttk.Button(left, text="Ajuda / Conceitos", command=self._mostrar_conceito_ajuda).pack(fill=tk.X, pady=5)
        
        # Canvas de desenho (Abaixo das listas de adjacência na direita)
        self.canvas = tk.Canvas(right, bg=self.cor_fundo, highlightthickness=0, height=350)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self._desenhar_grafo()
        self._atualizar_controles_etapa()

    def _executar_bfs_step(self):
        """Executa um único passo da BFS (desenfileira, processa vizinhos, enfileira)."""
        if not self.bfs_queue:
            return False 

        u = self.bfs_queue.popleft()
        self.current_bfs_node = u
        
        new_nodes = []
        current_level = self.levels.get(u, 0)
        next_level = current_level + 1

        for v in self.current_graph.get(u, []):
            if v not in self.bfs_visited:
                self.bfs_visited.add(v)
                self.bfs_queue.append(v)
                self.levels[v] = next_level
                new_nodes.append(v)
        
        if self.current_step == 1:
            self.visited_original.update(new_nodes)
            status_prefix = "IDA (G)"
        elif self.current_step == 3:
            self.visited_transposed.update(new_nodes)
            status_prefix = "VOLTA (G^T)"

        if new_nodes:
            self.status_message = f"[{status_prefix}] Processado {u} (Camada {current_level}). Novos sistemas alcançados: {', '.join(new_nodes)}"
        else:
            self.status_message = f"[{status_prefix}] Processado {u} (Camada {current_level}). Fim de rota, nenhum vizinho novo enfileirado."
        
        return True 

    def _validar_decisao(self, action_voto):
        """
        Valida a decisão do jogador contra o gabarito real.
        """
        
        is_scc_gabarito = self.is_scc_gabarito
        
        # 1. VALIDAÇÃO NA DECISÃO REVERSO (Após a BFS de Ida)
        if self.current_step == 2:
            bfs1_falhou = len(self.all_nodes) != len(self.visited_original)
            
            if action_voto == "FALHA_PRECOCE":
                if bfs1_falhou:
                    self.current_step = 6
                    self._finalizar_missao(is_scc=False, msg="O Analista concluiu a falha após a primeira BFS. Decisão correta.")
                    return
                else:
                    self.status_message = "❌ Erro! A BFS de Ida alcançou TUDO. Você DEVE testar o Reverso para confirmar o retorno. Decisão Incorreta."
                    return
            elif action_voto == "MONTAR_REVERSO":
                if bfs1_falhou:
                    self.status_message = "❌ Erro! A BFS de Ida falhou. Não há por que montar o Reverso (Perda de tempo/recursos). Decisão Incorreta."
                    return
                else:
                    self.current_step = 3 
                    self._proximo_passo(action="MONTAR_REVERSO")
                    return

        # 2. VALIDAÇÃO FINAL (Após a BFS de Volta)
        elif self.current_step == 4:
            is_scc_voto = True if action_voto == "VEREDITO_SCC" else False
            
            # NOTA: O gabarito é SCC, então a decisão correta é VEREDITO_SCC
            if is_scc_voto == self.is_scc_gabarito:
                self.current_step = 6 
                self._finalizar_missao(is_scc=is_scc_voto, msg="")
                return
            else:
                gabarito_msg = "Fortemente Conectado" if self.is_scc_gabarito else "Fracamente Conectado"
                self.status_message = f"❌ Erro! O diagnóstico real é: {gabarito_msg}. Sua decisão está errada."
                return
        
        self._montar_tela_missao()

    def _proximo_passo(self, action=None):
        
        if self.next_command == "AVANCAR_BFS":
            if self.bfs_queue:
                self._executar_bfs_step()
            else:
                self.next_command = "DECISAO_REVERSO" if self.current_step == 1 else "DECISAO_FINAL"
                self.current_bfs_node = None
                self.current_step = 2 if self.current_step == 1 else 4
                self.status_message = "BFS CONCLUÍDA. Analise o resultado e tome a decisão crítica."
                
                # Mensagem de conclusão da BFS de Volta (Step 4)
                if self.current_step == 4:
                    if len(self.all_nodes) == len(self.visited_transposed):
                         messagebox.showinfo("Resultado da BFS Reversa", "SUCESSO! O Grafo Reverso alcançou TODOS os nós. O caminho de volta está garantido!")
                    else:
                         messagebox.showinfo("Resultado da BFS Reversa", "FALHA! O Grafo Reverso não alcançou todos os nós. O retorno é FRACAMENTE CONECTADO.")
            
        elif self.next_command == "INICIAR":
            self.current_step = 1
            self.next_command = "AVANCAR_BFS"
            self.status_message = "1. INÍCIO DA BFS DE IDA (G). Nó inicial (Tatooine) na fila."

        elif action == "MONTAR_REVERSO":
            self.current_step = 3 
            self.graph_to_draw = get_transposed_graph(self.graph_original)
            self.current_graph = self.transposed_graph

            self.bfs_queue.clear()
            self.bfs_visited.clear()
            self.levels.clear()
            self.bfs_queue.append(self.start_node)
            self.bfs_visited.add(self.start_node)
            self.levels[self.start_node] = 0
            
            self.status_message = "3. GRAFO REVERSO CONSTRUÍDO. Iniciando BFS de Volta (G^T)."
            self.lbl_graph_type.config(text="Grafo Atual: Transposto (G^T)", fg=self.cor_titulo)
            self.next_command = "AVANCAR_BFS"
            self.current_bfs_node = self.start_node 
        
        elif action in ["FALHA_PRECOCE", "VEREDITO_SCC", "VEREDITO_NAO_SCC"]:
            self._validar_decisao(action)
            return
        
        self._montar_tela_missao()

    def _atualizar_controles_etapa(self):
        for widget in self.controls_frame.winfo_children():
            widget.destroy()

        if self.next_command == "AVANCAR_BFS":
            self.btn_next = ttk.Button(self.controls_frame, text=f"Processar Nó Atual (BFS)", command=self._proximo_passo)
            self.btn_next.pack(fill=tk.X)
        elif self.next_command == "DECISAO_REVERSO":
            self.lbl_status.config(text="DECISÃO CRÍTICA: Baseado no resultado da BFS de Ida, monte o Grafo Reverso para o diagnóstico SCC?")
            
            bfs1_falhou = len(self.all_nodes) != len(self.visited_original)
            
            if bfs1_falhou:
                 # Se falhou na IDA, a ÚNICA opção lógica é Falhar Precocemente.
                 ttk.Button(self.controls_frame, text="NÃO, ROTAS FRACAS (Confirma Diagnóstico)", command=lambda: self._validar_decisao("FALHA_PRECOCE")).pack(fill=tk.X, pady=5)
            else:
                 # Se sucedeu na IDA, a única opção lógica é Montar Reverso.
                 ttk.Button(self.controls_frame, text="Sim, Montar Grafo Reverso (G^T)", command=lambda: self._validar_decisao("MONTAR_REVERSO")).pack(fill=tk.X, pady=5)
            
            ttk.Button(self.controls_frame, text="Crítica de Rota: Analisar Alcançabilidade", command=lambda: self._mostrar_critica_ida()).pack(fill=tk.X, pady=5)
            
        elif self.next_command == "DECISAO_FINAL":
            
            if self.is_scc_gabarito == False:
                 self.lbl_status.config(text="VEREDICTO: A conexão é FRACAMENTE CONECTADA. Confirme o diagnóstico.")
                 # Única opção lógica é NÃO
                 ttk.Button(self.controls_frame, text="NÃO, ROTAS FRACAS (Confirma Diagnóstico)", command=lambda: self._validar_decisao("VEREDITO_NAO_SCC")).pack(fill=tk.X, pady=5)
            else:
                 self.lbl_status.config(text="VEREDICTO: Compare BFS(G) e BFS(G^T). A conexão é forte?")
                 # Opções para Grafo Forte (SCC)
                 ttk.Button(self.controls_frame, text="Não, Rotas Fracas", command=lambda: self._validar_decisao("VEREDITO_SCC")).pack(fill=tk.X, pady=2)
            

            ttk.Button(self.controls_frame, text="Crítica de Rota: Analisar o Retorno (G^T)", command=lambda: self._mostrar_critica_volta()).pack(fill=tk.X, pady=5)
            
        elif self.next_command == "FIM":
            ttk.Button(self.controls_frame, text="Concluir Missão", command=self._finalizar_missao, style="Accent.Dark.TButton").pack(fill=tk.X, pady=2)
        else:
            self.btn_next = ttk.Button(self.controls_frame, text="Iniciar Diagnóstico", command=self._proximo_passo)
            self.btn_next.pack(fill=tk.X)

    def _mostrar_conceito_ajuda(self):
        """Exibe uma caixa de diálogo com as definições de BFS, SCC e Grafo Reverso."""
        
        full_message = "\n\n".join([f"**{k}**: {v}" for k, v in self.conceitos.items()])
        
        messagebox.showinfo(
            "Protocolos de Ajuda (Conceitos de Grafo)",
            full_message
        )


    def _mostrar_critica_ida(self):
        """Mostra crítica baseada no resultado da primeira BFS."""
        missed_nodes = self.all_nodes - self.visited_original
        if missed_nodes:
            messagebox.showinfo(
                "Crítica de Rota (Ida)",
                f"Sua BFS de Ida (Grafo Original G) FALHOU em alcançar os sistemas: {', '.join(missed_nodes)}. Lembre-se: para SCC, 100% dos nós devem ser alcançados na IDA."
            )
        else:
            messagebox.showinfo(
                "Crítica de Rota (Ida)",
                "SUCESSO! Sua BFS de Ida alcançou todos os sistemas. A falha, se houver, estará no caminho de volta. Você precisa do Grafo Reverso!"
            )

    def _mostrar_critica_volta(self):
        """Mostra crítica baseada no resultado da BFS reversa."""
        missed_nodes = self.all_nodes - self.visited_transposed
        
        if missed_nodes:
            messagebox.showinfo(
                "Crítica de Rota (Volta)",
                f"Sua BFS de Volta (Grafo Reverso G^T) FALHOU em alcançar os sistemas: {', '.join(missed_nodes)}. Lembre-se: se G^T não alcança todos, o retorno falha! (NÃO SCC)"
            )
        else:
            messagebox.showinfo(
                "Crítica de Rota (Volta)",
                "SUCESSO! O Grafo Reverso alcançou todos os todos os sistemas. O caminho de volta está garantido. (Muito provável que seja SCC)"
            )


    def _desenhar_grafo(self):
        if not self.canvas: return
        self.canvas.delete("all")
        
        pos = {"Tatooine": (100, 150), "Naboo": (250, 50), "Coruscant": (400, 150), 
               "Endor": (400, 300), "Dagobah": (250, 400), "Hoth": (100, 300)}
        
        graph = self.graph_to_draw

        for u, neighbors in graph.items():
            x1, y1 = pos[u]
            for v in neighbors:
                x2, y2 = pos[v]
                self.canvas.create_line(x1, y1, x2, y2, fill="#777777", arrow=tk.LAST, width=2)
        
        r = 25
        for node, (x, y) in pos.items():
            fill = "#333333"
            outline = "#eeeeee"
            text_color = "#ffffff"
            
            if node == self.start_node:
                outline = self.cor_titulo
                fill = "#000080"
            
            if node in self.bfs_visited:
                 fill = "#005f87"
                 
            if node == self.current_bfs_node:
                fill = self.cor_processando
                outline = self.cor_alerta
                
            self.canvas.create_oval(x - r, y - r, x + r, y + r, fill=fill, outline=outline, width=3)
            self.canvas.create_text(x, y, text=node, fill=text_color, font=("Arial", 10, "bold"))

    def _finalizar_missao(self, is_scc=None, msg=""):
        is_scc_gabarito = self._is_scc_gabarito_calc()
        
        if is_scc == is_scc_gabarito:
            self.game_manager.mission_completed("Missao2")
        else:
            gabarito_msg = "Forte" if is_scc_gabarito else "Fraca"
            
            self.game_manager.mission_failed_options(
                self, 
                "Decisão de Diagnóstico Incorreta", 
                f"Sua decisão ({'Forte' if is_scc else 'Fraca'}) não corresponde ao diagnóstico real do sistema ({gabarito_msg}). Analise melhor a BFS de Ida e a de Volta!"
            )
    
    def retry_mission(self):
        self._iniciar_diagnostico()