################################################################################################################################################
# source for base structure of code and to learn how to work with customtkiner: https://github.com/RoyChng/customtkinter-examples/tree/master
# I found this example code and transformed it into my use case
# I used CTk to make look tkinter better
################################################################################################################################################

from customtkinter import *
from Menu import Menu
from Prescription import Prescription


class PharmacyManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("The Pharmacy Management System")
        self.root.geometry("856x645")
        self.root.resizable(0, 0)

        set_appearance_mode("light")
        menu = Menu(self.root)
        menu.create_default_main_view()


if __name__ == "__main__":
    root = CTk()
    app = PharmacyManagementSystem(root)
    root.mainloop()