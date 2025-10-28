from loguru import logger
from loguru_config import LoguruConfig
import yaml

def load_config_section(filename: str, section_name: str):
    """Loads a specific section from a YAML configuration file."""
    with open(filename, 'r') as file:
        config = yaml.safe_load(file)
    return config.get(section_name)

log_config = load_config_section("config.yaml", "logging")
configurator = LoguruConfig.load(log_config, configure=False).parse().configure()
logger = logger

allow_origins = load_config_section("config.yaml", "allow_origins") 

db_conn_info = load_config_section("config.yaml", "db_conn_info")

checks = load_config_section("config.yaml", "checks")

jwt_info = load_config_section("config.yaml", "jwt_info")
