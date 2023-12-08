class BaseValidatorMixin:
    """Mixin class for common validators."""

    @staticmethod
    def validate_string(key: str, value: str, max_length: int = None, nullable: bool = False) -> str:
        """Validates that value is a string and, if provided, is not longer than max_length."""
        if value is None and not nullable:
            raise ValueError(f"{key} cannot be None")
        if value is not None:
            if not isinstance(value, str):
                raise ValueError(f"{key} must be a string")
            if max_length is not None and len(value) > max_length:
                raise ValueError(f"{key} must be a string with no more than {max_length} characters (received {len(value)} characters)")
        return value

    @staticmethod
    def validate_integer(key: str, value: int, min_value: int = None, max_value: int = None, nullable: bool = False) -> int:
        """Validates that value is an integer and, if provided, is within the specified range."""
        if value is None and not nullable:
            raise ValueError(f"{key} cannot be None")
        if value is not None:
            if not isinstance(value, int):
                raise ValueError(f"{key} must be an integer")
            if min_value is not None and value < min_value:
                raise ValueError(f"{key} must be greater than or equal to {min_value}")
            if max_value is not None and value > max_value:
                raise ValueError(f"{key} must be less than or equal to {max_value}")
        return value

    @staticmethod
    def validate_boolean(key: str, value: bool, nullable: bool = False) -> bool:
        """Validates that value is a boolean."""
        if value is None and not nullable:
            raise ValueError(f"{key} cannot be None")
        if value is not None and not isinstance(value, bool):
            raise ValueError(f"{key} must be a boolean")
        return value

    @staticmethod
    def validate_choice(key: str, value: str, choices: list, nullable: bool = False) -> str:
        """Validates that value is one of the provided choices."""
        if value is None and not nullable:
            raise ValueError(f"{key} cannot be None")
        if value is not None and value not in choices:
            raise ValueError(f"{key} must be one of {', '.join(choices)}")
        return value
