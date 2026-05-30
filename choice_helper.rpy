init python:
    def get_choice_text(text):
        if not isinstance(text, str):
            text = str(text)
        for tag in choice_tags:
            text = text.replace("[" + tag + "]", "")
            text = text.replace("[" + tag + "-red]", "")
        return text

    def get_choice_idle_color(text, default="#ffffff"):
        import renpy.store as store
        if not isinstance(text, str):
            text = str(text)
        
        # Check active route selection
        route = getattr(store, 'selected_route', 'all')
        
        # Write to game/choice_debug.log for debugging
        try:
            import os
            import renpy
            log_path = os.path.join(renpy.config.gamedir, "choice_debug.log")
            with open(log_path, "a", encoding="utf-8") as log_f:
                log_f.write("text={} | route={} | tags={}\n".format(text, route, list(choice_tags)))
        except:
            pass
            
        if route == "none":
            return default
            
        for tag in choice_tags:
            # If a specific route is selected, only highlight that route's choices
            if route != "all" and route != tag:
                continue
                
            if "[" + tag + "-red]" in text:
                return "#ff3333"  # Soft red
            elif "[" + tag + "]" in text:
                return "#39ff14"  # Vibrant green
        return default

    def get_choice_hover_color(text, default="#ff006c"):
        import renpy.store as store
        if not isinstance(text, str):
            text = str(text)
            
        route = getattr(store, 'selected_route', 'all')
        for tag in choice_tags:
            if route != "all" and route != tag:
                continue
                
            if "[" + tag + "-red]" in text:
                return "#ff7777"  # Light red on hover
            elif "[" + tag + "]" in text:
                return "#8aff8a"  # Light green on hover
        return default
