init -1:
    image yukare_gallery_bg = Solid("#121216")

###############################################################################
##
## Yukare Replay Gallery Screens
##
###############################################################################

style yukare_gallery_button:
    color "#FFF"
    hover_color "#0f0"
    size 30

style yukare_gallery_return_button is yukare_gallery_button:
    # Estilo próprio para o botão de retornar
    xalign 0.95
    yalign 0.95

style yukare_gallery_random_button is yukare_gallery_button:
    # Estilo próprio para o botão de galeria aleatória
    xalign 0.05
    yalign 0.95

style yukare_replay_end_button is yukare_gallery_button:
    # Estilo para o botão de encerrar replay (Canto superior direito)
    xalign 0.99
    yalign 0.01
    background Solid("#00000066") # Fundo semi-transparente opcional
    padding (10, 5)

style yukare_gallery_char_button:
    color "#FFF"
    hover_color "#0f0"
    size 32


style yukare_gallery_title:
    color "#FF86C2"
    size 32

    outlines [(2, "#000", 0, 0)]

style yukare_gallery_label:
    color "#FFF"
    size 22
    outlines [(1, "#000", 0, 0)]

# Tela que exibe o botão apenas durante um replay
screen yukare_replay_controls():
    zorder 100
    if _in_replay:
        # Variável para o tooltip
        default my_tooltip = ""

        # Mini Menu no canto superior direito
        hbox:
            align (0.98, 0.02)
            spacing 5

            # Botão Ocultar Interface
            button:
                xsize 60 ysize 35
                idle_background Transform(Solid("#000a"), xsize=60, ysize=35)
                hover_background Transform(Solid("#FF86C2cc"), xsize=60, ysize=35)
                action HideInterface()
                hovered SetScreenVariable("my_tooltip", "HIDE UI")
                unhovered SetScreenVariable("my_tooltip", "")

                text "HIDE" align (0.5, 0.5) size 14 color "#fff" bold True

            # Botão Skip (Próxima Imagem)
            button:
                xsize 60 ysize 35
                idle_background Transform(Solid("#000a"), xsize=60, ysize=35)
                hover_background Transform(Solid("#FF86C2cc"), xsize=60, ysize=35)
                action Skip() alternate Skip(fast=True)
                hovered SetScreenVariable("my_tooltip", "FAST FORWARD")
                unhovered SetScreenVariable("my_tooltip", "")

                text "SKIP" align (0.5, 0.5) size 14 color "#fff" bold True

            # Botão Loop
            $ is_loop = getattr(store, "yukare_replay_loop", False)
            button:
                xsize 60 ysize 35
                idle_background Transform(Solid("#000a"), xsize=60, ysize=35)
                hover_background Transform(Solid("#FF86C2cc"), xsize=60, ysize=35)
                action ToggleVariable("yukare_replay_loop")
                hovered SetScreenVariable("my_tooltip", "TOGGLE LOOP")
                unhovered SetScreenVariable("my_tooltip", "")

                text "LOOP" align (0.5, 0.5) size 14 color ("#0f0" if is_loop else "#fff") bold True

            # Botão Sair do Replay
            button:
                xsize 32 ysize 35
                idle_background Transform(Solid("#f44336aa"), xsize=40, ysize=35)
                hover_background Transform(Solid("#f44336"), xsize=40, ysize=35)
                if persistent.yukare_random_mode_active:
                    action Confirm(_("End the replay?"), Function(stop_yukare_random_mode))
                else:
                    action EndReplay(confirm=True)
                hovered SetScreenVariable("my_tooltip", "EXIT REPLAY")
                unhovered SetScreenVariable("my_tooltip", "")

                text "X" align (0.5, 0.5) size 18 color "#fff" bold True

        # Tooltip simplificado e compatível
        if my_tooltip:
            frame:
                align (0.97, 0.07)
                background Solid("#000c")
                padding (8, 4)
                text "[my_tooltip]" size 12 color "#FF86C2"

