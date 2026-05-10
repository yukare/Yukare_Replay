# Yukare Replay - Infrastructure Variables
# These variables are core to the mod's functionality and are game-agnostic.

# Mod configuration
default persistent.yukare_lock_enabled = False # If True, scenes with ##@origin will be locked until seen
default persistent.yukare_pc_name = "Player" # Default name for the player in replays
default persistent.yukare_favorites = [] # List of labels marked as favorites
default persistent.yukare_random_favorites_only = False # Toggle for random mode
default persistent.yukare_highlight_char = None # Chosen character path for walkthrough highlights

# Store variables for gallery filtering and state
default yukare_selected_tags = []
default yukare_replay_loop = False
