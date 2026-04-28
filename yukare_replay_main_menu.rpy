
init 1000 python:
    # Garante que a tela seja adicionada aos overlays após todos os outros scripts
    if "yukare_replay_main_menu_hook" not in config.overlay_screens:
        config.overlay_screens.append("yukare_replay_main_menu_hook")

screen yukare_replay_main_menu_hook():
    zorder 1000 # Valor extremamente alto para ficar acima de imagemaps e outros elementos

    # Verifica se a tela main_menu está ativa
    if renpy.get_screen("main_menu"):
        frame:
            xalign 0.98
            yalign 0.05
            background Solid("#00000080") # Fundo preto semi-transparente para contraste
            padding (10, 10)

            textbutton _("Yukare Replay"):
                action ShowMenu("Yukare_Replay_Character_Select")
                text_size 35
                text_font "fonts/TerminalDosis-Medium.ttf"
                text_color "#ffffff"
                text_hover_color "#00ff00"
                text_outlines [(2, "#000000", 0, 0)]

                # Sons e comportamento do mouse
                activate_sound "audio/button_click.ogg"
                hover_sound "audio/button_hover.ogg"
                mouse "active"
