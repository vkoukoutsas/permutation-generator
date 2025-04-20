# **Permutation Generator**

A powerful tool for generating permutations of a given string with support for uppercase/lowercase letters, digits, and special characters. The script offers multiple options for customization, such as limiting the number of permutations, choosing output formats (`.txt`, `.csv`, `.json`), and utilizing a GUI or command-line interface.

---

## **Features**

- **String Permutation**: Generates all permutations of a given string.
- **Customization**: 
  - Choose whether to include uppercase/lowercase letters, digits, and/or special characters.
  - Limit the number of permutations generated.
- **Multiple Export Formats**: Export results in `.txt`, `.csv`, or `.json` formats.
- **Multi-core Processing**: Utilizes multiple CPU cores to speed up the generation and writing of permutations.
- **GUI Interface**: A simple Tkinter-based GUI to make usage easier.
- **Auto Compression**: Large result files are automatically compressed into `.zip` files.

---

## **Installation**

1. **Clone the repository or download the script**.

   ```bash
   git clone https://your-repo-url.git
   cd permgen
   ```

2. **Install necessary dependencies**.

   For **Ubuntu/Debian-based systems**, run:

   ```bash
   sudo apt update
   sudo apt install python3-tk
   ```

   Ensure that Python 3 and `pip` are installed. If you don’t have `tkinter` installed, you can run:

   ```bash
   sudo apt install python3-tk
   ```

3. **Install any additional dependencies** (if any).

   ```bash
   pip install -r requirements.txt  # If you have dependencies
   ```

---

## **Usage**

### **Command-Line Interface (CLI)**

#### Basic Usage

Generate permutations of the string with the default settings (all variants enabled):

```bash
python3 permgen_full.py <input_string>
```

#### Options:

- `--characters`: Include both uppercase and lowercase letters.
- `--digits`: Include digits (0-9).
- `--special`: Include special characters (`!@#$%^&*()_+-=[]{}|;:,.<>?`).
- `--export <format>`: Choose the export format (`txt`, `csv`, `json`).
- `--max <number>`: Limit the maximum number of permutations to generate.
- `--progress`: Show progress as permutations are being generated.
- `--gui`: Launch the graphical user interface (GUI).

#### Examples:

1. **Generate permutations with all variants** and save to `.txt` (default format):

   ```bash
   python3 permgen_full.py a1!b2@C3#
   ```

2. **Generate permutations with digits and letters**, export to `.csv`, and limit to 1000 permutations:

   ```bash
   python3 permgen_full.py abc123 --characters --digits --export csv --max 1000
   ```

3. **Launch the GUI** to generate permutations interactively:

   ```bash
   python3 permgen_full.py --gui
   ```

---

### **Graphical User Interface (GUI)**

1. **Launch the GUI**:

   ```bash
   python3 permgen_full.py --gui
   ```

2. **In the GUI**:
   - **Input String**: Enter the string to permute.
   - **Check Options**: Select whether to include letters, digits, and/or special characters.
   - **Max Permutations**: Optionally, enter the maximum number of permutations to generate.
   - **Export Format**: Choose the output format (`txt`, `csv`, `json`).
   - **Progress**: Check to show progress while generating.
   - **Generate**: Click to start the permutation generation process.

---

## **Estimated Output Size**

Before generating the permutations, the script will **estimate** the total number of permutations and show the expected file size. You will be prompted to confirm if you'd like to proceed with the generation.

---

## **Example Output**

### **Console Output**:

```bash
Estimated permutations: 2,097,152
Estimated file size: 1.25 MB
Continue? [y/N]: y
Generating permutations...
Done. Saved 1,000 permutations to a1!b2@C3#.txt
```

### **GUI Output**:

After generating permutations, the GUI will display a success message showing the location of the saved file and the total number of permutations written.

---

## **File Compression**

For **large results** (more than 10,000 permutations), the script will automatically **compress the output file** into a `.zip` archive to save disk space.

---

## **Performance**

This script leverages **multi-core processing** to speed up the generation and writing of permutations. This allows you to handle large sets of permutations without significant slowdowns, especially when working with longer strings.

---

## **Notes**

- If your machine has **limited memory** or is generating **massive outputs**, it might take some time depending on the input string.
- For very long strings, consider limiting the number of permutations or using the `--max` flag to restrict the output.

---

## **Contributions**

Feel free to **open issues** or **submit pull requests** for any improvements or fixes. If you encounter any bugs or need additional features, please let us know!

---

## **License**

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

Let me know if you need any adjustments or want to add more details to the README!