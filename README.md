# Yukare_Replay
Scenes gallery for renpy games.

  Alterações Realizadas:

- game/Yukare_Replay/scripts/yukare_replay_init.rpy: Atualizei o script de inicialização para que, ao encontrar o marcador ##@person (ou ##@girl), ele divida os nomes fornecidos por
     vírgula. A cena agora é registrada na galeria de cada uma das personagens mencionadas.
- Compatibilidade: Se uma cena possuir o marcador ##@char_image, a imagem será aplicada a todas as personagens listadas naquela cena (caso elas ainda não possuam uma imagem definida).

  Exemplo de Uso:
  Agora você pode definir cenas com múltiplas pessoas no arquivo game/Yukare_Replay/scenes.rpy da seguinte forma:

   1 label replay_exemplo_multiplo:
   2     ##@person Bianca, Summer, Eva
   3     ##@title Cena em Grupo
   4     # ... código da cena ...
   5     return
  Esta cena aparecerá automaticamente nas galerias da Bianca, da Summer e da Eva.

✦ Adicionei suporte à nova marcação ##@scene_image.

  O que mudou:

- Prioridade de Imagem: Na galeria de cenas, o sistema agora segue esta ordem de prioridade para exibir a miniatura:
       1. ##@scene_image (se definida)
       2. ##@image (se definida e a anterior não existir)
       3. Miniatura padrão do mod (se nenhuma das anteriores estiver definida)
- Flexibilidade: Isso permite que você use @image para uma finalidade e @scene_image especificamente para o que deve aparecer na galeria, se desejar diferenciá-las.

  Exemplo de Uso:

   1 label replay_exemplo:
   2     ##@person Bianca
   3     ##@title Encontro no Parque
   4     ##@scene_image Yukare_Replay/images/thumb_parque.webp
   5     # ... resto da cena ...
   6     return

✦ Como não posso gerar um arquivo de imagem binário (como .png ou .jpg) diretamente, criei uma definição de imagem procedural dentro do Ren'Py. Isso permite que você tenha um fundo
  elegante e consistente sem depender de arquivos externos pesados.

  O que eu fiz:

   1. Definição de Imagem: Criei uma imagem chamada yukare_gallery_bg no arquivo game/Yukare_Replay/scripts/yukare_replay_screen.rpy.
   2. Estética: Atualmente, ela está definida como um fundo cinza muito escuro (#121216) com uma leve transparência, o que dá um ar moderno e faz com que os botões e títulos se destaquem
      melhor.
   3. Atualização das Telas: Configurei as telas de Seleção de Personagem e Seleção de Cena para usar esse novo fundo.

  Como personalizar:
  Se você quiser usar uma imagem específica no futuro, basta alterar a definição no topo do arquivo game/Yukare_Replay/scripts/yukare_replay_screen.rpy:

    1 image yukare_gallery_bg:
    2     # Para usar uma imagem de arquivo:
    3     "Yukare_Replay/images/SeuFundoNovo.webp"
    4
    5     # Ou mantenha o efeito de sobreposição escura sobre uma imagem:
    6     # contains:
    7     #     "gui/main_menu.png" # Exemplo: usa o fundo do menu principal
    8     # contains:
    9     #     Solid("#000")
   10     #     alpha 0.6 # Escurece a imagem de fundo em 60%

  Dessa forma, o fundo agora é controlado por código, facilitando qualquer ajuste futuro de cor ou imagem!
