from urllib.parse import urlparse


def is_valid_url(url: str) -> tuple[bool, str]:
    parse_object = urlparse(url)
    if all([parse_object.scheme, parse_object.netloc]):
        return True, ""
    return False, "invalid url, [OK: http(s)://example.com]"


def is_valid_rate_limit(rate_limit: int | float) -> tuple[bool, str]:
    if not type(rate_limit) in [int, float]:
        return False, "invalid type, [OK: rate_limit > 0]"
    if rate_limit <= 0:
        return False, "invalid value, [OK: rate_limit > 0]"
    return True, ""


def is_non_blank_string(value: str) -> tuple[bool, str]:
    if value and isinstance(value, str):
        return True, ""
    return False, "invalid value, [OK: non blank string]"


def is_string_key_value_dict(mapper: dict[str, str]):
    error = ""
    if not all([isinstance(key, str) for key in mapper.keys()]):
        error += "header keys must be non blank strings"

    if not all([isinstance(key, str) for key in mapper.values()]):
        error += " header values must be non blank strings"

    if error:
        return False, error
    return True, ""


def is_positive_int(value: int) -> tuple[bool, str]:
    if value > 0:
        return True, ""
    return False, "invalid value, [OK: N > 0]"


def is_normal_int(value: int) -> tuple[bool, str]:
    if value >= 0:
        return True, ""
    return False, "invalid value, [OK: N >= 0]"


def is_colon_separated_key_value(value: str) -> tuple[bool, str]:
    key_value = value.split(":")
    if len(key_value) == 2 and all([is_non_blank_string(item) for item in key_value]):
        return True, ""
    return False, "invalid colon separated key, value pairs [OK `key:value`]"
