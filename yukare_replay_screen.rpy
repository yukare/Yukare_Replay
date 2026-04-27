###############################################################################
##
## Yukare Replay Gallery Screens
##
###############################################################################

style yukare_gallery_button:
    color "#FFF"
    hover_color "#0f0"
    size 30
    font "fonts/TerminalDosis-Medium.ttf"

style yukare_gallery_char_button:
    color "#FFF"
    hover_color "#0f0"
    size 80
    font "fonts/TerminalDosis-Medium.ttf"

style yukare_gallery_title:
    color "#FF86C2"
    size 40
    font "fonts/TerminalDosis-Medium.ttf"
    outlines [(2, "#000", 0, 0)]

style yukare_gallery_label:
    color "#FFF"
    size 22
    font "fonts/TerminalDosis-Medium.ttf"
    outlines [(1, "#000", 0, 0)]

screen Yukare_Replay_Character_Select():
    tag menu
    add "Yukare_Replay/images/GalleryBG.jpg"

    vbox:
        align (0.5, 0.1)
        text "Yukare Replay Gallery" style "yukare_gallery_title"

    viewport:
        align (0.5, 0.5)
        xsize 1300
        ysize 750
        scrollbars "vertical"
        mousewheel True
        draggable True
        
        vpgrid:
            cols 3
            spacing 80
            xfill True
            
            for c in yukare_characters:
                $ char_thumb = yukare_character_images.get(c, "Yukare_Replay/images/img.webp")
                vbox:
                    spacing 20
                    imagebutton:
                        idle Transform(char_thumb, zoom=0.2)
                        hover Transform(char_thumb, zoom=0.21)
                        action ShowMenu("Yukare_Replay_Scene_Select", char_name=c)
                        align (0.5, 0.5)
                    textbutton c:
                        action ShowMenu("Yukare_Replay_Scene_Select", char_name=c)
                        style "yukare_gallery_char_button"
                        xalign 0.5

    textbutton "Return" action Return() align (0.95, 0.95) style "yukare_gallery_button"

screen Yukare_Replay_Scene_Select(char_name):
    tag menu
    add "Yukare_Replay/images/GalleryBG.jpg"

    vbox:
        align (0.5, 0.05)
        text "[char_name] Scenes" style "yukare_gallery_title"

    $ current_scenes = yukare_scenes.get(char_name, [])

    viewport:
        align (0.5, 0.5)
        xsize 1500
        ysize 800
        scrollbars "vertical"
        mousewheel True
        draggable True
        
        vpgrid:
            cols 3
            spacing 70
            xfill True
            
            for s in current_scenes:
                $ display_thumb = s.image if s.image else s.thumbnail
                vbox:
                    spacing 15
                    xsize 400
                    imagebutton:
                        idle Transform(display_thumb, zoom=0.18)
                        hover Transform(display_thumb, zoom=0.19)
                        action Replay(s.label, locked=False)
                        align (0.5, 0.5)
                    text "[s.title]":
                        style "yukare_gallery_label"
                        xalign 0.5
                        text_align 0.5
                    if s.tags:
                        text "([s.tags])":
                            style "yukare_gallery_label"
                            size 16
                            xalign 0.5
                            text_align 0.5

    textbutton "Return" action ShowMenu("Yukare_Replay_Character_Select") align (0.95, 0.95) style "yukare_gallery_button"
