init -10 python:
    import re
    import os

    class YukareScene(object):
        def __init__(self, label, character, title, tags, image=None, scene_image=None):
            self.label = label
            self.character = character
            self.title = title
            self.tags = tags
            self.image = image
            self.scene_image = scene_image
            self.thumbnail = "Yukare_Replay/images/img.webp" # Default thumbnail

    yukare_scenes = {}
    yukare_characters = []
    # Dicionário para imagens dos personagens
    yukare_character_images = {}
    # Dicionário para descrições dos personagens
    yukare_character_descriptions = {}

    # Adiciona a tela de controles de replay aos overlays do sistema
    config.overlay_screens.append("yukare_replay_controls")

    def parse_yukare_scenes():
        global yukare_scenes, yukare_characters, yukare_character_images, yukare_character_descriptions

        scenes_file = os.path.join(config.gamedir, "Yukare_Replay/scenes.rpy")
        if not os.path.exists(scenes_file):
            return

        with open(scenes_file, "r") as f:
            content = f.read()

        # Regex to find labels and metadata
        labels = re.split(r"label\s+(replay_[a-zA-Z0-9_]+):", content)

        for i in range(1, len(labels), 2):
            label_name = labels[i]
            label_content = labels[i+1]

            # Extract metadata
            character = re.search(r"##@(person|girl)\s+(.*)", label_content, re.IGNORECASE)

            if not character:
                continue

            title = re.search(r"##@title\s+(.*)", label_content, re.IGNORECASE)
            tags = re.search(r"##@tags\s+(.*)", label_content, re.IGNORECASE)
            image = re.search(r"##@image\s+(.*)", label_content, re.IGNORECASE)
            scene_img = re.search(r"##@scene_image\s+(.*)", label_content, re.IGNORECASE)
            char_img = re.search(r"##@char_image\s+(.*)", label_content, re.IGNORECASE)
            char_desc = re.search(r"##@char_description\s+(.*)", label_content, re.IGNORECASE)

            char_raw = character.group(2).strip()
            char_names = [c.strip() for c in char_raw.split(",")]
            scene_title = title.group(1).strip() if title else ""
            scene_tags = tags.group(1).strip() if tags else ""
            scene_image_path = image.group(1).strip() if image else None
            specific_scene_image = scene_img.group(1).strip() if scene_img else None

            for char_name in char_names:
                char_name = char_name.strip()
                if char_img:
                    yukare_character_images[char_name] = char_img.group(1).strip()

                if char_desc:
                    yukare_character_descriptions[char_name] = char_desc.group(1).strip()

                if char_name not in yukare_scenes:
                    yukare_scenes[char_name] = []
                    yukare_characters.append(char_name)

                yukare_scenes[char_name].append(YukareScene(label_name, char_name, scene_title, scene_tags, scene_image_path, specific_scene_image))

    parse_yukare_scenes()
    yukare_characters.sort()
