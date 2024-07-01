# Github2Text

Github2Text is a Python application that allows users to easily convert the contents of a GitHub repository into a single text file. It provides a graphical user interface for selecting specific files from the repository and generating a comprehensive text output.

![image](https://github.com/Egalitaristen/Github2Text/assets/86793055/19c66380-d34a-4b68-bf33-6f0aa8661ee5)


## Features

- Fetch files from any public GitHub repository
- Select/deselect specific files to include in the output
- Real-time preview of the generated content
- Save the output as a .txt file
- Copy the generated content to clipboard
- Display character count and estimated token count

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/Github2Text.git
   cd Github2Text
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the script:
   ```
   python Github2Text.py
   ```

2. Enter the URL of the GitHub repository you want to convert.

3. Click "Fetch Files" to retrieve the repository structure.

4. Select/deselect the files you want to include in the output.

5. Use the "Save as .txt" button to save the generated content to a file, or "Copy Content" to copy it to your clipboard.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
