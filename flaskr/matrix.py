import reedsolo

def create_matrix(rows, cols):
    matrix = [[0 for _ in range(cols)] for _ in range(rows)]

    for i in range(rows):
        for j in range(cols):
            matrix[i][j] = 0

    return matrix

def reserve_matrix(matrix):
    rows = len(matrix)
    cols = len(matrix[0])

    for i in range(rows):
        for j in range(cols):
            if (i < 9 and j < 9) or (i < 9 and j >= cols - 8) or (i >= rows - 8 and j < 9):
                matrix[i][j] = 2
            elif (i == 6) or (j == 6):
                matrix[i][j] = 3

    return matrix

def add_finder_patterns(matrix):
    finder_pattern = [
        [1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 0, 1],
        [1, 0, 1, 1, 1, 0, 1],
        [1, 0, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1]
    ]

    for i in range(7):
        for j in range(7):
            matrix[i][j] = finder_pattern[i][j]

    # Top-right corner
    for i in range(7):
        for j in range(7):
            matrix[i][-(j + 1)] = finder_pattern[i][j]

    # Bottom-left corner
    for i in range(7):
        for j in range(7):
            matrix[-(i + 1)][j] = finder_pattern[i][j]


    return matrix

def add_separators(matrix):
    rows = len(matrix)
    cols = len(matrix[0])

    for row in range(rows):
        for col in range(cols):
            if (row == 7 and (col < 8 or col >= cols - 8)) or (col == 7 and (row < 8 or row >= rows - 8)) or (row == rows - 8 and (col < 8)) or (col == cols - 8 and (row < 8)):
                matrix[row][col] = 0

    

    return matrix

def add_timing_patterns(matrix):
    rows = len(matrix)
    cols = len(matrix[0])

    for i in range(8, rows - 8):
        matrix[i][6] = 1 if i % 2 == 0 else 0
        matrix[6][i] = 1 if i % 2 == 0 else 0

    return matrix

def add_alignment_patterns(matrix, version):
    alignment_patterns = {
        1: [],
        2: [(6, 18)],
    }

    if version in alignment_patterns:
        for pattern in alignment_patterns[version]:
            row, col = pattern
            matrix[row][col] = 1

    return matrix

