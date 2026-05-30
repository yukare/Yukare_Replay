init python:
    def get_char_image(char_name):
        # Checks possible extensions in Yukare_Replay/images/
        exts = [".png", ".jpg", ".webp"]
        cap_name = char_name.capitalize()
        
        # Check capitalized name first
        for ext in exts:
            path = "Yukare_Replay/images/" + cap_name + ext
            if renpy.loadable(path):
                return path
                
        # Check lowercase name
        for ext in exts:
            path = "Yukare_Replay/images/" + char_name + ext
            if renpy.loadable(path):
                return path
                
        # Fallback to standard NoImageSet
        fallback_path = "Yukare_Replay/scripts/NoImageSet.png"
        if renpy.loadable(fallback_path):
            return fallback_path
        return None

# --- Route selection screen called at the start of game ---
screen select_route_screen():
    modal True
    add Solid("#090b11e6")  # Dark semi-transparent background

    frame:
        align (0.5, 0.5)
        xysize (1200, 700)
        background (Frame("Yukare_Guide/images/frame.png", Borders(4, 4, 4, 4)) if renpy.loadable("Yukare_Guide/images/frame.png") else Solid("#0f172a"))
        padding (30, 30, 30, 30)

        vbox:
            spacing 20
            xfill True
            yfill True

            # Header
            text "CHOOSE YOUR STORY GUIDE PATH" color "#38bdf8" size 32 bold True xalign 0.5
            text "Select a character to highlight their path, or choose to show all or play without guide." color "#94a3b8" size 16 xalign 0.5

            null height 10

            # Horizontal cards layout for characters
            hbox:
                spacing 30
                align (0.5, 0.5)

                # Loops over sorted choice_tags from choice_config.rpy
                for char_name in sorted(list(choice_tags)):
                    $ img = get_char_image(char_name)
                    $ display_name = char_name.upper()
                    
                    button:
                        action [SetVariable("selected_route", char_name), Return()]
                        xysize (220, 420)
                        background Solid("#1e293b80")
                        hover_background Solid("#38bdf820")
                        padding (15, 15)
                        
                        vbox:
                            spacing 15
                            xfill True
                            yfill True
                            
                            # Character Image (properly scaled)
                            if img:
                                add im.Scale(img, 190, 320) xalign 0.5 yalign 0.5
                            else:
                                frame:
                                    xysize (190, 320)
                                    background Solid("#334155")
                                    text "No Image" align (0.5, 0.5) color "#64748b"
                                    
                            # Character Name Button Text
                            text display_name align (0.5, 1.0) color "#ffffff" hover_color "#38bdf8" size 18 bold True

            # Bottom options (All / None)
            hbox:
                spacing 40
                align (0.5, 1.0)
                yoffset 10

                textbutton "{b}HIGHLIGHT ALL ROUTES{/b}":
                    action [SetVariable("selected_route", "all"), Return()]
                    xysize (320, 60)
                    background Solid("#1e293b")
                    hover_background Solid("#22c55e40")
                    text_color "#ffffff"
                    text_hover_color "#22c55e"
                    text_size 16
                    text_align (0.5, 0.5)

                textbutton "{b}PLAY WITHOUT GUIDE{/b}":
                    action [SetVariable("selected_route", "none"), Return()]
                    xysize (320, 60)
                    background Solid("#1e293b")
                    hover_background Solid("#ef444440")
                    text_color "#ffffff"
                    text_hover_color "#ef4444"
                    text_size 16
                    text_align (0.5, 0.5)
