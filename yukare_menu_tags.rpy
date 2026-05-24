# Yukare Replay - Menu Tag Support
# This script handles custom tags in menu items like [green], [red], and [last].
# By overriding the choice screen here, we keep the original screens.rpy clean.

init offset = 5

init python:
    def yukare_process_menu_caption(item):
        """
        Processes a menu item caption to handle custom Yukare tags.
        Returns (processed_caption, custom_style or None).
        """
        caption = item.caption
        
        # 1. Style-changing tags (only one can be active, forces a specific style)
        if "[green]" in caption:
            return caption.replace("[green]", ""), "choice_button_text_green"
        if "[red]" in caption:
            return caption.replace("[red]", ""), "choice_button_text_red"
            
        # 2. Replay guide tags (dynamic based on game-specific config)
        selected_route = getattr(store, "yukare_guide_route", None)
        guide_chars = getattr(store, "yukare_guide_characters", [])
        
        for char_info in guide_chars:
            char_tag = char_info[0]
            green_tag = "[{}]".format(char_tag)
            red_tag = "[{}-red]".format(char_tag)
            
            if green_tag in caption:
                caption = caption.replace(green_tag, "")
                if selected_route == char_tag:
                    return caption, "choice_button_text_green"
                else:
                    return caption, None
                    
            if red_tag in caption:
                caption = caption.replace(red_tag, "")
                if selected_route == char_tag:
                    return caption, "choice_button_text_red"
                else:
                    return caption, None

        # 3. Text-appending tags (can be combined, uses default style)
        if "[last]" in caption:
            caption = caption.replace("[last]", "") + " {color=#0f0}(Last){/color}"
            
        return caption, None

# Custom styles for menu tags
style choice_button_text_green is choice_button_text:
    idle_color "#00ff00"
    hover_color "#adffad"

style choice_button_text_red is choice_button_text:
    idle_color "#ff0000"
    hover_color "#ffadad"

# Override the standard choice screen
screen choice(items):
    style_prefix "choice"

    vbox:
        for i in items:
            $ caption, custom_style = yukare_process_menu_caption(i)
            if custom_style:
                textbutton caption action i.action text_style custom_style
            else:
                textbutton caption action i.action