screen Yukare_Replay_Character_Select():
    key 'ctrl_K_r' action Function(reload_yukare_data)
    tag menu
    add "yukare_gallery_bg"
    on "show" action [SetVariable("yukare_selected_tags", []), SetVariable("pc_name", persistent.yukare_pc_name)]

    # Variável para rastrear qual personagem está sob o mouse
    default hovered_char = None

    vbox:
        align (0.5, 0.05)
        spacing 10
        text "Scene Replay Gallery" style "yukare_gallery_title"

        # Global Progress Bar
        $ u_all, t_all, p_all = get_yukare_stats()
        if t_all > 0:
            hbox:
                xalign 0.5
                spacing 15
                bar value u_all range t_all xsize 320 ysize 20 yalign 0.5
                text "[p_all]% Complete ([u_all]/[t_all])" style "yukare_gallery_label" size 16 yalign 0.5

    # Toggle for Lock System
    hbox:
        align (0.95, 0.05)
        spacing 10
        text "Gallery Lock:" style "yukare_gallery_label" size 18 yalign 0.5
        textbutton ("[persistent.yukare_lock_enabled]"):
            action ToggleField(persistent, "yukare_lock_enabled")
            style "yukare_gallery_button"
            text_size 18
            text_color ("#0f0" if persistent.yukare_lock_enabled else "#f00")

    viewport:
        align (0.5, 0.5)
        xsize 1200
        ysize 500
        scrollbars "vertical"
        mousewheel True
        draggable True

        vpgrid:
            cols 3
            xspacing 30
            yspacing 60
            bottom_margin 100
            xfill True

            for c in yukare_characters:
                $ char_thumb = yukare_character_images.get(c, "Yukare_Replay/images/img.webp")
                vbox:
                    spacing 15
                    imagebutton:
                        idle Transform(char_thumb, xsize=300, ysize=170, fit="cover")
                        hover Transform(char_thumb, xsize=300, ysize=170, fit="cover", matrixcolor=BrightnessMatrix(0.2) * ContrastMatrix(1.2))
                        action ShowMenu("Yukare_Replay_Scene_Select", char_name=c)
                        hovered SetScreenVariable("hovered_char", c)
                        unhovered SetScreenVariable("hovered_char", None)
                        align (0.5, 0.5)

                    vbox:
                        spacing 5
                        xalign 0.5
                        textbutton c:
                            action ShowMenu("Yukare_Replay_Scene_Select", char_name=c)
                            style "yukare_gallery_char_button"
                            xalign 0.5
                            hovered SetScreenVariable("hovered_char", c)
                            unhovered SetScreenVariable("hovered_char", None)

                        # Individual Character Stats
                        if c == "Favorites":
                            $ fav_count = len(persistent.yukare_favorites)
                            text "[fav_count] Favorites":
                                style "yukare_gallery_label"
                                size 14
                                xalign 0.5
                                color "#ffffffb3"
                        else:
                            $ u_c, t_c, p_c = get_yukare_stats(c)
                            text "[u_c] / [t_c]":
                                style "yukare_gallery_label"
                                size 14
                                xalign 0.5
                                color "#ffffffb3"

                        $ char_desc = yukare_character_descriptions.get(c, "")
                        if char_desc:
                            text "[char_desc]":
                                style "yukare_gallery_label"
                                size 18
                                xalign 0.5
                                text_align 0.5
                                xsize 380
                                layout "subtitle"

    # Painel de descrição completa (aparece ao passar o mouse)
    if hovered_char:
        $ full_desc = yukare_character_descriptions.get(hovered_char, "")
        if full_desc:
            frame:
                align (0.5, 0.98)
                xsize 1200
                padding (20, 20)
                background Solid("#000000DD")

                text "[hovered_char]: [full_desc]":
                    style "yukare_gallery_label"
                    size 24
                    xalign 0.5
                    text_align 0.5
                    layout "subtitle"

    textbutton "Random Mode" action ShowMenu("Yukare_Replay_Random_Config") style "yukare_gallery_random_button"
    textbutton "Return" action Return() style "yukare_gallery_return_button"

screen Yukare_Replay_Random_Config():
    tag menu
    add "yukare_gallery_bg"

    vbox:
        align (0.5, 0.1)
        text "Random Mode Configuration" style "yukare_gallery_title"

    vbox:
        align (0.5, 0.4)
        spacing 20

        text "Select tags to filter random scenes:" style "yukare_gallery_label" size 30 xalign 0.5
        text "(Scenes must contain ALL selected tags)" style "yukare_gallery_label" size 18 xalign 0.5 italic True

        frame:
            xsize 900
            ysize 320
            background Solid("#ffffff11")
            padding (20, 20)
            xalign 0.5

            viewport:
                scrollbars "vertical"
                mousewheel True
                draggable True

                vpgrid:
                    cols 4
                    spacing 20
                    xfill True

                    textbutton "Clear All" action SetVariable("yukare_selected_tags", []) style "yukare_gallery_button" text_size 22:
                        if not yukare_selected_tags:
                            text_color "#0f0"

                    textbutton "Select All" action SetVariable("yukare_selected_tags", list(yukare_all_tags)) style "yukare_gallery_button" text_size 22:
                        if len(yukare_selected_tags) == len(yukare_all_tags) and len(yukare_all_tags) > 0:
                            text_color "#0f0"

                    for t in yukare_all_tags:
                        textbutton t action ToggleSetMembership(yukare_selected_tags, t) style "yukare_gallery_button" text_size 22:
                            if t in yukare_selected_tags:
                                text_color "#0f0"

    vbox:
        align (0.5, 0.82)
        spacing 15

        hbox:
            xalign 0.5
            spacing 20
            textbutton "START RANDOM MODE" action ui.callsinnewcontext("yukare_random_start") style "yukare_gallery_button":
                text_size 32
                text_hover_color "#ff0"

            vbox:
                yalign 0.5
                text "Favorites Only:" style "yukare_gallery_label" size 14 xalign 0.5
                textbutton ("[persistent.yukare_random_favorites_only]"):
                    action ToggleField(persistent, "yukare_random_favorites_only")
                    style "yukare_gallery_button"
                    text_size 16
                    text_color ("#0f0" if persistent.yukare_random_favorites_only else "#f00")
                    xalign 0.5

    textbutton "Return" action ShowMenu("Yukare_Replay_Character_Select") style "yukare_gallery_return_button"

