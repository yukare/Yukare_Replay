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

## 3. Tags de Menu Dinâmicas (`yukare_menu_tags.rpy`)

Este script intercepta o comportamento padrão do `screen choice` para permitir a estilização de opções de menu via tags de texto.

### Tags Suportadas:
- `[green]`: Torna o texto da opção verde (útil para escolhas corretas).
- `[red]`: Torna o texto da opção vermelho (útil para escolhas perigosas).
- `[last]`: Adiciona uma seta `»` antes do texto (útil para indicar a última escolha feita).

**Exemplo:**
```renpy
menu:
    "Falar a verdade [green]":
        pass
    "Mentir descaradamente [red]":
        pass
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

## Observações Técnicas
- **Fundo da Galeria**: A imagem `yukare_gallery_bg` é definida de forma procedural no topo de `yukare_replay_screen.rpy` para evitar dependência de arquivos externos.
- **Isolamento**: Estes scripts não devem ser alterados para lógica específica de um jogo. Para isso, utilize o arquivo de ponte na raiz da pasta `Yukare_Replay`.
