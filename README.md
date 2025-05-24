# QR Code Generator — Python Coursework 2

This project implements a fully interactive, web-based QR code generator using Python and Flask. It supports multiple QR encoding features and interactive customisation, including mask selection, version control, step-by-step construction views, and accessible visual styling.

---

## Features

- **Byte mode encoding** with terminator, padding, and codeword generation
- **Reed-Solomon error correction** (Level L) using `reedsolo`
- **Data matrix construction** including finder, alignment, timing, and format patterns
- **Version 1 and Version 2 QR support**
- **Masking logic**: Applies all 8 QR mask patterns and chooses the best (lowest penalty)
- **Flask web interface** for real-time generation and display
- **Step-by-step QR matrix visualisation** at each construction stage
- **User-defined foreground/background colour customisation** for accessibility
- **Responsive interface** with input validation and error handling

---

## Screenshots

### Final Output Example:
![Final QR Code](static/stage4_final.png)

### Step-by-Step Views:
- **Reserved Matrix** ![Reserved](static/stage1_reserved.png)
- **With Data + Patterns** ![Data](static/stage2_patterns_data.png)
- **After Masking** ![Mask](static/stage3_masked.png)

---

## Getting Started

### Requirements

- Python 3.10+
- `Flask`
- `Pillow`
- `reedsolo`

### Installation

```bash
git clone https://github.com/sp2023lab/Y2-Summer-Python-Coursework-2.git
cd Y2-Summer-Python-Coursework-2
pip install -r requirements.txt