def get_mask_function(mask_id):
    return [
        lambda i, j: (i + j) % 2 == 0,
        lambda i, j: i % 2 == 0,
        lambda i, j: j % 3 == 0,
        lambda i, j: (i + j) % 3 == 0,
        lambda i, j: (i // 2 + j // 3) % 2 == 0,
        lambda i, j: ((i * j) % 2 + (i * j) % 3) == 0,
        lambda i, j: (((i * j) % 2 + (i * j) % 3) % 2) == 0,
        lambda i, j: (((i + j) % 2 + (i * j) % 3) % 2) == 0,
    ][mask_id]

def apply_mask(matrix, mask_fn):
    masked = [row.copy() for row in matrix]
    size = len(matrix)

    for i in range(size):
        for j in range(size):
            if should_mask(i, j):
                if mask_fn(i, j):
                    masked[i][j] ^= 1

    return masked

def should_mask(i, j):
    # Reserved finder/separator/alignment/timing areas
    if (i < 9 and j < 9) or (i < 9 and j >= 21 - 8) or (i >= 21 - 8 and j < 9):
        return False
    if i == 6 or j == 6:
        return False
    return True

def penalty_rule1(matrix):
    penalty = 0
    size = len(matrix)

    for row in matrix:
        count = 1
        for i in range(1, size):
            if row[i] == row[i - 1]:
                count += 1
            else:
                if count >= 5:
                    penalty += 3 + (count - 5)
                count = 1
        if count >= 5:
            penalty += 3 + (count - 5)

    for col in zip(*matrix):
        count = 1
        for i in range(1, size):
            if col[i] == col[i - 1]:
                count += 1
            else:
                if count >= 5:
                    penalty += 3 + (count - 5)
                count = 1
        if count >= 5:
            penalty += 3 + (count - 5)

    return penalty

def penalty_rule2(matrix):
    penalty = 0
    size = len(matrix)

    for i in range(size - 1):
        for j in range(size - 1):
            if matrix[i][j] == matrix[i][j+1] == matrix[i+1][j] == matrix[i+1][j+1]:
                penalty += 3

    return penalty

def penalty_rule3(matrix):
    penalty = 0
    size = len(matrix)
    pattern = [1, 0, 1, 1, 1, 0, 1]

    for row in matrix:
        for i in range(size - 6):
            if row[i:i+7] == pattern:
                if i >= 4 and row[i-4:i] == [0, 0, 0, 0] or i+11 <= size and row[i+7:i+11] == [0, 0, 0, 0]:
                    penalty += 40

    for j in range(size):
        col = [matrix[i][j] for i in range(size)]
        for i in range(size - 6):
            if col[i:i+7] == pattern:
                if i >= 4 and col[i-4:i] == [0, 0, 0, 0] or i+11 <= size and col[i+7:i+11] == [0, 0, 0, 0]:
                    penalty += 40

    return penalty

def penalty_rule4(matrix):
    dark = sum(cell for row in matrix for cell in row if cell == 1)
    total = len(matrix) ** 2
    ratio = dark / total * 100
    k = abs(ratio - 50) // 5
    return int(k) * 10


def calculate_penalty(matrix):
    return (
        penalty_rule1(matrix) +
        penalty_rule2(matrix) +
        penalty_rule3(matrix) +
        penalty_rule4(matrix)
    )

def add_format_information(matrix, mask_id):
    rows = len(matrix)
    cols = len(matrix[0])
    mask = format(mask_id, '03b')
    correction_level = '01'

    format_info = f'{correction_level}{mask}'
    format_info = list(map(int, format_info))

    rs = reedsolo.RSCodec(10)
    try:
        # Convert bit data to bytes
        byte_data = bytearray()
        for i in range(0, len(format_info), 8):
            byte = int(''.join(map(str, format_info[i:i+8])), 2)
            byte_data.append(byte)
        
        encoded_data = rs.encode(byte_data)
        # Extract error correction codewords
        error_correction_codewords = encoded_data[10:]
        # Convert to binary string
        binary_string = ''.join(format(byte, '08b') for byte in error_correction_codewords)
        binary_list = [int(bit) for bit in binary_string]
    except reedsolo.ReedSolomonError as e:
        print(f"Error encoding data: {e}")

    # Append the error correction bits to the format information
    format_info.extend(binary_list)

    
    #format_info = list(map(str, "111011111000100"))
    format_info_inverse = format_info[::-1]

    print(f"Format info: {format_info}")

    matrix[rows - 8][8] = 1 # dark module

    for i in range(7):
        matrix[rows - 1 - i][8] = int(format_info[i])  # Vertical format info (bottom-left)

        if i < 6:
            matrix[8][i] = int(format_info[i])  # Horizontal format info (top-left)
        else:
            matrix[8][i + 1] = int(format_info[i])  # Horizontal format info (top-left)

        print(f"Adding format info index: {i} at ({rows - 1 - i}, 8)")

    for i in range(8):
        matrix[8][cols - 1 - i] = int(format_info_inverse[i])  # Horizontal format info (top-right)


        if i < 6:
            matrix[i][8] = int(format_info_inverse[i])
            print(f"Adding format info indexd: {i} at ({i - 7}, 8)")
            print(f"info: {format_info_inverse[i]}")
        else:
            matrix[i + 1][8] = int(format_info_inverse[i])
            print(f"Adding format info indexd: {i} at ({i - 6}, 8)")
            print(f"info: {format_info_inverse[i]}")


    return matrix

def add_data_mask(matrix):
    rows = len(matrix)
    cols = len(matrix[0])

    for i in range(rows):
        for j in range(cols):
            # Skip reserved areas for timing, alignment, and format information
            if (i < 9 and j < 9) or (i < 9 and j >= cols - 8) or (i >= rows - 8 and j < 9) or (i == 6) or (j == 6):
                continue

            if (i + j) % 2 == 0:
                matrix[i][j] = 1 - matrix[i][j]

    return matrix




# The data is placed in a zigzag pattern starting from the bottom right corner of the matrix
# to go up
# go left one, then up and right one and repeat until top is reached
# if top is reached, go left twice and down one, then place data, go left one and start going down diagonally
# to go down
# go left one, then down and right one and repeat until bottom is reached
# if bottom is reached, go left twice and up one, then place data, go left one more and start going up diagonally again
#0100000001010110101101101110011011110111011101101110000011101100000100011110110000010001111011000001000111101100000100011110110000010001111011000001000111101011100100000100100010100101001110111001101100010001
#0100000001010110101101101110011011110111011101101110000011101100000100011110110000010001111011000001000111101100000100011110110000010001111011000001000111101011100100000100100010100101001110111001101100010001

def add_data(matrix, data, error_correction_codewords):

    rows = len(matrix)
    cols = len(matrix[0])

    timeout = 0

    data_bits = data + error_correction_codewords
    data_index = 0

    vertical = rows - 1
    horizontal = cols - 1

    data_bits_text = ''.join(map(str, data_bits))
    print(f"Data: {data_bits_text}")

    while data_index < len(data_bits):
        if timeout > 300:
            print("Timeout reached while adding data")
            break
        timeout += 1

        print("Moving UP")
        while (True):
            if data_index == 0:
                print(f"vertical: {vertical}, horizontal: {horizontal}, data_index: {data_index}, data: {data_bits[data_index]}")
                matrix[vertical][horizontal] = data_bits[data_index]
                data_index += 1
            

            horizontal -= 1

            if matrix[vertical][horizontal] == 3:
                horizontal -= 1
                print("hit vertical timing pattern")
                print(f"vertical: {vertical}, horizontal: {horizontal}, data_index: {data_index}, data: {data_bits[data_index]}")
                matrix[vertical][horizontal] = data_bits[data_index]
                data_index += 1

            if horizontal < 0:
                break

            if data_index >= len(data_bits):
                break
            
            print(f"vertical: {vertical}, horizontal: {horizontal}, data_index: {data_index}, data: {data_bits[data_index]}")
            matrix[vertical][horizontal] = data_bits[data_index]
            data_index += 1

            if data_index >= len(data_bits):
                break

            vertical -= 1
            horizontal += 1

            if vertical < 0 or matrix[vertical][horizontal] == 2:
                vertical += 1
                horizontal -= 2

                if matrix[vertical][horizontal] == 3:
                    horizontal -= 1
                    print("hit vertical timing pattern")

                print(f"vertical: {vertical}, horizontal: {horizontal}, data_index: {data_index}, data: {data_bits[data_index]}")
                matrix[vertical][horizontal] = data_bits[data_index]
                data_index += 1
                break
            elif matrix[vertical][horizontal] == 3:
                vertical -= 1
                print(f"vertical: {vertical}, horizontal: {horizontal}, data_index: {data_index}, data: {data_bits[data_index]}")
                matrix[vertical][horizontal] = data_bits[data_index]
                data_index += 1
            else:
                print(f"vertical: {vertical}, horizontal: {horizontal}, data_index: {data_index}, data: {data_bits[data_index]}")
                matrix[vertical][horizontal] = data_bits[data_index]
                data_index += 1

        print("Moving DOWN")
        while (True):
            if data_index >= len(data_bits):
                break

            horizontal -= 1

            if matrix[vertical][horizontal] == 3:
                horizontal -= 1
                print("hit vertical timing pattern")
                print(f"vertical: {vertical}, horizontal: {horizontal}, data_index: {data_index}, data: {data_bits[data_index]}")
                matrix[vertical][horizontal] = data_bits[data_index]
                data_index += 1

            if horizontal < 0:
                break

            print(f"vertical: {vertical}, horizontal: {horizontal}, data_index: {data_index}, data: {data_bits[data_index]}")
            matrix[vertical][horizontal] = data_bits[data_index]
            data_index += 1

            if data_index >= len(data_bits):
                break

            vertical += 1
            horizontal += 1
            

            if vertical >= rows or matrix[vertical][horizontal] == 2:
                vertical -= 1
                horizontal -= 2
                while matrix[vertical][horizontal] == 2:
                    vertical -= 1

                if matrix[vertical][horizontal] == 3:
                    horizontal -= 1
                    print("hit vertical timing pattern")

                print(f"vertical: {vertical}, horizontal: {horizontal}, data_index: {data_index}, data: {data_bits[data_index]}")
                matrix[vertical][horizontal] = data_bits[data_index]
                data_index += 1
                break
            elif matrix[vertical][horizontal] == 3:
                vertical += 1
                print(f"vertical: {vertical}, horizontal: {horizontal}, data_index: {data_index}, data: {data_bits[data_index]}")
                matrix[vertical][horizontal] = data_bits[data_index]
                data_index += 1
            else:
                print(f"vertical: {vertical}, horizontal: {horizontal}, data_index: {data_index}, data: {data_bits[data_index]}")
                matrix[vertical][horizontal] = data_bits[data_index]
                data_index += 1

        if horizontal < 0:
            break

        if data_index >= len(data_bits):
            break



    matrix = add_data_mask(matrix)


    return matrix