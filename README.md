Cobrinha Supreme:

Jogo da Cobrinha clássico recriado em Python com Pygame — com temas visuais, personagens, níveis de dificuldade, sons, obstáculos e partículas.
Este projeto é uma versão aprimorada do clássico **Jogo da Cobrinha**, desenvolvido em **Python** com a biblioteca **Pygame**. O jogador controla uma cobra que cresce ao comer maçãs, evitando colidir com as paredes, obstáculos e o próprio corpo.
O jogo conta com um **menu interativo completo** que permite personalizar a experiência antes de jogar, sistema de recordes por dificuldade, efeitos visuais com partículas e sons gerados por código.

## 🚀 Como Executar

1. Pré-requisitos
Certifique-se de ter o **Python 3.8+** instalado. Verifique com:

```bash
python --version
```

2. Instalar dependências

```bash
pip install pygame numpy
```

> `numpy` é necessário para a geração de sons procedurais. Se não estiver instalado, o jogo roda normalmente, apenas sem efeitos sonoros.

3. Rodar o jogo

Coloque os três arquivos na mesma pasta:

```
📁 sua-pasta/
├── cobrinha.py
├── cabeca_cobra.png
└── maca.png
```

Depois execute:

```bash
python cobrinha.py
```

---

🎮 Controles
| Tecla | Ação |
|-------|------|
| ← → ↑ ↓ | Mover a cobra |
| W A S D | Mover a cobra (alternativo) |
| ESC | Pausar / voltar ao menu |
| C | Continuar após game over |
| M | Voltar ao menu |
| S | Sair do jogo |

---

## ⚙️ Funcionalidades

### 🎛️ Menu de Configurações
Ao iniciar, um menu interativo permite configurar:

- **Personagem** — escolha entre 4 opções com visuais únicos
- **Tema visual** — 4 temas com paletas de cores diferentes
- **Dificuldade** — 4 níveis com velocidade e obstáculos variados

Todas as opções são clicáveis com o mouse.

Personagens

| Personagem | Descrição |
|------------|-----------|
| Cobra | A clássica cobra com olhos e língua |
| Lagarta | Verde vibrante com anteninhas |
| Dragão | Forma de chama com olhos dourados |
| Alien | Robótico com antenas e pernas |

🎨 Temas Visuais

| Tema | Paleta |
|------|--------|
| Selva | Verde grama com paredes vermelhas |
| Noite | Azul escuro com neon roxo |
| Deserto | Tons dourados e laranja |
| Gelo | Branco azulado e gelado |

🏆 Dificuldades

| Dificuldade | Velocidade | Obstáculos |
|-------------|-----------|------------|
| Fácil | Lenta | Nenhum |
| Médio | Normal | 3 iniciais |
| Difícil | Rápida | 6 iniciais |
| Insano | Muito rápida | 10 iniciais |


✨ Efeitos Visuais
- **Grade de fundo** para orientação do jogador
- **Paredes coloridas** indicando zona de morte
- **Corpo arredondado** com sombra e brilho
- **Cabeça rotacionada** conforme a direção do movimento
- **Partículas coloridas** ao comer uma maçã

🔊 Sons Procedurais
- **Comer maçã** — bip agudo
- **Morte** — som grave descendente
- **Novo obstáculo** — bip de alerta


📁 Estrutura do Projeto
📁 projeto/
├── cobrinha.py       # Código principal do jogo
├── cabeca_cobra.png  # Imagem da cabeça (fallback)
├── maca.png          # Imagem da maçã (fallback)
└── README.md         # Este arquivo


🛠️ Tecnologias Utilizadas
- **Python 3** — linguagem de programação
- **Pygame** — renderização gráfica, janela e entrada do teclado
- **NumPy** — geração de ondas sonoras procedurais
- **Math / Random** — cálculos para partículas e posicionamento
