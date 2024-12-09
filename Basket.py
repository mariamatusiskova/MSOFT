import os
import sys
from tkinter import messagebox
import json
from customtkinter import CTkLabel, CTkFrame, CTkButton, CTkEntry, CTkScrollableFrame, CTkComboBox

############### UC 3: Buy the desired products
class Basket:
    def __init__(self, main_view, menu):
        self.main_view = main_view
        self.products = []
        self.total_price = 0.0
        self.current_frame = None
        self.menu = menu

        try:
            with open("basket_data.json", "r") as file:
                self.products = json.load(file)
            with open("total_price.json", "r") as file:
                self.total_price = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.products = []
            self.total_price = 0.0

    def create_title(self):
        title_frame = CTkFrame(master=self.main_view, fg_color="transparent")
        # fill width
        title_frame.pack(anchor="n", fill="x",  padx=27, pady=(29, 0))
        CTkLabel(master=title_frame,
                 text="Basket",
                 font=("Arial Black", 25),
                 text_color="#3EAEB1").pack(anchor="nw", side="left")

    def add_to_basket(self, product, quantity):
        for existing_product in self.products:
            if existing_product["product_id"] == product["product_id"]:
                existing_product["quantity"] += quantity
                break
        else:
            product["quantity"] = quantity
            self.products.append(product)

        self.calculate_total_price()
        messagebox.showinfo("Success", f"{product['name']} added to basket")
        self.save_data()

    def remove_product(self, product):
        for existing_product in self.products:
            if existing_product["product_id"] == product["product_id"]:
                self.products.remove(existing_product)
                break
        self.calculate_total_price()
        self.save_data()
        self.show_basket()

    def calculate_total_price(self):
        self.total_price = sum(product["price"]*product["quantity"] for product in self.products)
        with open("total_price.json", "w") as file:
            json.dump(self.total_price, file)

    def show_basket(self):
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = CTkFrame(master=self.main_view, fg_color="transparent")
        self.current_frame.pack(fill="both", expand=True)

        if not self.products:
            CTkLabel(master=self.current_frame, text="Your basket is empty", font=("Arial", 12)).pack(pady=20)
        else:
            for product in self.products:
                product_frame = CTkFrame(master=self.current_frame, fg_color="#f0f0f0")
                product_frame.pack(fill="x", pady=5)

                CTkLabel(
                    master=product_frame,
                    text=f"{product['name']} - {product['quantity']} x {product['price']}€",
                    font=("Arial", 12)
                ).pack(side="left", padx=10, pady=10)

                CTkButton(
                    master=product_frame,
                    text="Remove",
                    command=lambda x=product: self.remove_product(x),
                    fg_color="#FF5733",
                    hover_color="#FF0000"
                ).pack(side="right", padx=10)

            CTkLabel(
                master=self.current_frame,
                text=f"Total: {self.total_price}€",
                font=("Arial Bold", 14)
            ).pack(pady=20)

            CTkButton(
                master=self.current_frame,
                text="Proceed to Checkout",
                command=self.checkout,
                fg_color="#3EAEB1",
                hover_color="#1D837F"
            ).pack(pady=10)

    def checkout(self):
        self.enter_contact_information()
        self.enter_shipping_information()

    def enter_contact_information(self):
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = CTkFrame(master=self.main_view, fg_color="transparent")
        self.current_frame.pack(fill="both", expand=True)

        CTkLabel(master=self.current_frame, text="Provide Contact Details:").pack(pady=10)

        self.email_entry = CTkEntry(master=self.current_frame, placeholder_text="Email")
        self.email_entry.pack(pady=5)

        self.phone_num_entry = CTkEntry(master=self.current_frame, placeholder_text="Phone Number")
        self.phone_num_entry.pack(pady=5)

        CTkButton(
            master=self.current_frame,
            text="Delivery Options",
            command=self.checkout,
            fg_color="#3EAEB1",
            hover_color="#1D837F"
        ).pack(pady=10)

        self.whole_contact_frame = CTkScrollableFrame(
            master=self.current_frame,
            fg_color="transparent"
        )
        self.whole_contact_frame.pack(fill="both", expand=True, padx=27, pady=(0, 20))

    def enter_shipping_information(self):
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = CTkFrame(master=self.main_view, fg_color="transparent")
        self.current_frame.pack(fill="both", expand=True)

        CTkLabel(
                master=self.current_frame,
                 text="Provide Shipping Details:",
                 font=("Arial Bold", 12)
        ).pack(pady=10)

        self.city_entry = CTkEntry(master=self.current_frame, placeholder_text="City")
        self.city_entry.pack(pady=5)

        self.country_entry = CTkEntry(master=self.current_frame, placeholder_text="Country")
        self.country_entry.pack(pady=5)

        self.address_entry = CTkEntry(master=self.current_frame, placeholder_text="Address")
        self.address_entry.pack(pady=5)

        self.postal_code_entry = CTkEntry(master=self.current_frame, placeholder_text="Postal Code")
        self.postal_code_entry.pack(pady=5)

        self.street_entry = CTkEntry(master=self.current_frame, placeholder_text="Street")
        self.street_entry.pack(pady=5)


        CTkButton(
            master=self.current_frame,
            text="Delivery Options",
            command=self.select_delivery_method,
            fg_color="#3EAEB1",
            hover_color="#1D837F"
        ).pack(pady=10)

        self.whole_shipping_frame = CTkScrollableFrame(
            master=self.current_frame,
            fg_color="transparent"
        )
        self.whole_shipping_frame.pack(fill="both", expand=True, padx=27, pady=(0, 20))

    def select_delivery_method(self):
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = CTkFrame(master=self.main_view, fg_color="transparent")
        self.current_frame.pack(fill="both", expand=True)

        CTkLabel(master=self.current_frame, text="Select Delivery Method").pack(pady=10)

        self.delivery_type = CTkComboBox(
            master=self.current_frame,
            values=["Postal Office", "Courier", "Medical Box", "Pharmacy"],
            state="readonly",
            button_color="#3EAEB1",
            button_hover_color="#1D837F"
        )
        self.delivery_type.pack(pady=10)
        self.delivery_type.set("Select Delivery Type")

        CTkButton(
            master=self.current_frame,
            text="Continue to Payment",
            command=self.payment_method,
            fg_color="#3EAEB1",
            hover_color="#1D837F"
        ).pack(pady=20)

    def payment_method(self):
        if not self.delivery_type.get() or self.delivery_type.get() == "Select Delivery Type":
            messagebox.showwarning("Warning", "Please select a delivery method")
            return

        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = CTkFrame(master=self.main_view, fg_color="transparent")
        self.current_frame.pack(fill="both", expand=True)

        CTkLabel(
            master=self.current_frame,
            text="Select Payment Method:",
            font=("Arial Bold", 12)
        ).pack(pady=(0, 10))

        # pick type of payment
        CTkButton(
            master=self.current_frame,
            text="Pay by Credit Card",
            command=lambda: self.confirm_order("Credit Card"),
            fg_color="#3EAEB1",
            hover_color="#1D837F"
        ).pack(pady=10)

        CTkButton(
            master=self.current_frame,
            text="Pay on Delivery",
            command=lambda: self.confirm_order("Pay on Delivery"),
            fg_color="#3EAEB1",
            hover_color="#1D837F"
        ).pack(pady=10)

    def confirm_order(self, payment_method):
        self.current_frame = CTkFrame(master=self.main_view, fg_color="transparent")
        self.current_frame.pack(fill="both", expand=True)

        CTkLabel(master=self.current_frame, text="Order Confirmed!").pack(pady=10)
        CTkLabel(master=self.current_frame, text=f"Payment Method: {payment_method}").pack(pady=5)
        CTkLabel(master=self.current_frame, text=f"Total: {self.total_price}€").pack(pady=5)

        self.clear_basket()

        CTkButton(
            master=self.current_frame,
            text="Back to Home",
            command=lambda: self.menu.change_page("symptoms"),
            fg_color="#3EAEB1",
            hover_color="#1D837F"
        ).pack(pady=10)

    def save_data(self):
        with open("basket_data.json", "w") as file:
            json.dump(self.products, file)
        with open("total_price.json", "w") as file:
            json.dump(self.total_price, file)

    def clear_basket(self):
        self.products = []
        self.total_price = 0.0
        os.remove("basket_data.json")
        os.remove("total_price.json")
#############################################






