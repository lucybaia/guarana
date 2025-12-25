---

# 🦁 Guaraná

> **Guaraná é um Mico-leão-dourado digital que vive no seu PC e troca sua procrastinação por XP.**

## 📜 Sobre o Projeto

O **Guaraná** não é apenas um bichinho virtual fofo. Ele é um **Tamagotchi de Produtividade** open-source desenhado para desenvolvedores que precisam de um empurrãozinho extra para focar.

Inspirado na nostalgia dos anos 90 e na fauna brasileira, o Guaraná gamifica sua rotina:

* 🍅 **Técnica Pomodoro:** Ele foca junto com você.
* ⚡ **Sistema de Energia:** Se você trabalhar demais sem pausas, ele fica exausto.
* 🎮 **RPG:** Ganhe XP codando para desbloquear itens e "skins".

## ✨ Funcionalidades

* **Ciclo de Vida:** O Guaraná sente fome, sono e tédio.
* **Modo Foco (Work):** Ativa um timer (estilo Pomodoro) onde o Guaraná veste seu "capuz de dev" e te acompanha no código.
* **Loja de Itens:** Use o XP ganho trabalhando para comprar bananas, jacas e café virtual.
* **Save Automático:** Seu progresso (e a vida do Guaraná) é salvo localmente. Não deixe ele morrer!

## 🛠️ Tecnologias Utilizadas

* 🐍 **Python 3:** A linguagem base.
* 🖥️ **Tkinter:** Para a interface gráfica (GUI) nativa e leve.
* 💾 **JSON:** Para persistência de dados (Save/Load).
* 🎨 **Pixel Art:** Design visual retro (Assets na pasta `/assets`).

## 🚀 Como Rodar o Guaraná

Pré-requisitos: Você só precisa ter o [Python](https://www.python.org/) instalado.

```bash
# 1. Clone este repositório
git clone https://github.com/lucybaia/guarana.git

# 2. Entre na pasta do projeto
cd guarana

# 3. Execute o mico!
python src/main.py

```

## 🎮 Como Jogar

1. **Inicie o App:** O Guaraná aparecerá no seu desktop.
2. **Verifique os Status:**
* 🍖 **Fome:** Aumenta com o tempo. Se chegar a 100%, game over.
* ⚡ **Energia:** Diminui trabalhando. Recupere dormindo.
* ✨ **XP:** Sua moeda de troca.


3. **Botões:**
* `Focar (25m)`: Inicia um ciclo de trabalho. Ganha muito XP e gasta Energia.
* `Alimentar`: Gasta XP para reduzir a Fome.
* `Descansar`: Recupera Energia (o Guaraná dorme e não pode interagir).



## 🗺️ Roadmap (Próximos Passos)

* [ ] Adicionar sons (efeitos sonoros de 8-bits).
* [ ] Criar sistema de evolução (Bebê -> Jovem -> Rei da Selva).
* [ ] Implementar "Moods" (ele fica bravo se você abre o jogo de madrugada).
* [ ] Adicionar chapéus colecionáveis (Boné do Mario, Bandana do Naruto, etc).

## 🤝 Contribuindo

Pull requests são bem-vindos! Se você desenha pixel art ou sabe melhorar a lógica do Python, sinta-se à vontade para sugerir melhorias.

1. Faça um Fork do projeto
2. Crie sua Feature Branch (`git checkout -b feature/IncrivelFeature`)
3. Commit suas mudanças (`git commit -m 'Add some IncrivelFeature'`)
4. Push para a Branch (`git push origin feature/IncrivelFeature`)
5. Abra um Pull Request

---

<div align="center">

**Feito com 🧡 e muito código por [Seu Nome]**

*Proteja a fauna brasileira (e o seu código)!* 🐒🌳

</div>
