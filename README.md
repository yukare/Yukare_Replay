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
