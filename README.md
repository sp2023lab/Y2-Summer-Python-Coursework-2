## This is the gitlab repo for the CS2PP QR code project.

#### a) Application Overview &amp; Instructions

The files are split into 2 folders. The version 1 folder contains the files responsible for the original program which only has version 1 functionality. The version 2 folder contains the modified files which adds the project enhancements, as well as version 2 functionality.

To use the the program you need to enter one of the folders and open a command prompt/terminal in that folder. Make sure to install flask and then run the following command:

```
flask --app QR run
```
You then need to head over to a browser and open this webpage:
```
http://localhost:5000
```

The version 1 program has limited functionality, It creates a version 1 QR code from a string and that's it. The version 2 program can also generate version 2 QR codes by dynamically selecting the required QR version for the input text. There are also options to change the background colour and the data colour of the QR code. The program is divided into modules to handle byte encoding, error correction, matrix generation and styling.


#### b) Programming Paradigms Used
Visual representation of the program is shown bellow: Programming Paradigms Used The application is implemented using several programming paradigms. The control of application flow and data processing is managed through imperative programming. These tools are exploited especially in the `matrix.py` module, where functional programming paradigms like lambda functions and list comprehensions allow for quick and clean data manipulations.


#### c) Social, Legal, Ethical Considerations
The web interface will be accessible across multiple devices and simple enough to be used by anyone with minimal barriers, allowing users of all backgrounds equal access to the program object-oriented programming is demonstrated by encapsulating each task in separate files, e.g. `encode.py` and `errorcorrection.py`, and the modular file structure. A note of the legal implications of QR codes, such as phishing or malicious links, is also integrated into the user interface as a disclaimer. It is also morally ethical as there is no data harvesting or storage and uses input constraints to protect against inappropriate or harmful usage. Again, this is in line with privacy, transparency and safety.


#### d) Known Flaws or Limitations
The system only uses Mask Pattern 0; the system does not automatically decide which is the best mask pattern to use. There is very little input sanitation for special characters, and no more advanced error messaging for unacceptable or unscannable output. This is something that can be explored in future iterations.


#### e) Data Handling &amp; Integrity
Input to the user is via Flask form submission, where simple validation ensures that no string is empty nor over the character length that the inputs are limited to. Usability is increased by providing feedback via Flask’s flash messages. The app functions entirely in memory, never sharing or writing any user data to disk or to another location where it might be viewable.


#### f) Real world application features:

Our application includes several features that make it suitable for real-world use in domains such as marketing, inventory management, education, and scientific tracking:

•	Automatic Version Selection: The system adjusts between Version 1 and Version 2 QR codes based on data length, ensuring efficient use of space while maintaining scannability.

•	Reed-Solomon Error Correction: Robust ECC integration (Level L) allows the QR codes to remain scannable even with partial damage or distortion, which is essential in physical environments like shipping labels and advertisements.

•	Customisation Options: Users can change foreground and background colours, allowing businesses to align QR codes with branding or enhance visibility on different surfaces.

•	Step-by-Step Visualisation: The interface shows QR construction stages, making it ideal for educational use in teaching how QR encoding and masking work.

•	Web-Based Interface: The Flask application can be deployed as a cloud tool or integrated into internal systems (e.g., warehouse inventory tools) for on-demand QR generation.


#### g) Intermediate Proof of Functionality (Test String: known):

To test the qr code generator, the input string ‘known’ was also used. This was byte agreement and the system indeed interpreted it to be in byte mode as it had the mode bits 0100 and the character count bits to encode the size of a string of characters 5 characters. This data was then Reed-Solomon encoded at level L, thus producing 19 data and 7 ECC codewords. These were arranged in a 21×21 matrix following the QR Version 1 stipulations, with finder patterns, timing patterns, format information, and the Mask Pattern 0 applied. The console output confirmed each intermediate operation of that process from the data encoded to the masking was working, and the final QR code was scannable by a standard mobile reader. For longer inputs, the system automatically switched to Version 2, which uses a 25×25 matrix layout.

Stage 1: Reserved Matrix
	
Stage 2: With Data and Patterns
	
Stage 3: After Masking
	
Stage 4: Final QR Code (with Format Info)

The QR is successfully scanned using a mobile phone QR reader.


#### h) Screen-capture Animation:

[Output Video](./Screen_Recording_2025-05-29_222850_1_.gif)


#### References
Thonky- https://www.thonky.com/qr-code-tutorial/

Flask Documentation- https://flask.palletsprojects.com/en/stable/


#### Extra notes:

This was a group project
