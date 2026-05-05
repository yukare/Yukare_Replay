
# Yukare Replay - Random Gallery Mode
# This script implements a randomized playback system for the gallery.

# Initialize variables safely
default persistent.yukare_played_random = []
default yukare_random_mode_active = False

init python:
    import random

    def get_next_random_yukare_scene():
        """Selects the next random scene label and returns it."""
        all_scenes_dict = getattr(store, 'yukare_scenes', {})
        selected_tags = getattr(store, 'yukare_selected_tags', [])
        
        all_labels = []
        for char_scenes in all_scenes_dict.values():
            for s in char_scenes:
                if not selected_tags or all(tag in s.tag_list for tag in selected_tags):
                    all_labels.append(s.label)
        
        if not all_labels:
            return None

        available = [s for s in all_labels if s not in persistent.yukare_played_random]

        if not available:
            persistent.yukare_played_random = []
            available = all_labels

        chosen = random.choice(available)
        persistent.yukare_played_random.append(chosen)
        return chosen

# Label based loop to avoid deep recursion with renpy.replay
label yukare_random_start:
    $ yukare_random_mode_active = True
    jump yukare_random_loop

label yukare_random_loop:
    if not yukare_random_mode_active:
        return

    $ next_scene = get_next_random_yukare_scene()
    
    if next_scene is None:
        $ renpy.notify("No scenes found in gallery.")
        $ yukare_random_mode_active = False
        return

    # Execute the replay sem o argumento 'locked' que causa erro.
    $ renpy.call_replay(next_scene)
    
    # Se o usuário clicar em "End Replay", o Ren'Py retorna para este ponto.
    # Verificamos se alguma tela de menu ou galeria está visível agora.
    python:
        # Se voltamos para a galeria ou o menu, o modo aleatório deve parar.
        screens_to_check = ["Yukare_Replay_Character_Select", "Yukare_Replay_Scene_Select", "navigation", "game_menu", "main_menu"]
        
        for sn in screens_to_check:
            if renpy.get_screen(sn):
                yukare_random_mode_active = False
                break

    if not yukare_random_mode_active:
        return

    # Continua se não houver interrupção detectada
    jump yukare_random_loop

label yukare_random_stop:
    $ yukare_random_mode_active = False
    return
