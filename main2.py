################################################################################################################################################
# source for base structure of code and to learn how to work with customtkiner: https://github.com/RoyChng/customtkinter-examples/tree/master
# I found this example code and transformed it into my use case
# I used CTk to make look tkinter better
################################################################################################################################################
from tkinter import messagebox

from customtkinter import *
from CTkTable import CTkTable
from PIL import Image

class PharmacyManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("The Pharmacy Management System")
        self.root.geometry("856x645")
        self.root.resizable(0, 0)

        self.insurance_id = 0

        set_appearance_mode("light")

        self.side_menu_frame = None
        self.main_view = None
        self.table_frame = None

        self.create_side_menu()
        self.create_main_view()

    def create_side_menu(self):
        self.side_menu_frame = CTkFrame(master=self.root, fg_color="#3EAEB1", width=176, height=650, corner_radius=0)
        # prevents from automatically resizing
        self.side_menu_frame.pack_propagate(0)
        # stick to left side
        self.side_menu_frame.pack(fill="y", anchor="w", side="left")

        logo_img_data = Image.open("imgs/pharmacy.png")
        logo_img = CTkImage(dark_image=logo_img_data, light_image=logo_img_data, size=(78, 86))

        CTkLabel(master=self.side_menu_frame, text="", image=logo_img).pack(pady=(38, 0), anchor="center")

        self.menu_items()

    def create_image(self, img_path):
        img_data = Image.open(img_path)
        img = CTkImage(dark_image=img_data, light_image=img_data)
        return img

    def menu_items(self):
        # prescription
        prescription_img = self.create_image("imgs/menu/medical-prescription.png")
        CTkButton(master=self.side_menu_frame, image=prescription_img, text="Prescriptions", fg_color="transparent",
                  font=("Arial Bold", 14), hover_color="#1D837F", anchor="w").pack(anchor="center", ipady=5,
                                                                                   pady=(60, 1))

        # symptoms
        symptoms_img = self.create_image("imgs/menu/red-eyes.png")
        CTkButton(master=self.side_menu_frame, image=symptoms_img, text="Symptoms", fg_color="#fff", font=("Arial Bold", 14),
                  text_color="#1D837F", hover_color="#eee", anchor="w").pack(anchor="center", ipady=5, pady=(16, 1))

        # categories
        categories_img = self.create_image("imgs/menu/tag.png")
        CTkButton(master=self.side_menu_frame, image=categories_img, text="Categories", fg_color="transparent", font=("Arial Bold", 14),
                  hover_color="#1D837F", anchor="w").pack(anchor="center", ipady=5, pady=(16, 1))

        # basket
        basket_img = self.create_image("imgs/menu/basket.png")
        CTkButton(master=self.side_menu_frame, image=basket_img, text="Basket", fg_color="transparent",
                  font=("Arial Bold", 14), hover_color="#1D837F", anchor="w").pack(anchor="center", ipady=5,
                                                                                   pady=(16, 1))
        # orders
        orders_img = self.create_image("imgs/menu/cardboard-box.png")
        CTkButton(master=self.side_menu_frame, image=orders_img, text="Orders", fg_color="transparent",
                  font=("Arial Bold", 14), hover_color="#1D837F", anchor="w").pack(anchor="center", ipady=5,
                                                                                   pady=(16, 1))

        # settings
        settings_img = self.create_image("imgs/menu/settings_icon.png")
        CTkButton(master=self.side_menu_frame, image=settings_img, text="Settings", fg_color="transparent",
                  font=("Arial Bold", 14), hover_color="#1D837F", anchor="w").pack(anchor="center", ipady=5,
                                                                                   pady=(16, 1))
        # account
        person_img = self.create_image("imgs/menu/person_icon.png")
        CTkButton(master=self.side_menu_frame, image=person_img, text="Account", fg_color="transparent",
                  font=("Arial Bold", 14), hover_color="#1D837F", anchor="w").pack(anchor="center", ipady=5,
                                                                                   pady=(100, 1))

    def create_main_view(self):
        self.main_view = CTkFrame(master=self.root, fg_color="#fff",  width=680, height=650, corner_radius=0)
        self.main_view.pack_propagate(0)
        self.main_view.pack(side="left")

        self.create_title()
        self.get_insurance_id()
        #self.create_table()

    def create_title(self):
        title_frame = CTkFrame(master=self.main_view, fg_color="transparent")
        # fill width
        title_frame.pack(anchor="n", fill="x",  padx=27, pady=(29, 0))
        CTkLabel(master=title_frame, text="Prescriptions", font=("Arial Black", 25), text_color="#3EAEB1").pack(anchor="nw", side="left")

    # def get_insurance_id(self):
    #     insurance_container = CTkFrame(master=self.main_view, height=50, fg_color="#F0F0F0")
    #     insurance_container.pack(fill="x", pady=(45, 0), padx=27)
    #     self.insurance_id = CTkEntry(master=insurance_container, width=305, placeholder_text="Enter Insurance ID", border_color="#3EAEB1", border_width=2).pack(side="left", padx=(13, 0), pady=15)
    #
    #     CTkButton(master=insurance_container, text="View Prescriptions", font=("Arial Black", 13), text_color="#fff",
    #               fg_color="#3EAEB1", hover_color="#1D837F").pack(anchor="ne", side="left", padx=(13, 0), pady=15)


    def get_insurance_id(self):
        insurance_container = CTkFrame(master=self.main_view, height=50, fg_color="#F0F0F0")
        insurance_container.pack(fill="x", pady=(45, 0), padx=27)

        # Store the Entry widget as an instance variable
        self.insurance_entry = CTkEntry(
            master=insurance_container,
            width=305,
            placeholder_text="Enter Insurance ID",
            border_color="#3EAEB1",
            border_width=2
        )
        self.insurance_entry.pack(side="left", padx=(13, 0), pady=15)

        CTkButton(
            master=insurance_container,
            text="View Prescriptions",
            font=("Arial Black", 13),
            text_color="#fff",
            fg_color="#3EAEB1",
            hover_color="#1D837F",
            command=self.view_prescriptions  # Connect to view_prescriptions method
        ).pack(anchor="ne", side="left", padx=(13, 0), pady=15)

    def create_table(self):
        prescription_data = [
            ["Medicine", "Dosage", "Issue Date", "Expiry Date", "Status"],  # Header row
            ["Amoxicillin", "500mg", "2024-01-01", "2024-02-01", "Active"],
            ["Ibuprofen", "400mg", "2024-01-15", "2024-02-15", "Active"],
            ["Omeprazole", "20mg", "2024-01-10", "2024-02-10", "Expired"],
            ["Metformin", "850mg", "2024-01-20", "2024-02-20", "Active"],
            ["Simvastatin", "40mg", "2024-01-05", "2024-02-05", "Active"]
        ]

        table_frame = CTkScrollableFrame(master=self.main_view, fg_color="transparent")
        table_frame.pack(expand=True, fill="both", padx=27, pady=21)

        # Create table with pharmacy color scheme
        table = CTkTable(
            master=table_frame,
            values=prescription_data,
            colors=["#E6E6E6", "#EEEEEE"],  # Alternating row colors
            header_color="#3EAEB1",  # Match your primary color
            hover_color="#1D837F",  # Match your hover color
            corner_radius=0
        )

        # Style the header row
        table.edit_row(0, text_color="#fff", hover_color="#3EAEB1")
        table.pack(expand=True)

        # table_data = [
        #     ["Order ID", "Item Name", "Customer", "Address", "Status", "Quantity"],
        #     ['3833', 'Smartphone', 'Alice', '123 Main St', 'Confirmed', '8'],
        #     ['6432', 'Laptop', 'Bob', '456 Elm St', 'Packing', '5'],
        #     ['2180', 'Tablet', 'Crystal', '789 Oak St', 'Delivered', '1'],
        #     ['5438', 'Headphones', 'John', '101 Pine St', 'Confirmed', '9'],
        #     ['9144', 'Camera', 'David', '202 Cedar St', 'Processing', '2'],
        #     ['7689', 'Printer', 'Alice', '303 Maple St', 'Cancelled', '2'],
        #     ['1323', 'Smartwatch', 'Crystal', '404 Birch St', 'Shipping', '6'],
        #     ['7391', 'Keyboard', 'John', '505 Redwood St', 'Cancelled', '10'],
        #     ['4915', 'Monitor', 'Alice', '606 Fir St', 'Shipping', '6'],
        #     ['5548', 'External Hard Drive', 'David', '707 Oak St', 'Delivered', '10'],
        #     ['5485', 'Table Lamp', 'Crystal', '808 Pine St', 'Confirmed', '4'],
        #     ['7764', 'Desk Chair', 'Bob', '909 Cedar St', 'Processing', '9'],
        #     ['8252', 'Coffee Maker', 'John', '1010 Elm St', 'Confirmed', '6'],
        #     ['2377', 'Blender', 'David', '1111 Redwood St', 'Shipping', '2'],
        #     ['5287', 'Toaster', 'Alice', '1212 Maple St', 'Processing', '1'],
        #     ['7739', 'Microwave', 'Crystal', '1313 Cedar St', 'Confirmed', '8'],
        #     ['3129', 'Refrigerator', 'John', '1414 Oak St', 'Processing', '5'],
        #     ['4789', 'Vacuum Cleaner', 'Bob', '1515 Pine St', 'Cancelled', '10']
        # ]
        #
        # table_frame = CTkScrollableFrame(master=self.main_view, fg_color="transparent")
        # table_frame.pack(expand=True, fill="both", padx=27, pady=21)
        # table = CTkTable(master=table_frame, values=table_data, colors=["#E6E6E6", "#EEEEEE"], header_color="#3EAEB1", hover_color="#1D837F")
        # table.edit_row(0, text_color="#fff", hover_color="#2A8C55")
        # table.pack(expand=True)



if __name__ == "__main__":
    root = CTk()
    app = PharmacyManagementSystem(root)
    root.mainloop()