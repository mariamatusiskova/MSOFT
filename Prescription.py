import json
from tkinter import messagebox

from customtkinter import CTkFrame, CTkLabel, CTkButton, CTkEntry, CTkScrollableFrame


class Prescription:
    def __init__(self, main_view):
        self.main_view = main_view
        self.prescription_data = self.load_prescriptions_data()
        self.current_table = None

    def load_prescriptions_data(self):
        try:
            with open('data/prescription_data.json', 'r') as file:
                prescriptions_data = json.load(file)
            return prescriptions_data
        except FileNotFoundError:
            messagebox.showerror("Error", "Prescriptions data file not found!")
            prescriptions_data = {}
            return prescriptions_data
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Invalid prescriptions data file!")
            prescriptions_data = {}
            return prescriptions_data

    def get_insurance_id(self):
        insurance_container = CTkFrame(master=self.main_view, height=50, fg_color="#F0F0F0")
        insurance_container.pack(fill="x", pady=(45, 0), padx=27)

        self.entered_insurance_id = (
            CTkEntry(
                master=insurance_container,
                width=305,
                placeholder_text="Enter Insurance ID",
                border_color="#3EAEB1",
                border_width=2
            ))
        self.entered_insurance_id.pack(side="left", padx=(13, 0), pady=15)

        CTkButton(
            master=insurance_container,
            text="View Prescriptions",
            font=("Arial Black", 13),
            text_color="#fff",
            fg_color="#3EAEB1",
            hover_color="#1D837F",
            command=self.view_prescriptions
        ).pack(anchor="ne", side="left", padx=(13, 0), pady=15)

    def create_title(self):
        title_frame = CTkFrame(master=self.main_view, fg_color="transparent")
        # fill width
        title_frame.pack(anchor="n", fill="x",  padx=27, pady=(29, 0))
        CTkLabel(master=title_frame,
                 text="Prescriptions",
                 font=("Arial Black", 25),
                 text_color="#3EAEB1").pack(anchor="nw", side="left")

    def clear_current_table(self):
        if self.current_table:
            self.current_table.destroy()
            self.current_table = None

    def view_prescriptions(self):
        insurance_id = self.entered_insurance_id.get()

        self.clear_current_table()

        if insurance_id not in self.prescription_data:
            messagebox.showwarning("Not Found", "No prescriptions found for this ID")
            return

        self.current_table = CTkFrame(master=self.main_view, fg_color="#fff")
        self.current_table.pack(expand=True, fill="both", padx=27, pady=21)

        CTkLabel(
            master=self.current_table,
            text=f"Prescriptions for id: {insurance_id}",
            font=("Arial Bold", 16),
            text_color="#3EAEB1"
        ).pack(anchor="w", pady=(0, 10))

        data_frame = CTkScrollableFrame(master=self.current_table, fg_color="#fff")
        data_frame.pack(expand=True, fill="both")

        for prescription in self.prescription_data[insurance_id]:
            prescription_frame = CTkFrame(master=data_frame, fg_color="#f0f0f0", corner_radius=10)
            prescription_frame.pack(fill="x", pady=5, padx=5)

            CTkButton(
                master=prescription_frame,
                text=f"Prescription {prescription['prescription_id']} - {prescription['issue_date']} - {prescription['doctor_name']} - {prescription['status']}",
                # when button ic clicked
                command=lambda x=prescription: self.show_prescribed_medicines(x),
                fg_color="#3EAEB1",
                hover_color="#1D837F",
                corner_radius=5
            ).pack(fill="x", padx=10, pady=10)

    def show_prescribed_medicines(self, prescription):
        self.clear_current_table()

        # table for drugs
        self.current_table = CTkFrame(master=self.main_view, fg_color="#fff")
        self.current_table.pack(expand=True, fill="both", padx=27, pady=21)

        # back button
        top_frame = CTkFrame(master=self.current_table, fg_color="transparent")
        top_frame.pack(fill="x", pady=(0, 10))

        CTkButton(
            master=top_frame,
            text="← Back",
            command=self.view_prescriptions,
            fg_color="#3EAEB1",
            hover_color="#1D837F",
            width=60
        ).pack(side="left")

        CTkLabel(
            master=top_frame,
            text=f"Medicines in the prescription for id: {prescription['prescription_id']}",
            font=("Arial Bold", 16),
            text_color="#3EAEB1"
        ).pack(side="left", padx=20)

        # scrollable
        medicines_frame = CTkScrollableFrame(master=self.current_table, fg_color="#fff")
        medicines_frame.pack(expand=True, fill="both")

        for medicine in prescription['medicines']:
            medicine_frame = CTkFrame(master=medicines_frame, fg_color="#f0f0f0", corner_radius=10)
            medicine_frame.pack(fill="x", pady=5, padx=5)

            CTkButton(
                master=medicine_frame,
                text=f"{medicine['name']} - {medicine['dosage_recommendation']}",
                command=lambda x=medicine: self.show_medicine_details(x, prescription['prescription_id']),
                fg_color="#3EAEB1",
                hover_color="#1D837F",
                corner_radius=5
            ).pack(fill="x", padx=10, pady=10)

    def show_medicine_details(self, medicine, prescription_id):
        self.clear_current_table()

        # table for medicine details
        self.current_table = CTkFrame(master=self.main_view, fg_color="#fff")
        self.current_table.pack(expand=True, fill="both", padx=27, pady=21)

        # back button
        top_frame = CTkFrame(master=self.current_table, fg_color="transparent")
        top_frame.pack(fill="x", pady=(0, 10))

        CTkButton(
            master=top_frame,
            text="← Back",
            command=lambda: self.show_prescribed_medicines(
                next(x for x in self.prescription_data[self.entered_insurance_id.get()]
                     if x['prescription_id'] == prescription_id)),
            fg_color="#3EAEB1",
            hover_color="#1D837F",
            width=60
        ).pack(side="left")

        CTkLabel(
            master=top_frame,
            text=f"Medicine Details - {medicine['name']}",
            font=("Arial Bold", 16),
            text_color="#3EAEB1"
        ).pack(side="left", padx=20)

        details_frame = CTkFrame(master=self.current_table, fg_color="#f0f0f0", corner_radius=10)
        details_frame.pack(fill="both", expand=True, pady=10)

        details = [
            ("Medicine Name", medicine['name']),
            ("Dosage Recommendation", medicine['dosage_recommendation']),
            ("Leaflet", medicine['leaflet']),
            ("Expiry Date", medicine['expiry_date']),
        ]

        for label, value in details:
            row_frame = CTkFrame(master=details_frame, fg_color="transparent")
            row_frame.pack(fill="x", pady=5, padx=10)

            CTkLabel(
                master=row_frame,
                text=label,
                font=("Arial Bold", 12),
                text_color="#3EAEB1"
            ).pack(side="left", padx=(10, 20))

            CTkLabel(
                master=row_frame,
                text=value,
                font=("Arial", 12)
            ).pack(side="left")

