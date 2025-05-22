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

    matrix_size = 21  # Example size for QR code version 1
    
    matrix_data = matrix.create_matrix(matrix_size, matrix_size)

    matrix_data = matrix.reserve_matrix(matrix_data)
    matrix_data = matrix.add_data(matrix_data, encoded_data, error_correction_codewords)



    matrix_data = matrix.add_finder_patterns(matrix_data)
    matrix_data = matrix.add_separators(matrix_data)
    matrix_data = matrix.add_timing_patterns(matrix_data)
    matrix_data = matrix.add_alignment_patterns(matrix_data, version=1)
    matrix_data = matrix.add_format_information(matrix_data)
    


    img = Image.new('RGB', (matrix_size, matrix_size), (255, 255, 255))  # Create a new image with white background
    pixels = img.load()
    for row in range(matrix_size):
        for col in range(matrix_size):
            if matrix_data[row][col] == 1:
                pixels[col, row] = (0, 0, 0)  # Set pixel to black
            elif matrix_data[row][col] == 2:
                pixels[col, row] = (255, 0, 0)  # Set pixel to red
            elif matrix_data[row][col] == 3:
                pixels[col, row] = (0, 0, 255) # Set pixel to blue
            elif matrix_data[row][col] == 4:
                pixels[col, row] = (255, 255, 0)

    img = img.resize((300, 300), Image.NEAREST)  # Resize the image for better visibility

    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = b64encode(buffered.getvalue()).decode()


#    import qrcode
#    from io import BytesIO
#    from base64 import b64encode

#    qr = qrcode.QRCode(
#        version=1,
#        error_correction=qrcode.constants.ERROR_CORRECT_L,
#        box_size=10,
#        border=4,
#    )
#    qr.add_data(data)
#    qr.make(fit=True)
#
#    img = qr.make_image(fill_color="black", back_color="white")
#    buffered = BytesIO()
#    img.save(buffered, format="PNG")
#    img_str = b64encode(buffered.getvalue()).decode()

    return img_str