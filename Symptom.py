import json
from tkinter import messagebox

from customtkinter import CTkLabel, CTkFrame, CTkComboBox, CTkScrollableFrame, CTkButton, CTkTextbox


class Symptom:
    def __init__(self, main_view):
        self.main_view = main_view
        self.current_frame = None
        self.symptom_data = self.load_symptoms_data()

    def load_symptoms_data(self):
        try:
            with open('data/symptoms.json', 'r') as file:
                symptom_data = json.load(file)
            return symptom_data
        except FileNotFoundError:
            messagebox.showerror("Error", "Symptoms data file not found!")
            symptom_data = {}
            return symptom_data
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Invalid symptoms data file!")
            symptom_data = {}
            return symptom_data

    def create_title(self):
        title_frame = CTkFrame(master=self.main_view, fg_color="transparent")
        # fill width
        title_frame.pack(anchor="n", fill="x",  padx=27, pady=(29, 0))
        CTkLabel(master=title_frame,
                 text="Find Medicine by Symptoms",
                 font=("Arial Black", 25),
                 text_color="#3EAEB1").pack(anchor="nw", side="left")

    def symptom_search(self):
        self.current_frame = CTkFrame(master=self.main_view, fg_color="transparent")
        self.current_frame.pack(fill="both", expand=True)

        symptoms_list = list(self.symptom_data["symptoms"].keys())
        self.symptoms_combobox = CTkComboBox(
            master=self.current_frame,
            values=symptoms_list,
            width=300,
            state="readonly",
            button_color="#3EAEB1",
            button_hover_color="#1D837F",
            command=self.selected_symptom
        )
        self.symptoms_combobox.pack(padx=27, pady=(30, 30))
        self.symptoms_combobox.set("Select Symptom")

        self.products_frame = CTkScrollableFrame(
            master=self.current_frame,
            fg_color="transparent"
        )
        self.products_frame.pack(fill="both", expand=True, padx=27, pady=(0, 20))

    def selected_symptom(self, choice):
        # clear previous products
        for widget in self.products_frame.winfo_children():
            widget.destroy()

        symptom_data = self.symptom_data["symptoms"][choice]

        # show symptom description
        description_frame = CTkFrame(master=self.products_frame, fg_color="#f0f0f0")
        description_frame.pack(fill="x", pady=(0, 10))

        CTkLabel(
            master=description_frame,
            text=f"Description: {symptom_data['description']}",
            font=("Arial", 12),
            wraplength=600
        ).pack(padx=10, pady=10)

        product_frame = CTkFrame(master=self.products_frame, fg_color="transparent", corner_radius=10)
        product_frame.pack(fill="x", expand=True)

        for product in symptom_data["products"]:
            product_button = CTkButton(
                master=product_frame,
                text=f"{product['name']} - {product['brand']}",
                fg_color="#3EAEB1",
                hover_color="#1D837F",
                corner_radius=5
            )
            product_button.configure(command=lambda x=product, c=choice: self.show_product_details(x, c))
            product_button.pack(fill="x", padx=10, pady=10)

    def show_product_details(self, product, symptom_type):
        for widget in self.products_frame.winfo_children():
            widget.destroy()

        CTkButton(
            master=self.products_frame,
            text="← Back",
            command=lambda: self.selected_symptom(symptom_type),
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
        print(f"Added {product['name']} to Basket")