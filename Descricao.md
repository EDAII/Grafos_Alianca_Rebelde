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

### MISSÃO 2: *A definir*  
#### Estrutura: _____

> **Larissa.**  

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
