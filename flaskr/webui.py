from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from PIL import Image
from . import encode
from . import errorcorrection
from . import matrix
from io import BytesIO
from base64 import b64encode


bp = Blueprint('webui', __name__, url_prefix='/webui')

@bp.route('/test')
def test():
    return "Test route is working!"

@bp.route('/', methods=['GET', 'POST'])
def index():
    qr_code_url = None  # Initialize the QR code URL as None

    if request.method == 'POST':
        data = request.form.get('data')  # Get the data from the form
        if not data:
            flash("No data provided!", "error")
        elif len(data) > 17:
            flash("Data must be 17 characters or fewer!", "error")
        else:
            qr_code_url = f"data:image/png;base64,{generate_qr(data)}"  # Generate the QR code

    return render_template('webui/index.html', qr_code_url=qr_code_url)

def generate_qr(data):
    encoded_data = encode.byte_mode_encode(data)
    img_str = None

    error_correction_codewords = errorcorrection.reed_solomon_encode(encoded_data, 'L')
    matrix_size = 21  # QR Code Version 1

    base_matrix = matrix.create_matrix(matrix_size, matrix_size)
    base_matrix = matrix.reserve_matrix(base_matrix)
    base_matrix = matrix.add_data(base_matrix, encoded_data, error_correction_codewords)
    base_matrix = matrix.add_finder_patterns(base_matrix)
    base_matrix = matrix.add_separators(base_matrix)
    base_matrix = matrix.add_timing_patterns(base_matrix)
    base_matrix = matrix.add_alignment_patterns(base_matrix, version=1)

    # --------- Apply All Masks & Select Best One ---------
    best_score = float('inf')
    best_matrix = None
    best_mask_id = 0

    for mask_id in range(8):
        mask_fn = matrix.get_mask_function(mask_id)
        masked_matrix = matrix.apply_mask(base_matrix, mask_fn)
        score = matrix.calculate_penalty(masked_matrix)

        if score < best_score:
            best_score = score
            best_mask_id = mask_id
            best_matrix = masked_matrix

    # Add format info using best_mask_id
    final_matrix = matrix.add_format_information(best_matrix, best_mask_id)

    # --------- Convert Matrix to Image ---------
    img = Image.new('RGB', (matrix_size, matrix_size), (255, 255, 255))  # White background
    pixels = img.load()
    for row in range(matrix_size):
        for col in range(matrix_size):
            if final_matrix[row][col] == 1:
                pixels[col, row] = (0, 0, 0)      # Black
            elif final_matrix[row][col] == 2:
                pixels[col, row] = (255, 0, 0)    # Red (Reserved)
            elif final_matrix[row][col] == 3:
                pixels[col, row] = (0, 0, 255)    # Blue (Timing)
            elif final_matrix[row][col] == 4:
                pixels[col, row] = (255, 255, 0)  # Yellow (Debug)

    img = img.resize((300, 300), Image.NEAREST)

    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = b64encode(buffered.getvalue()).decode()

    return img_str
