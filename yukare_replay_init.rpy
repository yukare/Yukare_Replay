init -10 python:
    import re
    import os

    class YukareScene(object):
        def __init__(self, label, character, title, tags, image=None):
            self.label = label
            self.character = character
            self.title = title
            self.tags = tags
            self.image = image
            self.thumbnail = "Yukare_Replay/images/img.webp" # Default thumbnail

    yukare_scenes = {}
    yukare_characters = []
    # Dicionário para imagens dos personagens
    # Você pode definir manualmente aqui: yukare_character_images["Summer"] = "caminho/da/imagem.png"
    yukare_character_images = {}

    def parse_yukare_scenes():
        global yukare_scenes, yukare_characters, yukare_character_images

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
            character = re.search(r"##@(person|girl)\s+(.*)", label_content)

            if not character:
                continue

            title = re.search(r"##@title\s+(.*)", label_content)
            tags = re.search(r"##@tags\s+(.*)", label_content)
            image = re.search(r"##@image\s+(.*)", label_content)
            char_img = re.search(r"##@char_image\s+(.*)", label_content)

            char_name = character.group(2).strip()
            scene_title = title.group(1).strip() if title else label_name.replace("replay_", "").replace("_", " ").title()
            scene_tags = tags.group(1).strip() if tags else ""
            scene_image = image.group(1).strip() if image else None

            if char_img:
                yukare_character_images[char_name] = char_img.group(1).strip()

            if char_name not in yukare_scenes:
                yukare_scenes[char_name] = []
                yukare_characters.append(char_name)

            yukare_scenes[char_name].append(YukareScene(label_name, char_name, scene_title, scene_tags, scene_image))

    parse_yukare_scenes()
    yukare_characters.sort()
