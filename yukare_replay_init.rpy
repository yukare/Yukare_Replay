init -5 python:
    import re
    import os

    class YukareScene(object):
        def __init__(self, label, character, title, tags, image=None, scene_image=None, origin=None):
            self.label = label
            self.character = character
            self.title = title
            self.tags = tags
            self.tag_list = [t.strip() for t in tags.split(",")] if tags else []
            self.image = image
            self.scene_image = scene_image
            self.origin = origin # The original game label to check for "seen" status
            self.thumbnail = "Yukare_Replay/images/img.webp" # Default thumbnail

        @property
        def is_unlocked(self):
            # If lock is disabled, everything is unlocked
            if not persistent.yukare_lock_enabled:
                return True
            # If no origin is specified, it's always unlocked (backward compatibility)
            if not self.origin:
                return True
            # Check if the player has seen the original label in the game
            import renpy
            return renpy.seen_label(self.origin)

    yukare_scenes = {}
    yukare_characters = []
    yukare_all_tags = set()
    yukare_character_images = {}
    yukare_character_descriptions = {}

    config.overlay_screens.append("yukare_replay_controls")

    def parse_yukare_scenes():
        global yukare_scenes, yukare_characters, yukare_character_images, yukare_all_tags, yukare_character_descriptions

        yukare_scenes = {}
        yukare_characters = []
        yukare_all_tags = set()
        yukare_character_images = {}
        yukare_character_descriptions = {}

        import renpy
        
        # Discover files directly in the Yukare_Replay folder
        files_to_parse = []
        try:
            replay_path = os.path.join(config.gamedir, "Yukare_Replay")
            if os.path.exists(replay_path):
                for f in os.listdir(replay_path):
                    if f.startswith("scenes") and f.endswith(".rpy"):
                        files_to_parse.append(os.path.join("Yukare_Replay", f))
        except Exception:
            pass

        # To keep track of all scenes for the "All" category
        all_scenes_list = []

        for filepath in files_to_parse:
            content = ""
            try:
                full_path = os.path.join(config.gamedir, filepath)
                with open(full_path, "r") as f:
                    content = f.read()
            except Exception:
                continue

            if not content:
                continue

            # Split by label but keep the label name
            labels = re.split(r"label\s+(replay_[a-zA-Z0-9_]+):", content)

            for i in range(1, len(labels), 2):
                label_name = labels[i]
                label_content = labels[i+1]

                # Robust metadata extraction
                char_match = re.search(r"##@(person|girl)\s+(.*)", label_content, re.IGNORECASE)
                if not char_match:
                    continue

                title_match = re.search(r"##@title\s+(.*)", label_content, re.IGNORECASE)
                tags_match = re.search(r"##@tags\s+(.*)", label_content, re.IGNORECASE)
                image_match = re.search(r"##@image\s+(.*)", label_content, re.IGNORECASE)
                scene_img_match = re.search(r"##@scene_image\s+(.*)", label_content, re.IGNORECASE)
                char_img_match = re.search(r"##@char_image\s+(.*)", label_content, re.IGNORECASE)
                char_desc_match = re.search(r"##@char_description\s+(.*)", label_content, re.IGNORECASE)
                origin_match = re.search(r"##@origin\s+(.*)", label_content, re.IGNORECASE)

                char_raw = char_match.group(2).strip()
                char_names = [c.strip() for c in char_raw.split(",")]
                scene_title = title_match.group(1).strip() if title_match else ""
                scene_tags = tags_match.group(1).strip() if tags_match else ""
                scene_image_path = image_match.group(1).strip() if image_match else None
                specific_scene_image = scene_img_match.group(1).strip() if scene_img_match else None
                scene_origin = origin_match.group(1).strip() if origin_match else None

                if scene_tags:
                    for t in [t.strip() for t in scene_tags.split(",")]:
                        if t:
                            yukare_all_tags.add(t)

                new_scene = YukareScene(label_name, char_raw, scene_title, scene_tags, scene_image_path, specific_scene_image, scene_origin)
                all_scenes_list.append(new_scene)

                for char_name in char_names:
                    if char_img_match:
                        yukare_character_images[char_name] = char_img_match.group(1).strip()
                    if char_desc_match:
                        yukare_character_descriptions[char_name] = char_desc_match.group(1).strip()

                    if char_name not in yukare_scenes:
                        yukare_scenes[char_name] = []
                        if char_name not in yukare_characters:
                            yukare_characters.append(char_name)

                    yukare_scenes[char_name].append(new_scene)

        yukare_characters.sort()
        
        # Add "All" option
        if all_scenes_list:
            yukare_characters.insert(0, "All")
            yukare_scenes["All"] = all_scenes_list
            
            # Check for custom "All" image
            import renpy
            def is_loadable(img):
                try:
                    return renpy.exports.loadable(img)
                except AttributeError:
                    try:
                        return renpy.loadable(img)
                    except AttributeError:
                        return False

            all_img = "Yukare_Replay/images/All.webp"
            if not is_loadable(all_img):
                all_img = "Yukare_Replay/images/All.png"
            if not is_loadable(all_img):
                # If no file exists, use a stylized Solid placeholder
                all_img = "#34495e" # A nice dark blue-grey
            
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
                # If no file exists, use a stylized Solid placeholder (heart-like color)
                fav_img = "#9b59b6" # A nice purple
                
            yukare_character_images["Favorites"] = fav_img
            yukare_character_descriptions["Favorites"] = "Your favorite scenes"

        yukare_all_tags = sorted(list(yukare_all_tags))

    def get_yukare_stats(char_name=None):
        """
        Calculates (unlocked_count, total_count, percentage) for a character or globally.
        """
        scenes = []
        if char_name:
            scenes = yukare_scenes.get(char_name, [])
        else:
            # Global stats using the "All" category
            scenes = yukare_scenes.get("All", [])

        if not scenes:
            return 0, 0, 0

        total = len(scenes)
        unlocked = sum(1 for s in scenes if s.is_unlocked)
        percentage = int((float(unlocked) / total) * 100) if total > 0 else 0
        
        return unlocked, total, percentage

    # Initial parse
    parse_yukare_scenes()
