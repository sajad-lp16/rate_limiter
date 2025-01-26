import json
from utils.validators import is_colon_separated_key_value


def parse_config_file(file_path: str = "config.json") -> dict[str, dict]:
    with open(file_path) as file:
        config = json.load(file)

    assert config, "config file cannot be empty"
    assert isinstance(config, dict), "config file must contain mappings"
    assert all([isinstance(key, str) for key in config.keys()]), "all keys in config file must be strings"
    assert all([isinstance(key, dict) for key in config.values()]), "all values in config file must be mappings"

    required_keys = {"api_endpoint", "headers", "rate_limit"}

    for provider_config in config.values():
        assert not (required_keys - set(provider_config.keys())), \
            "all [api_endpoint, headers, rate_limit] must be present in all providers config"

    return config


def parse_headers(value: str) -> dict:
    assert is_colon_separated_key_value(value)

    key_value = value.split(":")
    return {key_value[0].strip(): key_value[1].strip()}
