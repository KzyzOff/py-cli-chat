

def right_pad(data: str, width_bytes: int) -> str:
    return ' ' * (width_bytes - len(data)) + data
