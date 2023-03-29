import random


def idv2(prefix: str, *, version: int = 0, code: int = 1022) -> str:  # fix calculation
    random_bytes = (version << 127) + (code << 127) + random.getrandbits(117)
    return f"{prefix}-{random_bytes:032x}"
