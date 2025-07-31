# Alien vs Monsters

Um simples jogo de sobrevivência 2D top-down criado em Python com a biblioteca **Pygame Zero**. Controle um alienígena e enfrente hordas de monstros para sobreviver o maior tempo possível, coletando itens e acumulando pontos.

##  Como Jogar

O objetivo é simples: sobreviva, derrote monstros e faça a maior pontuação que conseguir!

* **Movimentação:** Use as teclas `W`, `A`, `S`, `D` para se mover pelo mapa.
* **Tiro:** O tiro é automático e dispara na última direção em que você se moveu.
* **Itens:** Derrote inimigos para que eles deixem itens que melhoram seus atributos (vida, velocidade, cadência de tiro) ou aumentam sua pontuação.

## Recursos

* Movimentação e animações do jogador.
* Sistema de tiro automático com cooldown.
* Inimigos que perseguem o jogador.
* Drop de itens com diferentes efeitos.
* Sistema de pontuação e dificuldade progressiva.
* Menu principal e tela de Game Over.
* Efeitos sonoros e música (com opção de ligar/desligar).

---

## ⚠️ Nota para Avaliação

Para facilitar a avaliação e a demonstração dos recursos, a **velocidade de progressão de dificuldade do jogo foi acelerada**. Isso permite que todos os níveis e mecânicas sejam observados em um período de tempo mais curto.

---

## Como Executar

Você precisará do Python e da biblioteca Pygame Zero instalados.

1.  **Clone o repositório:**

2.  **Instale o Pygame Zero:**
    ```bash
    pip install pgzero
    ```

3.  **Execute o jogo:**
    (Substitua `game.py` pelo nome do seu arquivo principal)
    ```bash
    pgzrun game.py
    ```
