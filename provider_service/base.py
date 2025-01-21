from abc import ABC


class BaseProvider(ABC):
    """
    includes common behavior for all providers.

    field_2_validator:
        maps the value given for a field to it validator
    """
    def validate_fields(self, field_2_validator) -> None:
        errors = {}

        for value, validator in field_2_validator.items():
            ok, error = validator(value)
            if not ok:
                errors[value] = error

        if errors:
            raise ValueError(errors)
