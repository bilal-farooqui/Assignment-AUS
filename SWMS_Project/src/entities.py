from datetime import datetime

class Resident:
    def __init__(self, resident_id, full_name, address):
        self.resident_id = resident_id
        self.full_name = full_name
        self.address = address
        self.bins = []
        self.current_requests = []

    def to_dict(self):
        return {
            "resident_id": self.resident_id,
            "full_name": self.full_name,
            "address": self.address,
            "current_requests": self.current_requests
        }

    @classmethod
    def from_dict(cls, data):
        r = cls(data["resident_id"], data["full_name"], data["address"])
        r.current_requests = data.get("current_requests", [])
        return r

    def __str__(self):
        return f"ID: {self.resident_id} | Name: {self.full_name}"

class Collector:
    def __init__(self, collector_id, name, vehicle_id):
        self.collector_id = collector_id
        self.name = name
        self.vehicle_id = vehicle_id
        self.assigned_route_ids = []
        self.assigned_tasks = []

    def assign_task(self, task_obj):
        self.assigned_tasks.append(task_obj)

    def to_dict(self):
        return {
            "collector_id": self.collector_id,
            "name": self.name,
            "vehicle_id": self.vehicle_id
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["collector_id"], data["name"], data["vehicle_id"])

    def __str__(self):
        return f"ID: {self.collector_id} | Name: {self.name}"

class Bin:
    def __init__(self, bin_id, bin_type, capacity, location, status="OK"):
        self.bin_id = bin_id
        self.bin_type = bin_type
        self.capacity = capacity
        self.location = location
        self.status = status
        self.assigned_resident = None

    def link_resident(self, resident):
        self.assigned_resident = resident
        resident.bins.append(self)

    def to_dict(self):
        return {
            "bin_id": self.bin_id,
            "bin_type": self.bin_type,
            "capacity": self.capacity,
            "location": self.location,
            "status": self.status,
            "assigned_resident_id": self.assigned_resident.resident_id if self.assigned_resident else None
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["bin_id"], data["bin_type"], data["capacity"], data["location"], data["status"])

    def __str__(self):
        return f"ID: {self.bin_id} | Type: {self.bin_type} | Status: {self.status}"

class Route:
    def __init__(self, route_id, zone_name):
        self.route_id = route_id
        self.zone_name = zone_name
        self.stop_sequence = []
        self.estimated_distance = 0.0
        self.estimated_duration = 0.0

    def add_stop(self, stop):
        self.stop_sequence.append(stop)

    def compute_estimates(self):
        count = len(self.stop_sequence)
        self.estimated_distance = count * 1.5
        self.estimated_duration = count * 5.0

    def to_dict(self):
        return {
            "route_id": self.route_id,
            "zone_name": self.zone_name,
            "stop_sequence": self.stop_sequence,
            "estimated_distance": self.estimated_distance,
            "estimated_duration": self.estimated_duration
        }

    @classmethod
    def from_dict(cls, data):
        r = cls(data["route_id"], data["zone_name"])
        r.stop_sequence = data.get("stop_sequence", [])
        r.estimated_distance = data.get("estimated_distance", 0.0)
        r.estimated_duration = data.get("estimated_duration", 0.0)
        return r

    def __str__(self):
        return f"ID: {self.route_id} | Zone: {self.zone_name}"

class WasteCollectionTask:
    def __init__(self, task_id, description, target_date, route):
        self.task_id = task_id
        self.description = description
        self.target_date = target_date
        self.route = route
        self.assigned_collector = None
        self.status = "Pending"

    def assign_to_collector(self, collector):
        self.assigned_collector = collector
        collector.assign_task(self)

    def to_dict(self):
        return {
            "task_id": self.task_id,
            "description": self.description,
            "target_date": self.target_date,
            "route_id": self.route.route_id if self.route else None,
            "assigned_collector_id": self.assigned_collector.collector_id if self.assigned_collector else None,
            "status": self.status
        }

    @classmethod
    def from_dict(cls, data, route_obj=None):
        task = cls(data["task_id"], data["description"], data["target_date"], route_obj)
        task.status = data["status"]
        return task

    def __str__(self):
        return f"ID: {self.task_id} | {self.description} | {self.status}"

class Transaction:
    def __init__(self, transaction_id, payer, amount, service_type, status="Pending"):
        self.transaction_id = transaction_id
        self.payer = payer
        self.amount = amount
        self.payment_date = datetime.now().strftime("%Y-%m-%d") if status == "Paid" else None
        self.service_type = service_type
        self.status = status  # "Pending" or "Paid"

    def process_payment(self):
        """Mark payment as paid"""
        self.status = "Paid"
        if not self.payment_date:
            self.payment_date = datetime.now().strftime("%Y-%m-%d")
        print(f"Processed ${self.amount} for {self.service_type}")

    def generate_receipt(self):
        return f"Receipt: {self.transaction_id} | Paid: ${self.amount}"

    def to_dict(self):
        payer_id = self.payer.resident_id if hasattr(self.payer, 'resident_id') else str(self.payer)
        return {
            "transaction_id": self.transaction_id,
            "payer_id": payer_id,
            "amount": self.amount,
            "payment_date": self.payment_date,
            "service_type": self.service_type,
            "status": self.status
        }

    @classmethod
    def from_dict(cls, data, payer_obj=None):
        t = cls(
            data["transaction_id"], 
            payer_obj or data["payer_id"], 
            data["amount"], 
            data["service_type"],
            data.get("status", "Pending")
        )
        t.payment_date = data.get("payment_date")
        return t

    def __str__(self):
        return f"Tx: {self.transaction_id} | Amount: ${self.amount}"

# === NEW INCIDENT CLASS (ASSIGNMENT 4 REQUIREMENT) ===
class Incident:
    """
    Represents an issue reported (e.g., overflow, damage).
    """
    def __init__(self, incident_id, description, reported_date, location, status="Open"):
        self.incident_id = incident_id
        self.description = description
        self.reported_date = reported_date
        self.location = location
        self.status = status

    def resolve(self):
        self.status = "Resolved"

    def to_dict(self):
        return {
            "incident_id": self.incident_id,
            "description": self.description,
            "reported_date": self.reported_date,
            "location": self.location,
            "status": self.status
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["incident_id"], 
            data["description"], 
            data["reported_date"], 
            data["location"], 
            data["status"]
        )

    def __str__(self):
        return f"ID: {self.incident_id} | Issue: {self.description} | Status: {self.status}"