import yaml
from pathlib import Path

def load_config(config_path="config/settings.yaml"):
    """
    Loads the project configuration from the YAML file.
    """
    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"Configuration file not found at {path.absolute()}")
        
    with open(path, "r") as file:
        config = yaml.safe_load(file)
        
    return config

# Optional: Create a singleton configuration instance
# config = load_config()
