# Injeção via config.overlay_screens
init 999 python:
    # Adiciona a nossa tela como um overlay, 
    # que será exibido por cima do menu principal.
    if "yukare_replay_main_menu_hook" not in config.overlay_screens:
        config.overlay_screens.append("yukare_replay_main_menu_hook")

screen yukare_replay_main_menu_hook():
    zorder 10000

    if main_menu: # Só exibe se for o menu principal mesmo
        frame:
            xalign 0.98
            yalign 0.05
            background Solid("#00000080")
            padding (10, 10)

            textbutton "Yukare Replay":
                action ShowMenu("Yukare_Replay_Character_Select")
                text_size 35
                text_color "#ffffff"
                text_hover_color "#00ff00"
                text_outlines [(2, "#000000", 0, 0)]
                activate_sound "audio/button_click.ogg"
                hover_sound "audio/button_hover.ogg"
                mouse "active"
