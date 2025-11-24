# Star Wars: Aliança Rebelde – Rotas da Orla Externa

### Em tempos sombrios, navegação é sobrevivência. A Rebelião enfrenta um novo desafio: mapear rotas seguras pela galáxia enquanto o Império bloqueia sistemas e distorce sinais.  
Você, como **Engenheiro(a) de Rotas da Rebelião**, deve analisar, explorar e reconstruir caminhos estratégicos — antes que o Império intercepte o próximo salto hiperespacial.

### Cada missão do jogo é uma simulação prática de como os **algoritmos de grafos** permitem explorar sistemas, calcular distâncias e revelar caminhos seguros, com uma narrativa imersiva inspirada no universo Star Wars.  
Explorar é resistir.

## EXPLORAR PARA SOBREVIVER!

## Descrição do Jogo

**"Aliança Rebelde – Rotas da Orla Externa"** é um jogo de puzzle e simulação em que o jogador atua como um(a)  
**Analista de Rotas da Rebelião**.

Sua missão é reconstruir a malha de caminhos espaciais da Orla Externa, utilizando **algoritmos de grafos**, começando pela **Busca em Largura (BFS)**.  
Os desafios mostram, de forma visual e interativa, como o BFS percorre sistemas em ondas, determinando distâncias e revelando a origem de sinais de socorro.

O jogo combina **narrativa sci-fi**, **conceitos teóricos de Estrutura de Dados (GRAFOS)** e **simulação educacional**, tornando o aprendizado mais intuitivo e imersivo.

---

## Público-Alvo

- Estudantes da disciplina de **Estrutura de Dados / Grafos**  
- Interessados em **teoria dos grafos aplicada**  
- Fãs do universo **Star Wars** que queiram aprender algoritmos jogando  

---

## Objetivos do Jogo

- **Para o Jogador:** Reconstruir rotas rebeldes, explorando sistemas e calculando distâncias com o algoritmo BFS.  
- **Educacional:** Ensinar de forma prática:
  - A mecânica da **Busca em Largura (BFS)**  


---

## Estrutura do Projeto

O jogo é composto por duas missões principais, cada uma abordando um algoritmo de grafos:

- **JogoGrafos**  
  Contém os minigames, narrativa e interfaces gráficas que representam as missões interativas.

- **Grafos**  
  Contém as implementações dos algoritmos, o **BFS**.

---

## Missões do Jogo (Desafios de Grafos) em JogoGrafos

### MISSÃO 1: Sinal de Socorro  
#### Estrutura: Busca em Largura (BFS)

- **Contexto:**  
  Um sinal de socorro da Rebelião ecoa pela Orla Externa.  
  O Império barrou as rotas principais e distorceu grande parte do mapa estelar.  
  Você deve reconstruir a região, visitando sistemas em ondas a partir da base rebelde,  
  descobrindo:
  - quais sistemas estão a 1 salto,
  - quais estão a 2 saltos,
  - e qual deles foi a origem do pedido de ajuda.

- **Descrição:**  
  A missão consiste em executar o **algoritmo BFS** sobre um grafo espacial:
  - Inserir o sistema inicial na fila  
  - Explorar seus vizinhos  
  - Marcar visitados  
  - Montar as camadas (níveis)  
  - Determinar qual nó está a menor distância  
  - Identificar a origem do sinal de socorro  

- **Conceitos Aprendidos:**  
  - Funcionamento da **fila (queue)**  
  - Propriedade de níveis/camadas do BFS  
  - Menor distância em grafos não ponderados  
  - Exploração sistemática de vizinhos  
  - Vantagens do BFS em mapas estelares  

- **Analogias no Jogo:**  
  Cada **camada descoberta** representa uma expansão do alcance de scanners rebeldes.  
  Cada **visitado** simboliza um sistema analisado e seguro para navegação.  
  O **nível** corresponde ao número de saltos hiperespaciais necessários  
  para sair da base rebelde até cada sistema.

---

### MISSÃO 2: Estabilidade das Rotas
#### Estrutura: Grafo Fortemente Conectado (SCC)

- **Contexto:**
  Um ataque cibernético imperial comprometeu o sistema de navegação. Algumas rotas hiperespaciais se tornaram unidirecionais.
  Para garantir a segurança da frota, é preciso que todos os sistemas sejam **mutuamente alcançáveis** (caminho de ida e caminho de volta).

- **Descrição:**
  A missão consiste em realizar um **diagnóstico SCC** completo para confirmar a estabilidade das rotas:
  - Realizar a Busca em Largura (BFS) no grafo original (G).
  - Construir o **Grafo Reverso** ($\text{G}^\text{T}$), invertendo a direção das rotas.
  - Realizar a BFS no grafo reverso ($\text{G}^\text{T}$).
  - Comparar os resultados para **validar** se o conjunto é Fortemente Conectado.

