from dataclasses import dataclass
import json
import tkinter as tk

DEFAULT_CONFIG = {
    "total_miles": 300,
    "gas_per_gal": 2.75,
    "vehicle_classes": ["sedan", "suv"],
    "expected_mpg": {"sedan": 35, "suv": 30},
    "max_occupants": {"sedan": 2, "suv": 3},
}

DEFAULT_TRIPS = "Sedan 2 30\nSUV 3 35"


@dataclass
class Trip:

    vehicle_class: str
    num_occupants: int
    actual_cost: float
    config: dict
    expected_cost: float = None
    reimbursed: float = None

    def __post_init__(self):

        occupancy_multiplier: float = (
            self.num_occupants / self.config["max_occupants"][self.vehicle_class]
        )
        occupancy_multiplier = min(1.0, occupancy_multiplier)

        actual_mpg: float = (
            self.config["total_miles"] / self.actual_cost * self.config["gas_per_gal"]
        )
        mpg_multiplier: float = (
            actual_mpg / self.config["expected_mpg"][self.vehicle_class]
        )
        mpg_multiplier = min(1.0, mpg_multiplier)

        expected_gallons_consumed: float = (
            self.config["total_miles"] / self.config["expected_mpg"][self.vehicle_class]
        )
        self.expected_cost: float = (
            self.config["gas_per_gal"] * expected_gallons_consumed
        )
        self.reimbursed: float = (
            occupancy_multiplier * mpg_multiplier * self.expected_cost
        )
        self.reimbursed = min(self.reimbursed, self.actual_cost)

    def __str__(self):

        return f"Type: {self.vehicle_class}, # occupants: {self.num_occupants}, cost: ${self.actual_cost:.2f}, expected cost: ${self.expected_cost:.2f}, reimburseable cost: ${self.reimbursed:.2f}"


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

        vehicle_class, num_occupants, actual_cost = line.split()
        return Trip(
            vehicle_class=vehicle_class.lower(),
            num_occupants=int(num_occupants),
            actual_cost=float(actual_cost),
            config=self.config,
        )

    def trip_press(self):

        self.trip_lines = self.trip_txt.get(1.0, "end-1c").split("\n")
        self.reimbursement_txt.delete("1.0", tk.END)
        for line in self.trip_lines:
            trip = self.parse_trip(line)
            self.reimbursement_txt.insert("1.0", f"{trip}\n")
        self.trip_lbl.config(text="Info collected!")


app = App()
