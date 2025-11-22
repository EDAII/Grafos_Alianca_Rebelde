# Star Wars: Aliança Rebelde – Rotas da Orla Externa

<div align="center">
    Figura 1: Aliança Rebelde – Rotas da Orla Externa
    <br>
    <img src="https://raw.githubusercontent.com/EDAII/Algoritmos_Grafos_Alianca_Rebelde/main/Imagens/alianca_simbolo.png" width="500">
    <br>
    <br>
</div>

**Número da Lista:** 4  
**Conteúdo da Disciplina:** Grafos

## Alunas
| Matrícula | Aluna |
| -- | -- |
| 21/1039573 | Larissa Stéfane Barboza Santos |
| 21/1029497 | Mylena Angélica Silva Farias |
<br>


### Explorar para sobreviver!

**"Aliança Rebelde – Rotas da Orla Externa"** é um jogo de puzzle e simulação em que o jogador assume o papel de **Analista de Rotas da Rebelião**.  
A frota rebelde captou um **sinal de socorro codificado**, perdido entre os sistemas da Orla Externa.  
Para decifrar a origem, você deve percorrer um **grafo espacial** utilizando os algoritmos de **Grafos**, explorando sistemas em ondas e determinando suas distâncias.

A narrativa segue o universo de Star Wars, com uma abordagem lúdica e didática para o ensino de Grafos.

Para compreender melhor sobre o jogo, suas missões e a relação com os algoritmos de grafos, acesse a [Descrição](Descricao.md).


## Inspiração

Este projeto é a continuidade do universo criado pelas estudantes em módulos anteriores da saga **Aliança Rebelde**, que exploram algoritmos de forma narrativa e visual.  
Após lidar com ordenações, buscas e árvores, a Rebelião agora precisa de **eficiência estratégica em suas rotas espaciais**, nas quais grafos são fundamentais para navegação interestelar.

Os repositórios anteriores podem ser acessados nos links abaixo:

**Projeto de algoritmos**

- [Greed – Aliança Rebelde](https://github.com/projeto-de-algoritmos-2025/Greed_Alianca_Rebelde)  
- [Divide and Conquer – Aliança Rebelde 2](https://github.com/projeto-de-algoritmos-2025/DC_Alianca_Rebelde_2)  
- [Programação Dinâmica – Aliança Rebelde: Confronto Final](https://github.com/projeto-de-algoritmos-2025/PD_Alianca_Rebelde_Confronto_Final)

**Estrutura de dados 2**
- [Algoritmos de Busca – Aliança Rebelde](https://github.com/EDAII/Algoritmos_Busca_Alianca_Rebelde)  
- [Algoritmos de Ordenação – Aliança Rebelde](https://github.com/EDAII/Algoritmos_Ordenacao_Alianca_Rebelde)  
<br>
-[Árvores - Aliança Rebelde](https://github.com/EDAII/Arvores_Alianca_Rebelde)

## Estrutura do Projeto

O jogo é dividido em dois conjuntos de missões, localizados em pastas separadas, mas que compartilham o mesmo tema central de **grafos**:

- `JogoGrafos/` → contém as interfaces e minigames das missões  
- `Grafos/` → contém as implementações dos algoritmos (ex.: BFS)  

<br>

## Missões do Jogo (Desafios de Grafos) em JogoGrafos

Localização da pasta: **JogoGrafos**

**Estruturas Focadas:**  
Busca em Largura (BFS)

Cada missão é um minigame projetado para ensinar visualmente os conceitos fundamentais de grafos.

---

### Missão 1: Sinal de Socorro – Busca em Largura (BFS)

**Objetivo:**  
Percorrer um grafo que representa rotas hiperespaciais e descobrir:
- As camadas (níveis) de cada sistema  
- A distância mínima em saltos a partir da base rebelde  
- O sistema responsável pelo sinal de socorro  

**Operações ensinadas:**  
- Uso da **fila** (queue)  
- Marcação de **visitados**  
- Cálculo de **níveis** (distância em arestas)  
- Exploração dos nós vizinhos em ondas  

**Contexto:**  
Um pedido de socorro rebelde foi criptografado.  
A única pista é que o sinal veio de um dos sistemas conectados pelas rotas espaciais.  
Você deve explorar o grafo utilizando BFS para identificar, de forma eficiente, qual planeta enviou o sinal e em quantos saltos ele está.


---

### Missão 2: *LARISSA*



---

## Dados Utilizados

Para a simulação, foi utilizado um grafo fixo representando:
- Sistemas estelares (nós)  
- Rotas hiperespaciais (arestas)  
- Conexões usadas pela Rebelião  

Os nós são planetas/estações, e as arestas representam rotas possíveis.  
Esses dados são convertidos para estruturas de lista de adjacência utilizadas no BFS.

<br>

## Link do vídeo

[Assista ao vídeo aqui](LINK)

<br>

## Screenshots

### Intro

<div align="center">
    Figura 2: Introdução do jogo
    <br>
    <img src="https://github.com/EDAII/Grafos_Alianca_Rebelde/blob/main/screenshots/intro_grafos.png?raw=true" width="500">
    <br><br>
</div>

### Missão 1 – BFS

<div align="center">
    Figura 3: Introdução missão 1
    <br>
    <img src="https://github.com/EDAII/Grafos_Alianca_Rebelde/blob/main/screenshots/intro_missao_1.png?raw=true" width="500">
    <br><br>
</div>

<div align="center">
    Figura 4: Missão 1 concluída
    <br>
    <img src="https://github.com/EDAII/Grafos_Alianca_Rebelde/blob/main/screenshots/missao1_grafos_concluida.png?raw=true" width="500">
    <br><br>
</div>

---

## Instalação

### 1. Pré-requisitos

Antes de começar, certifique-se de que você tem os seguintes softwares instalados:
* **Python 3:** (versão 3.7 ou superior)  
* **Git:** para clonar o repositório  
* **Tkinter:** para a interface gráfica  
  - **Linux (Debian/Ubuntu):**  
    `sudo apt-get update && sudo apt-get install python3-tk`  
  - **Windows/macOS:** já vem com o Python  

---

### 2. Configuração do Jogo

1. **Clone o Repositório:**

```bash
git clone git@github.com:EDAII/Algoritmos_Grafos_Alianca_Rebelde.git
cd Algoritmos_Grafos_Alianca_Rebelde/JogoGrafos
