def is_integer(
        value: int
) -> bool:
    try:
        int(value)
        return True
    except Exception:
        return False
