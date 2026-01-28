import json
import os
# Imports bina dot ke (taake run.py se chal sake)
from entities import Resident, Collector, Bin, Route, WasteCollectionTask, Transaction, Incident

class WasteManagementSystem:
    def __init__(self):
        self.residents = []
        self.collectors = []
        self.bins = []
        self.routes = []
        self.tasks = []
        self.transactions = []
        self.incidents = []  # <--- NEW LIST FOR INCIDENTS

    def _get_data_path(self):
        """Helper to get path to data folder"""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_dir, "data", "swms_data.json")
    
    def generate_resident_id(self):
        """Generate sequential Resident ID"""
        if not self.residents:
            return "R001"
        # Get all resident IDs and find the highest number
        max_num = 0
        for r in self.residents:
            if r.resident_id.startswith("R"):
                try:
                    num = int(r.resident_id[1:])
                    max_num = max(max_num, num)
                except ValueError:
                    pass
        return f"R{max_num + 1:03d}"
    
    def generate_bin_id(self):
        """Generate sequential Bin ID"""
        if not self.bins:
            return "B001"
        max_num = 0
        for b in self.bins:
            if b.bin_id.startswith("B"):
                try:
                    num = int(b.bin_id[1:])
                    max_num = max(max_num, num)
                except ValueError:
                    pass
        return f"B{max_num + 1:03d}"
    
    def generate_collector_id(self):
        """Generate sequential Collector ID"""
        if not self.collectors:
            return "C001"
        max_num = 0
        for c in self.collectors:
            if c.collector_id.startswith("C"):
                try:
                    num = int(c.collector_id[1:])
                    max_num = max(max_num, num)
                except ValueError:
                    pass
        return f"C{max_num + 1:03d}"
    
    def generate_route_id(self):
        """Generate sequential Route ID"""
        if not self.routes:
            return "RT01"
        max_num = 0
        for r in self.routes:
            if r.route_id.startswith("RT"):
                try:
                    num = int(r.route_id[2:])
                    max_num = max(max_num, num)
                except ValueError:
                    pass
        return f"RT{max_num + 1:02d}"
    
    def generate_task_id(self):
        """Generate sequential Task ID"""
        if not self.tasks:
            return "T001"
        max_num = 0
        for t in self.tasks:
            if t.task_id.startswith("T"):
                try:
                    num = int(t.task_id[1:])
                    max_num = max(max_num, num)
                except ValueError:
                    pass
        return f"T{max_num + 1:03d}"
    
    def generate_transaction_id(self):
        """Generate sequential Transaction ID"""
        if not self.transactions:
            return "TX0001"
        max_num = 0
        for t in self.transactions:
            if t.transaction_id.startswith("TX"):
                try:
                    num = int(t.transaction_id[2:])
                    max_num = max(max_num, num)
                except ValueError:
                    pass
        return f"TX{max_num + 1:04d}"
    
    def generate_incident_id(self):
        """Generate sequential Incident ID"""
        if not self.incidents:
            return "INC001"
        max_num = 0
        for i in self.incidents:
            if i.incident_id.startswith("INC"):
                try:
                    num = int(i.incident_id[3:])
                    max_num = max(max_num, num)
                except ValueError:
                    pass
        return f"INC{max_num + 1:03d}"

    def register_resident(self, resident):
        self.residents.append(resident)
        print(f"Resident '{resident.full_name}' registered.")
    
    def delete_resident(self, resident_id):
        """Delete resident by ID"""
        resident = next((r for r in self.residents if r.resident_id == resident_id), None)
        if resident:
            # Unlink bins
            for bin_obj in self.bins:
                if bin_obj.assigned_resident == resident:
                    bin_obj.assigned_resident = None
            self.residents.remove(resident)
            return True
        return False

    def add_collector(self, collector):
        self.collectors.append(collector)
        print(f"Collector '{collector.name}' added.")
    
    def delete_collector(self, collector_id):
        """Delete collector by ID"""
        collector = next((c for c in self.collectors if c.collector_id == collector_id), None)
        if collector:
            # Unlink tasks
            for task in self.tasks:
                if task.assigned_collector == collector:
                    task.assigned_collector = None
            self.collectors.remove(collector)
            return True
        return False

    def register_bin(self, bin_obj):
        self.bins.append(bin_obj)
        print(f"Bin {bin_obj.bin_id} registered.")
    
    def delete_bin(self, bin_id):
        """Delete bin by ID"""
        bin_obj = next((b for b in self.bins if b.bin_id == bin_id), None)
        if bin_obj:
            # Unlink from resident
            if bin_obj.assigned_resident:
                if bin_obj in bin_obj.assigned_resident.bins:
                    bin_obj.assigned_resident.bins.remove(bin_obj)
            self.bins.remove(bin_obj)
            return True
        return False

    def create_route(self, route):
        self.routes.append(route)
        print(f"Route {route.route_id} created.")
    
    def delete_route(self, route_id):
        """Delete route by ID"""
        route = next((r for r in self.routes if r.route_id == route_id), None)
        if route:
            # Unlink tasks
            for task in self.tasks:
                if task.route == route:
                    task.route = None
            self.routes.remove(route)
            return True
        return False

    def schedule_task(self, task):
        self.tasks.append(task)
        print(f"Task '{task.description}' scheduled.")
    
    def delete_task(self, task_id):
        """Delete task by ID"""
        task = next((t for t in self.tasks if t.task_id == task_id), None)
        if task:
            # Unlink from collector
            if task.assigned_collector:
                if task in task.assigned_collector.assigned_tasks:
                    task.assigned_collector.assigned_tasks.remove(task)
            self.tasks.remove(task)
            return True
        return False

    def process_transaction(self, transaction):
        """Process transaction - mark as paid and add to system"""
        transaction.process_payment()
        self.transactions.append(transaction)
        print(transaction.generate_receipt())
    
    def create_pending_payment(self, transaction):
        """Create a pending payment (not processed yet)"""
        self.transactions.append(transaction)
        print(f"Pending payment {transaction.transaction_id} created for {transaction.service_type}")
    
    def get_pending_payments_for_resident(self, resident_id):
        """Get all pending payments for a resident"""
        return [t for t in self.transactions 
                if hasattr(t.payer, 'resident_id') and t.payer.resident_id == resident_id 
                and t.status == "Pending"]
    
    def get_total_revenue(self):
        """Get total revenue from paid transactions only"""
        return sum(t.amount for t in self.transactions if t.status == "Paid")
    
    def delete_transaction(self, transaction_id):
        """Delete transaction by ID"""
        transaction = next((t for t in self.transactions if t.transaction_id == transaction_id), None)
        if transaction:
            self.transactions.remove(transaction)
            return True
        return False

    # === NEW METHOD FOR INCIDENTS ===
    def log_incident(self, incident):
        """Logs a new incident/observation."""
        self.incidents.append(incident)
        print(f"Incident {incident.incident_id} logged.")
    
    def delete_incident(self, incident_id):
        """Delete incident by ID"""
        incident = next((i for i in self.incidents if i.incident_id == incident_id), None)
        if incident:
            self.incidents.remove(incident)
            return True
        return False
    
    def verify_management_login(self, username, password):
        """Verify management login credentials (Hardcoded)"""
        # Hardcoded admin credentials
        ADMIN_USERNAME = "admin"
        ADMIN_PASSWORD = "admin123"
        
        return username == ADMIN_USERNAME and password == ADMIN_PASSWORD
    
    def get_management_info(self):
        """Get management information (Hardcoded)"""
        # Hardcoded management info
        return {
            "management_id": "MGT001",
            "username": "admin"
        }

    def find_resident(self, query):
        results = [r for r in self.residents if query.lower() in r.resident_id.lower() or query.lower() in r.full_name.lower()]
        return results

    def view_residents(self):
        print("\n--- Residents ---")
        for r in self.residents: print(r)

    def view_resident_requests(self, r_id):
        res = next((r for r in self.residents if r.resident_id == r_id), None)
        if res:
            print(f"Requests for {res.full_name}: {res.current_requests}")
        else:
            print("Resident not found.")

    def generate_financial_report(self):
        total = sum(t.amount for t in self.transactions)
        print(f"Total Revenue: ${total}")
        return str(total)

    def export_financial_report(self):
        self.generate_financial_report()
        print("Report exported (simulated).")

    # === UPDATED SAVE DATA ===
    def save_data(self):
        filepath = self._get_data_path()
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        data = {
            "residents": [r.to_dict() for r in self.residents],
            "collectors": [c.to_dict() for c in self.collectors],
            "bins": [b.to_dict() for b in self.bins],
            "routes": [r.to_dict() for r in self.routes],
            "tasks": [t.to_dict() for t in self.tasks],
            "transactions": [t.to_dict() for t in self.transactions],
            "incidents": [i.to_dict() for i in self.incidents] # <--- SAVING INCIDENTS
        }
        with open(filepath, "w") as f:
            json.dump(data, f, indent=4)
        print(f"Data saved to {filepath}")

    # === UPDATED LOAD DATA ===
    def load_data(self):
        filepath = self._get_data_path()
        if not os.path.exists(filepath):
            print("No saved data found.")
            return

        with open(filepath, "r") as f:
            data = json.load(f)

        self.residents = [Resident.from_dict(d) for d in data.get("residents", [])]
        self.collectors = [Collector.from_dict(d) for d in data.get("collectors", [])]
        self.routes = [Route.from_dict(d) for d in data.get("routes", [])]
        self.incidents = [Incident.from_dict(d) for d in data.get("incidents", [])] # <--- LOADING INCIDENTS

        # Re-link Bins
        self.bins = []
        for b_data in data.get("bins", []):
            bin_obj = Bin.from_dict(b_data)
            res_id = b_data.get("assigned_resident_id")
            if res_id:
                resident = next((r for r in self.residents if r.resident_id == res_id), None)
                if resident: bin_obj.link_resident(resident)
            self.bins.append(bin_obj)

        # Re-link Tasks
        self.tasks = []
        for t_data in data.get("tasks", []):
            route = next((r for r in self.routes if r.route_id == t_data.get("route_id")), None)
            task = WasteCollectionTask.from_dict(t_data, route)
            col_id = t_data.get("assigned_collector_id")
            if col_id:
                col = next((c for c in self.collectors if c.collector_id == col_id), None)
                if col: task.assign_to_collector(col)
            self.tasks.append(task)

        # Re-link Transactions
        self.transactions = []
        for tr_data in data.get("transactions", []):
            payer_id = tr_data.get("payer_id")
            payer = next((r for r in self.residents if r.resident_id == payer_id), payer_id)
            transaction = Transaction.from_dict(tr_data, payer)
            # Set status if not present (for backward compatibility)
            if not hasattr(transaction, 'status') or transaction.status is None:
                transaction.status = "Paid" if transaction.payment_date else "Pending"
            self.transactions.append(transaction)

        print(f"Data loaded from {filepath}")