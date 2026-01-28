# (Renamed) Purana Assignment 3 wala main

"""
Main entry point for the Smart Waste Management System (SWMS).
Handles user interaction via a CLI menu.
"""
# === src/cli_main.py ===

import sys
import os

# --- YEH CODE PASTE KARDO (Imports fix) ---
# Is se Python ko pata chal jayega ke system.py yahin par hai
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from system import WasteManagementSystem
from entities import Resident, Collector, Bin, Route, WasteCollectionTask, Transaction
# ------------------------------------------

# ... baaki code wesa hi rehne do ...
# ... baaki code wesa hi rahega ...
def get_valid_input(prompt, required=True, is_float=False):
    """Helper to get valid user input."""
    while True:
        value = input(prompt).strip()
        if required and not value:
            print("Error: This field cannot be empty.")
            continue
        if is_float:
            try:
                float_val = float(value)
                if float_val < 0:
                    print("Error: Amount must be positive.")
                    continue
                return float_val
            except ValueError:
                print("Error: Please enter a valid number.")
                continue
        return value

def handle_register_resident(system):
    """Handles resident registration."""
    r_id = get_valid_input("Enter Resident ID: ")
    name = get_valid_input("Enter Full Name: ")
    address = get_valid_input("Enter Address: ")
    resident = Resident(r_id, name, address)
    system.register_resident(resident)

def handle_bin_management(system):
    """Handles bin registration and viewing."""
    sub_choice = input("Type '1' to Register Bin, '2' to View Bins: ").strip()
    if sub_choice == '1':
        b_id = get_valid_input("Enter Bin ID: ")
        b_type = get_valid_input("Enter Type (General/Recycle/Green): ")
        capacity = get_valid_input("Enter Capacity (litres): ")
        location = get_valid_input("Enter Location: ")
        bin_obj = Bin(b_id, b_type, capacity, location)

        link = input("Link to a resident? (y/n): ").lower()
        if link == 'y':
            r_id = get_valid_input("Enter Resident ID to link: ")
            resident = next((r for r in system.residents if r.resident_id == r_id), None)
            if resident:
                bin_obj.link_resident(resident)
            else:
                print("Resident not found. Bin registered without link.")

        system.register_bin(bin_obj)
    elif sub_choice == '2':
        print("\n--- List of Bins ---")
        for b in system.bins:
            owner = b.assigned_resident.full_name if b.assigned_resident else "Unassigned"
            print(f"{b} | Owner: {owner}")
    else:
        print("Invalid option.")

def handle_route_management(system):
    """Handles route creation and viewing."""
    sub_choice = input("Type '1' to Create Route, '2' to View Routes: ").strip()
    if sub_choice == '1':
        rt_id = get_valid_input("Enter Route ID: ")
        zone = get_valid_input("Enter Zone Name: ")
        route = Route(rt_id, zone)

        while True:
            stop = input("Add a stop (address/bin ID) or type 'done': ")
            if stop.lower() == 'done':
                break
            if stop.strip():
                route.add_stop(stop)

        route.compute_estimates()
        system.create_route(route)
    elif sub_choice == '2':
        print("\n--- List of Routes ---")
        for rt in system.routes:
            print(f"{rt} | Dist: {rt.estimated_distance}km | Dur: {rt.estimated_duration}mins")

def handle_task_scheduling(system):
    """Handles task scheduling."""
    t_id = get_valid_input("Enter Task ID: ")
    desc = get_valid_input("Enter Description: ")
    date = get_valid_input("Enter Target Date (YYYY-MM-DD): ")

    print("Available Routes:")
    for r in system.routes:
        print(f" - {r.route_id} ({r.zone_name})")
    rt_id = get_valid_input("Enter Route ID to assign: ")
    route = next((r for r in system.routes if r.route_id == rt_id), None)

    if route:
        task = WasteCollectionTask(t_id, desc, date, route)
        c_name = get_valid_input("Enter Collector Name to create/assign (or existing ID): ")
        collector = next((c for c in system.collectors if c.name == c_name), None)
        if not collector:
            c_id = get_valid_input(f"New Collector ID for {c_name}: ")
            v_id = get_valid_input("Vehicle ID: ")
            collector = Collector(c_id, c_name, v_id)
            system.add_collector(collector)

        task.assign_to_collector(collector)
        system.schedule_task(task)
    else:
        print("Route not found.")

def handle_payment(system):
    """Handles payment processing."""
    t_id = get_valid_input("Enter Transaction ID: ")
    r_id = get_valid_input("Enter Payer Resident ID (or 'Guest'): ")
    resident = next((r for r in system.residents if r.resident_id == r_id), None)
    payer = resident if resident else r_id

    amount = get_valid_input("Enter Amount: ", is_float=True)
    service = get_valid_input("Enter Service Type: ")

    transaction = Transaction(t_id, payer, amount, service)
    system.process_transaction(transaction)

def main():
    """Main loop for the application."""
    system = WasteManagementSystem()
    system.load_data()

    menu_options = {
        '1': lambda: handle_register_resident(system),
        '2': system.view_residents,
        '3': lambda: handle_bin_management(system),
        '4': lambda: handle_route_management(system),
        '5': lambda: handle_task_scheduling(system),
        '6': lambda: handle_payment(system),
        '7': system.generate_financial_report,
        '8': lambda: system.view_resident_requests(get_valid_input("Enter Resident ID: ")),
        '9': lambda: print_search_results(
            system.find_resident(get_valid_input("Enter Name or ID: "))
        ),
        '10': system.export_financial_report,
        '11': lambda: (system.save_data(), sys.exit())
    }

    while True:
        print_menu()
        choice = input("Enter your choice: ").strip()
        try:
            action = menu_options.get(choice)
            if action:
                action()
            else:
                print("Invalid choice. Please try again.")
        except Exception as e: # pylint: disable=broad-exception-caught
            print(f"An unexpected error occurred: {e}")

def print_search_results(results):
    """Helper to print search results."""
    if results:
        print(f"Found {len(results)} matches:")
        for r in results:
            print(r)
    else:
        print("No matches found.")

def print_menu():
    """Prints the main menu."""
    print("\n=============================================")
    print(" Welcome to Smart Waste Management System (SWMS)")
    print("=============================================")
    print("1. Register New Resident")
    print("2. View All Residents")
    print("3. Register Bin / View Bins")
    print("4. Create Route / View Routes")
    print("5. Schedule Collection Task")
    print("6. Process Payment")
    print("7. Generate Financial Report")
    print("8. View Resident Requests")
    print("9. Search Resident")
    print("10. Export Report")
    print("11. Save & Exit")
    print("=============================================")

if __name__ == "__main__":
    main()
