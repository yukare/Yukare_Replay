init -5 python:
    import re
    import os

    class YukareScene(object):
        def __init__(self, label, character, title, tags, image=None, scene_image=None):
            self.label = label
            self.character = character
            self.title = title
            self.tags = tags
            self.tag_list = [t.strip() for t in tags.split(",")] if tags else []
            self.image = image
            self.scene_image = scene_image
            self.thumbnail = "Yukare_Replay/images/img.webp" # Default thumbnail

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

                char_raw = char_match.group(2).strip()
                char_names = [c.strip() for c in char_raw.split(",")]
                scene_title = title_match.group(1).strip() if title_match else ""
                scene_tags = tags_match.group(1).strip() if tags_match else ""
                scene_image_path = image_match.group(1).strip() if image_match else None
                specific_scene_image = scene_img_match.group(1).strip() if scene_img_match else None

                if scene_tags:
                    for t in [t.strip() for t in scene_tags.split(",")]:
                        if t:
                            yukare_all_tags.add(t)

                new_scene = YukareScene(label_name, char_raw, scene_title, scene_tags, scene_image_path, specific_scene_image)
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
            yukare_character_images["All"] = "Yukare_Replay/images/img.webp" # Default icon for All
            yukare_character_descriptions["All"] = "All available scenes"

        yukare_all_tags = sorted(list(yukare_all_tags))

    parse_yukare_scenes()
