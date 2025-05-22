def byte_mode_encode(data):
    char_count = len(data)
    char_count_bits = f'{char_count:08b}'

    if isinstance(data, str):
        encoded_data = data.encode('iso-8859-1')
    elif isinstance(data, bytes):
        encoded_data = data
    else:
        raise TypeError("Data must be a string or bytes.")

    # Ensure each byte is represented as 8 bits, padded with leading zeros if necessary
    encoded_data = [f'{byte:08b}' for byte in encoded_data]
    encoded_data = ''.join(encoded_data)
    
    bits = encoded_data
    bits = '0100' + char_count_bits + bits

    needed_bits = 152
    total_bits = len(bits)
    if total_bits < needed_bits:
        bits += '0' * min(4, needed_bits - total_bits)

    if len(bits) % 8 != 0:
        bits += '0' * (8 - (len(bits) % 8))

    while len(bits) < needed_bits:
        bits += '11101100'
        if len(bits) < needed_bits:
            bits += '00010001'

    bits = list(map(int, bits))
    return bits