from dataclasses import dataclass
import json
import tkinter as tk


DEFAULT_CONFIG = {
    "total_miles": 433,
    "gas_per_gal": 2.70,
    "tax_per_gal": 0.26,
    "vehicle_classes": ["sedan", "suv"],
    "expected_mpg": {"sedan": 35, "suv": 30},
    "max_occupants": {"sedan": 2, "suv": 3},
}

DEFAULT_TRIPS = "Sedan 2 28 Jack\nSUV 3 33 Jill"


@dataclass
class Trip:

    config: dict
    vehicle_class: str
    reported_mpg: int
    num_occupants: int
    user: str
    reimbursed: float = None
    expected: float = None

    def __post_init__(self):
    
       actual_gas_rate = self.config["gas_per_gal"] + self.config["tax_per_gal"]
    
       expected_mpg = self.config["expected_mpg"][self.vehicle_class]
       max_occupants = self.config["max_occupants"][self.vehicle_class]
       
       expected_gallons_consumed = self.config["total_miles"] / self.reported_mpg
       self.expected = expected_gallons_consumed * actual_gas_rate
       
       max_gallons_consumed = self.config["total_miles"] / expected_mpg
       self.reimbursed = max_gallons_consumed * actual_gas_rate * min(1.0, self.num_occupants / max_occupants)

    def __str__(self):
    
        return f'Class: {self.vehicle_class}, MPG: {self.reported_mpg}, Expected: ${self.expected:.2f}, Reimbursement: ${self.reimbursed:.2f}, User: {self.user}'


class App:

    def __init__(self):

        self.config = DEFAULT_CONFIG
        self.trips = DEFAULT_TRIPS

        application = tk.Tk("Reimbursement Calculator Application")

        input_frame = tk.LabelFrame(application, text="Configuration")
        input_frame.grid(row=0, column=0)

        # TextBox Creation
        self.input_txt = tk.Text(input_frame, height=20, width=60)
        self.input_txt.insert("1.0", json.dumps(self.config, indent=4))

        self.input_txt.pack()

        # Button Creation
        config_button = tk.Button(input_frame, text="Enter", command=self.load_config)
        config_button.pack()

        # Label Creation
        self.config_lbl = tk.Label(input_frame, text="Configuration")
        self.config_lbl.pack()

        trip_frame = tk.LabelFrame(application, text="Reimbursement Info")
        trip_frame.grid(row=0, column=1)

        self.trip_txt = tk.Text(trip_frame, height=20, width=60)
        self.trip_txt.insert("1.0", self.trips)
        self.trip_txt.pack()

        print_button = tk.Button(trip_frame, text="Enter", command=self.trip_press)
        print_button.pack()

        self.trip_lbl = tk.Label(trip_frame, text="Trips")
        self.trip_lbl.pack()

        reimbursement_frame = tk.LabelFrame(application, text="Reimbursements")
        reimbursement_frame.grid(row=1, column=0, columnspan=2)

        self.reimbursement_txt = tk.Text(reimbursement_frame, height=20, width=120)
        self.reimbursement_txt.pack()

        application.mainloop()

    def load_config(self):

        self.config = json.loads(self.input_txt.get(1.0, "end-1c"))
        self.config_lbl.config(text="Configuration loaded!")

    def parse_trip(self, line: str) -> Trip:

        vehicle_class, num_occupants, reported_mpg, user = line.split()
        return Trip(
            config=self.config,
            vehicle_class=vehicle_class.lower(),
            num_occupants=int(num_occupants),
            reported_mpg=int(reported_mpg),
            user=user
        )

    def trip_press(self):

        self.trip_lines = self.trip_txt.get(1.0, "end-1c").split("\n")
        self.reimbursement_txt.delete("1.0", tk.END)
        txt = ""
        for line in self.trip_lines:
            try:
                trip = self.parse_trip(line)
            except ValueError:
                trip = ''
            txt += f"{trip}\n"
        self.reimbursement_txt.insert("1.0", txt)
        self.trip_lbl.config(text="Info collected!")


if __name__ == '__main__':

    app = App()
