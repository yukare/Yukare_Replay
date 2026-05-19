init -5 python:
    # Custom callback to handle replay variables
    def yukare_replay_callback(label=None):
        # Force pc_name to match persistent
        store.pc_name = persistent.yukare_pc_name

    config.replay_scope = {"pc_name": persistent.yukare_pc_name}
    config.after_replay_callback = yukare_replay_callback

init -100 python:
    import re as real_re
    import os
    import io

    class YukareScene(object):
        def __init__(self, label, character, title, tags, image=None, scene_image=None, origin=None):
            self.label = label
            self.character = character
            self.title = title
            self.tags = tags
            self.thumbnail = image
            self.scene_image = scene_image
            self.origin = origin # The original game label to check for "seen" status
            
            # Check if the player has seen the original label in the game
            # Split by label but keep the label name
            self.is_unlocked = False
            if persistent.yukare_lock_enabled:
                if self.origin and renpy.seen_label(self.origin):
                    self.is_unlocked = True
                elif renpy.seen_label(self.label):
                    self.is_unlocked = True
            else:
                self.is_unlocked = True
                
            self.tag_list = [t.strip() for t in tags.split(",")] if tags else []

    if "yukare_replay_controls" not in config.overlay_screens:
        config.overlay_screens.append("yukare_replay_controls")

    yukare_characters = []
    yukare_scenes = {}
    yukare_character_images = {}
    yukare_character_descriptions = {}
    yukare_all_tags = set()

    def get_yukare_scope():
        rv = {"pc_name": persistent.yukare_pc_name}
        # Add game-specific variables if defined
        if hasattr(store, 'yukare_game_scope_vars'):
            for var_name, persistent_attr, default_val in store.yukare_game_scope_vars:
                rv[var_name] = getattr(persistent, persistent_attr, getattr(store, persistent_attr, default_val))
        return rv

    def parse_yukare_scenes():
        global yukare_characters, yukare_scenes, yukare_all_tags
        
        yukare_characters = []
        yukare_scenes = {}
        yukare_all_tags = set()
        all_scenes_list = []
        
        # Scan all .rpy files in game/Yukare_Replay/
        # Use absolute path to ensure we find the directory
        game_dir = config.gamedir
        replay_dir = os.path.join(game_dir, "Yukare_Replay")
        
        if not os.path.exists(replay_dir):
            return

        for filename in os.listdir(replay_dir):
            if not filename.endswith(".rpy"):
                continue
                
            file_path = os.path.join(replay_dir, filename)
            with io.open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                
            # Regex to find label and tags
            # Format:
            # label replay_labelname:
            #     ##@person Character Name
            #     ##@title Scene Title
            #     ##@scene_image image_name
            #     ##@tags tag1, tag2
            
            pattern = r'label\s+(replay_[a-zA-Z0-9_]+)(\(.*\))?\s*:'
            labels = real_re.finditer(pattern, content)
            
            for match in labels:
                label_name = match.group(1)
                start_pos = match.start()
                
                # Look for metadata in the next few lines
                end_pos = content.find("label ", start_pos + 1)
                if end_pos == -1:
                    label_block = content[start_pos:]
                else:
                    label_block = content[start_pos:end_pos]
                
                person_match = real_re.search(r'##@person\s+(.*)', label_block)
                title_match = real_re.search(r'##@title\s+(.*)', label_block)
                image_match = real_re.search(r'##@scene_image\s+(.*)', label_block)
                tags_match = real_re.search(r'##@tags\s+(.*)', label_block)
                origin_match = real_re.search(r'##@origim\s+(.*)', label_block)
                
                char_raw = person_match.group(1).strip() if person_match else "Unknown"
                scene_title = title_match.group(1).strip() if title_match else label_name
                specific_scene_image = image_match.group(1).strip() if image_match else None
                scene_tags = tags_match.group(1).strip() if tags_match else ""
                scene_origin = origin_match.group(1).strip() if origin_match else None

                if scene_tags:
                    for t in [t.strip() for t in scene_tags.split(",")]:
                        if t:
                            yukare_all_tags.add(t)

                # Find a thumbnail (first image in the label)
                scene_image_path = None
                if not specific_scene_image:
                    img_match = real_re.search(r'scene\s+([a-zA-Z0-9_]+)', label_block)
                    if img_match:
                        scene_image_path = img_match.group(1)
                
                new_scene = YukareScene(label_name, char_raw, scene_title, scene_tags, scene_image_path, specific_scene_image, scene_origin)
                all_scenes_list.append(new_scene)

        # Organize scenes by character
        for s in all_scenes_list:
            # Handle multiple characters in person tag
            chars = [c.strip() for c in s.character.split(",")]
            for c in chars:
                if c not in yukare_characters:
                    yukare_characters.append(c)
                    yukare_scenes[c] = []
                yukare_scenes[c].append(s)

        # Sort characters alphabetically
        yukare_characters.sort()

        # Group "Others" characters
        others_list = getattr(store, "yukare_others_characters", [])
        if others_list:
            real_chars = [c for c in yukare_characters if c not in others_list]
            others_scenes = []
            for c in others_list:
                if c in yukare_scenes:
                    for s in yukare_scenes[c]:
                        if s not in others_scenes:
                            others_scenes.append(s)
            
            yukare_characters = real_chars
            if others_scenes:
                yukare_characters.append("Others")
                yukare_scenes["Others"] = others_scenes
        
        def is_loadable(img):
            try:
                return renpy.loadable(img)
            except:
                return False

        # Build image map and descriptions
        for c in yukare_characters:
            # Search for character image in Yukare_Replay/images/
            img_path = "Yukare_Replay/images/{}.webp".format(c)
            if not is_loadable(img_path):
                img_path = "Yukare_Replay/images/{}.png".format(c)
            if not is_loadable(img_path):
                img_path = "Yukare_Replay/images/img.webp" # Fallback
            
            if c not in yukare_character_images:
                yukare_character_images[c] = img_path
            
            if c not in yukare_character_descriptions:
                yukare_character_descriptions[c] = "View all scenes with {}".format(c)

        # Special "All" character
        if all_scenes_list:
            yukare_characters.insert(0, "All")
            yukare_scenes["All"] = all_scenes_list
            
            all_img = "Yukare_Replay/images/All.webp"
            if not is_loadable(all_img):
                all_img = "Yukare_Replay/images/All.png"
            if not is_loadable(all_img):
                all_img = Transform(Solid("#34495e"), xsize=1280, ysize=720)
            
            yukare_character_images["All"] = all_img
            yukare_character_descriptions["All"] = "All available scenes"
            
            # Add "Favorites" option
            yukare_characters.insert(1, "Favorites")
            yukare_scenes["Favorites"] = []
            
            # Check for custom "Favorites" image
            fav_img = "Yukare_Replay/images/Favorites.webp"
            if not is_loadable(fav_img):
                fav_img = "Yukare_Replay/images/Favorites.png"
            if not is_loadable(fav_img):
                fav_img = Transform(Solid("#9b59b6"), xsize=1280, ysize=720)
                
            yukare_character_images["Favorites"] = fav_img
            yukare_character_descriptions["Favorites"] = "Your favorite scenes"

        yukare_all_tags = sorted(list(yukare_all_tags))

    parse_yukare_scenes()

init 20 python:
    parse_yukare_scenes()

    def reload_yukare_data():
        parse_yukare_scenes()
        renpy.notify("Gallery Reloaded!")
        renpy.restart_interaction()

    def get_yukare_stats(char_name=None):
        """Returns (unlocked_count, total_count, percentage)"""
        if char_name:
            scenes = yukare_scenes.get(char_name, [])
        else:
            scenes = yukare_scenes.get("All", [])
            
        if not scenes:
            return (0, 0, 0)
            
        unlocked = len([s for s in scenes if s.is_unlocked])
        total = len(scenes)
        percent = int((float(unlocked) / total) * 100) if total > 0 else 0
        return (unlocked, total, percent)

    # Define the shortcut Ctrl + R
    config.keymap['reload_yukare'] = ['ctrl_K_r', 'ctrl_r', 'alt_K_r']
    config.underlay.append(renpy.Keymap(reload_yukare=reload_yukare_data))
