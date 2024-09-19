### English / [Русский](README_RU.md) / [中文](README_ZH.md)

**Alex(GoD) tool for .trans**

This is a simple GUI application for extracting and adding strings from/to .trans files, commonly used in game localization.

![image](https://github.com/user-attachments/assets/19307c0f-eb01-4acf-9a19-0187676bad35) ![image](https://github.com/user-attachments/assets/a0c52db5-e283-4bcb-a3fd-21087fb0d6c0)
![image](https://github.com/user-attachments/assets/bdeb6b7e-a67f-462d-826d-e8356ff56e21)


**Features:**

* Extract strings from selected columns of a .trans file.
* Add strings from a text file to a selected column of a .trans file.
* Preview the contents of a .trans file in a table format.
* Select specific files to extract from the .trans file.
* Dark theme for improved visual experience.

**How to Use:**

1. Select the .trans file using the "Browse" button.
2. Choose the column to extract strings from using the radio buttons.
3. Click "Extract Strings" to extract the strings to a text file named "output_strings.txt".
4. To add strings, select the output text file and the column to add to.
5. Click "Add Strings" to add the strings to the .trans file (a new file with "_modified" suffix will be created).
A. Use the "Preview" button to view the contents of the .trans file.
B. Use the "Select Files" button to choose specific files to extract strings from.

**Requirements:**

* Python 3
* Tkinter
* ttkthemes

**Installation:**

1. Install the required packages:
   ```
   pip install tkinter ttkthemes
   ```
2. Download the script.
3. Run the script:
   ```
   python ImExTrans.py
   ```
