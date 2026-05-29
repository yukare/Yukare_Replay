
# Yukare Replay - Random Gallery Mode
# This script implements a randomized playback system for the gallery.

# Initialize variables safely
default persistent.yukare_played_random = []
default persistent.yukare_random_mode_active = False

init python:
    import random

    def stop_yukare_random_mode():
        """Stops the random mode and ends any ongoing replay."""
        persistent.yukare_random_mode_active = False
        store.yukare_was_skipping = False
        if getattr(store, '_in_replay', False):
            renpy.end_replay()

    def get_next_random_yukare_scene():
        """Selects the next random scene label and returns it."""
        all_scenes_dict = getattr(store, 'yukare_scenes', {})
        selected_tags = getattr(store, 'yukare_selected_tags', [])
        
        all_labels = []
        # Normalização das tags selecionadas (lower case e sem espaços)
        clean_selected = [t.strip().lower() for t in selected_tags if t.strip()]

        for char_scenes in all_scenes_dict.values():
            for s in char_scenes:
                # Se o modo favoritos estiver ativo, ignora o que não for favorito
                if persistent.yukare_random_favorites_only and s.label not in persistent.yukare_favorites:
                    continue

                if not clean_selected:
                    all_labels.append(s.label)
                else:
                    # Normalização das tags da cena
                    scene_tags_lower = [t.lower() for t in s.tag_list]
                    # Verifica se PELO MENOS UMA das tags selecionadas está presente na cena (Lógica OR)
                    if any(tag in scene_tags_lower for tag in clean_selected):
                        all_labels.append(s.label)
        
        if not all_labels:
            if selected_tags:
                tags_str = ", ".join(selected_tags)
                renpy.notify("No scenes found with any of these tags: {}".format(tags_str))
            else:
                renpy.notify("No scenes found in gallery.")
            return None

        # Remover duplicatas mantendo a ordem (caso a mesma cena apareça em vários personagens)
        unique_labels = []
        for l in all_labels:
            if l not in unique_labels:
                unique_labels.append(l)

        available = [l for l in unique_labels if l not in persistent.yukare_played_random]

        if not available:
            # Se todas as cenas filtradas já foram jogadas, resetamos o histórico apenas para as cenas filtradas
            # ou resetamos tudo se preferir. Aqui resetamos tudo para simplificar.
            persistent.yukare_played_random = [l for l in persistent.yukare_played_random if l not in unique_labels]
            available = unique_labels

        chosen = random.choice(available)
        persistent.yukare_played_random.append(chosen)
        return chosen

# Label based loop to avoid deep recursion with renpy.replay
label yukare_random_start:
    $ persistent.yukare_random_mode_active = True
    jump yukare_random_loop

label yukare_random_loop:
    if not persistent.yukare_random_mode_active:
        return

    $ next_scene = get_next_random_yukare_scene()
    
    if next_scene is None:
        $ renpy.notify("No scenes found in gallery.")
        $ persistent.yukare_random_mode_active = False
        return

    # Execute the replay sem o argumento 'locked' que causa erro.
    $ renpy.call_replay(next_scene, scope=get_yukare_scope())
    
    # Se o usuário clicar em "End Replay", o Ren'Py retorna para este ponto.
    # Verificamos se alguma tela de menu ou galeria está visível agora.
    python:
        # Se voltamos para a galeria ou o menu, o modo aleatório deve parar.
        screens_to_check = ["Yukare_Replay_Character_Select", "Yukare_Replay_Scene_Select", "navigation", "game_menu", "main_menu"]
        
        for sn in screens_to_check:
            if renpy.get_screen(sn):
                persistent.yukare_random_mode_active = False
                break

    if not persistent.yukare_random_mode_active:
        $ store.yukare_was_skipping = False
        return

    # Continua se não houver interrupção detectada
    jump yukare_random_loop

label yukare_random_stop:
    $ persistent.yukare_random_mode_active = False
    $ store.yukare_was_skipping = False
    return
