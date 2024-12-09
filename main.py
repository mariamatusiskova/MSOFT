import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime


class PharmacyManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("The Pharmacy Management System")
        self.root.geometry("800x600")

        # Create main notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=5)

        # Create tabs for each use case
        self.prescription_tab = ttk.Frame(self.notebook)
        self.symptoms_tab = ttk.Frame(self.notebook)
        self.basket_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.prescription_tab, text='View Prescriptions')
        self.notebook.add(self.symptoms_tab, text='Find Medicine')
        self.notebook.add(self.basket_tab, text='Shopping Basket')

        # Initialize shopping basket
        self.basket = []

        # Load dummy data
        self.load_dummy_data()

        # Setup each tab
        self.setup_prescription_view()
        self.setup_symptoms_view()
        self.setup_basket_view()

    def load_dummy_data(self):
        # Dummy data for testing
        self.prescriptions = {
            "12345": [{
                "id": "P001",
                "medicine": "Amoxicillin",
                "dosage": "500mg",
                "issue_date": "2024-01-01",
                "expiry_date": "2024-02-01",
                "status": "Active"
            }],
            "67890": [{
                "id": "P002",
                "medicine": "Ibuprofen",
                "dosage": "400mg",
                "issue_date": "2024-01-15",
                "expiry_date": "2024-02-15",
                "status": "Active"
            }]
        }

        self.symptoms_data = {
            "Headache": ["Paracetamol", "Ibuprofen", "Aspirin"],
            "Cough": ["Cough Syrup A", "Cough Tablets B", "Throat Lozenges"],
            "Fever": ["Paracetamol", "Ibuprofen", "Fever Reducer Plus"]
        }

    def setup_prescription_view(self):
        # Insurance ID entry
        frame = ttk.Frame(self.prescription_tab, padding="10")
        frame.pack(fill='both', expand=True)

        ttk.Label(frame, text="Enter Insurance ID:").pack(pady=5)
        self.insurance_id = ttk.Entry(frame)
        self.insurance_id.pack(pady=5)

        ttk.Button(frame, text="View Prescriptions",
                   command=self.view_prescriptions).pack(pady=5)

        # Treeview for prescriptions
        self.prescription_tree = ttk.Treeview(frame,
                                              columns=("Medicine", "Dosage", "Issue Date", "Expiry Date", "Status"))
        self.prescription_tree.heading("Medicine", text="Medicine")
        self.prescription_tree.heading("Dosage", text="Dosage")
        self.prescription_tree.heading("Issue Date", text="Issue Date")
        self.prescription_tree.heading("Expiry Date", text="Expiry Date")
        self.prescription_tree.heading("Status", text="Status")
        self.prescription_tree["show"] = "headings"
        self.prescription_tree.pack(pady=10, fill='both', expand=True)

    def setup_symptoms_view(self):
        frame = ttk.Frame(self.symptoms_tab, padding="10")
        frame.pack(fill='both', expand=True)

        ttk.Label(frame, text="Select Symptom:").pack(pady=5)
        self.symptom_var = tk.StringVar()
        self.symptom_combo = ttk.Combobox(frame, textvariable=self.symptom_var)
        self.symptom_combo['values'] = list(self.symptoms_data.keys())
        self.symptom_combo.pack(pady=5)

        self.symptom_combo.bind('<<ComboboxSelected>>', self.show_medicines)

        # Listbox for medicines
        self.medicine_listbox = tk.Listbox(frame, height=10)
        self.medicine_listbox.pack(pady=10, fill='both', expand=True)

        ttk.Button(frame, text="Add to Basket",
                   command=self.add_to_basket).pack(pady=5)

    def setup_basket_view(self):
        frame = ttk.Frame(self.basket_tab, padding="10")
        frame.pack(fill='both', expand=True)

        self.basket_listbox = tk.Listbox(frame, height=10)
        self.basket_listbox.pack(pady=10, fill='both', expand=True)

        ttk.Button(frame, text="Remove Selected",
                   command=self.remove_from_basket).pack(pady=5)
        ttk.Button(frame, text="Checkout",
                   command=self.checkout).pack(pady=5)

    def view_prescriptions(self):
        insurance_id = self.insurance_id.get()
        self.prescription_tree.delete(*self.prescription_tree.get_children())

        if insurance_id in self.prescriptions:
            for prescription in self.prescriptions[insurance_id]:
                self.prescription_tree.insert("", "end", values=(
                    prescription["medicine"],
                    prescription["dosage"],
                    prescription["issue_date"],
                    prescription["expiry_date"],
                    prescription["status"]
                ))
        else:
            messagebox.showwarning("Not Found", "No prescriptions found for this ID")

    def show_medicines(self, event=None):
        symptom = self.symptom_var.get()
        self.medicine_listbox.delete(0, tk.END)

        if symptom in self.symptoms_data:
            for medicine in self.symptoms_data[symptom]:
                self.medicine_listbox.insert(tk.END, medicine)

    def add_to_basket(self):
        selection = self.medicine_listbox.curselection()
        if selection:
            medicine = self.medicine_listbox.get(selection)
            self.basket.append(medicine)
            self.update_basket_view()
            messagebox.showinfo("Success", f"{medicine} added to basket")

    def remove_from_basket(self):
        selection = self.basket_listbox.curselection()
        if selection:
            index = selection[0]
            self.basket.pop(index)
            self.update_basket_view()

    def update_basket_view(self):
        self.basket_listbox.delete(0, tk.END)
        for item in self.basket:
            self.basket_listbox.insert(tk.END, item)

    def checkout(self):
        if not self.basket:
            messagebox.showwarning("Empty Basket", "Your basket is empty!")
            return

        # In a real application, this would open a new window for shipping/payment
        result = messagebox.askyesno("Checkout",
                                     "Proceed to payment?\nTotal items: " +
                                     str(len(self.basket)))
        if result:
            messagebox.showinfo("Success", "Order placed successfully!")
            self.basket.clear()
            self.update_basket_view()



if __name__ == "__main__":
    root = tk.Tk()
    app = PharmacyManagementSystem(root)
    root.mainloop()