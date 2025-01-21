from typing import Any
from utils.functions import parse_headers, parse_config_file
from utils.validators import (
    is_positive_int,
    is_normal_int,
    is_non_blank_string,
    is_string_key_value_dict,
    is_valid_url,
    is_valid_rate_limit, is_colon_separated_key_value
)


def hint():
    print(
        "welcome :)\n"
        "in order to run the service choose one of below\n"
        "1) enter providers config manually\n"
        "2) use default config file\n"
    )


def _get_coerced_input(type_: Any, prompt_message: str, validator=None) -> Any | None:
    while True:
        user_input = input(prompt_message)
        try:
            value = type_(user_input)
            if validator is not None:
                ok, error = validator(value)
                if ok:
                    return value
                print(error + "\n")
        except ValueError:
            print(f"{user_input} is not a valid {type_.__name__}\n")


def option_prompt() -> str:
    while (option := input("enter option: ")) not in ["1", "2"]:
        print("invalid option :/\n")
    return option


def get_config_manually() -> dict[str, dict]:
    providers_config: dict[str, dict] = {}
    providers_count = _get_coerced_input(
        type_=int, prompt_message="[1/3]-enter providers count: ", validator=is_positive_int
    )

    for provider in range(providers_count):
        provider_name = _get_coerced_input(
            type_=str, prompt_message="\t[1/4]enter provider name: ", validator=is_non_blank_string
        )
        api_endpoint = _get_coerced_input(
            type_=str, prompt_message="\t[2/4]enter provider endpoint api: ", validator=is_valid_url
        )
        rate_limit = _get_coerced_input(
            type_=float, prompt_message="\t[3/4]enter provider rate_limit: ", validator=is_valid_rate_limit
        )
        headers = {}
        headers_count = _get_coerced_input(
            type_=int, prompt_message="\t[4/4]enter headers count [0 if no headers]: ", validator=is_normal_int
        )
        for counter in range(headers_count):
            key_value = _get_coerced_input(
                type_=str, prompt_message=f"\t\t[1/1]enter key_value_{counter} separated by colon(:): ",
                validator=is_colon_separated_key_value
            )
            headers.update(parse_headers(key_value))

        providers_config[provider_name] = {
            "api_endpoint": api_endpoint,
            "rate_limit": rate_limit,
            "headers": headers,
        }
    print("Setup Completed.")
    return providers_config


OPTION_2_CONFIG_FUNCTION = {
    "1": get_config_manually,
    "2": parse_config_file  # custom file is not implemented :)
}


def load_config():
    hint()
    option = option_prompt()
    config_function = OPTION_2_CONFIG_FUNCTION[option]

    return config_function()
