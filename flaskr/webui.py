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
import os


bp = Blueprint('webui', __name__, url_prefix='/webui')

#@bp.route('/test')
def test():
    return "Test route is working!"

@bp.route('/', methods=['GET', 'POST'])
def index():
    qr_code_url = None    
    
    version = int(request.form.get("version", 1))  # default to version 1
    if request.method == 'POST':
        data = request.form.get('data')  # Get the data from the form
        fg_color = request.form.get("fg", "#000000")
        bg_color = request.form.get("bg", "#ffffff")

        if not data:
            flash("No data provided!", "error")
        elif len(data) > (19 if version == 1 else 34):
            flash(f"Data must be {19 if version == 1 else 34} characters or fewer for version {version}!", "error")
        else:
            qr_code_url = f"data:image/png;base64,{generate_qr(data, version, fg_color, bg_color)}" # Generate the QR code

    return render_template('webui/index.html', qr_code_url=qr_code_url)

def generate_qr(data, version, fg_color, bg_color):

    matrix_size = 21 if version == 1 else 25
    max_data_bytes = 19 if version == 1 else 34
    ecc_level = 'L'

    if len(data) > max_data_bytes:
        raise ValueError(f"Data exceeds limit for QR version {version}")

    encoded_data = encode.byte_mode_encode(data, version)
    img_str = None

    error_correction_codewords = errorcorrection.reed_solomon_encode(encoded_data, f'{ecc_level}{version}')

    print(''.join(str(b) for b in encoded_data + error_correction_codewords))

    base_matrix = matrix.create_matrix(matrix_size, matrix_size)
    base_matrix = matrix.reserve_matrix(base_matrix)
    save_stage_image(base_matrix, "stage1_reserved.png")

    base_matrix = matrix.add_data(base_matrix, encoded_data, error_correction_codewords)
    base_matrix = matrix.add_finder_patterns(base_matrix)
    base_matrix = matrix.add_separators(base_matrix)
    base_matrix = matrix.add_timing_patterns(base_matrix)
    base_matrix = matrix.add_alignment_patterns(base_matrix, version=version)
    save_stage_image(base_matrix, "stage2_patterns_data.png")

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
    
    save_stage_image(best_matrix, "stage3_masked.png")
    
    
    # Add format info using best_mask_id
    final_matrix = matrix.add_format_information(best_matrix, best_mask_id)

    # --------- Clean matrix of debug values ---------
    for row in range(len(final_matrix)):
        for col in range(len(final_matrix[0])):
            if final_matrix[row][col] not in [0, 1]:
                final_matrix[row][col] = 0


    save_stage_image(final_matrix, "stage4_final.png")


    # --------- Convert Matrix to Image ---------

    bg_rgb = tuple(int(bg_color[i:i+2], 16) for i in (1, 3, 5))
    fg_rgb = tuple(int(fg_color[i:i+2], 16) for i in (1, 3, 5))

    img = Image.new('RGB', (matrix_size, matrix_size), bg_rgb)


    pixels = img.load()
    for row in range(matrix_size):
        for col in range(matrix_size):
            pixels[col, row] = fg_rgb if final_matrix[row][col] == 1 else bg_rgb
            
    # Clean all debug markings (2 = reserved, 3 = timing, 4 = debug)
    for row in range(matrix_size):
        for col in range(matrix_size):
            if final_matrix[row][col] > 1:
                final_matrix[row][col] = 0  # Or set appropriately to 0 or 1 if known


    img = img.resize((300, 300), Image.NEAREST)
    

    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = b64encode(buffered.getvalue()).decode()

    return img_str

def save_stage_image(matrix, filename):
    size = len(matrix)
    img = Image.new('RGB', (size, size), (255, 255, 255))
    pixels = img.load()

    for row in range(size):
        for col in range(size):
            val = matrix[row][col]
            if val == 1:
                pixels[col, row] = (0, 0, 0)
            elif val == 2:
                pixels[col, row] = (255, 0, 0)
            elif val == 3:
                pixels[col, row] = (0, 0, 255)
            elif val == 4:
                pixels[col, row] = (255, 255, 0)

    img = img.resize((300, 300), Image.NEAREST)

    # ✅ Use absolute path to "static/" one level up
    static_path = os.path.join(os.path.dirname(__file__), 'static', filename)
    static_path = os.path.abspath(static_path)

    os.makedirs(os.path.dirname(static_path), exist_ok=True)
    img.save(static_path)