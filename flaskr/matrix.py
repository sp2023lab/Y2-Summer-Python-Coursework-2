def create_matrix(rows, cols):
    matrix = [[0 for _ in range(cols)] for _ in range(rows)]

    for i in range(rows):
        for j in range(cols):
            matrix[i][j] = 0

    return matrix

def reserve_matrix(matrix, version):
    rows = len(matrix)
    cols = len(matrix[0])

    for i in range(rows):
        for j in range(cols):
            if (i < 9 and j < 9) or (i < 9 and j >= cols - 8) or (i >= rows - 8 and j < 9):
                matrix[i][j] = 2
            elif (i == 6) or (j == 6):
                matrix[i][j] = 3
            elif version == 2 and ((i >= rows - 8) and (i <= rows - 4) and (j >= cols -8) and (j <= cols - 4)):
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
    if version < 2:
        return matrix
    finder_pattern = [
        [1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 1, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1]
    ]

    # Bottom-right corner
    for i in range(5):
        for j in range(5):
            matrix[-(i + 4)][j - 8] = finder_pattern[i][j]

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

def apply_mask(matrix, mask_fn, version):
    masked = [row.copy() for row in matrix]
    rows = len(matrix)
    cols = len(matrix[0])


    for i in range(rows):
        for j in range(cols):
            if should_mask(i, j, rows, cols, version):
                if mask_fn(i, j):
                    masked[i][j] ^= 1

    return masked

def should_mask(i, j, rows, cols, version):
    # Reserved finder/separator/alignment/timing areas
    if (i < 9 and j < 9) or (i < 9 and j >= 21 - 8) or (i >= 21 - 8 and j < 9):
        return False
    if i == 6 or j == 6:
        return False
    if version == 2 and (i >= rows - 8) and (i <= rows - 4) and (j >= cols -8) and (j <= cols - 4):
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

            
    print(f'1st penalty: {penalty}')
    return penalty

def penalty_rule2(matrix):
    penalty = 0
    size = len(matrix)

    for i in range(size - 1):
        for j in range(size - 1):
            if matrix[i][j] == matrix[i][j+1] == matrix[i+1][j] == matrix[i+1][j+1]:
                penalty += 3

    print(f'2nd penalty: {penalty}')
    return penalty

def penalty_rule3(matrix):
    penalty = 0
    size = len(matrix)
    pattern = [1, 0, 1, 1, 1, 0, 1]

    for row in matrix:
        for i in range(size - 6):
            if row[i:i+7] == pattern:
                if (i >= 4 and row[i-4:i] == [0, 0, 0, 0]) or (i+11 <= size and row[i+7:i+11] == [0, 0, 0, 0]):

                    penalty += 40

    for j in range(size):
        col = [matrix[i][j] for i in range(size)]
        for i in range(size - 6):
            if col[i:i+7] == pattern:
                if (i >= 4 and row[i-4:i] == [0, 0, 0, 0]) or (i+11 <= size and row[i+7:i+11] == [0, 0, 0, 0]):
                    penalty += 40

    print(f'3rd penalty: {penalty}')
    return penalty

def penalty_rule4(matrix):
    dark = sum(cell for row in matrix for cell in row if cell == 1)
    total = len(matrix) ** 2
    ratio = dark / total * 100
    k = abs(ratio - 50) // 5

    print(f'4th penalty: {int(k) * 10}')
    return int(k) * 10


def calculate_penalty(matrix):
    print(f'Total penalties are: {penalty_rule1(matrix) + penalty_rule2(matrix) + penalty_rule3(matrix) + penalty_rule4(matrix)}')
    return (
        penalty_rule1(matrix) +
        penalty_rule2(matrix) +
        penalty_rule3(matrix) +
        penalty_rule4(matrix)
    )

def add_format_information(matrix, mask_id=0):
    # ECC Level: L (01), Mask: 000
    # Final masked format bits: 111011111000100
    format_bits = [1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0]
    size = len(matrix)

    # Horizontal format info (top-left)
    for i in range(6):
        matrix[8][i] = format_bits[i]
    matrix[8][7] = format_bits[6]
    matrix[8][8] = format_bits[7]
    matrix[7][8] = format_bits[8]

    # Vertical format info (top-left)
    for i in range(6):
        matrix[i][8] = format_bits[14 - i]

    # Top-right horizontal
    for i in range(8):
        matrix[8][size - 1 - i] = format_bits[i]

    # Bottom-left vertical
    for i in range(7):
        matrix[size - 1 - i][8] = format_bits[8 + i]

    # Dark module
    matrix[size - 8][8] = 1

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

def add_data(matrix, data, ecc):
    bits = data + ecc
    size = len(matrix)
    idx = 0

    def is_reserved(i, j):
        return matrix[i][j] in (2, 3)

    j = size - 1
    upward = True

    while j > 0:
        if j == 6:
            j -= 1  # Skip vertical timing
        row_range = range(size - 1, -1, -1) if upward else range(size)
        for i in row_range:
            for dj in [0, -1]:
                col = j + dj
                if col >= 0 and not is_reserved(i, col):
                    if idx < len(bits):
                        matrix[i][col] = bits[idx]
                        idx += 1
        j -= 2
        upward = not upward

    return matrix
