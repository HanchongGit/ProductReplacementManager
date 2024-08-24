from tkinter import filedialog, messagebox, ttk
from customtkinter import CTk, CTkButton, CTkLabel, CTkEntry, CTkTabview
from tkcalendar import DateEntry
import pandas as pd
from product_replacement_manager import ProductReplacementManager
from datetime import datetime
import pickle


class ProductReplacementApp(CTk):
    def __init__(self, manager: ProductReplacementManager):
        super().__init__()

        self.manager = manager
        self.title("Product Replacement Manager")
        self.geometry("800x500")

        # Create Tabs
        self.tab_view = CTkTabview(self)
        self.tab_view.pack(fill="both", expand=True)

        self.tab_load_download = self.tab_view.add("Load/Download")
        self.tab_add_replacement = self.tab_view.add("Add Replacement")
        self.tab_retrieve_version = self.tab_view.add("Retrieve Version")
        self.tab_batch_process = self.tab_view.add("Batch Process")

        # Create tab contents
        self.create_load_download_tab()
        self.create_add_replacement_tab()
        self.create_retrieve_version_tab()
        self.create_batch_process_tab()

    def create_load_download_tab(self):
        # Load State Button
        self.load_button = CTkButton(self.tab_load_download, text="Load State (.pkl)", command=self.load_state)
        self.load_button.pack(pady=10)

        # Download Mapping List Button
        self.download_button = CTkButton(self.tab_load_download, text="Download Mapping List", command=self.download_mapping_list)
        self.download_button.pack(pady=10)

        # Progress Bar
        self.progress_bar = ttk.Progressbar(self.tab_load_download, orient="horizontal", length=300, mode="determinate")
        self.progress_bar.pack(pady=10)

    def create_add_replacement_tab(self):
        # Add Replacement Inputs
        self.old_product_label = CTkLabel(self.tab_add_replacement, text="Old Product")
        self.old_product_label.pack()
        self.old_product_entry = CTkEntry(self.tab_add_replacement)
        self.old_product_entry.pack(pady=5)

        self.new_product_label = CTkLabel(self.tab_add_replacement, text="New Product")
        self.new_product_label.pack()
        self.new_product_entry = CTkEntry(self.tab_add_replacement)
        self.new_product_entry.pack(pady=5)

        self.date_label = CTkLabel(self.tab_add_replacement, text="Replacement Date")
        self.date_label.pack()
        self.date_entry = DateEntry(self.tab_add_replacement, width=16, background="darkblue", foreground="white", bd=2, date_pattern="yyyy-mm-dd")
        self.date_entry.pack(pady=5)

        self.add_button = CTkButton(self.tab_add_replacement, text="Add Replacement", command=self.add_replacement)
        self.add_button.pack(pady=10)

        # Import Replacements from File Button
        self.import_button = CTkButton(self.tab_add_replacement, text="Import Replacements (CSV/XLSX)", command=self.import_replacements)
        self.import_button.pack(pady=10)

    def create_retrieve_version_tab(self):
        # Retrieve Version Inputs
        self.product_name_label = CTkLabel(self.tab_retrieve_version, text="Product Name")
        self.product_name_label.pack()
        self.product_name_entry = CTkEntry(self.tab_retrieve_version)
        self.product_name_entry.pack(pady=5)

        self.retrieve_button = CTkButton(self.tab_retrieve_version, text="Retrieve Latest Version",
                                         command=self.retrieve_latest_version)
        self.retrieve_button.pack(pady=10)

        self.result_label = CTkLabel(self.tab_retrieve_version, text="")
        self.result_label.pack(pady=5)

    def create_batch_process_tab(self):
        # Load and Process CSV/XLSX Button
        self.load_batch_file_button = CTkButton(self.tab_batch_process, text="Load and Process File (CSV/XLSX)",
                                                command=self.load_and_process_file)
        self.load_batch_file_button.pack(pady=10)

        # Progress Bar
        self.batch_progress_bar = ttk.Progressbar(self.tab_batch_process, orient="horizontal", length=300, mode="determinate")
        self.batch_progress_bar.pack(pady=10)

    def load_state(self):
        file_path = filedialog.askopenfilename(filetypes=[("Pickle Files", "*.pkl")])
        if file_path:
            try:
                with open(file_path, 'rb') as f:
                    new_state = pickle.load(f)
                with open(self.manager.state_file, 'wb') as f:
                    pickle.dump(new_state, f)
                self.manager.load_state()
                messagebox.showinfo("Success", "State loaded and current state file overwritten successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load and overwrite state: {e}")

    def download_mapping_list(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                                 filetypes=[("Excel Files", "*.xlsx"), ("CSV Files", "*.csv")])
        if file_path:
            try:
                # Prepare the data for saving
                data = []
                self.progress_bar["value"] = 0
                self.progress_bar["maximum"] = len(self.manager.products)
                
                for i, product in enumerate(self.manager.products):
                    latest_version, latest_date = self.manager.get_latest_version(product, include_date=True)
                    data.append([product, latest_version, latest_date])
                    self.progress_bar["value"] = i + 1  # Update progress bar
                    self.update_idletasks()  # Force GUI update

                df = pd.DataFrame(data, columns=["Old Product", "New Product", "Date"])

                # Sort data by 'New Product' to group related products together
                df.sort_values(by="New Product", inplace=True)

                # Save to file
                if file_path.endswith(".csv"):
                    df.to_csv(file_path, index=False)
                else:
                    df.to_excel(file_path, index=False)

                messagebox.showinfo("Success", "Mapping list saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save mapping list: {e}")
            finally:
                self.progress_bar["value"] = 0  # Reset progress bar

    def add_replacement(self):
        old_product = self.old_product_entry.get()
        new_product = self.new_product_entry.get()
        date_str = self.date_entry.get()

        try:
            date = datetime.strptime(date_str, "%Y-%m-%d")
            self.manager.add_replacement(old_product, new_product, date)
            messagebox.showinfo("Success", "Replacement added successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add replacement: {e}")
            
    def import_replacements(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv"), ("Excel Files", "*.xlsx")])
        if file_path:
            try:
                if file_path.endswith('.csv'):
                    df = pd.read_csv(file_path)
                else:
                    df = pd.read_excel(file_path)

                # Validate required columns
                required_columns = ["Old Product", "New Product", "Date"]
                if not all(col in df.columns for col in required_columns):
                    messagebox.showerror("Error", f"The file must contain the following columns: {', '.join(required_columns)}.")
                    return

                for index, row in df.iterrows():
                    old_product = row['Old Product']
                    new_product = row['New Product']
                    date = pd.to_datetime(row['Date'])

                    self.manager.add_replacement(old_product, new_product, date)

                messagebox.showinfo("Success", "Replacements imported successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to import replacements: {e}")

    def retrieve_latest_version(self):
        product_name = self.product_name_entry.get()

        try:
            result = self.manager.get_latest_version(product_name, include_date=True)
            if result[1] is not None:
                self.result_label.configure(
                    text=f"Latest version of '{product_name}' is '{result[0]}' on {result[1].strftime('%Y-%m-%d')}")
            else:
                self.result_label.configure(text=f"Latest version of '{product_name}' is '{result[0]}' (No date available)")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to retrieve latest version: {e}")
            
    def load_and_process_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv"), ("Excel Files", "*.xlsx")])
        if file_path:
            try:
                if file_path.endswith('.csv'):
                    df = pd.read_csv(file_path)
                else:
                    df = pd.read_excel(file_path)

                # Validate required columns
                required_columns = ["Old Product"]
                if not all(col in df.columns for col in required_columns):
                    messagebox.showerror("Error", f"The file must contain the following column: {', '.join(required_columns)}.")
                    return

                self.batch_progress_bar["value"] = 0
                self.batch_progress_bar["maximum"] = len(df)

                # Create empty lists to store new products and dates
                new_products = []
                dates = []

                for i, row in df.iterrows():
                    old_product = row["Old Product"]
                    latest_version, latest_date = self.manager.get_latest_version(old_product, include_date=True)

                    new_products.append(latest_version)
                    dates.append(latest_date.strftime('%Y-%m-%d') if latest_date else None)

                    self.batch_progress_bar["value"] = i + 1
                    self.update_idletasks()

                df['New Product'] = new_products
                df['Date'] = dates

                # Save the updated DataFrame back to the file
                if file_path.endswith('.csv'):
                    df.to_csv(file_path, index=False)
                else:
                    df.to_excel(file_path, index=False)

                messagebox.showinfo("Success", f"File processed and saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to process file: {e}")
            finally:
                self.batch_progress_bar["value"] = 0  # Reset progress bar

if __name__ == "__main__":
    manager = ProductReplacementManager()
    app = ProductReplacementApp(manager)
    app.mainloop()