- **Conceitos Aprendidos:**
  - Definir a **Conectividade Forte** em grafos direcionados.
  - Construir o **Grafo Reverso** ($\text{G}^\text{T}$).
  - Entender a necessidade de **Duas BFS** para provar o SCC.
  - Aplicar **validação estrita** na tomada de decisão.

- **Analogias no Jogo:**
  O **Grafo Reverso** simboliza o teste do caminho de volta.
  A **Estabilidade Total** é alcançada quando o caminho de ida e volta é garantido.
  A **Tomada de Decisão** representa a ordem do Comandante de prosseguir com recursos ou abortar a missão.

---

### MISSÃO 3: Infiltração na Base
#### Estrutura: Busca em Profundidade (DFS)

- **Contexto:**
  É necessário plantar um explosivo no núcleo da base Imperial. Os túneis de ventilação formam um grafo, e cada túnel deve ser explorado para encontrar a rota mais profunda e discreta.
  O caminho deve ser mapeado antes de ser usado.

- **Descrição:**
  A missão consiste em simular a execução do **algoritmo DFS** de forma interativa:
  - Iniciar a **recursão** a partir do nó inicial.
  - Explorar cada rota na **profundidade** máxima.
  - Observar o **Backtracking** (Recuo Tático) ao atingir um beco sem saída.
  - Marcar e registrar o caminho de visita.

- **Conceitos Aprendidos:**
  - Entender o fluxo de **recursão** e o uso da pilha.
  - Identificar o momento do **Backtracking** (revelar o beco sem saída).
  - Mapear a **ordem de visita** do DFS.
  - Contrastar o conceito de Profundidade com Largura (BFS).

- **Analogias no Jogo:**
  A **recursão** simboliza o aprofundamento nos túneis de ventilação.
  O **Backtracking** (Recuo Tático) representa o retorno para o último ponto de decisão no mapa.
  A **Profundidade** da busca corresponde à discrição e complexidade da rota de infiltração.

---

### MISSÃO 4: Negociação de Alianças
#### Estrutura: Grafo Bipartido

- **Contexto:**
  A Princesa Leia precisa formar uma aliança planetária contra o Império. Contudo, alguns planetas são inimigos naturais (conflito de interesse) e só podem se aliar a planetas de um grupo oposto.

- **Descrição:**
  A missão consiste em **colorir** o grafo para verificar se a aliança é estável:
  - Dividir os planetas em dois grupos (Grupo Rebelde - Azul e Grupo Neutro - Vermelho).
  - Garantir que não existam **arestas (ligações) entre planetas da mesma cor**.
  - Identificar se ocorre um **conflito de cor** (prova de que o grafo não é Bipartido).

- **Conceitos Aprendidos:**
  - Definir e identificar um **Grafo Bipartido** (2-colorível).
  - Utilizar o algoritmo de **coloração** para dividir nós em dois conjuntos.
  - Reconhecer que um **conflito de cor** prova a instabilidade da aliança (falha do Grafo Bipartido).
  - Relacionar as arestas com a regra de aliança/inimizade.

- **Analogias no Jogo:**
  A **coloração** representa a separação dos planetas em dois grupos de aliança.
  O **conflito de cor** simboliza a instabilidade da aliança, que o Império pode explorar.
  A **estabilidade** é garantida quando a regra de Bipartição é mantida em todo o conjunto.


---

## Dados Utilizados

Para a simulação das missões, foi construído um grafo representando:
- Sistemas estelares (nós)  
- Rotas hiperespaciais seguras (arestas)  
- Conexões estratégicas da Rebelião  

Cada sistema estelar recebe um identificador (string), organizado em uma **lista de adjacência**, usada pelo BFS.

Esses dados são exibidos visualmente na forma de:
- Pontos (sistemas)
- Arestas (rotas)
- Destaques de cor (fila, visitados, níveis)

---

## Importante!

O jogo possui **duas pastas executáveis**, cada uma com seu `main.py`:

- **JogoGrafos:**  
  Interface gráfica, narrativa e execução visual do BFS.  

- **Grafos:**  
  Implementações dos algoritmos e estruturas necessárias (por enquanto, BFS).  

Ambas as partes trabalham juntas para demonstrar, de forma visual,  
como o grafo é explorado e como o algoritmo determina distâncias.

---

## Conclusão

Em “**Star Wars: Aliança Rebelde – Rotas da Orla Externa**”, explorar é mais que uma técnica —  
é uma questão de sobrevivência.

O domínio do algoritmo **BFS** representa a capacidade da Rebelião  
de navegar pela galáxia mesmo sob bloqueios imperiais,  
descobrindo caminhos seguros, sistemas aliados  
e a origem de pedidos de socorro.

Assim como nas guerras estelares, nos **grafos**,  
cada salto conta — e cada caminho importa.

**A vitória começa com o primeiro nó visitado.**
