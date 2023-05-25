from pathlib import Path
from pydantic import BaseSettings, Field


class Config(BaseSettings):
    """
    A configuration class that loads variables from a .env file or uses default values.
    """

    DATA_DIR: Path = Field(
        "data", description="Path for data dir", env="DATA_DIR")
    UNI_LIST: str = Field(
        "uni_list.txt", description="File name for list of universities", env="UNI_LIST")

    class Config:
        env_file = ".env"

    def __init__(self, **data):
        super().__init__(**data)
        self.create_directories()

    def create_directories(self):
        """
        Creates directories for all Path variables if they don't exist.
        """
        for name, value in vars(self).items():
            if not name.startswith('_') and isinstance(value, Path):
                value.mkdir(parents=True, exist_ok=True)


def create_default_env_file(env_file_path: Path, default_config: Config):
    """
    Creates a new .env file with default values for each attribute in the Config class.

    Args:
        env_file_path (Path): The path to the .env file to be created.
        default_config (Config): The Config instance containing the default values.
    """
    with env_file_path.open("w") as env_file:
        for name, value in vars(default_config).items():
            if not name.startswith('_'):
                env_file.write(f"{name}={str(value)}\n")


# Define the .env file path
env_file_path = Path(".env")

# Check if the .env file exists, create it with default values if not
if not env_file_path.exists():
    default_config = Config()
    create_default_env_file(env_file_path, default_config)

# Create a global Config instance, which can be imported and used by other scripts
config = Config()
