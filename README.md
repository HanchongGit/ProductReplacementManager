
# Product Replacement Manager

## Overview

The **Product Replacement Manager** is a Python-based GUI application that helps manage product replacement relationships using the Union-Find data structure. The application allows you to track and find the latest replacement version of each product, import and export product replacement data, and batch process files.

## Features

- **Load and Save State**: Load a previously saved state from a `.pkl` file or download the current product mapping as a CSV or Excel file.
- **Add Replacement**: Manually add product replacements via the GUI or import replacements from a CSV or Excel file.
- **Retrieve Latest Version**: Enter a product name and retrieve the latest replacement version, including the date of the replacement.
- **Batch Process Files**: Load a CSV or Excel file, process it to find the latest version and date for each product, and save the results back to the file.

## Installation

### Requirements

Ensure you have Python installed. You can install the necessary packages by running:

```bash
pip install -r requirements.txt
```

### Packages

The following packages are required:
- pandas
- customtkinter
- tkcalendar
- openpyxl

## Usage

### Running the Application

To run the application, execute the following command:

```bash
python app.py
```

### Tabs Overview

1. **Load/Download Tab**:
    - **Load State**: Load the application state from a `.pkl` file.
    - **Download Mapping List**: Save the current product mapping as a CSV or Excel file.

2. **Add Replacement Tab**:
    - **Add Replacement**: Manually enter an old product, new product, and replacement date.
    - **Import Replacements**: Import a CSV or Excel file containing replacements to add them to the system.

3. **Retrieve Version Tab**:
    - **Retrieve Latest Version**: Enter a product name to get its latest version and the date of replacement.

4. **Batch Process Tab**:
    - **Load and Process File**: Load a CSV or Excel file, find the latest version and date for each product, and save the updated file.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