screen Yukare_Replay_Scene_Select(char_name):
    key 'ctrl_K_r' action Function(reload_yukare_data)
    tag menu
    add "yukare_gallery_bg"

    vbox:
        align (0.5, 0.05)
        text "[char_name] Scenes" style "yukare_gallery_title"

    # Filter selection
    vbox:
        align (0.5, 0.15)
        xsize 1100
        spacing 10
        
        text "Filter:" style "yukare_gallery_label" size 24

        hbox:
            box_wrap True
            xsize 1100  # Explicitly set width to force wrapping
            spacing 20
            
            textbutton "All" action SetVariable("yukare_selected_tags", []) style "yukare_gallery_button" text_size 20:
                if not yukare_selected_tags:
                    text_color "#0f0"

            for t in yukare_all_tags:
                textbutton t action ToggleSetMembership(yukare_selected_tags, t) style "yukare_gallery_button" text_size 20:
                    if t in yukare_selected_tags:
                        text_color "#0f0"

    python:
        # If the virtual category "Favorites" is selected, filter All scenes by their presence in persistent.yukare_favorites
        if char_name == "Favorites":
            current_scenes = [s for s in yukare_scenes.get("All", []) if s.label in persistent.yukare_favorites]
        else:
            current_scenes = yukare_scenes.get(char_name, [])

        if yukare_selected_tags:
            temp_scenes = []
            for scene_obj in current_scenes:
                found = False
                for t in yukare_selected_tags:
                    if t in scene_obj.tag_list:
                        found = True
                        break
                if found:
                    temp_scenes.append(scene_obj)
            current_scenes = temp_scenes

    viewport:
        align (0.5, 0.6)
        xsize 1200
        ysize 500
        scrollbars "vertical"
        mousewheel True
        draggable True

        vpgrid:
            cols 3
            spacing 30
            bottom_margin 100
            xfill True

            for s in current_scenes:
                $ is_unlocked = s.is_unlocked
                $ display_thumb = s.scene_image if s.scene_image else s.thumbnail
                vbox:
                    spacing 15
                    xsize 320
                    fixed:
                        xsize 320
                        ysize 200
                        imagebutton:
                            if is_unlocked:
                                idle Transform(display_thumb, xsize=300, ysize=170, fit="cover")
                                hover Transform(display_thumb, xsize=300, ysize=170, fit="cover", matrixcolor=BrightnessMatrix(0.25) * ContrastMatrix(1.25))
                                action Replay(s.label, scope=get_yukare_scope(), locked=False)
                            else:
                                idle Transform(display_thumb, xsize=300, ysize=170, fit="cover", matrixcolor=SaturationMatrix(0.0)*BrightnessMatrix(-0.5))
                                action Notify("This scene is locked. Play the game to unlock it!")
                            align (0.5, 0.5)

                        if is_unlocked:
                            # Favorite Toggle Button (Heart)
                            $ is_fav = s.label in persistent.yukare_favorites
                            textbutton ("♥" if is_fav else "♡") text_font "fonts/DejaVuSansCondensed-Bold.ttf":
                                action ToggleSetMembership(persistent.yukare_favorites, s.label)
                                xalign 0.9
                                yalign 0.1
                                text_size 32
                                text_color ("#f00" if is_fav else "#fff")
                                text_outlines [(2, "#000", 0, 0)]

                    if s.title:
                        text (s.title if is_unlocked else "???"):
                            style "yukare_gallery_label"
                            xalign 0.5
                            text_align 0.5

                    if s.tags:
                        text "([s.tags])":
                            style "yukare_gallery_label"
                            size 16
                            xalign 0.5
                            text_align 0.5

    textbutton "Return" action ShowMenu("Yukare_Replay_Character_Select") style "yukare_gallery_return_button"
