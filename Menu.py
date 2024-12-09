from customtkinter import CTkButton, CTkFrame, CTkImage, CTkLabel
from PIL import Image

from Account import Account
from Basket import Basket
from Category import Category
from Order import Order
from Prescription import Prescription
from Settings import Settings
from Symptom import Symptom


class Menu:
    def __init__(self, root):
        self.root = root
        self.active_page = "prescriptions"
        self.side_menu_frame = None
        self.current_frame = None
        self.main_view = None

        self.create_side_menu()
        self.create_main_view()

    def create_image(self, img_path):
        img_data = Image.open(img_path)
        img = CTkImage(dark_image=img_data, light_image=img_data)
        return img

    def create_default_main_view(self):
        if self.main_view:
            self.main_view.destroy()

        self.main_view = CTkFrame(master=self.root,
                                  fg_color="#fff",
                                  width=680,
                                  height=650,
                                  corner_radius=0)
        self.main_view.pack_propagate(0)
        self.main_view.pack(side="left")

        prescription = Prescription(self.main_view)
        prescription.create_title()
        prescription.get_insurance_id()

    def create_main_view(self):
        if self.main_view:
            self.main_view.destroy()

        if not self.side_menu_frame:
            self.create_side_menu()

        self.main_view = CTkFrame(master=self.root,
                                  fg_color="#fff",
                                  width=680,
                                  height=650,
                                  corner_radius=0)
        self.main_view.pack_propagate(0)
        self.main_view.pack(side="left")

    def create_side_menu(self):
        if self.side_menu_frame:
            self.side_menu_frame.destroy()

        self.side_menu_frame = CTkFrame(
                                        master=self.root,
                                        fg_color="#3EAEB1",
                                        width=176,
                                        height=650,
                                        corner_radius=0
                                        )
        # prevents from automatically resizing
        self.side_menu_frame.pack_propagate(0)
        # stick to left side
        self.side_menu_frame.pack(fill="y", anchor="w", side="left")

        logo_img_data = Image.open("imgs/pharmacy.png")
        logo_img = CTkImage(dark_image=logo_img_data, light_image=logo_img_data, size=(78, 86))

        CTkLabel(master=self.side_menu_frame,
                 text="",
                 image=logo_img).pack(pady=(38, 0), anchor="center")

        self.menu_items()

    def menu_items(self):
        for widget in self.side_menu_frame.winfo_children()[1:]:
            widget.destroy()

        # prescription
        prescription_img = self.create_image("imgs/menu/medical-prescription.png")
        (CTkButton(master=self.side_menu_frame,
                   image=prescription_img,
                   text="Prescriptions",
                   fg_color="#fff" if self.active_page == "prescriptions" else "transparent",
                   font=("Arial Bold", 14),
                   text_color="#1D837F" if self.active_page == "prescriptions" else "#fff",
                   hover_color="#eee",
                   command=lambda: self.change_page("prescriptions"),
                   anchor="w").pack(anchor="center", ipady=5, pady=(60, 1)))

        # symptoms
        symptoms_img = self.create_image("imgs/menu/red-eyes.png")
        CTkButton(master=self.side_menu_frame,
                  image=symptoms_img,
                  text="Symptoms",
                  fg_color="#fff" if self.active_page == "symptoms" else "transparent",
                  text_color="#1D837F" if self.active_page == "symptoms" else "#fff",
                  font=("Arial Bold", 14),
                  hover_color="#1D837F",
                  command=lambda: self.change_page("symptoms"),
                  anchor="w").pack(anchor="center", ipady=5, pady=(16, 1))

        # categories
        categories_img = self.create_image("imgs/menu/tag.png")
        CTkButton(master=self.side_menu_frame,
                  image=categories_img,
                  text="Categories",
                  fg_color="#fff" if self.active_page == "categories" else "transparent",
                  text_color="#1D837F" if self.active_page == "categories" else "#fff",
                  font=("Arial Bold", 14),
                  command=lambda: self.change_page("categories"),
                  hover_color="#1D837F", anchor="w").pack(anchor="center", ipady=5, pady=(16, 1))

        # basket
        basket_img = self.create_image("imgs/menu/basket.png")
        CTkButton(master=self.side_menu_frame,
                  image=basket_img,
                  text="Basket",
                  fg_color="#fff" if self.active_page == "basket" else "transparent",
                  text_color="#1D837F" if self.active_page == "basket" else "#fff",
                  font=("Arial Bold", 14),
                  hover_color="#1D837F",
                  command=lambda: self.change_page("basket"),
                  anchor="w").pack(anchor="center", ipady=5, pady=(16, 1))

        # orders
        orders_img = self.create_image("imgs/menu/cardboard-box.png")
        CTkButton(master=self.side_menu_frame,
                  image=orders_img,
                  text="Orders",
                  fg_color="#fff" if self.active_page == "orders" else "transparent",
                  text_color="#1D837F" if self.active_page == "orders" else "#fff",
                  font=("Arial Bold", 14),
                  hover_color="#1D837F",
                  command=lambda: self.change_page("orders"),
                  anchor="w").pack(anchor="center", ipady=5, pady=(16, 1))

        # settings
        settings_img = self.create_image("imgs/menu/settings_icon.png")
        CTkButton(master=self.side_menu_frame,
                  image=settings_img,
                  text="Settings",
                  fg_color="#fff" if self.active_page == "settings" else "transparent",
                  text_color="#1D837F" if self.active_page == "settings" else "#fff",
                  font=("Arial Bold", 14),
                  hover_color="#1D837F",
                  command=lambda: self.change_page("settings"),
                  anchor="w").pack(anchor="center", ipady=5, pady=(16, 1))

        # account
        person_img = self.create_image("imgs/menu/person_icon.png")
        CTkButton(master=self.side_menu_frame,
                  image=person_img,
                  text="Account",
                  fg_color="#fff" if self.active_page == "account" else "transparent",
                  text_color="#1D837F" if self.active_page == "account" else "#fff",
                  font=("Arial Bold", 14),
                  hover_color="#1D837F",
                  command=lambda: self.change_page("account"),
                  anchor="w").pack(anchor="center", ipady=5, pady=(100, 1))

    def clear_frame(self):
        if self.current_frame:
            self.current_frame.destroy()
            self.current_frame = None

    def change_page(self, page_name):
        self.active_page = page_name
        self.clear_frame()

        if self.main_view:
            self.main_view.destroy()

        self.create_main_view()

        self.current_frame = CTkFrame(master=self.main_view, fg_color="#fff")
        self.current_frame.pack(fill="both", expand=True)

        # update menu
        self.menu_items()

        if page_name == "prescriptions":
            prescription = Prescription(self.current_frame)
            prescription.create_title()
            prescription.get_insurance_id()
        elif page_name == "symptoms":
            symptom = Symptom(self.current_frame)
            symptom.create_title()
            symptom.symptom_search()
        elif page_name == "categories":
            category = Category(self.current_frame)
            category.create_title()
            category.category_search()
        elif page_name == "basket":
            basket = Basket(self.current_frame)
            basket.create_title()
        elif page_name == "orders":
            order = Order(self.current_frame)
            order.create_title()
        elif page_name == "settings":
            settings = Settings(self.current_frame)
            settings.create_title()
        elif page_name == "account":
            account = Account(self.current_frame)
            account.create_title()