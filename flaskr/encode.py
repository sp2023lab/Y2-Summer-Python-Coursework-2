def byte_mode_encode(data, version=1):
    # Step 1: Mode Indicator (Byte Mode = '0100')
    mode_indicator = '0100'

    # Step 2: Character Count Indicator
    # Version 1–9 uses 8 bits for Byte mode
    char_count = len(data)
    char_count_indicator = f'{char_count:08b}'  # 8-bit binary

    # Step 3: Encode each character as 8-bit ISO-8859-1 binary
    if isinstance(data, str):
        encoded_bytes = data.encode('iso-8859-1')  # Use ISO-8859-1
    elif isinstance(data, bytes):
        encoded_bytes = data
    else:
        raise TypeError("Data must be a string or bytes.")

    byte_bits = ''.join(f'{byte:08b}' for byte in encoded_bytes)

    # Step 4: Combine into bit string
    bits = mode_indicator + char_count_indicator + byte_bits

    # Step 5: Terminator (up to 4 zeros if needed)
    max_bits = 152 if version == 1 else 272
    if len(bits) < max_bits:
        bits += '0' * min(4, max_bits - len(bits))

    # Step 6: Make multiple of 8
    if len(bits) % 8 != 0:
        bits += '0' * (8 - (len(bits) % 8))

    # Step 7: Pad with 0xEC and 0x11 alternately
    pad_bytes = ['11101100', '00010001']
    i = 0
    while len(bits) < max_bits:
        bits += pad_bytes[i % 2]
        i += 1
    print("FML",len(bits))

    # Final output: convert to list of ints (bitstream)
    return list(map(int, bits))
'''
0100000001010110101101101110011011110111011101101110000011101100000100011110110000010001111011000001000111101100000100011110110000010001111011000001000111101011100100000100100010100101001110111001101100010001
0100000001010110101101101110011011110111011101101110000011101100000100011110110000010001111011000001000111101100000100011110110000010001111011000001000111101011100100000100100010100101001110111001101100010001
'''