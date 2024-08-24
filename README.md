
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

### Generate `requirements.txt`

If you need to generate a `requirements.txt` file:

```bash
pip freeze > requirements.txt
```

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

### Testing

Synthetic data for testing can be generated using the following script:

```python
import pandas as pd
import random
from datetime import datetime, timedelta

def generate_synthetic_data(num_records=50):
    products = [f"Product_{{i}}" for i in range(1, num_records + 1)]
    data = []

    for i in range(num_records):
        old_product = products[i]
        new_product = products[i + 1] if i < num_records - 1 else old_product
        date = datetime.now() - timedelta(days=random.randint(1, 100))
        data.append([old_product, new_product, date.strftime('%Y-%m-%d')])

    df = pd.DataFrame(data, columns=["Old Product", "New Product", "Date"])
    return df

df_synthetic = generate_synthetic_data(num_records=20)
df_synthetic.to_csv("synthetic_replacement_data.csv", index=False)
df_synthetic.to_excel("synthetic_replacement_data.xlsx", index=False)
```

This script creates a CSV and Excel file with synthetic product replacement data for testing purposes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
