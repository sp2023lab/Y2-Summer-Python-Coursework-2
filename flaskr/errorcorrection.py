import reedsolo

def reed_solomon_encode(data, level):
    level_mapping = {
        'L1': 7,   # Version 1, ECC level L → 7 codewords
        'L2': 10   # Version 2, ECC level L → 10 codewords
    }

    if level not in level_mapping:
        raise ValueError(f"Invalid error correction level: {level}")
    
    rs = reedsolo.RSCodec(level_mapping[level])
    try:
        # Convert bit data to bytes
        byte_data = bytearray()
        for i in range(0, len(data), 8):
            byte = int(''.join(map(str, data[i:i+8])), 2)
            byte_data.append(byte)
        
        encoded_data = rs.encode(byte_data)
        # Extract error correction codewords
        error_correction_codewords = encoded_data[-level_mapping[level]:]
        # Convert to binary string
        binary_string = ''.join(format(byte, '08b') for byte in error_correction_codewords)
        binary_list = [int(bit) for bit in binary_string]
        return binary_list
    except reedsolo.ReedSolomonError as e:
        print(f"Error encoding data: {e}")
        return None

#def reed_solomon_encode(data, level):
#    level_mapping = {'L': 7, 'M': 15, 'Q': 25, 'H': 30}  # Example mapping
#    if level not in level_mapping:
#        raise ValueError(f"Invalid error correction level: {level}")
#    
#    rs = reedsolo.RSCodec(level_mapping[level])
#    try:
#        encoded_data = rs.encode(data)
#        # Extract error correction codewords
#        error_correction_codewords = encoded_data[len(data):]
#        # Convert to binary string
#        binary_string = ''.join(format(byte, '08b') for byte in error_correction_codewords)
#        binary_list = list(map(int, binary_string))
#        return binary_list
#    except reedsolo.ReedSolomonError as e:
#        print(f"Error encoding data: {e}")
#        return None

'0100000101000110101101101110011011110111011101101110011010110110111001101111011101110110111001101011011011100110111101110111011011100110101101101110011011110111011101101110000011101100000100011110110000010001111011000001000111101100000100011110110000010001111011000001000111110111110101111110100101010100011101100010111011100100100100010001110010101101'
'0100000101000110101101101110011011110111011101101110011010110110111001101111011101110110111001101011011011100110111101110111011011100110101101101110011011110111011101101110000011101100000100011110110000010001111011000001000111101100000100011110110000010001111011000001000111110111110101111110100101010100011101100010111011100100100100010001110010101101'