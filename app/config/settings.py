import os
import tomli
from pathlib import Path 

def load_settings():
    config_dir = Path(__file__).parent

    with open(config_dir / "settings.default.toml", "rb") as f:
        settings_default = tomli.load(f)

    # configure no arquivo .env a variável APP_ENV com o valor "dev" ou "prod", dependendo do ambiente.
    # Exmplo: APP_ENV="dev" ou APP_ENV="prod"
    enviroment = os.getenv("APP_ENV", "dev")
    with open(config_dir / f"settings.{enviroment}.toml", "rb") as f:
        settings = tomli.load(f)

    settings.update(settings_default)
    #GEOSON_PATH = settings["geojson"]["path_dir"]
    #print(GEOSON_PATH)

    return settings

SETTINGS = load_settings()