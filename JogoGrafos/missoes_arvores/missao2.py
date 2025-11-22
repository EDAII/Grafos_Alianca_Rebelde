import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk 
import os
import random

# Importa a lógica AVL que atua como gabarito, e a classe do Nó
from algoritmos_arvores.arvores_avl import ArvAVL, NoAVL

class Missao2:
    def __init__(self, root, game_manager, content_frame):
        self.root = root
        self.game_manager = game_manager
        self.base_content_frame = content_frame

        self.MAX_ACOES = 15 

        self.tree = ArvAVL()
        self.lista_inseridos = []

        self.sequencia_acoes = [
            ('I', 30), ('I', 20), ('I', 10),  
            ('I', 40), ('I', 50),            
            ('R', 20),                       
            ('I', 35), ('I', 45),            
            ('I', 42),                       
            ('I', 25),                     
            ('R', 50),
            ('I', 5), ('I', 15), ('I', 12)
        ]
        self.idx_acao = 0
        
        self.rotacoes_corretas = 0
        self.total_rotacoes_aplicadas = 0
        
        self.estado = "INSERINDO"
        self.acao_atual = 'I'
        self.valor_acao = None
        self.no_desbalanceado_valor = None
        self.rotacao_gabarito = None
        self.tipo_imbalance = None 
        self.fb_no_desbalanceado = 0
        self.fb_filho_critico = 0

        self._carregar_estilos()
        self.canvas = None
        
        self.explicacoes_rotacao = {
            'RR': "ROTAÇÃO SIMPLES À DIREITA (LL): Padrão 'Linha' à esquerda (FB Pai e Filho Positivos). Rotação simboliza uma reorganização da frota rebelde.",
            'LL': "ROTAÇÃO SIMPLES À ESQUERDA (RR): Padrão 'Linha' à direita (FB Pai e Filho Negativos). Rotação simboliza uma reorganização da frota rebelde.",
            'LR': "ROTAÇÃO DUPLA ESQUERDA-DIREITA (LR): Padrão 'Zigue-Zague' (FB Pai Positivo, Filho Negativo). Manobra de duas etapas para estabilizar a frota.",
            'RL': "ROTAÇÃO DUPLA DIREITA-ESQUERDA (RL): Padrão 'Zigue-Zague' (FB Pai Negativo, Filho Positivo). Manobra de duas etapas para estabilizar a frota.",
        }

    def _carregar_estilos(self):
        try:
            self.cor_fundo = self.game_manager.bg_color_dark
            self.cor_texto = self.game_manager.fg_color_light
            self.cor_titulo = self.game_manager.title_color_accent
            self.font_titulo = self.game_manager.header_font_obj
            self.font_narrativa = self.game_manager.narrative_font_obj
            self.font_subtitulo = self.game_manager.small_bold_font_obj
            self.cor_desbalanceado = "#FF4500" 
            self.cor_dica = "#00FFFF" 
            self.cor_alerta_cmd = "#FF0000" 
        except AttributeError:
            self.cor_fundo = "black"
            self.cor_texto = "white"
            self.cor_titulo = "yellow"
            self.font_titulo = ("Arial", 20, "bold")
            self.font_narrativa = ("Arial", 12)
            self.font_subtitulo = ("Arial", 10, "bold")
            self.cor_desbalanceado = "#FF4500"
            self.cor_dica = "#00FFFF"
            self.cor_alerta_cmd = "#FF0000"

    def _mostrar_dica_rotacao(self, tipo_rotacao):
        titulo = f"Lógica de Manobra: {tipo_rotacao}"
        mensagem = self.explicacoes_rotacao.get(tipo_rotacao, "Descrição não disponível.")
        messagebox.showinfo(titulo, mensagem)

    def iniciar_missao_contexto(self, image_to_display=None):
        self._limpar_frame()

        try:
            image_path = os.path.join("JogoArvores", "img", "missao2.png") 
            img = Image.open(image_path)
            img = img.resize((380, 250), Image.Resampling.LANCZOS) 
            self.tk_image = ImageTk.PhotoImage(img) 
            img_label = tk.Label(self.base_content_frame, image=self.tk_image, bg=self.cor_fundo)
            img_label.pack(pady=10)
        except FileNotFoundError:
            tk.Label(
                self.base_content_frame,
                text="(AVISO: Imagem missao2.png não encontrada. Verifique o caminho.)",
                fg="#FF0000", bg=self.cor_fundo
            ).pack(pady=5)

        tk.Label(
            self.base_content_frame,
            text="Missão 2: Santuário de Endor – Reorganização de Recursos AVL",
            font=self.font_titulo,
            fg=self.cor_titulo,
            bg=self.cor_fundo
        ).pack(pady=(10, 6))

        contexto = (
            "**MISSAO ÚNICA: SOBREVIVÊNCIA DO ÍNDICE**\n\n"
            "Central Rebelde: Na lua florestal de Endor, nosso banco de dados de recursos é vital. O sistema está sob ataque! "
            "Inserções desordenadas ou remoções causadas pelo inimigo comprometem as defesas da base.\n\n"
            "**Sua Tarefa:** Aplique o algoritmo da **Árvore AVL** para garantir o equilíbrio constante. O Fator de Balanceamento (FB) representa a **estabilidade do comando**. Se o FB for +/- 2, a estabilidade está em risco!"
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
            text="Iniciar Missão (LIGAR SISTEMA AVL)",
            command=self._iniciar_fase,
            style="Accent.Dark.TButton"
        ).pack(pady=10)

    def _limpar_frame(self):
        for w in self.base_content_frame.winfo_children():
            w.destroy()

    def _iniciar_fase(self):
        self._reset_missao()
        self._montar_tela_arvore()

    def _reset_missao(self):
        self.tree = ArvAVL()
        self.lista_inseridos = []
        self.idx_acao = 0
        self.rotacoes_corretas = 0
        self.total_rotacoes_aplicadas = 0
        self.estado = "INSERINDO"
        self.no_desbalanceado_valor = None
        self.rotacao_gabarito = None
        self.tipo_imbalance = None
        self.fb_no_desbalanceado = 0
        self.fb_filho_critico = 0

    def _montar_tela_arvore(self):
        self._limpar_frame()

        tk.Label(
            self.base_content_frame,
            text=f"Missão Única: Sobrevivência do Índice (Ação {self.idx_acao} de {self.MAX_ACOES})",
            font=self.font_titulo,
            fg=self.cor_titulo,
            bg=self.cor_fundo
        ).pack(pady=(8, 2))

        main = tk.Frame(self.base_content_frame, bg=self.cor_fundo)
        main.pack(fill=tk.BOTH, expand=True, padx=10, pady=8)

        left = tk.Frame(main, bg=self.cor_fundo, width=420) 
        left.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left.pack_propagate(False)

        right = tk.Frame(main, bg=self.cor_fundo)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.lbl_inserts = tk.Label(left, text=f"Ações Realizadas: {self.idx_acao}", font=self.font_subtitulo, fg=self.cor_texto, bg=self.cor_fundo)
        self.lbl_rotacoes_corretas = tk.Label(left, text="Manobras Corretas: 0", font=self.font_subtitulo, fg=self.cor_texto, bg=self.cor_fundo)
        self.lbl_total_rotacoes = tk.Label(left, text="Total de Ações: 0", font=self.font_subtitulo, fg=self.cor_texto, bg=self.cor_fundo)
        
        self.lbl_status = tk.Label(left, text="", font=("Arial", 12, "bold"), fg=self.cor_titulo, bg=self.cor_fundo,
                                   wraplength=400, justify=tk.LEFT)
        self.lbl_dica = tk.Label(left, text="Dica: Inicie a indexação e mantenha a vigilância.", 
                                 font=("Arial", 11, "bold"), fg=self.cor_dica, bg=self.cor_fundo,
                                   wraplength=400, justify=tk.LEFT, anchor="w")

        self.lbl_inserts.pack(anchor="w", pady=(8, 2))
        self.lbl_rotacoes_corretas.pack(anchor="w", pady=2)
        self.lbl_total_rotacoes.pack(anchor="w", pady=2)
        self.lbl_status.pack(anchor="w", pady=(8, 10))
        self.lbl_dica.pack(anchor="w", pady=(10, 10))

        controls_acao = tk.Frame(left, bg=self.cor_fundo)
        controls_acao.pack(fill=tk.X, pady=(6, 2))
        self.btn_proxima_acao = ttk.Button(controls_acao, text="EXECUTAR PRÓXIMA AÇÃO", command=self._processar_proxima_acao, style="Accent.Dark.TButton")
        self.btn_proxima_acao.pack(fill=tk.X, padx=4, pady=2)

        self.controls_rotacao = tk.Frame(left, bg=self.cor_fundo)
        
        tk.Label(self.controls_rotacao, text="MANOBRAS DE REORGANIZAÇÃO (APLIQUE NO NÓ VERMELHO):", 
                 font=("Arial", 12, "bold"), fg=self.cor_alerta_cmd, bg=self.cor_fundo).pack(anchor="w", pady=(0, 5), padx=4)
        
        ttk.Button(self.controls_rotacao, text="Rotação SIMPLES: Inverter Desvio (RR/LL)", command=lambda: self._aplicar_rotacao('RR')).pack(fill=tk.X, padx=4, pady=2)
        ttk.Button(self.controls_rotacao, text="Rotação SIMPLES: Inverter Inclinação (LL/RR)", command=lambda: self._aplicar_rotacao('LL')).pack(fill=tk.X, padx=4, pady=2)
        ttk.Button(self.controls_rotacao, text="Rotação DUPLA: Ajuste Interno (LR)", command=lambda: self._aplicar_rotacao('LR')).pack(fill=tk.X, padx=4, pady=2)
        ttk.Button(self.controls_rotacao, text="Rotação DUPLA: Ajuste Cruzado (RL)", command=lambda: self._aplicar_rotacao('RL')).pack(fill=tk.X, padx=4, pady=2)
        
        tk.Label(self.controls_rotacao, text="APRENDIZADO:", 
                 font=("Arial", 10, "bold"), fg=self.cor_dica, bg=self.cor_fundo).pack(anchor="w", padx=4, pady=(8, 2))
                 
        ttk.Button(self.controls_rotacao, text="Lógica de Manobra (Simples) ?", command=lambda: self._mostrar_dica_rotacao('RR')).pack(fill=tk.X, padx=4, pady=2)
        ttk.Button(self.controls_rotacao, text="Lógica de Manobra (Dupla) ?", command=lambda: self._mostrar_dica_rotacao('LR')).pack(fill=tk.X, padx=4, pady=2)
        
        self.controls_rotacao.configure(highlightbackground=self.cor_desbalanceado, highlightthickness=3)
        self.controls_rotacao.pack_forget() 
        
        self.btn_fim_missao = ttk.Button(left, text="FINALIZAR MISSÃO", command=self._finalizar_missao,
                                   state="disabled", style="Accent.Dark.TButton")
        self.btn_fim_missao.pack(fill=tk.X, pady=(10, 4))

        ttk.Button(left, text="Sair do Jogo", command=self._sair, style="Dark.TButton").pack(fill=tk.X, pady=(2, 8))

        self.canvas = tk.Canvas(right, bg=self.cor_fundo, highlightthickness=0, height=400)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self._desenhar_arvore()
        self._atualizar_estado_controles()


    def _processar_proxima_acao(self):
        
        if self.idx_acao >= self.MAX_ACOES:
            self.lbl_status.config(text="Limite de ações atingido. Missão concluída!", fg="#00FF00")
            self.btn_fim_missao.config(state="normal")
            self.btn_proxima_acao.config(state="disabled")
            self._atualizar_estado_controles()
            return
        
        if self.idx_acao < len(self.sequencia_acoes):
            self.acao_atual, self.valor_acao = self.sequencia_acoes[self.idx_acao]
        else:
            self.acao_atual = 'I'
            self.valor_acao = self._gerar_valor_aleatorio()

        self.idx_acao += 1
        valor = self.valor_acao

        
        if self.acao_atual == 'I':
            self.lbl_status.config(text=f"NOVA ORDEM DE INSERÇÃO: Código de Recurso {valor}. Processando...", fg=self.cor_titulo)
            self.lista_inseridos.append(valor)
        
        elif self.acao_atual == 'R':
            if valor in self.lista_inseridos:
                self.lbl_status.config(text=f"ATAQUE IMPERIAL! Código de Recurso {valor} PERDIDO. Reorganizando frota de dados...", fg=self.cor_alerta_cmd)
                self.lista_inseridos.remove(valor)
            else:
                 self.lbl_status.config(text=f"AVISO: Código {valor} não encontrado, ataque falhou. Avançando...", fg=self.cor_titulo)
                 self.idx_acao -= 1 

        self.tree = ArvAVL()
        for v in self.lista_inseridos:
            self.tree.raiz = self._inserir_simples_abb(self.tree.raiz, v) 
        
        
        self._checar_desbalanceamento_pos_acao()


    def _checar_desbalanceamento_pos_acao(self):
        
        no_desb = self._encontrar_primeiro_desbalanceado(self.tree.raiz)
        
        if no_desb:

            self.estado = "AGUARDANDO_ROTACAO"
            self.no_desbalanceado_valor = no_desb.valor
            self.fb_no_desbalanceado = self.tree._get_fb(no_desb)
            
            self.rotacao_gabarito = self._determinar_rotacao_gabarito(no_desb)
            
            if no_desb:
                fb_pai = self.tree._get_fb(no_desb)
                if fb_pai > 0:
                    filho = no_desb.esquerda
                else:
                    filho = no_desb.direita
                self.fb_filho_critico = self.tree._get_fb(filho) if filho else 0
                self.tipo_imbalance = self._obter_tipo_imbalance(no_desb)


            self.lbl_status.config(
                text=f"ALERTA CRÍTICO! A ESTABILIDADE DO COMANDO CAIU! FB +/-2 em {self.no_desbalanceado_valor}.",
                fg=self.cor_alerta_cmd
            )
            self._mostrar_passo_a_passo_crise()

        else:
            self.estado = "INSERINDO"
            
        self._atualizar_metricas()
        self._desenhar_arvore()
        self._atualizar_estado_controles()

    def _encontrar_primeiro_desbalanceado(self, no_atual):
        if no_atual is None:
            return None
        
        desb = self._encontrar_primeiro_desbalanceado(no_atual.esquerda)
        if desb: return desb
        
        desb = self._encontrar_primeiro_desbalanceado(no_atual.direita)
        if desb: return desb
        
        if abs(self.tree._get_fb(no_atual)) > 1:
            return no_atual
        
        return None

    def _determinar_rotacao_gabarito(self, no_desb):
        
        fb_pai = self.tree._get_fb(no_desb)
        
        if fb_pai > 1:
            if no_desb.esquerda and self.tree._get_fb(no_desb.esquerda) >= 0:
                 return 'RR' 
            else:
                 return 'LR' 
        
        elif fb_pai < -1:
            if no_desb.direita and self.tree._get_fb(no_desb.direita) <= 0:
                 return 'LL' 
            else:
                 return 'RL' 
        
        return None

    def _mostrar_passo_a_passo_crise(self):
        
        passo1 = f"1. DIAGNÓSTICO: O ponto de falha mais baixo é o Recurso {self.no_desbalanceado_valor}."
        passo2 = f"2. FB DO NÓ (Pai): O FB deste nó é {self.fb_no_desbalanceado}."
        
        if self.fb_no_desbalanceado > 0:
            lado_critico = "ESQUERDA (Comando Pende para a Esquerda)"
        else:
            lado_critico = "DIREITA (Comando Pende para a Direita)"
            
        passo3 = f"3. LADO CRÍTICO: O desequilíbrio é para a {lado_critico}. O FB do filho nesse lado é {self.fb_filho_critico}."
        
        if self.rotacao_gabarito in ('RR', 'LL'):
            tipo_rot = "SIMPLES"
            logica = "Os FBs (Pai e Filho) têm o mesmo sinal (Linha)."
        else:
            tipo_rot = "DUPLA"
            logica = "Os FBs (Pai e Filho) têm sinais opostos (Zigue-Zague)."

        passo4 = f"4. TIPO DE MANOBRA: O padrão {self.tipo_imbalance} exige uma Reorganização {tipo_rot}. ({logica})"
        
        passo_final = f"COMANDANTE ACKER: \"Analista! Reorganize a frota de dados! Execute a manobra **{self.rotacao_gabarito}** agora!\""
        
        mensagem_passos = f"{passo1}\n{passo2}\n{passo3}\n{passo4}\n\n{passo_final}"

        self.lbl_dica.config(
            text=mensagem_passos,
            fg=self.cor_alerta_cmd,
            justify=tk.LEFT
        )

    def _obter_tipo_imbalance(self, no_desb):
        fb_pai = self.tree._get_fb(no_desb)
        
        if fb_pai > 1:
            if no_desb.esquerda and self.tree._get_fb(no_desb.esquerda) >= 0:
                 return "LL (Esquerda-Esquerda)"
            else:
                 return "LR (Esquerda-Direita)"
        
        elif fb_pai < -1:
            if no_desb.direita and self.tree._get_fb(no_desb.direita) <= 0:
                 return "RR (Direita-Direita)"
            else:
                 return "RL (Direita-Esquerda)"
        
        return "Balanceado (Erro de Lógica)"


    def _inserir_simples_abb(self, no_atual, valor):
        if not no_atual:
            return NoAVL(valor) 
        
        if valor < no_atual.valor:
            no_atual.esquerda = self._inserir_simples_abb(no_atual.esquerda, valor)
        elif valor > no_atual.valor:
            no_atual.direita = self._inserir_simples_abb(no_atual.direita, valor)
        
        self.tree._atualizar_altura(no_atual)
        
        return no_atual

    def _aplicar_rotacao(self, tipo_rotacao_jogador):
        if self.estado != "AGUARDANDO_ROTACAO":
            messagebox.showinfo("Ação Inválida", "Não há desequilíbrio ativo. Execute a próxima ação.")
            return

        self.total_rotacoes_aplicadas += 1
        
        if tipo_rotacao_jogador == self.rotacao_gabarito:
            self.rotacoes_corretas += 1
            
            no_desbalanceado = self.tree.buscar_no(self.no_desbalanceado_valor)
            if no_desbalanceado:
                self._executar_rotacao_no_pai(self.tree.raiz, no_desbalanceado.valor, tipo_rotacao_jogador)
                
                self.no_desbalanceado_valor = None
                self._checar_desbalanceamento_pos_acao()
                
                if self.estado == "INSERINDO":
                    self.lbl_status.config(
                        text=f"Manobra {tipo_rotacao_jogador} BEM SUCEDIDA! Estabilidade do comando restaurada!",
                        fg="#00FF00"
                    )
                    self.lbl_dica.config(
                        text=f"BASE ESTÁVEL: Rotação bem-sucedida. O comando da frota foi restaurado. Continue com a próxima ação.",
                        fg=self.cor_texto
                    )
            
        else:
            self.lbl_status.config(
                text=f"Rotação {tipo_rotacao_jogador} INCORRETA! O comando rejeitou a ação. (-1 tentativa).",
                fg=self.cor_alerta_cmd
            )
            self.lbl_dica.config(
                text=f"COMANDANTE ACKER: \"Erro! O padrão {self.tipo_imbalance} exige a manobra {self.rotacao_gabarito}. Consulte a Lógica de Manobra!\"",
                fg=self.cor_alerta_cmd
            )
            
        self._atualizar_metricas()
        self._desenhar_arvore()
        self._atualizar_estado_controles()


    def _executar_rotacao_no_pai(self, no_atual, valor_no_desbalanceado, tipo_rotacao):
        if no_atual is None:
            return None

        if no_atual.valor == valor_no_desbalanceado:
            return self.tree._realizar_rotacao(no_atual, tipo_rotacao)

        no_atual.esquerda = self._executar_rotacao_no_pai(no_atual.esquerda, valor_no_desbalanceado, tipo_rotacao)
        no_atual.direita = self._executar_rotacao_no_pai(no_atual.direita, valor_no_desbalanceado, tipo_rotacao)
        
        self.tree._atualizar_altura(no_atual)

        return no_atual
    
    def _atualizar_estado_controles(self):
        self.lbl_inserts.config(text=f"Ações Realizadas: {self.idx_acao} de {self.MAX_ACOES}")
        
        if self.estado == "AGUARDANDO_ROTACAO":
            self.btn_proxima_acao.pack_forget()
            self.controls_rotacao.pack(fill=tk.X, pady=(10, 2))
        else:
            self.controls_rotacao.pack_forget()
            self.btn_proxima_acao.pack(fill=tk.X, padx=4, pady=2)

        if self.idx_acao >= self.MAX_ACOES:
             self.btn_proxima_acao.config(state="disabled")
             self.btn_fim_missao.config(state="normal")


    def _atualizar_metricas(self):
        self.lbl_rotacoes_corretas.config(text=f"Manobras Corretas: {self.rotacoes_corretas}")
        self.lbl_total_rotacoes.config(text=f"Total de Ações (Incluindo Erros): {self.total_rotacoes_aplicadas}")

    def _desenhar_arvore(self):
        if not self.canvas: return
        self.canvas.delete("all")

        if self.tree.raiz is None:
            self.canvas.create_text(300, 200, text="(Índice vazio)", fill=self.cor_texto, font=("Arial", 12))
            return

        width = self.canvas.winfo_width() or 700
        start_y = 40
        y_step = 70
        r = 18
        
        node_coords = self._calcular_posicoes(self.tree.raiz, width, start_y, y_step)
        
        for node_valor, (x, y, parent_valor, fb) in node_coords.items():
            if parent_valor is not None and parent_valor in node_coords:
                parent_x, parent_y, _, _ = node_coords[parent_valor]
                self.canvas.create_line(parent_x, parent_y + r, x, y - r, fill="#777777", width=1)
                
        for node_valor, (x, y, parent_valor, fb) in node_coords.items():
            
            fill_color = "#333333" 
            outline_color = self.cor_texto
            
            if node_valor == self.no_desbalanceado_valor:
                fill_color = self.cor_desbalanceado
                outline_color = self.cor_titulo
                
            self.canvas.create_oval(x - r, y - r, x + r, y + r, fill=fill_color, outline=outline_color, width=3 if node_valor == self.no_desbalanceado_valor else 2)
            self.canvas.create_text(x, y, text=str(node_valor), fill="#FFD700", font=("Arial", 10, "bold"))
            
            fb_text = f"FB: {fb}"
            fb_color = "#00FF00" if abs(fb) <= 1 else self.cor_alerta_cmd
            
            self.canvas.create_text(x, y + r + 10, text=fb_text, fill=fb_color, font=("Arial", 9, "bold"))

    def _calcular_posicoes(self, node, width, start_y, y_step):
        if node is None:
            return {}

        node_coords = {}
        queue = [(node, 0, None)]
        
        while queue:
            current_node, depth, parent_val = queue.pop(0)
            if current_node:
                fb = self.tree._get_fb(current_node)
                node_coords[current_node.valor] = [0, start_y + depth * y_step, parent_val, fb]
                if current_node.esquerda:
                    queue.append((current_node.esquerda, depth + 1, current_node.valor))
                if current_node.direita:
                    queue.append((current_node.direita, depth + 1, current_node.valor))
        
        sorted_values = self._get_in_order_values(self.tree.raiz)
        
        if not sorted_values:
            return {}
            
        x_step = width / (len(sorted_values) + 1)
        x_map = {val: x_step * (i + 1) for i, val in enumerate(sorted_values)}

        def _set_x_position(n):
            if n is None:
                return 0, 0
            
            x_left, count_left = _set_x_position(n.esquerda)
            x_right, count_right = _set_x_position(n.direita)
            
            total_children = count_left + count_right
            
            if total_children == 0:
                x = x_map.get(n.valor, width / 2) 
            elif n.esquerda and n.direita:
                x = (x_left + x_right) / 2
            elif n.esquerda:
                x = x_left + (x_step / 2)
            else:
                x = x_right - (x_step / 2)

            node_coords[n.valor][0] = x
            
            return x, total_children + 1

        _set_x_position(node)
        
        final_coords = {val: tuple(coords) for val, coords in node_coords.items()}
        return final_coords


    def _get_in_order_values(self, node):
        if node is None:
            return []
        return (self._get_in_order_values(node.esquerda) + 
                [node.valor] + 
                self._get_in_order_values(node.direita))

    def _gerar_valor_aleatorio(self):
        while True:
            novo_valor = random.randint(1, 100)
            if novo_valor not in self.lista_inseridos:
                return novo_valor

    def _finalizar_missao(self):
        self._limpar_frame()
        self.game_manager.mission_completed("Missao2")

    def _sair(self: 'Missao2') -> None:
        self.game_manager.set_game_state("MISSION_2_SUCCESS")