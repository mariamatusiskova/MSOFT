import json
from tkinter import messagebox

from customtkinter import CTkFrame, CTkLabel, CTkComboBox, CTkScrollableFrame, CTkButton, CTkTextbox

from Basket import Basket


class Category:
    def __init__(self, main_view, menu):
        self.main_view = main_view
        self.current_frame = None
        self.category_data = self.load_categories_data()
        self.menu = menu

    def load_categories_data(self):
        try:
            with open('data/categories.json', 'r') as file:
                category_data = json.load(file)
            return category_data
        except FileNotFoundError:
            messagebox.showerror("Error", "Categories data file not found!")
            category_data = {}
            return category_data
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Invalid categories data file!")
            category_data = {}
            return category_data

    def create_title(self):
        title_frame = CTkFrame(master=self.main_view, fg_color="transparent")
        # fill width
        title_frame.pack(anchor="n", fill="x",  padx=27, pady=(29, 0))
        CTkLabel(master=title_frame,
                 text="Find Medicine by Categories",
                 font=("Arial Black", 25),
                 text_color="#3EAEB1").pack(anchor="nw", side="left")

    def category_search(self):
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = CTkFrame(master=self.main_view, fg_color="transparent")
        self.current_frame.pack(fill="both", expand=True)

        categories_list = list(self.category_data["categories"].keys())
        self.categories_combobox = CTkComboBox(
            master=self.current_frame,
            values=categories_list,
            width=300,
            state="readonly",
            button_color="#3EAEB1",
            button_hover_color="#1D837F",
            command=self.selected_category
        )
        self.categories_combobox.pack(padx=27, pady=(30, 30))
        self.categories_combobox.set("Select Category")

        self.products_frame = CTkScrollableFrame(
            master=self.current_frame,
            fg_color="transparent"
        )
        self.products_frame.pack(fill="both", expand=True, padx=27, pady=(0, 20))

    def selected_category(self, choice):
        # clear previous products
        for widget in self.products_frame.winfo_children():
            widget.destroy()

        category_data = self.category_data["categories"][choice]

        # show category description
        description_frame = CTkFrame(master=self.products_frame, fg_color="#f0f0f0")
        description_frame.pack(fill="x", pady=(0, 10))

        CTkLabel(
            master=description_frame,
            text=f"Description: {category_data['description']}",
            font=("Arial", 12),
            wraplength=600
        ).pack(padx=10, pady=10)

        product_frame = CTkFrame(master=self.products_frame, fg_color="transparent", corner_radius=10)
        product_frame.pack(fill="x", expand=True)

        for product in category_data["products"]:
            product_button = CTkButton(
                master=product_frame,
                text=f"{product['name']} - {product['brand']}",
                fg_color="#3EAEB1",
                hover_color="#1D837F",
                corner_radius=5
            )
            product_button.configure(command=lambda x=product, c=choice: self.show_product_details(x, c))
            product_button.pack(fill="x", padx=10, pady=10)

    def show_product_details(self, product, category_type):
        for widget in self.products_frame.winfo_children():
            widget.destroy()

        CTkButton(
            master=self.products_frame,
            text="← Back",
            command=lambda: self.selected_category(category_type),
            fg_color="#3EAEB1",
            hover_color="#1D837F",
            width=60
        ).pack(anchor="w", pady=(0, 20))

        header_frame = CTkFrame(master=self.products_frame, fg_color="#f0f0f0", corner_radius=13)
        header_frame.pack(fill="x", pady=(10))

        details_frame = CTkFrame(master=self.products_frame, fg_color="#f0f0f0", corner_radius=10)
        details_frame.pack(fill="x", pady=10)

        CTkLabel(
            master=header_frame,
            text=product["name"],
            font=("Arial Bold", 14)
        ).pack(side="left")

        CTkLabel(
            master=header_frame,
            text=f"{product['price']}€",
            font=("Arial", 14),
            text_color="#3EAEB1"
        ).pack(side="right")

        # Product details
        details = [
            ("Brand", product.get("brand", "N/A")),
            ("Description", product.get("description", "No description available")),
            ("Dosage", product.get("dosage_recommendation", "N/A")),
            ("Expiry Date", product.get("expiry_date", "N/A")),
            ("Quantity Available", str(product.get("quantity", 0)) + " units"),
        ]

        if "leaflet" in product:
            leaflet_text = CTkTextbox(
                master=self.products_frame,
                height=60,
                fg_color="transparent",
                wrap="word"
            )
            leaflet_text.pack(fill="x", padx=10, pady=2)
            leaflet_text.insert("1.0", f"Additional Information: {product['leaflet']}")
            leaflet_text.configure(state="disabled")

        for label, value in details:
            detail_label = CTkLabel(
                master=details_frame,
                text=f"{label}: {value}",
                font=("Arial", 12),
                justify="left",
                anchor="w",
                text_color="#000000"
            )
            detail_label.pack(fill="x", padx=20, pady=5, anchor="w")

        CTkButton(
            master=self.products_frame,
            text="Add to Basket",
            font=("Arial Bold", 12),
            fg_color="#3EAEB1",
            hover_color="#1D837F",
            command=lambda x=product: self.add_to_basket(x)
        ).pack(pady=(5, 10))

    def add_to_basket(self, product):
        basket = Basket(self.main_view, self.menu)
        basket.add_to_basket(product)
        basket.show_basket()