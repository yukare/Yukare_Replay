# Yukare Replay System - Scripts

Este repositório contém a lógica modular do sistema **Yukare Replay**. Estes scripts foram projetados para serem agnósticos ao jogo, permitindo sua fácil portabilidade para outros projetos Ren'Py.

---

## 1. Galeria de Replays (`yukare_replay_init.rpy` e `yukare_replay_screen.rpy`)

O sistema escaneia automaticamente o diretório `game/Yukare_Replay/` em busca de labels que comecem com `replay_`.

### Como registrar uma cena:
Adicione metadados em comentários logo após a definição da label:

```renpy
label replay_exemplo_cena:
    ##@person Summer, Lynda        # Nomes das personagens (separados por vírgula)
    ##@title Titulo da Cena        # Nome exibido na galeria
    ##@scene_image thumb_cena      # Imagem da miniatura (opcional)
    ##@tags Oral, Hardcore         # Tags para filtragem (opcional)
    ##@origim label_original       # Label original do jogo para checagem de progresso (opcional)

    # ... código da cena ...
    return
```

### Ordem de Prioridade para Miniaturas:
1. Marcador `##@scene_image`.
2. Primeira instrução `scene` encontrada no bloco da label.
3. Imagem padrão configurada em `yukare_replay_init.rpy`.

---

## 2. Sistema de Janela de Dicas (`yukare_tips.rpy`)

Permite exibir uma janela flutuante com objetivos ou dicas que o jogador pode mover ou fechar.

### Uso via Python:
```python
# Exibir uma dica
python:
    show_tip("Você precisa encontrar a chave no corredor.")

# Esconder a dica
python:
    hide_tip()
```

---

## 3. Tags de Menu e Escolhas Dinâmicas (`yukare_menu_tags.rpy` e `choice_helper.rpy`)

Oferece suporte para estilização de escolhas com base em marcações/tags de texto.

### A) Menus Padrão (`yukare_menu_tags.rpy`)
Intercepta o comportamento padrão do `screen choice` para menus feitos com a instrução `menu:`.
*   `[green]`: Torna a opção verde.
*   `[red]`: Torna a opção vermelha.
*   `[last]`: Adiciona uma seta `»` antes do texto.

### B) Escolhas via Screens (`choice_helper.rpy` e `choice_config.rpy`)
Para jogos que utilizam telas customizadas (screens) com `textbutton` em vez de menus nativos, criamos uma solução desacoplada:
*   **Logica (`choice_helper.rpy`)**: Localizado na pasta `scripts/`, implementa funções de processamento de texto e cor (`get_choice_text`, `get_choice_idle_color`, `get_choice_hover_color`).
*   **Configuração (`choice_config.rpy`)**: Localizado na raiz de `Yukare_Replay/`, define o conjunto de tags de personagens monitorados (ex: `choice_tags = {"amber", "brenda", "karen", "sarah", "maria", "kar"}`).

**Como usar nos textbuttons:**
Qualquer tag cadastrada em `choice_tags` (ex: `[amber]`) colorirá o botão de **verde** e seu sufixo `-red` (ex: `[amber-red]`) o colorirá de **vermelho**, ocultando a tag no texto final.
```renpy
textbutton get_choice_text("Falar com a Amber [amber]") action Jump("label"):
    text_color get_choice_idle_color("Falar com a Amber [amber]", "#ffffff")
    text_hover_color get_choice_hover_color("Falar com a Amber [amber]", "#ff006c")
```

---

## 4. Modo Galeria Aleatória (`yukare_random_gallery.rpy`)

Implementa um sistema que escolhe e reproduz cenas aleatórias da galeria.

- **Fila de Reprodução**: O sistema evita repetir cenas até que todas tenham sido exibidas.
- **Favoritos**: Pode ser configurado para sortear apenas cenas marcadas como favoritas pelo jogador.

---

## 5. Variáveis de Infraestrutura (`yukare_variables.rpy`)

Contém as definições de persistência do mod.
- `persistent.yukare_lock_enabled`: Se `True`, trava cenas não vistas no jogo original.
- `persistent.yukare_pc_name`: Nome padrão do jogador em replays.
- `persistent.yukare_favorites`: Lista de cenas favoritadas.

---

