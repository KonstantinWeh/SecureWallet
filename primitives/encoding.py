
def ensure_bytes(x):
    if isinstance(x, int):
        return x.to_bytes((x.bit_length() + 7) // 8, 'big')
    elif isinstance(x, str):
        return x.encode('utf-8')
    elif isinstance(x, bytes):
        return x
    else:
        raise TypeError("Unsupported input type for bytes conversion")