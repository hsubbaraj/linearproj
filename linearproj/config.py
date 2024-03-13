from pydantic import BaseModel
from typing import List
import yaml

class Config(BaseModel):
    openai_api_key: str
    conversation_paths: List[str]
    linear_api_key: str
    linear_team_id: str
    linear_bug_label_id: str
    linear_feature_request_label_id: str
    linear_engineering_label_id: str


def load_config():
    with open("config.yml", "r") as file:
        config_data = yaml.safe_load(file)
    config = Config(**config_data)
    return config

CONFIG = load_config()