## 6. Guia de Progressão (`guide_screens.rpy` e `guide_steps.rpy`)

Implementa a visualização visual e lógica do guia de passos do jogo.
- **Logica (`guide_screens.rpy`)**: Localizado em `scripts/`, define a interface e telas do guia (`yukare_guide_selection`, `yukare_guide_detail` e `yukare_status_screen`), bem como a função helper `guide()`.
- **Configuração (`guide_steps.rpy`)**: Localizado na raiz de `Yukare_Replay/`, define o dicionário de passos estruturados de progresso de cada personagem (`yukare_guide_steps`) e as variáveis globais de rastreamento do passo atual.

---

## Observações Técnicas
- **Fundo da Galeria**: A imagem `yukare_gallery_bg` é definida de forma procedural no topo de `yukare_replay_screen.rpy` para evitar dependência de arquivos externos.
- **Isolamento**: Estes scripts não devem ser alterados para lógica específica de um jogo. Para isso, utilize os arquivos de ponte/configuração na raiz da pasta `Yukare_Replay` (como `choice_config.rpy` e `guide_steps.rpy`).

# Yukare Guide - Guia de Progressão de Personagens

Este diretório contém o sistema de guia de progresso para os personagens do jogo Jens Dilemma 3.

## Estrutura de Arquivos

* `guide_steps.rpy`: Contém as definições principais de dados e variáveis de estado do guia.
* `guide_screens.rpy`: Contém as definições das telas (`screens`) e funções visuais do guia.
* `mom.rpy`: Arquivo de exemplo que demonstra a invocação de passos específicos (ex: `mom_01`).
* `images/`: Diretório contendo os assets visuais locais (como botões, balões e bordas) para tornar o guia portátil.
* `readme.md`: Este arquivo de documentação.

---

## Variáveis Globais

### `step` (Matriz Associativa / Dicionário)

Armazena e rastreia o progresso atual de cada personagem.

* **Declaração:** `default step = {}`
* **Como definir/atualizar o progresso de um personagem:**

    ```renpy
    step["nadia"] = "02"
    ```

* **Como verificar o progresso em condicionais de diálogos/fluxo:**

    ```renpy
    if step.get("nadia") == "02":
        # Fluxo para quando Nadia estiver no passo 2
    ```

    *Nota: Recomenda-se o uso de `.get()` para evitar erros caso a chave ainda não tenha sido definida.*

### `yukare_selected_char` (String)

Controla qual personagem está selecionado atualmente na interface de seleção do guia.

* **Declaração:** `default yukare_selected_char = "youngsis"`

---

## Estrutura de Dados do Guia

### `yukare_guide_steps` (Dicionário)

Define os passos estruturados de progressão de cada personagem. Fica localizado no bloco `init python` dentro do arquivo `guide_steps.rpy`.

Exemplo de estrutura:

```python
yukare_guide_steps = {
    "nadia": {
        "name": _("Nadia"),
        "label_prefix": "nadia",
        "steps": {
            "01": {
                "title": _("Primeiros Passos"),
                "description": _("Fale com ela no quarto..."),
                "requirements": _("Nenhum")
            }
        }
    }
}
```

---

## Telas (Screens)

### `yukare_guide_selection`

Tela principal de seleção do guia que mostra a lista de personagens à esquerda e os passos do personagem selecionado à direita.

* **Invocação:**

    ```renpy
    show screen yukare_guide_selection
    ```

### `yukare_guide_detail`

Tela modal secundária usada para exibir informações detalhadas de um determinado passo.

---

## Funções Auxiliares

### `guide(pessoa, passo, descricao, requerimentos=None)`

Função síncrona para chamar e abrir diretamente a janela modal de detalhes de um passo.

* **Parâmetros:**
  * `pessoa` (str): O nome ou identificador do personagem.
  * `passo` (str): O número identificador do passo (ex: `"01"`).
  * `descricao` (str): Detalhes sobre o que o jogador deve fazer.
  * `requerimentos` (str, opcional): Requisitos necessários para o passo.
* **Exemplo de uso:**

    ```renpy
    label mom_01:
        $ guide("Mom", "01", "Passe um tempo com ela assistindo TV na sala para restabelecer a amizade.", "Nenhum")
        return
    ```

