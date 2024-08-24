import pandas as pd
import os
import pickle
import logging
from datetime import datetime
from typing import List, Tuple, Optional

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ProductReplacementManager:
    """
    A class to manage product replacement relationships using the Union-Find data structure.
    This class helps track and find the latest replacement version of each product.
    It supports importing replacement data from a DataFrame, adding new data, and saving/loading state.
    """

    def __init__(self, products: Optional[List[str]] = None, persist_dir: str = 'persist'):
        """
        Initializes the ProductReplacementManager.

        Args:
            products (List[str], optional): A list of initial product names. If None, attempts to load from persistence.
            persist_dir (str): Directory to persist the manager's state.
        """
        self.persist_dir = persist_dir
        self.state_file = os.path.join(persist_dir, 'product_replacement_state.pkl')

        # Ensure the persistence directory exists
        os.makedirs(self.persist_dir, exist_ok=True)

        # Load existing state if it exists, otherwise initialize with provided products
        if os.path.exists(self.state_file):
            self.load_state()
        else:
            self.products = products if products else []
            self.product_index = {product: i for i, product in enumerate(self.products)}
            self.size = len(self.products)
            # Initialize root as a list of tuples (index, date)
            self.root: List[Tuple[int, datetime]] = [(i, datetime.min) for i in range(self.size)]
            self.save_state()

    def find(self, product_id: int) -> Tuple[int, datetime]:
        """
        Finds the root of the product and applies path compression.

        Args:
            product_id (int): The index of the product to find.

        Returns:
            Tuple[int, datetime]: The root tuple (index, date) of the product.
        """
        if product_id != self.root[product_id][0]:
            # Path compression: update the root to the latest known root
            self.root[product_id] = self.find(self.root[product_id][0])
        return self.root[product_id]

    def replace(self, old_product_id: int, new_product_id: int, date: datetime):
        """
        Unifies two products by setting the new product as the root of the old product,
        if the replacement date of the new product is more recent.

        Args:
            old_product_id (int): The index of the old product.
            new_product_id (int): The index of the new product replacing the old one.
            date (datetime): The date of the replacement. If this date is more recent
                             than the current root's date, the root will be updated.
        """
        root_old, date_old = self.find(old_product_id)
        root_new, date_new = self.find(new_product_id)
        date_new = max(date, date_new)  # Ensure the latest date is used

        # Set the new product as the root if the new date is more recent
        if date_new >= date_old:
            self.root[root_old] = (root_new, date_new)
            self.root[root_new] = (root_new, date_new)
            logging.info(f"Replaced product '{self.products[old_product_id]}' with '{self.products[new_product_id]}' on {date_new.strftime('%Y-%m-%d')}")
        else:
            logging.warning(f"Replacement not made for '{self.products[old_product_id]}' because existing replacement is more recent or the same date.")   

    def add_product(self, product: str):
        """
        Adds a new product to the system if it does not already exist.

        Args:
            product (str): The name of the product to add.
        """
        if product not in self.product_index:
            self.products.append(product)
            self.product_index[product] = self.size
            self.root.append((self.size, datetime.min))
            self.size += 1
            self.save_state()
            logging.info(f"Product '{product}' added to the system.")
        else:
            logging.info(f"Product '{product}' already exists in the system.")

    def add_replacement(self, old_product: str, new_product: str, date: datetime):
        """
        Adds a new product replacement to the system.

        Args:
            old_product (str): The name of the old product.
            new_product (str): The name of the new product replacing the old one.
            date (datetime): The date of the replacement.
        """
        if old_product not in self.product_index:
            self.add_product(old_product)
        if new_product not in self.product_index:
            self.add_product(new_product)

        self.replace(self.product_index[old_product], self.product_index[new_product], date)
        self.save_state()

    def add_products_from_dataframe(self, df: pd.DataFrame):
        """
        Imports product replacement data from a DataFrame.

        Args:
            df (pd.DataFrame): DataFrame with columns ['OldProduct', 'NewProduct', 'Date'].
                               The 'Date' column should be in a format that can be parsed into a datetime object.
        """
        for _, row in df.iterrows():
            old_product = row['OldProduct']
            new_product = row['NewProduct']
            date = pd.to_datetime(row['Date']) if 'Date' in row else datetime.now()
            self.add_replacement(old_product, new_product, date)
        self.save_state()
               
    def load_state(self):
        """Loads the manager's state and product list from the persistence file if it exists."""
        if os.path.exists(self.state_file):
            with open(self.state_file, 'rb') as f:
                state = pickle.load(f)
                self.products = state['products']
                self.product_index = state['product_index']
                self.root = state['root']
                self.size = len(self.products)
                logging.info("State loaded from %s", self.state_file)
        else:
            logging.info("No existing state found. Starting fresh.")

    def save_state(self):
        """Saves the current state of the manager, including product list, to the persistence file."""
        state = {
            'products': self.products,
            'product_index': self.product_index,
            'root': self.root
        }
        with open(self.state_file, 'wb') as f:
            pickle.dump(state, f)
        logging.info("State saved to %s", self.state_file)
    
    def get_latest_version(self, product_name: str, include_date: bool = False) -> str:
        """
        Retrieves the latest replacement version of the given product by name.

        Args:
            product_name (str): The name of the product to query.
            include_date (bool): Whether to include the date of the latest replacement.

        Returns:
            str: The name of the latest replacement product.
            If include_date is True, returns a tuple (str, datetime) where the datetime is the date of the latest replacement.
            If the product is not found, returns the input product name, or (product_name, None) if include_date is True.
        """
        if product_name not in self.product_index:
            logging.warning(f"Product '{product_name}' not found in the system.")
            return (product_name, None) if include_date else product_name

        product_id = self.product_index[product_name]
        latest_product_id, latest_date = self.find(product_id)
        
        return (self.products[latest_product_id], latest_date) if include_date else self.products[latest_product_id]

