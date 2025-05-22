import reedsolo

def reed_solomon_encode(data, level):
    level_mapping = {'L': 7, 'M': 15, 'Q': 25, 'H': 30}  # Example mapping
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
