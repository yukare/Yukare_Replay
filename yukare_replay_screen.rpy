image yukare_gallery_bg:
    # Cria um fundo escuro elegante com uma leve transparência
    # Se quiser usar uma imagem de fundo, troque Solid por "caminho/da/imagem.jpg"
    Solid("#121216")
    alpha 0.95

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
    size 80


style yukare_gallery_title:
    color "#FF86C2"
    size 40

    outlines [(2, "#000", 0, 0)]

style yukare_gallery_label:
    color "#FFF"
    size 22
    outlines [(1, "#000", 0, 0)]

# Tela que exibe o botão apenas durante um replay
screen yukare_replay_controls():
    zorder 100
    if _in_replay:
        if persistent.yukare_random_mode_active:
            textbutton "End Replay" action Confirm(_("End the replay?"), Function(stop_yukare_random_mode)) style "yukare_replay_end_button"
        else:
            textbutton "End Replay" action EndReplay(confirm=True) style "yukare_replay_end_button"

screen Yukare_Replay_Character_Select():
    tag menu
    add "yukare_gallery_bg"
    on "show" action SetVariable("yukare_selected_tags", [])
    
    # Variável para rastrear qual personagem está sob o mouse
    default hovered_char = None

    vbox:
        align (0.5, 0.05)
        text "Scene Replay Gallery" style "yukare_gallery_title"

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
        xsize 1300
        ysize 700
        scrollbars "vertical"
        mousewheel True
        draggable True

        vpgrid:
            cols 3
            spacing 60
            xfill True

            for c in yukare_characters:
                $ char_thumb = yukare_character_images.get(c, "Yukare_Replay/images/img.webp")
                vbox:
                    spacing 10
                    imagebutton:
                        idle Transform(char_thumb, zoom=0.2)
                        hover Transform(char_thumb, zoom=0.21)
                        action ShowMenu("Yukare_Replay_Scene_Select", char_name=c)
                        hovered SetScreenVariable("hovered_char", c)
                        unhovered SetScreenVariable("hovered_char", None)
                        align (0.5, 0.5)

                    vbox:
                        spacing 0 # Minimum spacing
                        xalign 0.5
                        textbutton c:
                            action ShowMenu("Yukare_Replay_Scene_Select", char_name=c)
                            style "yukare_gallery_char_button"
                            xalign 0.5
                            hovered SetScreenVariable("hovered_char", c)
                            unhovered SetScreenVariable("hovered_char", None)

                        $ char_desc = yukare_character_descriptions.get(c, "")
                        if char_desc:
                            text "[char_desc]":
                                style "yukare_gallery_label"
                                size 18
                                xalign 0.5
                                text_align 0.5
                                xsize 380
                                ysize 100
                                layout "subtitle"

    # Painel de descrição completa (aparece ao passar o mouse)
    if hovered_char:
        $ full_desc = yukare_character_descriptions.get(hovered_char, "")
        if full_desc:
            frame:
                align (0.5, 0.98)
                xsize 1300
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
            xsize 1000
            ysize 400
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
        align (0.5, 0.8)
        spacing 30
        
        textbutton "START RANDOM MODE" action ui.callsinnewcontext("yukare_random_start") style "yukare_gallery_button":
            text_size 40
            text_hover_color "#ff0"
            xalign 0.5

    textbutton "Return" action ShowMenu("Yukare_Replay_Character_Select") style "yukare_gallery_return_button"

screen Yukare_Replay_Scene_Select(char_name):
    tag menu
    add "yukare_gallery_bg"

    vbox:
        align (0.5, 0.05)
        text "[char_name] Scenes" style "yukare_gallery_title"

    # Filter selection
    hbox:
        align (0.5, 0.15)
        spacing 30
        text "Filter:" style "yukare_gallery_label" size 24 yalign 0.5
        
        viewport:
            xsize 1000
            ysize 60
            mousewheel True
            draggable True
            yalign 0.5
            hbox:
                spacing 20
                yalign 0.5
                textbutton "All" action SetVariable("yukare_selected_tags", []) style "yukare_gallery_button" text_size 20 yalign 0.5:
                    if not yukare_selected_tags:
                        text_color "#0f0"
                
                for t in yukare_all_tags:
                    textbutton t action ToggleSetMembership(yukare_selected_tags, t) style "yukare_gallery_button" text_size 20 yalign 0.5:
                        if t in yukare_selected_tags:
                            text_color "#0f0"

    python:
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
        xsize 1500
        ysize 700
        scrollbars "vertical"
        mousewheel True
        draggable True

        vpgrid:
            cols 3
            spacing 70
            xfill True

            for s in current_scenes:
                $ is_unlocked = s.is_unlocked
                $ display_thumb = s.scene_image if s.scene_image else (s.image if s.image else s.thumbnail)
                vbox:
                    spacing 15
                    xsize 400
                    imagebutton:
                        if is_unlocked:
                            idle Transform(display_thumb, zoom=0.18)
                            hover Transform(display_thumb, zoom=0.19)
                            action Replay(s.label, locked=False)
                        else:
                            idle Transform(display_thumb, zoom=0.18, matrixcolor=SaturationMatrix(0.0)*BrightnessMatrix(-0.5))
                            action Notify("This scene is locked. Play the game to unlock it!")
                        align (0.5, 0.5)

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
