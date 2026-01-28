import tkinter as tk
from tkinter import ttk, messagebox
import datetime

# --- IMPORTS (Dots handled for safe execution) ---
try:
    from system import WasteManagementSystem
    from entities import Resident, Incident, Bin, Route, WasteCollectionTask, Collector, Transaction
except ImportError:
    from .system import WasteManagementSystem
    from .entities import Resident, Incident, Bin, Route, WasteCollectionTask, Collector, Transaction

# --- MATPLOTLIB SETUP ---
try:
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False

# ==================== VALIDATION FUNCTIONS ====================
def validate_name(name):
    """Validate name - should contain only letters, spaces, and common punctuation"""
    if not name or not name.strip():
        return False, "Name cannot be empty"
    
    name = name.strip()
    if len(name) < 2:
        return False, "Name must be at least 2 characters long"
    
    if len(name) > 100:
        return False, "Name is too long (max 100 characters)"
    
    # Allow letters, spaces, hyphens, apostrophes, and periods
    if not all(c.isalpha() or c.isspace() or c in "-'." for c in name):
        return False, "Name can only contain letters, spaces, hyphens, apostrophes, and periods"
    
    # Should start with a letter
    if not name[0].isalpha():
        return False, "Name must start with a letter"
    
    return True, ""

def validate_address(address):
    """Validate address"""
    if not address or not address.strip():
        return False, "Address cannot be empty"
    
    address = address.strip()
    if len(address) < 5:
        return False, "Address must be at least 5 characters long"
    
    if len(address) > 200:
        return False, "Address is too long (max 200 characters)"
    
    return True, ""

def validate_amount(amount_str):
    """Validate amount - should be a positive number"""
    if not amount_str or not amount_str.strip():
        return False, "Amount cannot be empty"
    
    try:
        amount = float(amount_str.strip())
        if amount <= 0:
            return False, "Amount must be greater than 0"
        if amount > 1000000:
            return False, "Amount is too large (max $1,000,000)"
        return True, amount
    except ValueError:
        return False, "Amount must be a valid number"

def validate_capacity(capacity_str):
    """Validate bin capacity - should be a positive number"""
    if not capacity_str or not capacity_str.strip():
        return False, "Capacity cannot be empty"
    
    try:
        capacity = float(capacity_str.strip())
        if capacity <= 0:
            return False, "Capacity must be greater than 0"
        if capacity > 10000:
            return False, "Capacity is too large (max 10,000 litres)"
        return True, capacity
    except ValueError:
        return False, "Capacity must be a valid number"

def validate_description(description):
    """Validate description"""
    if not description or not description.strip():
        return False, "Description cannot be empty"
    
    description = description.strip()
    if len(description) < 5:
        return False, "Description must be at least 5 characters long"
    
    if len(description) > 500:
        return False, "Description is too long (max 500 characters)"
    
    return True, ""

def validate_location(location):
    """Validate location"""
    if not location or not location.strip():
        return False, "Location cannot be empty"
    
    location = location.strip()
    if len(location) < 3:
        return False, "Location must be at least 3 characters long"
    
    if len(location) > 200:
        return False, "Location is too long (max 200 characters)"
    
    return True, ""

# ==================== LOGIN WINDOW ====================
class LoginWindow:
    def __init__(self, root, system):
        self.root = root
        self.system = system
        self.current_user = None
        self.user_type = None
        
        # Window Setup
        self.root.title("SWMS - Login")
        self.root.geometry("500x400")
        self.root.resizable(True, True)  # Allow resizing
        self.root.minsize(450, 350)  # Minimum size to prevent too small
        
        # Center window
        self.center_window()
        
        # Color Scheme
        self.bg_color = "#2C3E50"
        self.accent_color = "#3498DB"
        self.success_color = "#27AE60"
        self.warning_color = "#E67E22"
        self.text_color = "#ECF0F1"
        
        self.root.configure(bg=self.bg_color)
        
        # Main Frame
        main_frame = tk.Frame(root, bg=self.bg_color)
        main_frame.pack(expand=True, fill='both', padx=40, pady=40)
        
        # Title
        title_label = tk.Label(
            main_frame, 
            text="Smart Waste Management System",
            font=("Arial", 20, "bold"),
            bg=self.bg_color,
            fg=self.text_color
        )
        title_label.pack(pady=(0, 30))
        
        # Subtitle
        subtitle = tk.Label(
            main_frame,
            text="Please select your role to continue",
            font=("Arial", 11),
            bg=self.bg_color,
            fg="#BDC3C7"
        )
        subtitle.pack(pady=(0, 40))
        
        # Role Selection Frame
        role_frame = tk.Frame(main_frame, bg=self.bg_color)
        role_frame.pack(pady=20)
        
        # Resident Button
        self.btn_resident = tk.Button(
            role_frame,
            text="👤 Resident",
            font=("Arial", 14, "bold"),
            bg="#16A085",
            fg="white",
            activebackground="#1ABC9C",
            activeforeground="white",
            relief=tk.FLAT,
            padx=30,
            pady=15,
            cursor="hand2",
            command=lambda: self.login("resident")
        )
        self.btn_resident.pack(pady=10, fill='x', padx=20)
        
        # Collector Button
        self.btn_collector = tk.Button(
            role_frame,
            text="🚛 Collector",
            font=("Arial", 14, "bold"),
            bg="#E67E22",
            fg="white",
            activebackground="#F39C12",
            activeforeground="white",
            relief=tk.FLAT,
            padx=30,
            pady=15,
            cursor="hand2",
            command=lambda: self.login("collector")
        )
        self.btn_collector.pack(pady=10, fill='x', padx=20)
        
        # Management Button
        self.btn_management = tk.Button(
            role_frame,
            text="⚙️ Management",
            font=("Arial", 14, "bold"),
            bg="#8E44AD",
            fg="white",
            activebackground="#9B59B6",
            activeforeground="white",
            relief=tk.FLAT,
            padx=30,
            pady=15,
            cursor="hand2",
            command=lambda: self.login("management")
        )
        self.btn_management.pack(pady=10, fill='x', padx=20)
        
        # Info Label
        info_label = tk.Label(
            main_frame,
            text="Select a role to access the system",
            font=("Arial", 9),
            bg=self.bg_color,
            fg="#95A5A6"
        )
        info_label.pack(pady=(20, 0))
    
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def login(self, role):
        """Handle login based on role"""
        self.user_type = role
        
        if role == "resident":
            self.show_resident_selection()
        elif role == "collector":
            self.show_collector_selection()
        else:  # management
            self.show_management_login()
    
    def show_resident_selection(self):
        """Show resident ID selection window"""
        top = tk.Toplevel(self.root)
        top.title("Resident Login")
        top.geometry("400x250")
        top.configure(bg="#2C3E50")
        top.resizable(True, True)  # Allow resizing
        top.minsize(350, 200)  # Minimum size
        
        # Center
        top.update_idletasks()
        x = (top.winfo_screenwidth() // 2) - (400 // 2)
        y = (top.winfo_screenheight() // 2) - (250 // 2)
        top.geometry(f'400x250+{x}+{y}')
        
        frame = tk.Frame(top, bg="#2C3E50")
        frame.pack(expand=True, fill='both', padx=30, pady=30)
        
        tk.Label(
            frame, 
            text="Enter Resident ID",
            font=("Arial", 16, "bold"),
            bg="#2C3E50",
            fg="white"
        ).pack(pady=(0, 20))
        
        entry = tk.Entry(frame, font=("Arial", 12), width=20)
        entry.pack(pady=10)
        entry.focus()
        
        def submit():
            res_id = entry.get().strip()
            resident = next((r for r in self.system.residents if r.resident_id == res_id), None)
            if resident:
                self.current_user = resident
                top.destroy()
                self.open_main_app()
            else:
                messagebox.showerror("Error", "Resident ID not found!")
        
        btn = tk.Button(
            frame,
            text="Login",
            font=("Arial", 12, "bold"),
            bg="#16A085",
            fg="white",
            activebackground="#1ABC9C",
            relief=tk.FLAT,
            padx=20,
            pady=8,
            command=submit
        )
        btn.pack(pady=15)
        
        entry.bind('<Return>', lambda e: submit())
    
    def show_collector_selection(self):
        """Show collector ID selection window"""
        top = tk.Toplevel(self.root)
        top.title("Collector Login")
        top.geometry("400x250")
        top.configure(bg="#2C3E50")
        top.resizable(True, True)  # Allow resizing
        top.minsize(350, 200)  # Minimum size
        
        # Center
        top.update_idletasks()
        x = (top.winfo_screenwidth() // 2) - (400 // 2)
        y = (top.winfo_screenheight() // 2) - (250 // 2)
        top.geometry(f'400x250+{x}+{y}')
        
        frame = tk.Frame(top, bg="#2C3E50")
        frame.pack(expand=True, fill='both', padx=30, pady=30)
        
        tk.Label(
            frame,
            text="Enter Collector ID",
            font=("Arial", 16, "bold"),
            bg="#2C3E50",
            fg="white"
        ).pack(pady=(0, 20))
        
        entry = tk.Entry(frame, font=("Arial", 12), width=20)
        entry.pack(pady=10)
        entry.focus()
        
        def submit():
            col_id = entry.get().strip()
            collector = next((c for c in self.system.collectors if c.collector_id == col_id), None)
            if collector:
                self.current_user = collector
                top.destroy()
                self.open_main_app()
            else:
                messagebox.showerror("Error", "Collector ID not found!")
        
        btn = tk.Button(
            frame,
            text="Login",
            font=("Arial", 12, "bold"),
            bg="#E67E22",
            fg="white",
            activebackground="#F39C12",
            relief=tk.FLAT,
            padx=20,
            pady=8,
            command=submit
        )
        btn.pack(pady=15)
        
        entry.bind('<Return>', lambda e: submit())
    
    def show_management_login(self):
        """Show management login window with username and password"""
        top = tk.Toplevel(self.root)
        top.title("Management Login")
        top.geometry("450x320")
        top.configure(bg="#2C3E50")
        top.resizable(True, True)  # Allow resizing
        top.minsize(400, 280)  # Minimum size
        
        # Center
        top.update_idletasks()
        x = (top.winfo_screenwidth() // 2) - (450 // 2)
        y = (top.winfo_screenheight() // 2) - (320 // 2)
        top.geometry(f'450x320+{x}+{y}')
        
        frame = tk.Frame(top, bg="#2C3E50")
        frame.pack(expand=True, fill='both', padx=30, pady=30)
        
        tk.Label(
            frame,
            text="Management Login",
            font=("Arial", 18, "bold"),
            bg="#2C3E50",
            fg="white"
        ).pack(pady=(0, 30))
        
        # Username
        tk.Label(
            frame,
            text="Username:",
            font=("Arial", 11),
            bg="#2C3E50",
            fg="#BDC3C7"
        ).pack(anchor='w', pady=(0, 5))
        
        username_entry = tk.Entry(frame, font=("Arial", 12), width=25)
        username_entry.pack(pady=(0, 15), fill='x')
        username_entry.focus()
        
        # Password
        tk.Label(
            frame,
            text="Password:",
            font=("Arial", 11),
            bg="#2C3E50",
            fg="#BDC3C7"
        ).pack(anchor='w', pady=(0, 5))
        
        password_entry = tk.Entry(frame, font=("Arial", 12), width=25, show="*")
        password_entry.pack(pady=(0, 25), fill='x')
        
        # Management ID Info
        mgt_info = self.system.get_management_info()
        tk.Label(
            frame,
            text=f"Management ID: {mgt_info['management_id']}",
            font=("Arial", 9),
            bg="#2C3E50",
            fg="#95A5A6"
        ).pack(pady=(0, 10))
        
        def submit():
            username = username_entry.get().strip()
            password = password_entry.get().strip()
            
            if not username or not password:
                messagebox.showerror("Error", "Please enter both username and password!")
                return
            
            if self.system.verify_management_login(username, password):
                self.current_user = {
                    "management_id": mgt_info['management_id'],
                    "username": username,
                    "name": "Management"
                }
                top.destroy()
                self.open_main_app()
            else:
                messagebox.showerror("Error", "Invalid username or password!")
                password_entry.delete(0, 'end')
        
        btn = tk.Button(
            frame,
            text="Login",
            font=("Arial", 12, "bold"),
            bg="#8E44AD",
            fg="white",
            activebackground="#9B59B6",
            relief=tk.FLAT,
            padx=30,
            pady=10,
            cursor="hand2",
            command=submit
        )
        btn.pack(pady=10)
        
        # Bind Enter key
        username_entry.bind('<Return>', lambda e: password_entry.focus())
        password_entry.bind('<Return>', lambda e: submit())
    
    def open_main_app(self):
        """Open main application window"""
        self.root.destroy()
        main_root = tk.Tk()
        app = SWMS_GUI(main_root, self.system, self.current_user, self.user_type)
        main_root.mainloop()

# ==================== MAIN APPLICATION ====================
class SWMS_GUI:
    def __init__(self, root, system, current_user, user_type):
        self.root = root
        self.system = system
        self.current_user = current_user
        self.user_type = user_type
        
        # Window Setup
        self.root.title("Smart Waste Management System")
        self.root.geometry("1400x900")
        self.root.state('zoomed' if hasattr(self.root, 'state') else 'normal')
        
        # Color Scheme
        self.bg_color = "#ECF0F1"
        self.sidebar_color = "#34495E"
        self.accent_color = "#3498DB"
        self.success_color = "#27AE60"
        self.warning_color = "#E67E22"
        self.danger_color = "#E74C3C"
        
        self.root.configure(bg=self.bg_color)
        
        # Create UI based on user type
        self.create_ui()
    
    def create_ui(self):
        """Create UI based on user role"""
        # Top Bar
        self.create_topbar()
        
        # Main Container
        main_container = tk.Frame(self.root, bg=self.bg_color)
        main_container.pack(fill='both', expand=True)
        
        # Sidebar (only for Management)
        if self.user_type == "management":
            self.create_sidebar(main_container)
        
        # Content Area
        self.content_frame = tk.Frame(main_container, bg=self.bg_color)
        self.content_frame.pack(side='right', fill='both', expand=True, padx=10, pady=10)
        
        # Create appropriate tabs based on role
        if self.user_type == "management":
            self.create_management_tabs()
        elif self.user_type == "resident":
            self.create_resident_tabs()
        elif self.user_type == "collector":
            self.create_collector_tabs()
    
    def create_topbar(self):
        """Create top navigation bar"""
        topbar = tk.Frame(self.root, bg=self.sidebar_color, height=60)
        topbar.pack(fill='x')
        topbar.pack_propagate(False)
        
        # Title
        if isinstance(self.current_user, dict):
            user_name = self.current_user.get("name", "Management")
        elif hasattr(self.current_user, 'full_name'):
            user_name = self.current_user.full_name
        elif hasattr(self.current_user, 'name'):
            user_name = self.current_user.name
        else:
            user_name = "Management"
        
        title = tk.Label(
            topbar,
            text=f"SWMS - Welcome, {user_name}",
            font=("Arial", 16, "bold"),
            bg=self.sidebar_color,
            fg="white"
        )
        title.pack(side='left', padx=20, pady=15)
        
        # Logout Button (for all users)
        logout_btn = tk.Button(
            topbar,
            text="🚪 Logout",
            font=("Arial", 10, "bold"),
            bg="#E74C3C",
            fg="white",
            activebackground="#C0392B",
            relief=tk.FLAT,
            padx=15,
            pady=5,
            cursor="hand2",
            command=self.logout
        )
        logout_btn.pack(side='right', padx=10, pady=15)
        
        # Role Badge
        role_colors = {
            "resident": "#16A085",
            "collector": "#E67E22",
            "management": "#8E44AD"
        }
        role_text = self.user_type.title()
        role_badge = tk.Label(
            topbar,
            text=role_text,
            font=("Arial", 10, "bold"),
            bg=role_colors.get(self.user_type, "#7F8C8D"),
            fg="white",
            padx=15,
            pady=5
        )
        role_badge.pack(side='right', padx=10, pady=15)
        
        # Save Button (Management only)
        if self.user_type == "management":
            save_btn = tk.Button(
                topbar,
                text="💾 Save Data",
                font=("Arial", 10),
                bg=self.success_color,
                fg="white",
                activebackground="#229954",
                relief=tk.FLAT,
                padx=15,
                pady=5,
                cursor="hand2",
                command=self.save_data
            )
            save_btn.pack(side='right', padx=10, pady=15)
    
    def create_sidebar(self, parent):
        """Create sidebar navigation (Management only)"""
        sidebar = tk.Frame(parent, bg=self.sidebar_color, width=200)
        sidebar.pack(side='left', fill='y', padx=(10, 0), pady=10)
        sidebar.pack_propagate(False)
        
        # Navigation buttons
        nav_items = [
            ("📊 Dashboard", "dashboard"),
            ("🗑️ Bins Locations", "bins_locations"),
            ("⚠️ Incidents", "incidents"),
            ("👥 Customers", "customers"),
            ("💰 Customer Payments", "customer_payments"),
            ("🚛 Collectors", "collectors"),
            ("📍 Routes & Tasks", "tasks")
        ]
        
        for text, tab_name in nav_items:
            btn = tk.Button(
                sidebar,
                text=text,
                font=("Arial", 11),
                bg=self.sidebar_color,
                fg="white",
                activebackground="#2C3E50",
                activeforeground="white",
                relief=tk.FLAT,
                anchor='w',
                padx=20,
                pady=12,
                cursor="hand2",
                command=lambda t=tab_name: self.show_tab(t)
            )
            btn.pack(fill='x', padx=5, pady=2)
    
    def show_tab(self, tab_name):
        """Switch between tabs"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        if tab_name == "dashboard":
            self.create_dashboard_tab()
        elif tab_name == "bins_locations":
            self.create_bins_locations_tab()
        elif tab_name == "incidents":
            self.create_incidents_view_tab()
        elif tab_name == "customers":
            self.create_customers_view_tab()
        elif tab_name == "customer_payments":
            self.create_customer_payments_tab()
        elif tab_name == "collectors":
            self.create_collector_tab()
        elif tab_name == "tasks":
            self.create_task_tab()
    
    def create_management_tabs(self):
        """Create all tabs for management"""
        self.create_dashboard_tab()
    
    def create_resident_tabs(self):
        """Create tabs for resident view"""
        # Resident can only see their own info and report incidents
        self.create_resident_dashboard()
    
    def create_collector_tabs(self):
        """Create tabs for collector view"""
        # Collector can see their assigned tasks
        self.create_collector_dashboard()
    
    # ==================== MANAGEMENT TABS ====================
    def create_dashboard_tab(self):
        """Dashboard with stats and charts"""
        # Clear content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Stats Frame
        stats_frame = tk.Frame(self.content_frame, bg=self.bg_color)
        stats_frame.pack(fill='x', pady=10)
        
        stats = [
            ("Residents", len(self.system.residents), "#3498DB"),
            ("Bins", len(self.system.bins), "#27AE60"),
            ("Tasks", len(self.system.tasks), "#E67E22"),
            ("Revenue", f"${self.system.get_total_revenue():,.2f}", "#8E44AD")
        ]
        
        for i, (label, value, color) in enumerate(stats):
            card = tk.Frame(stats_frame, bg=color, relief=tk.RAISED, bd=2)
            card.pack(side='left', expand=True, fill='both', padx=5)
            
            tk.Label(
                card,
                text=str(value),
                font=("Arial", 24, "bold"),
                bg=color,
                fg="white"
            ).pack(pady=10)
            
            tk.Label(
                card,
                text=label,
                font=("Arial", 12),
                bg=color,
                fg="white"
            ).pack(pady=(0, 10))
        
        # Charts Frame
        chart_frame = tk.Frame(self.content_frame, bg="white", relief=tk.RAISED, bd=2)
        chart_frame.pack(fill='both', expand=True, pady=10)
        
        if HAS_MATPLOTLIB and self.system.incidents:
            statuses = [i.status for i in self.system.incidents]
            counts = {s: statuses.count(s) for s in set(statuses)}
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.pie(counts.values(), labels=counts.keys(), autopct='%1.1f%%', startangle=90)
            ax.set_title("Incident Status Distribution", fontsize=14, fontweight='bold')
            FigureCanvasTkAgg(fig, chart_frame).get_tk_widget().pack(fill='both', expand=True)
        else:
            tk.Label(
                chart_frame,
                text="No data available for charts",
                font=("Arial", 12),
                fg="#7F8C8D"
            ).pack(expand=True)
    
    def create_resident_tab(self):
        """Resident management tab"""
        self.show_tab("residents")
        # Implementation continues below...
    
    # ==================== RESIDENT VIEW ====================
    def create_resident_dashboard(self):
        """Dashboard for resident with Payment and Incident reporting"""
        # Clear content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Welcome Card
        welcome_frame = tk.Frame(self.content_frame, bg="white", relief=tk.RAISED, bd=2)
        welcome_frame.pack(fill='x', pady=10, padx=10)
        
        tk.Label(
            welcome_frame,
            text=f"Welcome, {self.current_user.full_name}!",
            font=("Arial", 18, "bold"),
            bg="white",
            fg="#2C3E50"
        ).pack(pady=15)
        
        tk.Label(
            welcome_frame,
            text=f"Resident ID: {self.current_user.resident_id} | Address: {self.current_user.address}",
            font=("Arial", 11),
            bg="white",
            fg="#7F8C8D"
        ).pack(pady=(0, 15))
        
        # Create Notebook for tabs
        notebook = ttk.Notebook(self.content_frame)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Tab 1: Make Payment
        payment_tab = ttk.Frame(notebook)
        notebook.add(payment_tab, text="💳 Make Payment")
        self.create_resident_payment_tab(payment_tab)
        
        # Tab 2: Report Incident
        incident_tab = ttk.Frame(notebook)
        notebook.add(incident_tab, text="⚠️ Report Incident")
        self.create_resident_incident_tab(incident_tab)
    
    def create_resident_payment_tab(self, parent):
        """Payment tab for resident with Pending Payments"""
        # Pending Payments Section
        pending_frame = tk.LabelFrame(parent, text="⚠️ Pending Payments", font=("Arial", 12, "bold"), bg="white")
        pending_frame.pack(fill='x', padx=20, pady=10)
        
        self.res_pending_tree = ttk.Treeview(pending_frame, columns=("ID", "Amount", "Service", "Due Date"), show='headings', height=5)
        for col in ["ID", "Amount", "Service", "Due Date"]:
            self.res_pending_tree.heading(col, text=col)
            self.res_pending_tree.column(col, width=150)
        self.res_pending_tree.pack(fill='x', padx=10, pady=10)
        
        tk.Button(
            pending_frame,
            text="💳 Pay Selected",
            font=("Arial", 10, "bold"),
            bg=self.success_color,
            fg="white",
            relief=tk.FLAT,
            padx=15,
            pady=5,
            cursor="hand2",
            command=self.resident_pay_pending
        ).pack(pady=5)
        
        # Payment Form (for new payments)
        form_frame = tk.LabelFrame(parent, text="Make New Payment", font=("Arial", 12, "bold"), bg="white")
        form_frame.pack(fill='x', padx=20, pady=10)
        
        input_frame = tk.Frame(form_frame, bg="white")
        input_frame.pack(fill='x', padx=20, pady=20)
        
        tk.Label(input_frame, text="Service Type:", font=("Arial", 11), bg="white").grid(row=0, column=0, padx=10, pady=10, sticky='w')
        self.res_pay_service = ttk.Combobox(input_frame, values=["Collection", "Recycling", "Penalty", "Extra Pickup"], width=25, state="readonly")
        self.res_pay_service.grid(row=0, column=1, padx=10, pady=10, sticky='ew')
        self.res_pay_service.current(0)
        
        tk.Label(input_frame, text="Amount ($):", font=("Arial", 11), bg="white").grid(row=1, column=0, padx=10, pady=10, sticky='w')
        self.res_pay_amount = tk.Entry(input_frame, font=("Arial", 11), width=27)
        self.res_pay_amount.grid(row=1, column=1, padx=10, pady=10, sticky='ew')
        
        input_frame.columnconfigure(1, weight=1)
        
        tk.Button(
            form_frame,
            text="💳 Process Payment",
            font=("Arial", 12, "bold"),
            bg=self.success_color,
            fg="white",
            relief=tk.FLAT,
            padx=20,
            pady=10,
            cursor="hand2",
            command=self.resident_process_payment
        ).pack(pady=15)
        
        # Payment History (Paid only)
        history_frame = tk.LabelFrame(parent, text="Payment History (Paid)", font=("Arial", 12, "bold"), bg="white")
        history_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        self.res_pay_tree = ttk.Treeview(history_frame, columns=("ID", "Amount", "Service", "Date"), show='headings', height=8)
        for col in ["ID", "Amount", "Service", "Date"]:
            self.res_pay_tree.heading(col, text=col)
            self.res_pay_tree.column(col, width=150)
        self.res_pay_tree.pack(fill='both', expand=True, padx=10, pady=10)
        self.refresh_resident_payments()
    
    def resident_pay_pending(self):
        """Pay a pending payment"""
        selection = self.res_pending_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a pending payment to pay")
            return
        
        item = self.res_pending_tree.item(selection[0])
        transaction_id = item['values'][0]
        
        # Find the transaction
        transaction = next((t for t in self.system.transactions if t.transaction_id == transaction_id), None)
        if not transaction:
            messagebox.showerror("Error", "Payment not found")
            return
        
        if transaction.status == "Paid":
            messagebox.showinfo("Info", "This payment is already paid")
            self.refresh_resident_payments()
            return
        
        # Confirm payment
        if messagebox.askyesno("Confirm Payment", f"Pay ${transaction.amount:.2f} for {transaction.service_type}?"):
            transaction.process_payment()
            self.system.save_data()  # Auto-save
            self.refresh_resident_payments()
            messagebox.showinfo("Success", f"Payment {transaction_id} processed successfully!")
    
    def refresh_resident_pending_payments(self):
        """Refresh pending payments list"""
        for item in self.res_pending_tree.get_children():
            self.res_pending_tree.delete(item)
        
        # Get pending payments for current resident
        pending = self.system.get_pending_payments_for_resident(self.current_user.resident_id)
        
        for t in pending:
            due_date = t.payment_date if t.payment_date else "N/A"
            self.res_pending_tree.insert("", "end", values=(t.transaction_id, f"${t.amount:.2f}", t.service_type, due_date))
    
    def resident_process_payment(self):
        """Process payment for resident (new direct payment)"""
        service = self.res_pay_service.get()
        amount_str = self.res_pay_amount.get().strip()
        
        # Validate amount
        is_valid, result = validate_amount(amount_str)
        if not is_valid:
            messagebox.showerror("Validation Error", result)
            return
        
        amount = result
        
        # Generate sequential ID
        tid = self.system.generate_transaction_id()
        # Create as Paid transaction (direct payment)
        transaction = Transaction(tid, self.current_user, amount, service, status="Paid")
        self.system.process_transaction(transaction)
        self.system.save_data()  # Auto-save after payment
        self.refresh_resident_payments()
        self.res_pay_amount.delete(0, 'end')
        messagebox.showinfo("Success", f"Payment of ${amount:.2f} processed successfully!")
    
    def refresh_resident_payments(self):
        """Refresh resident payment history"""
        # Refresh pending payments
        if hasattr(self, 'res_pending_tree'):
            self.refresh_resident_pending_payments()
        
        # Refresh paid payments
        for item in self.res_pay_tree.get_children():
            self.res_pay_tree.delete(item)
        
        # Show only current resident's PAID payments
        resident_payments = [t for t in self.system.transactions 
                            if hasattr(t.payer, 'resident_id') and t.payer.resident_id == self.current_user.resident_id
                            and t.status == "Paid"]
        
        for t in resident_payments:
            self.res_pay_tree.insert("", "end", values=(t.transaction_id, f"${t.amount:.2f}", t.service_type, t.payment_date))
    
    def create_resident_incident_tab(self, parent):
        """Incident reporting tab for resident"""
        # Report Form
        form_frame = tk.LabelFrame(parent, text="Report New Incident", font=("Arial", 12, "bold"), bg="white")
        form_frame.pack(fill='x', padx=20, pady=20)
        
        input_frame = tk.Frame(form_frame, bg="white")
        input_frame.pack(fill='x', padx=20, pady=20)
        
        tk.Label(input_frame, text="Description:", font=("Arial", 11), bg="white").pack(anchor='w', pady=5)
        self.res_inc_desc = tk.Text(input_frame, height=4, width=60, font=("Arial", 10))
        self.res_inc_desc.pack(fill='x', pady=5)
        
        tk.Label(input_frame, text="Location:", font=("Arial", 11), bg="white").pack(anchor='w', pady=5)
        self.res_inc_loc = tk.Entry(input_frame, font=("Arial", 11), width=60)
        self.res_inc_loc.pack(fill='x', pady=5)
        
        tk.Button(
            form_frame,
            text="⚠️ Submit Incident",
            font=("Arial", 12, "bold"),
            bg=self.warning_color,
            fg="white",
            relief=tk.FLAT,
            padx=20,
            pady=10,
            cursor="hand2",
            command=self.resident_submit_incident
        ).pack(pady=15)
        
        # My Incidents
        incidents_frame = tk.LabelFrame(parent, text="My Reported Incidents", font=("Arial", 12, "bold"), bg="white")
        incidents_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        self.res_inc_tree = ttk.Treeview(incidents_frame, columns=("ID", "Description", "Location", "Date", "Status"), show='headings', height=10)
        for col in ["ID", "Description", "Location", "Date", "Status"]:
            self.res_inc_tree.heading(col, text=col)
            self.res_inc_tree.column(col, width=150)
        self.res_inc_tree.pack(fill='both', expand=True, padx=10, pady=10)
        self.refresh_resident_incidents()
    
    def resident_submit_incident(self):
        """Submit incident for resident"""
        desc = self.res_inc_desc.get("1.0", tk.END).strip()
        loc = self.res_inc_loc.get().strip()
        
        # Validate description
        is_valid, error = validate_description(desc)
        if not is_valid:
            messagebox.showerror("Validation Error", error)
            return
        
        # Validate location
        is_valid, error = validate_location(loc)
        if not is_valid:
            messagebox.showerror("Validation Error", error)
            return
        
        # Generate sequential ID
        iid = self.system.generate_incident_id()
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        incident = Incident(iid, desc, date, loc)
        self.system.log_incident(incident)
        self.system.save_data()  # Auto-save after incident report
        self.refresh_resident_incidents()
        self.res_inc_desc.delete("1.0", tk.END)
        self.res_inc_loc.delete(0, 'end')
        messagebox.showinfo("Success", f"Incident {iid} reported successfully!")
    
    def refresh_resident_incidents(self):
        """Refresh resident incidents"""
        for item in self.res_inc_tree.get_children():
            self.res_inc_tree.delete(item)
        
        # Show all incidents (resident can see all)
        for inc in self.system.incidents:
            desc_short = inc.description[:50] + "..." if len(inc.description) > 50 else inc.description
            self.res_inc_tree.insert("", "end", values=(inc.incident_id, desc_short, inc.location, inc.reported_date, inc.status))
    
    def show_report_incident_dialog(self):
        """Show dialog to report incident"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Report Incident")
        dialog.geometry("500x300")
        dialog.configure(bg="white")
        dialog.resizable(False, False)
        
        # Center
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (dialog.winfo_screenheight() // 2) - (300 // 2)
        dialog.geometry(f'500x300+{x}+{y}')
        
        frame = tk.Frame(dialog, bg="white")
        frame.pack(expand=True, fill='both', padx=30, pady=20)
        
        tk.Label(frame, text="Description:", font=("Arial", 11, "bold"), bg="white").pack(anchor='w', pady=(0, 5))
        desc_entry = tk.Text(frame, height=4, width=50, font=("Arial", 10))
        desc_entry.pack(fill='x', pady=(0, 15))
        
        tk.Label(frame, text="Location:", font=("Arial", 11, "bold"), bg="white").pack(anchor='w', pady=(0, 5))
        loc_entry = tk.Entry(frame, font=("Arial", 10), width=50)
        loc_entry.pack(fill='x', pady=(0, 20))
        
        def submit():
            desc = desc_entry.get("1.0", tk.END).strip()
            loc = loc_entry.get().strip()
            
            # Validate description
            is_valid, error = validate_description(desc)
            if not is_valid:
                messagebox.showerror("Validation Error", error)
                return
            
            # Validate location
            is_valid, error = validate_location(loc)
            if not is_valid:
                messagebox.showerror("Validation Error", error)
                return
            
            # Generate sequential ID
            iid = self.system.generate_incident_id()
            date = datetime.datetime.now().strftime("%Y-%m-%d")
            incident = Incident(iid, desc, date, loc)
            self.system.log_incident(incident)
            self.system.save_data()  # Auto-save after incident report
            messagebox.showinfo("Success", f"Incident {iid} reported successfully!")
            dialog.destroy()
        
        tk.Button(
            frame,
            text="Submit",
            font=("Arial", 11, "bold"),
            bg=self.warning_color,
            fg="white",
            relief=tk.FLAT,
            padx=20,
            pady=8,
            command=submit
        ).pack()
    
    # ==================== COLLECTOR VIEW ====================
    def create_collector_dashboard(self):
        """Dashboard for collector with Incident reporting and Assigned Routes/Tasks"""
        # Clear content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Welcome Card
        welcome_frame = tk.Frame(self.content_frame, bg="white", relief=tk.RAISED, bd=2)
        welcome_frame.pack(fill='x', pady=10, padx=10)
        
        tk.Label(
            welcome_frame,
            text=f"Welcome, {self.current_user.name}!",
            font=("Arial", 18, "bold"),
            bg="white",
            fg="#2C3E50"
        ).pack(pady=15)
        
        tk.Label(
            welcome_frame,
            text=f"Collector ID: {self.current_user.collector_id} | Vehicle: {self.current_user.vehicle_id}",
            font=("Arial", 11),
            bg="white",
            fg="#7F8C8D"
        ).pack(pady=(0, 15))
        
        # Create Notebook for tabs
        notebook = ttk.Notebook(self.content_frame)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Tab 1: Assigned Routes & Tasks
        tasks_tab = ttk.Frame(notebook)
        notebook.add(tasks_tab, text="📍 Routes & Tasks")
        self.create_collector_tasks_tab(tasks_tab)
        
        # Tab 2: Report Incident
        incident_tab = ttk.Frame(notebook)
        notebook.add(incident_tab, text="⚠️ Report Incident")
        self.create_collector_incident_tab(incident_tab)
    
    def create_collector_tasks_tab(self, parent):
        """Routes and Tasks tab for collector"""
        # Assigned Routes
        routes_frame = tk.LabelFrame(parent, text="My Assigned Routes", font=("Arial", 12, "bold"), bg="white")
        routes_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        self.col_route_tree = ttk.Treeview(routes_frame, columns=("ID", "Zone", "Stops", "Distance", "Duration"), show='headings', height=8)
        for col in ["ID", "Zone", "Stops", "Distance", "Duration"]:
            self.col_route_tree.heading(col, text=col)
            self.col_route_tree.column(col, width=120)
        self.col_route_tree.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Assigned Tasks
        tasks_frame = tk.LabelFrame(parent, text="My Assigned Tasks", font=("Arial", 12, "bold"), bg="white")
        tasks_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        self.col_task_tree = ttk.Treeview(tasks_frame, columns=("ID", "Description", "Route", "Date", "Status"), show='headings', height=8)
        for col in ["ID", "Description", "Route", "Date", "Status"]:
            self.col_task_tree.heading(col, text=col)
            self.col_task_tree.column(col, width=150)
        self.col_task_tree.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.refresh_collector_tasks()
    
    def refresh_collector_tasks(self):
        """Refresh collector routes and tasks"""
        # Clear routes
        for item in self.col_route_tree.get_children():
            self.col_route_tree.delete(item)
        
        # Get routes from assigned tasks
        my_tasks = [t for t in self.system.tasks if t.assigned_collector == self.current_user]
        assigned_routes = {}
        for task in my_tasks:
            if task.route and task.route.route_id not in assigned_routes:
                assigned_routes[task.route.route_id] = task.route
        
        for route in assigned_routes.values():
            stops_count = len(route.stop_sequence)
            self.col_route_tree.insert("", "end", values=(
                route.route_id, 
                route.zone_name, 
                stops_count,
                f"{route.estimated_distance:.1f} km",
                f"{route.estimated_duration:.0f} mins"
            ))
        
        # Clear tasks
        for item in self.col_task_tree.get_children():
            self.col_task_tree.delete(item)
        
        # Show assigned tasks
        for t in my_tasks:
            route_name = t.route.zone_name if t.route else "N/A"
            self.col_task_tree.insert("", "end", values=(
                t.task_id, 
                t.description, 
                route_name, 
                t.target_date, 
                t.status
            ))
    
    def create_collector_incident_tab(self, parent):
        """Incident reporting tab for collector"""
        # Report Form
        form_frame = tk.LabelFrame(parent, text="Report New Incident", font=("Arial", 12, "bold"), bg="white")
        form_frame.pack(fill='x', padx=20, pady=20)
        
        input_frame = tk.Frame(form_frame, bg="white")
        input_frame.pack(fill='x', padx=20, pady=20)
        
        tk.Label(input_frame, text="Description:", font=("Arial", 11), bg="white").pack(anchor='w', pady=5)
        self.col_inc_desc = tk.Text(input_frame, height=4, width=60, font=("Arial", 10))
        self.col_inc_desc.pack(fill='x', pady=5)
        
        tk.Label(input_frame, text="Location:", font=("Arial", 11), bg="white").pack(anchor='w', pady=5)
        self.col_inc_loc = tk.Entry(input_frame, font=("Arial", 11), width=60)
        self.col_inc_loc.pack(fill='x', pady=5)
        
        tk.Button(
            form_frame,
            text="⚠️ Submit Incident",
            font=("Arial", 12, "bold"),
            bg=self.warning_color,
            fg="white",
            relief=tk.FLAT,
            padx=20,
            pady=10,
            cursor="hand2",
            command=self.collector_submit_incident
        ).pack(pady=15)
        
        # Reported Incidents
        incidents_frame = tk.LabelFrame(parent, text="Reported Incidents", font=("Arial", 12, "bold"), bg="white")
        incidents_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        self.col_inc_tree = ttk.Treeview(incidents_frame, columns=("ID", "Description", "Location", "Date", "Status"), show='headings', height=10)
        for col in ["ID", "Description", "Location", "Date", "Status"]:
            self.col_inc_tree.heading(col, text=col)
            self.col_inc_tree.column(col, width=150)
        self.col_inc_tree.pack(fill='both', expand=True, padx=10, pady=10)
        self.refresh_collector_incidents()
    
    def collector_submit_incident(self):
        """Submit incident for collector"""
        desc = self.col_inc_desc.get("1.0", tk.END).strip()
        loc = self.col_inc_loc.get().strip()
        
        # Validate description
        is_valid, error = validate_description(desc)
        if not is_valid:
            messagebox.showerror("Validation Error", error)
            return
        
        # Validate location
        is_valid, error = validate_location(loc)
        if not is_valid:
            messagebox.showerror("Validation Error", error)
            return
        
        # Generate sequential ID
        iid = self.system.generate_incident_id()
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        incident = Incident(iid, desc, date, loc)
        self.system.log_incident(incident)
        self.system.save_data()  # Auto-save after incident report
        self.refresh_collector_incidents()
        self.col_inc_desc.delete("1.0", tk.END)
        self.col_inc_loc.delete(0, 'end')
        messagebox.showinfo("Success", f"Incident {iid} reported successfully!")
    
    def refresh_collector_incidents(self):
        """Refresh collector incidents"""
        for item in self.col_inc_tree.get_children():
            self.col_inc_tree.delete(item)
        
        # Show all incidents
        for inc in self.system.incidents:
            desc_short = inc.description[:50] + "..." if len(inc.description) > 50 else inc.description
            self.col_inc_tree.insert("", "end", values=(inc.incident_id, desc_short, inc.location, inc.reported_date, inc.status))
    
    # ==================== MANAGEMENT TABS (Full Implementation) ====================
    def create_resident_tab(self):
        """Resident management tab"""
        # Clear content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Don't call show_tab here, just implement directly
        
        # Form Frame
        form_frame = tk.LabelFrame(self.content_frame, text="Register New Resident", font=("Arial", 12, "bold"), bg="white")
        form_frame.pack(fill='x', padx=10, pady=10)
        
        input_frame = tk.Frame(form_frame, bg="white")
        input_frame.pack(fill='x', padx=15, pady=15)
        
        tk.Label(input_frame, text="Name:", font=("Arial", 10), bg="white").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.ent_res_name = tk.Entry(input_frame, font=("Arial", 10), width=25)
        self.ent_res_name.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(input_frame, text="Address:", font=("Arial", 10), bg="white").grid(row=0, column=2, padx=5, pady=5, sticky='w')
        self.ent_res_addr = tk.Entry(input_frame, font=("Arial", 10), width=25)
        self.ent_res_addr.grid(row=0, column=3, padx=5, pady=5)
        
        tk.Button(
            input_frame,
            text="Add Resident",
            font=("Arial", 10, "bold"),
            bg=self.success_color,
            fg="white",
            relief=tk.FLAT,
            padx=15,
            pady=5,
            cursor="hand2",
            command=self.add_resident
        ).grid(row=0, column=4, padx=10, pady=5)
        
        # List Frame
        list_frame = tk.LabelFrame(self.content_frame, text="All Residents", font=("Arial", 12, "bold"), bg="white")
        list_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.res_tree = ttk.Treeview(list_frame, columns=("ID", "Name", "Address"), show='headings', height=15)
        for col in ["ID", "Name", "Address"]:
            self.res_tree.heading(col, text=col)
            self.res_tree.column(col, width=200)
        self.res_tree.pack(fill='both', expand=True, padx=10, pady=10)
        self.refresh_residents()
    
    def add_resident(self):
        """Add new resident"""
        name = self.ent_res_name.get().strip()
        addr = self.ent_res_addr.get().strip()
        
        # Validate name
        is_valid, error = validate_name(name)
        if not is_valid:
            messagebox.showerror("Validation Error", error)
            return
        
        # Validate address
        is_valid, error = validate_address(addr)
        if not is_valid:
            messagebox.showerror("Validation Error", error)
            return
        
        # Generate sequential ID
        rid = self.system.generate_resident_id()
        self.system.register_resident(Resident(rid, name, addr))
        self.refresh_residents()
        self.update_combos()
        self.ent_res_name.delete(0, 'end')
        self.ent_res_addr.delete(0, 'end')
        messagebox.showinfo("Success", f"Resident {rid} registered successfully!")
    
    def refresh_residents(self):
        """Refresh residents list"""
        for item in self.res_tree.get_children():
            self.res_tree.delete(item)
        for r in self.system.residents:
            self.res_tree.insert("", "end", values=(r.resident_id, r.full_name, r.address))
    
    def create_bin_tab(self):
        """Bin management tab"""
        # Clear content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Form Frame
        form_frame = tk.LabelFrame(self.content_frame, text="Register New Bin", font=("Arial", 12, "bold"), bg="white")
        form_frame.pack(fill='x', padx=10, pady=10)
        
        input_frame = tk.Frame(form_frame, bg="white")
        input_frame.pack(fill='x', padx=15, pady=15)
        
        tk.Label(input_frame, text="Type:", font=("Arial", 10), bg="white").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.cmb_bin_type = ttk.Combobox(input_frame, values=["General", "Recycle", "Green"], width=15, state="readonly")
        self.cmb_bin_type.grid(row=0, column=1, padx=5, pady=5)
        self.cmb_bin_type.current(0)
        
        tk.Label(input_frame, text="Capacity (L):", font=("Arial", 10), bg="white").grid(row=0, column=2, padx=5, pady=5, sticky='w')
        self.ent_bin_cap = tk.Entry(input_frame, font=("Arial", 10), width=15)
        self.ent_bin_cap.grid(row=0, column=3, padx=5, pady=5)
        
        tk.Label(input_frame, text="Location:", font=("Arial", 10), bg="white").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.ent_bin_loc = tk.Entry(input_frame, font=("Arial", 10), width=25)
        self.ent_bin_loc.grid(row=1, column=1, padx=5, pady=5, columnspan=2)
        
        tk.Label(input_frame, text="Owner:", font=("Arial", 10), bg="white").grid(row=1, column=3, padx=5, pady=5, sticky='w')
        self.cmb_bin_res = ttk.Combobox(input_frame, width=20, state="readonly")
        self.cmb_bin_res.grid(row=1, column=4, padx=5, pady=5)
        self.update_combos()
        
        tk.Button(
            input_frame,
            text="Add Bin",
            font=("Arial", 10, "bold"),
            bg=self.success_color,
            fg="white",
            relief=tk.FLAT,
            padx=15,
            pady=5,
            cursor="hand2",
            command=self.add_bin
        ).grid(row=2, column=2, columnspan=2, padx=10, pady=10)
        
        # List Frame
        list_frame = tk.LabelFrame(self.content_frame, text="All Bins", font=("Arial", 12, "bold"), bg="white")
        list_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.bin_tree = ttk.Treeview(list_frame, columns=("ID", "Type", "Capacity", "Location", "Owner", "Status"), show='headings', height=15)
        for col in ["ID", "Type", "Capacity", "Location", "Owner", "Status"]:
            self.bin_tree.heading(col, text=col)
            self.bin_tree.column(col, width=120)
        self.bin_tree.pack(fill='both', expand=True, padx=10, pady=10)
        self.refresh_bins()
    
    def add_bin(self):
        """Add new bin"""
        btype = self.cmb_bin_type.get()
        cap = self.ent_bin_cap.get().strip()
        loc = self.ent_bin_loc.get().strip()
        res_str = self.cmb_bin_res.get()
        
        # Validate capacity
        is_valid, result = validate_capacity(cap)
        if not is_valid:
            messagebox.showerror("Validation Error", result)
            return
        capacity = result
        
        # Validate location
        is_valid, error = validate_location(loc)
        if not is_valid:
            messagebox.showerror("Validation Error", error)
            return
        
        # Generate sequential ID
        bid = self.system.generate_bin_id()
        bin_obj = Bin(bid, btype, capacity, loc)
        
        if res_str:
            rid = res_str.split(" - ")[0]
            resident = next((r for r in self.system.residents if r.resident_id == rid), None)
            if resident:
                bin_obj.link_resident(resident)
        
        self.system.register_bin(bin_obj)
        self.refresh_bins()
        self.update_combos()
        self.ent_bin_cap.delete(0, 'end')
        self.ent_bin_loc.delete(0, 'end')
        messagebox.showinfo("Success", f"Bin {bid} registered successfully!")
    
    def refresh_bins(self):
        """Refresh bins list"""
        for item in self.bin_tree.get_children():
            self.bin_tree.delete(item)
        for b in self.system.bins:
            owner = b.assigned_resident.full_name if b.assigned_resident else "Unassigned"
            self.bin_tree.insert("", "end", values=(b.bin_id, b.bin_type, b.capacity, b.location, owner, b.status))
    
    def create_collector_tab(self):
        """Collector management tab"""
        # Clear content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Form Frame
        form_frame = tk.LabelFrame(self.content_frame, text="Add New Collector", font=("Arial", 12, "bold"), bg="white")
        form_frame.pack(fill='x', padx=10, pady=10)
        
        input_frame = tk.Frame(form_frame, bg="white")
        input_frame.pack(fill='x', padx=15, pady=15)
        
        tk.Label(input_frame, text="Name:", font=("Arial", 10), bg="white").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.ent_col_name = tk.Entry(input_frame, font=("Arial", 10), width=25)
        self.ent_col_name.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(input_frame, text="Vehicle ID:", font=("Arial", 10), bg="white").grid(row=0, column=2, padx=5, pady=5, sticky='w')
        self.ent_col_veh = tk.Entry(input_frame, font=("Arial", 10), width=25)
        self.ent_col_veh.grid(row=0, column=3, padx=5, pady=5)
        
        tk.Button(
            input_frame,
            text="Add Collector",
            font=("Arial", 10, "bold"),
            bg=self.success_color,
            fg="white",
            relief=tk.FLAT,
            padx=15,
            pady=5,
            cursor="hand2",
            command=self.add_collector
        ).grid(row=0, column=4, padx=10, pady=5)
        
        # Action Buttons
        btn_frame_col = tk.Frame(self.content_frame, bg=self.bg_color)
        btn_frame_col.pack(fill='x', padx=10, pady=5)
        
        tk.Button(
            btn_frame_col,
            text="🗑️ Delete Selected Collector",
            font=("Arial", 10, "bold"),
            bg=self.danger_color,
            fg="white",
            relief=tk.FLAT,
            padx=15,
            pady=5,
            cursor="hand2",
            command=self.delete_selected_collector
        ).pack(side='left', padx=5)
        
        # List Frame
        list_frame = tk.LabelFrame(self.content_frame, text="All Collectors", font=("Arial", 12, "bold"), bg="white")
        list_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.col_tree = ttk.Treeview(list_frame, columns=("ID", "Name", "Vehicle"), show='headings', height=15)
        for col in ["ID", "Name", "Vehicle"]:
            self.col_tree.heading(col, text=col)
            self.col_tree.column(col, width=200)
        self.col_tree.pack(fill='both', expand=True, padx=10, pady=10)
        self.refresh_collectors()
    
    def delete_selected_collector(self):
        """Delete selected collector"""
        selection = self.col_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a collector to delete")
            return
        
        item = self.col_tree.item(selection[0])
        collector_id = item['values'][0]
        
        # Check if collector has tasks
        collector = next((c for c in self.system.collectors if c.collector_id == collector_id), None)
        if collector and collector.assigned_tasks:
            if not messagebox.askyesno("Warning", f"Collector {collector_id} has {len(collector.assigned_tasks)} task(s) assigned. Delete anyway?\nTasks will be unlinked."):
                return
        
        # Confirm deletion
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete collector {collector_id}?"):
            if self.system.delete_collector(collector_id):
                self.refresh_collectors()
                self.update_combos()
                messagebox.showinfo("Success", f"Collector {collector_id} deleted successfully!")
            else:
                messagebox.showerror("Error", "Collector not found")
    
    def add_collector(self):
        """Add new collector"""
        name = self.ent_col_name.get().strip()
        veh = self.ent_col_veh.get().strip()
        
        # Validate name
        is_valid, error = validate_name(name)
        if not is_valid:
            messagebox.showerror("Validation Error", error)
            return
        
        # Vehicle ID is optional but if provided, should be valid
        if veh and len(veh.strip()) > 50:
            messagebox.showerror("Validation Error", "Vehicle ID is too long (max 50 characters)")
            return
        
        # Generate sequential ID
        cid = self.system.generate_collector_id()
        self.system.add_collector(Collector(cid, name, veh))
        self.refresh_collectors()
        self.update_combos()
        self.ent_col_name.delete(0, 'end')
        self.ent_col_veh.delete(0, 'end')
        messagebox.showinfo("Success", f"Collector {cid} added successfully!")
    
    def refresh_collectors(self):
        """Refresh collectors list"""
        for item in self.col_tree.get_children():
            self.col_tree.delete(item)
        for c in self.system.collectors:
            self.col_tree.insert("", "end", values=(c.collector_id, c.name, c.vehicle_id))
    
    def create_task_tab(self):
        """Tasks and routes tab"""
        # Clear content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Two column layout
        main_frame = tk.Frame(self.content_frame, bg=self.bg_color)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Left: Routes
        route_frame = tk.LabelFrame(main_frame, text="Routes", font=("Arial", 12, "bold"), bg="white")
        route_frame.pack(side='left', fill='both', expand=True, padx=5)
        
        route_form = tk.Frame(route_frame, bg="white")
        route_form.pack(fill='x', padx=10, pady=10)
        
        tk.Label(route_form, text="Zone Name:", font=("Arial", 10), bg="white").pack(anchor='w', pady=5)
        self.ent_route_zone = tk.Entry(route_form, font=("Arial", 10), width=30)
        self.ent_route_zone.pack(fill='x', pady=5)
        
        tk.Button(
            route_form,
            text="Create Route",
            font=("Arial", 10, "bold"),
            bg=self.success_color,
            fg="white",
            relief=tk.FLAT,
            padx=15,
            pady=5,
            cursor="hand2",
            command=self.add_route
        ).pack(pady=10)
        
        # Delete Route Button
        btn_frame_route = tk.Frame(route_frame, bg="white")
        btn_frame_route.pack(fill='x', padx=10, pady=5)
        
        tk.Button(
            btn_frame_route,
            text="🗑️ Delete Selected Route",
            font=("Arial", 9, "bold"),
            bg=self.danger_color,
            fg="white",
            relief=tk.FLAT,
            padx=10,
            pady=3,
            cursor="hand2",
            command=self.delete_selected_route
        ).pack(side='left', padx=5)
        
        self.route_list = tk.Listbox(route_frame, font=("Arial", 10), height=15)
        self.route_list.pack(fill='both', expand=True, padx=10, pady=10)
        self.refresh_routes()
        
        # Right: Tasks
        task_frame = tk.LabelFrame(main_frame, text="Schedule Task", font=("Arial", 12, "bold"), bg="white")
        task_frame.pack(side='right', fill='both', expand=True, padx=5)
        
        task_form = tk.Frame(task_frame, bg="white")
        task_form.pack(fill='x', padx=10, pady=10)
        
        tk.Label(task_form, text="Description:", font=("Arial", 10), bg="white").pack(anchor='w', pady=5)
        self.ent_task_desc = tk.Entry(task_form, font=("Arial", 10), width=30)
        self.ent_task_desc.pack(fill='x', pady=5)
        
        tk.Label(task_form, text="Route:", font=("Arial", 10), bg="white").pack(anchor='w', pady=5)
        self.cmb_task_route = ttk.Combobox(task_form, width=27, state="readonly")
        self.cmb_task_route.pack(fill='x', pady=5)
        
        tk.Label(task_form, text="Collector:", font=("Arial", 10), bg="white").pack(anchor='w', pady=5)
        self.cmb_task_col = ttk.Combobox(task_form, width=27, state="readonly")
        self.cmb_task_col.pack(fill='x', pady=5)
        
        tk.Button(
            task_form,
            text="Schedule Task",
            font=("Arial", 10, "bold"),
            bg=self.success_color,
            fg="white",
            relief=tk.FLAT,
            padx=15,
            pady=5,
            cursor="hand2",
            command=self.add_task
        ).pack(pady=10)
        
        # Delete Task Button
        btn_frame_task = tk.Frame(task_frame, bg="white")
        btn_frame_task.pack(fill='x', padx=10, pady=5)
        
        tk.Button(
            btn_frame_task,
            text="🗑️ Delete Selected Task",
            font=("Arial", 9, "bold"),
            bg=self.danger_color,
            fg="white",
            relief=tk.FLAT,
            padx=10,
            pady=3,
            cursor="hand2",
            command=self.delete_selected_task
        ).pack(side='left', padx=5)
        
        self.task_tree = ttk.Treeview(task_frame, columns=("ID", "Desc", "Route", "Collector", "Status"), show='headings', height=10)
        for col in ["ID", "Desc", "Route", "Collector", "Status"]:
            self.task_tree.heading(col, text=col)
            self.task_tree.column(col, width=120)
        self.task_tree.pack(fill='both', expand=True, padx=10, pady=10)
        self.refresh_tasks()
        self.update_combos()
    
    def delete_selected_route(self):
        """Delete selected route"""
        selection = self.route_list.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a route to delete")
            return
        
        route_str = self.route_list.get(selection[0])
        route_id = route_str.split(" - ")[0]
        
        # Check if route has tasks
        route = next((r for r in self.system.routes if r.route_id == route_id), None)
        if route:
            tasks_count = len([t for t in self.system.tasks if t.route == route])
            if tasks_count > 0:
                if not messagebox.askyesno("Warning", f"Route {route_id} has {tasks_count} task(s) assigned. Delete anyway?\nTasks will be unlinked."):
                    return
        
        # Confirm deletion
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete route {route_id}?"):
            if self.system.delete_route(route_id):
                self.refresh_routes()
                self.update_combos()
                messagebox.showinfo("Success", f"Route {route_id} deleted successfully!")
            else:
                messagebox.showerror("Error", "Route not found")
    
    def delete_selected_task(self):
        """Delete selected task"""
        selection = self.task_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a task to delete")
            return
        
        item = self.task_tree.item(selection[0])
        task_id = item['values'][0]
        
        # Confirm deletion
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete task {task_id}?"):
            if self.system.delete_task(task_id):
                self.refresh_tasks()
                messagebox.showinfo("Success", f"Task {task_id} deleted successfully!")
            else:
                messagebox.showerror("Error", "Task not found")
    
    def add_route(self):
        """Add new route"""
        zone = self.ent_route_zone.get().strip()
        
        # Validate zone name
        if not zone or not zone.strip():
            messagebox.showerror("Validation Error", "Zone name cannot be empty")
            return
        
        zone = zone.strip()
        if len(zone) < 2:
            messagebox.showerror("Validation Error", "Zone name must be at least 2 characters long")
            return
        
        if len(zone) > 50:
            messagebox.showerror("Validation Error", "Zone name is too long (max 50 characters)")
            return
        
        # Generate sequential ID
        rid = self.system.generate_route_id()
        r = Route(rid, zone)
        r.add_stop("Simulated Stop 1")
        r.compute_estimates()
        self.system.create_route(r)
        self.refresh_routes()
        self.update_combos()
        self.ent_route_zone.delete(0, 'end')
        messagebox.showinfo("Success", f"Route {rid} created!")
    
    def add_task(self):
        """Add new task"""
        desc = self.ent_task_desc.get().strip()
        r_str = self.cmb_task_route.get()
        c_str = self.cmb_task_col.get()
        
        # Validate description
        is_valid, error = validate_description(desc)
        if not is_valid:
            messagebox.showerror("Validation Error", error)
            return
        
        if not r_str or not c_str:
            messagebox.showerror("Validation Error", "Please select both route and collector")
            return
        
        # Generate sequential ID
        tid = self.system.generate_task_id()
        rid = r_str.split(" - ")[0]
        route = next((r for r in self.system.routes if r.route_id == rid), None)
        cid = c_str.split(" - ")[0]
        collector = next((c for c in self.system.collectors if c.collector_id == cid), None)
        
        if route and collector:
            date = datetime.datetime.now().strftime("%Y-%m-%d")
            task = WasteCollectionTask(tid, desc, date, route)
            task.assign_to_collector(collector)
            self.system.schedule_task(task)
            self.refresh_tasks()
            self.ent_task_desc.delete(0, 'end')
            messagebox.showinfo("Success", f"Task {tid} scheduled!")
        else:
            messagebox.showerror("Error", "Invalid route or collector")
    
    def refresh_routes(self):
        """Refresh routes list"""
        self.route_list.delete(0, 'end')
        for r in self.system.routes:
            self.route_list.insert('end', f"{r.route_id} - {r.zone_name}")
    
    def refresh_tasks(self):
        """Refresh tasks list"""
        for item in self.task_tree.get_children():
            self.task_tree.delete(item)
        for t in self.system.tasks:
            c_name = t.assigned_collector.name if t.assigned_collector else "None"
            r_name = t.route.zone_name if t.route else "None"
            self.task_tree.insert("", "end", values=(t.task_id, t.description, r_name, c_name, t.status))
    
    def create_payment_tab(self):
        """Payment management tab"""
        # Clear content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Form Frame
        form_frame = tk.LabelFrame(self.content_frame, text="Process Payment", font=("Arial", 12, "bold"), bg="white")
        form_frame.pack(fill='x', padx=10, pady=10)
        
        input_frame = tk.Frame(form_frame, bg="white")
        input_frame.pack(fill='x', padx=15, pady=15)
        
        tk.Label(input_frame, text="Payer (Resident):", font=("Arial", 10), bg="white").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.cmb_pay_res = ttk.Combobox(input_frame, width=25, state="readonly")
        self.cmb_pay_res.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(input_frame, text="Amount ($):", font=("Arial", 10), bg="white").grid(row=0, column=2, padx=5, pady=5, sticky='w')
        self.ent_pay_amt = tk.Entry(input_frame, font=("Arial", 10), width=15)
        self.ent_pay_amt.grid(row=0, column=3, padx=5, pady=5)
        
        tk.Label(input_frame, text="Service Type:", font=("Arial", 10), bg="white").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.cmb_pay_srv = ttk.Combobox(input_frame, values=["Collection", "Recycling", "Penalty"], width=25, state="readonly")
        self.cmb_pay_srv.grid(row=1, column=1, padx=5, pady=5)
        self.cmb_pay_srv.current(0)
        
        tk.Button(
            input_frame,
            text="Process Payment",
            font=("Arial", 10, "bold"),
            bg=self.success_color,
            fg="white",
            relief=tk.FLAT,
            padx=15,
            pady=5,
            cursor="hand2",
            command=self.process_payment
        ).grid(row=1, column=2, columnspan=2, padx=10, pady=5)
        
        # List Frame
        list_frame = tk.LabelFrame(self.content_frame, text="All Transactions", font=("Arial", 12, "bold"), bg="white")
        list_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.pay_tree = ttk.Treeview(list_frame, columns=("ID", "Payer", "Amount", "Service", "Date"), show='headings', height=15)
        for col in ["ID", "Payer", "Amount", "Service", "Date"]:
            self.pay_tree.heading(col, text=col)
            self.pay_tree.column(col, width=150)
        self.pay_tree.pack(fill='both', expand=True, padx=10, pady=10)
        self.refresh_payments()
        self.update_combos()
    
    def process_payment(self):
        """Process payment"""
        res_str = self.cmb_pay_res.get()
        amt = self.ent_pay_amt.get().strip()
        srv = self.cmb_pay_srv.get()
        
        if not res_str:
            messagebox.showerror("Validation Error", "Please select a resident")
            return
        
        # Validate amount
        is_valid, result = validate_amount(amt)
        if not is_valid:
            messagebox.showerror("Validation Error", result)
            return
        
        val = result
        
        # Generate sequential ID
        tid = self.system.generate_transaction_id()
        rid = res_str.split(" - ")[0]
        resident = next((r for r in self.system.residents if r.resident_id == rid), None)
        
        if resident:
            t = Transaction(tid, resident, val, srv)
            self.system.process_transaction(t)
            self.refresh_payments()
            self.ent_pay_amt.delete(0, 'end')
            messagebox.showinfo("Success", f"Payment of ${val:.2f} processed!")
        else:
            messagebox.showerror("Error", "Resident not found")
    
    def refresh_payments(self):
        """Refresh payments list"""
        for item in self.pay_tree.get_children():
            self.pay_tree.delete(item)
        for t in self.system.transactions:
            p_name = t.payer.full_name if hasattr(t.payer, 'full_name') else str(t.payer)
            self.pay_tree.insert("", "end", values=(t.transaction_id, p_name, f"${t.amount:.2f}", t.service_type, t.payment_date))
    
    def create_incident_tab(self):
        """Incident management tab"""
        # Clear content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Form Frame
        form_frame = tk.LabelFrame(self.content_frame, text="Report New Incident", font=("Arial", 12, "bold"), bg="white")
        form_frame.pack(fill='x', padx=10, pady=10)
        
        input_frame = tk.Frame(form_frame, bg="white")
        input_frame.pack(fill='x', padx=15, pady=15)
        
        tk.Label(input_frame, text="Description:", font=("Arial", 10), bg="white").pack(anchor='w', pady=5)
        self.ent_inc_desc = tk.Text(input_frame, height=3, width=60, font=("Arial", 10))
        self.ent_inc_desc.pack(fill='x', pady=5)
        
        tk.Label(input_frame, text="Location:", font=("Arial", 10), bg="white").pack(anchor='w', pady=5)
        self.ent_inc_loc = tk.Entry(input_frame, font=("Arial", 10), width=60)
        self.ent_inc_loc.pack(fill='x', pady=5)
        
        tk.Button(
            input_frame,
            text="Log Incident",
            font=("Arial", 10, "bold"),
            bg=self.warning_color,
            fg="white",
            relief=tk.FLAT,
            padx=15,
            pady=5,
            cursor="hand2",
            command=self.add_incident
        ).pack(pady=10)
        
        # List Frame
        list_frame = tk.LabelFrame(self.content_frame, text="All Incidents", font=("Arial", 12, "bold"), bg="white")
        list_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.inc_tree = ttk.Treeview(list_frame, columns=("ID", "Description", "Location", "Date", "Status"), show='headings', height=15)
        for col in ["ID", "Description", "Location", "Date", "Status"]:
            self.inc_tree.heading(col, text=col)
            self.inc_tree.column(col, width=150)
        self.inc_tree.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Add resolve button
        btn_frame = tk.Frame(list_frame, bg="white")
        btn_frame.pack(fill='x', padx=10, pady=5)
        tk.Button(
            btn_frame,
            text="Resolve Selected",
            font=("Arial", 10, "bold"),
            bg=self.success_color,
            fg="white",
            relief=tk.FLAT,
            padx=15,
            pady=5,
            cursor="hand2",
            command=self.resolve_incident
        ).pack(side='left')
        
        self.refresh_incidents()
    
    def add_incident(self):
        """Add new incident"""
        desc = self.ent_inc_desc.get("1.0", tk.END).strip()
        loc = self.ent_inc_loc.get().strip()
        
        # Validate description
        is_valid, error = validate_description(desc)
        if not is_valid:
            messagebox.showerror("Validation Error", error)
            return
        
        # Validate location
        is_valid, error = validate_location(loc)
        if not is_valid:
            messagebox.showerror("Validation Error", error)
            return
        
        # Generate sequential ID
        iid = self.system.generate_incident_id()
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        incident = Incident(iid, desc, date, loc)
        self.system.log_incident(incident)
        self.refresh_incidents()
        self.ent_inc_desc.delete("1.0", tk.END)
        self.ent_inc_loc.delete(0, 'end')
        messagebox.showinfo("Success", f"Incident {iid} logged!")
    
    def resolve_incident(self):
        """Resolve selected incident"""
        selection = self.inc_tree.selection()
        if selection:
            item = self.inc_tree.item(selection[0])
            inc_id = item['values'][0]
            incident = next((i for i in self.system.incidents if i.incident_id == inc_id), None)
            if incident:
                incident.resolve()
                self.refresh_incidents()
                messagebox.showinfo("Success", f"Incident {inc_id} resolved!")
        else:
            messagebox.showwarning("Warning", "Please select an incident")
    
    def refresh_incidents(self):
        """Refresh incidents list"""
        for item in self.inc_tree.get_children():
            self.inc_tree.delete(item)
        for inc in self.system.incidents:
            self.inc_tree.insert("", "end", values=(inc.incident_id, inc.description[:50], inc.location, inc.reported_date, inc.status))
    
    def update_combos(self):
        """Update dropdown menus"""
        res_list = [f"{r.resident_id} - {r.full_name}" for r in self.system.residents]
        route_list = [f"{r.route_id} - {r.zone_name}" for r in self.system.routes]
        col_list = [f"{c.collector_id} - {c.name}" for c in self.system.collectors]
        
        if hasattr(self, 'cmb_bin_res'):
            self.cmb_bin_res['values'] = res_list
        if hasattr(self, 'cmb_pay_res'):
            self.cmb_pay_res['values'] = res_list
        if hasattr(self, 'cmb_task_route'):
            self.cmb_task_route['values'] = route_list
        if hasattr(self, 'cmb_task_col'):
            self.cmb_task_col['values'] = col_list
    
    # ==================== NEW MANAGEMENT TABS ====================
    def create_bins_locations_tab(self):
        """Show all bins with their locations"""
        # Clear content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Title
        title_frame = tk.Frame(self.content_frame, bg="white", relief=tk.RAISED, bd=2)
        title_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(
            title_frame,
            text="🗑️ Bins Locations",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#2C3E50"
        ).pack(pady=15)
        
        # Action Buttons
        btn_frame = tk.Frame(self.content_frame, bg=self.bg_color)
        btn_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Button(
            btn_frame,
            text="🗑️ Delete Selected Bin",
            font=("Arial", 10, "bold"),
            bg=self.danger_color,
            fg="white",
            relief=tk.FLAT,
            padx=15,
            pady=5,
            cursor="hand2",
            command=lambda: self.delete_selected_bin()
        ).pack(side='left', padx=5)
        
        # Bins List
        bins_frame = tk.LabelFrame(self.content_frame, text="All Bins", font=("Arial", 12, "bold"), bg="white")
        bins_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.mgt_bins_tree = ttk.Treeview(bins_frame, columns=("ID", "Type", "Capacity", "Location", "Owner", "Status"), show='headings', height=20)
        for col in ["ID", "Type", "Capacity", "Location", "Owner", "Status"]:
            self.mgt_bins_tree.heading(col, text=col)
            self.mgt_bins_tree.column(col, width=150)
        self.mgt_bins_tree.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.refresh_bins_list()
    
    def refresh_bins_list(self):
        """Refresh bins list"""
        for item in self.mgt_bins_tree.get_children():
            self.mgt_bins_tree.delete(item)
        
        # Populate bins
        for b in self.system.bins:
            owner = b.assigned_resident.full_name if b.assigned_resident else "Unassigned"
            self.mgt_bins_tree.insert("", "end", values=(b.bin_id, b.bin_type, f"{b.capacity}L", b.location, owner, b.status))
    
    def delete_selected_bin(self):
        """Delete selected bin"""
        selection = self.mgt_bins_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a bin to delete")
            return
        
        item = self.mgt_bins_tree.item(selection[0])
        bin_id = item['values'][0]
        
        # Confirm deletion
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete bin {bin_id}?"):
            if self.system.delete_bin(bin_id):
                self.refresh_bins_list()
                messagebox.showinfo("Success", f"Bin {bin_id} deleted successfully!")
            else:
                messagebox.showerror("Error", "Bin not found")
    
    def create_incidents_view_tab(self):
        """Show all recorded incidents"""
        # Clear content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Title
        title_frame = tk.Frame(self.content_frame, bg="white", relief=tk.RAISED, bd=2)
        title_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(
            title_frame,
            text="⚠️ Recorded Incidents",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#2C3E50"
        ).pack(pady=15)
        
        # Incidents List
        incidents_frame = tk.LabelFrame(self.content_frame, text="All Incidents", font=("Arial", 12, "bold"), bg="white")
        incidents_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Action buttons
        btn_frame = tk.Frame(incidents_frame, bg="white")
        btn_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Button(
            btn_frame,
            text="✅ Resolve Selected",
            font=("Arial", 10, "bold"),
            bg=self.success_color,
            fg="white",
            relief=tk.FLAT,
            padx=15,
            pady=5,
            cursor="hand2",
            command=self.resolve_selected_incident
        ).pack(side='left', padx=5)
        
        tk.Button(
            btn_frame,
            text="🗑️ Delete Selected",
            font=("Arial", 10, "bold"),
            bg=self.danger_color,
            fg="white",
            relief=tk.FLAT,
            padx=15,
            pady=5,
            cursor="hand2",
            command=self.delete_selected_incident
        ).pack(side='left', padx=5)
        
        self.mgt_inc_tree = ttk.Treeview(incidents_frame, columns=("ID", "Description", "Location", "Date", "Status"), show='headings', height=20)
        for col in ["ID", "Description", "Location", "Date", "Status"]:
            self.mgt_inc_tree.heading(col, text=col)
            self.mgt_inc_tree.column(col, width=200)
        self.mgt_inc_tree.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.refresh_incidents_list()
    
    def refresh_incidents_list(self):
        """Refresh incidents list"""
        for item in self.mgt_inc_tree.get_children():
            self.mgt_inc_tree.delete(item)
        
        # Populate incidents
        for inc in self.system.incidents:
            desc_short = inc.description[:80] + "..." if len(inc.description) > 80 else inc.description
            self.mgt_inc_tree.insert("", "end", values=(inc.incident_id, desc_short, inc.location, inc.reported_date, inc.status))
    
    def resolve_selected_incident(self):
        """Resolve selected incident"""
        selection = self.mgt_inc_tree.selection()
        if selection:
            item = self.mgt_inc_tree.item(selection[0])
            inc_id = item['values'][0]
            incident = next((i for i in self.system.incidents if i.incident_id == inc_id), None)
            if incident:
                incident.resolve()
                self.refresh_incidents_list()
                messagebox.showinfo("Success", f"Incident {inc_id} resolved!")
        else:
            messagebox.showwarning("Warning", "Please select an incident")
    
    def delete_selected_incident(self):
        """Delete selected incident"""
        selection = self.mgt_inc_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an incident to delete")
            return
        
        item = self.mgt_inc_tree.item(selection[0])
        inc_id = item['values'][0]
        
        # Confirm deletion
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete incident {inc_id}?"):
            if self.system.delete_incident(inc_id):
                self.refresh_incidents_list()
                messagebox.showinfo("Success", f"Incident {inc_id} deleted successfully!")
            else:
                messagebox.showerror("Error", "Incident not found")
    
    def create_customers_view_tab(self):
        """Show all customers (residents) with edit functionality"""
        # Clear content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Title
        title_frame = tk.Frame(self.content_frame, bg="white", relief=tk.RAISED, bd=2)
        title_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(
            title_frame,
            text="👥 Customers (Residents)",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#2C3E50"
        ).pack(pady=15)
        
        # Action Buttons
        btn_frame = tk.Frame(self.content_frame, bg=self.bg_color)
        btn_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Button(
            btn_frame,
            text="✏️ Edit Selected",
            font=("Arial", 10, "bold"),
            bg=self.accent_color,
            fg="white",
            relief=tk.FLAT,
            padx=15,
            pady=5,
            cursor="hand2",
            command=self.edit_selected_customer
        ).pack(side='left', padx=5)
        
        tk.Button(
            btn_frame,
            text="➕ Add New Customer",
            font=("Arial", 10, "bold"),
            bg=self.success_color,
            fg="white",
            relief=tk.FLAT,
            padx=15,
            pady=5,
            cursor="hand2",
            command=self.add_new_customer
        ).pack(side='left', padx=5)
        
        tk.Button(
            btn_frame,
            text="🗑️ Delete Selected",
            font=("Arial", 10, "bold"),
            bg=self.danger_color,
            fg="white",
            relief=tk.FLAT,
            padx=15,
            pady=5,
            cursor="hand2",
            command=self.delete_selected_customer
        ).pack(side='left', padx=5)
        
        # Customers List
        customers_frame = tk.LabelFrame(self.content_frame, text="All Customers", font=("Arial", 12, "bold"), bg="white")
        customers_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.mgt_customers_tree = ttk.Treeview(customers_frame, columns=("ID", "Name", "Address", "Bins Count"), show='headings', height=20)
        for col in ["ID", "Name", "Address", "Bins Count"]:
            self.mgt_customers_tree.heading(col, text=col)
            self.mgt_customers_tree.column(col, width=200)
        self.mgt_customers_tree.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.refresh_customers_list()
    
    def refresh_customers_list(self):
        """Refresh customers list"""
        for item in self.mgt_customers_tree.get_children():
            self.mgt_customers_tree.delete(item)
        
        # Populate customers
        for r in self.system.residents:
            bins_count = len([b for b in self.system.bins if b.assigned_resident == r])
            self.mgt_customers_tree.insert("", "end", values=(r.resident_id, r.full_name, r.address, bins_count))
    
    def edit_selected_customer(self):
        """Edit selected customer"""
        selection = self.mgt_customers_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a customer to edit")
            return
        
        item = self.mgt_customers_tree.item(selection[0])
        resident_id = item['values'][0]
        resident = next((r for r in self.system.residents if r.resident_id == resident_id), None)
        
        if not resident:
            messagebox.showerror("Error", "Customer not found")
            return
        
        # Create edit dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Customer")
        dialog.geometry("500x350")
        dialog.configure(bg="white")
        dialog.resizable(False, False)
        
        # Center
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (dialog.winfo_screenheight() // 2) - (350 // 2)
        dialog.geometry(f'500x350+{x}+{y}')
        
        frame = tk.Frame(dialog, bg="white")
        frame.pack(expand=True, fill='both', padx=30, pady=20)
        
        tk.Label(
            frame,
            text="Edit Customer Information",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#2C3E50"
        ).pack(pady=(0, 20))
        
        # Resident ID (read-only)
        tk.Label(frame, text="Resident ID:", font=("Arial", 11), bg="white").pack(anchor='w', pady=5)
        id_label = tk.Label(frame, text=resident.resident_id, font=("Arial", 11), bg="#ECF0F1", relief=tk.SUNKEN, anchor='w', padx=10, pady=5)
        id_label.pack(fill='x', pady=(0, 15))
        
        # Name
        tk.Label(frame, text="Full Name:", font=("Arial", 11), bg="white").pack(anchor='w', pady=5)
        name_entry = tk.Entry(frame, font=("Arial", 11), width=50)
        name_entry.insert(0, resident.full_name)
        name_entry.pack(fill='x', pady=(0, 15))
        
        # Address
        tk.Label(frame, text="Address:", font=("Arial", 11), bg="white").pack(anchor='w', pady=5)
        address_entry = tk.Entry(frame, font=("Arial", 11), width=50)
        address_entry.insert(0, resident.address)
        address_entry.pack(fill='x', pady=(0, 20))
        
        def save_changes():
            new_name = name_entry.get().strip()
            new_address = address_entry.get().strip()
            
            # Validate name
            is_valid, error = validate_name(new_name)
            if not is_valid:
                messagebox.showerror("Validation Error", error)
                return
            
            # Validate address
            is_valid, error = validate_address(new_address)
            if not is_valid:
                messagebox.showerror("Validation Error", error)
                return
            
            # Update resident data
            resident.full_name = new_name
            resident.address = new_address
            
            # Save data
            self.system.save_data()
            
            # Refresh list
            self.refresh_customers_list()
            
            messagebox.showinfo("Success", f"Customer {resident.resident_id} updated successfully!")
            dialog.destroy()
        
        btn_frame = tk.Frame(frame, bg="white")
        btn_frame.pack(fill='x', pady=10)
        
        tk.Button(
            btn_frame,
            text="💾 Save Changes",
            font=("Arial", 11, "bold"),
            bg=self.success_color,
            fg="white",
            relief=tk.FLAT,
            padx=20,
            pady=8,
            cursor="hand2",
            command=save_changes
        ).pack(side='left', padx=5)
        
        tk.Button(
            btn_frame,
            text="❌ Cancel",
            font=("Arial", 11),
            bg="#95A5A6",
            fg="white",
            relief=tk.FLAT,
            padx=20,
            pady=8,
            cursor="hand2",
            command=dialog.destroy
        ).pack(side='left', padx=5)
    
    def add_new_customer(self):
        """Add new customer"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Customer")
        dialog.geometry("500x300")
        dialog.configure(bg="white")
        dialog.resizable(False, False)
        
        # Center
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (dialog.winfo_screenheight() // 2) - (300 // 2)
        dialog.geometry(f'500x300+{x}+{y}')
        
        frame = tk.Frame(dialog, bg="white")
        frame.pack(expand=True, fill='both', padx=30, pady=20)
        
        tk.Label(
            frame,
            text="Add New Customer",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#2C3E50"
        ).pack(pady=(0, 20))
        
        # Name
        tk.Label(frame, text="Full Name:", font=("Arial", 11), bg="white").pack(anchor='w', pady=5)
        name_entry = tk.Entry(frame, font=("Arial", 11), width=50)
        name_entry.pack(fill='x', pady=(0, 15))
        name_entry.focus()
        
        # Address
        tk.Label(frame, text="Address:", font=("Arial", 11), bg="white").pack(anchor='w', pady=5)
        address_entry = tk.Entry(frame, font=("Arial", 11), width=50)
        address_entry.pack(fill='x', pady=(0, 20))
        
        def save_new():
            new_name = name_entry.get().strip()
            new_address = address_entry.get().strip()
            
            # Validate name
            is_valid, error = validate_name(new_name)
            if not is_valid:
                messagebox.showerror("Validation Error", error)
                return
            
            # Validate address
            is_valid, error = validate_address(new_address)
            if not is_valid:
                messagebox.showerror("Validation Error", error)
                return
            
            # Generate sequential ID
            rid = self.system.generate_resident_id()
            new_resident = Resident(rid, new_name, new_address)
            self.system.register_resident(new_resident)
            
            # Save data
            self.system.save_data()
            
            # Refresh list
            self.refresh_customers_list()
            
            messagebox.showinfo("Success", f"Customer {rid} added successfully!")
            dialog.destroy()
        
        btn_frame = tk.Frame(frame, bg="white")
        btn_frame.pack(fill='x', pady=10)
        
        tk.Button(
            btn_frame,
            text="➕ Add Customer",
            font=("Arial", 11, "bold"),
            bg=self.success_color,
            fg="white",
            relief=tk.FLAT,
            padx=20,
            pady=8,
            cursor="hand2",
            command=save_new
        ).pack(side='left', padx=5)
        
        tk.Button(
            btn_frame,
            text="❌ Cancel",
            font=("Arial", 11),
            bg="#95A5A6",
            fg="white",
            relief=tk.FLAT,
            padx=20,
            pady=8,
            cursor="hand2",
            command=dialog.destroy
        ).pack(side='left', padx=5)
        
        # Bind Enter key
        name_entry.bind('<Return>', lambda e: address_entry.focus())
        address_entry.bind('<Return>', lambda e: save_new())
    
    def delete_selected_customer(self):
        """Delete selected customer"""
        selection = self.mgt_customers_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a customer to delete")
            return
        
        item = self.mgt_customers_tree.item(selection[0])
        resident_id = item['values'][0]
        
        # Check if customer has bins
        resident = next((r for r in self.system.residents if r.resident_id == resident_id), None)
        if resident and resident.bins:
            if not messagebox.askyesno("Warning", f"Customer {resident_id} has {len(resident.bins)} bin(s) assigned. Delete anyway?\nBins will be unlinked."):
                return
        
        # Confirm deletion
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete customer {resident_id}?\nThis will also unlink all associated bins."):
            if self.system.delete_resident(resident_id):
                self.refresh_customers_list()
                self.update_combos()
                messagebox.showinfo("Success", f"Customer {resident_id} deleted successfully!")
            else:
                messagebox.showerror("Error", "Customer not found")
    
    def create_customer_payments_tab(self):
        """Set customer payments"""
        # Clear content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Title
        title_frame = tk.Frame(self.content_frame, bg="white", relief=tk.RAISED, bd=2)
        title_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(
            title_frame,
            text="💰 Set Customer Payment",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#2C3E50"
        ).pack(pady=15)
        
        # Payment Form
        form_frame = tk.LabelFrame(self.content_frame, text="Process Payment for Customer", font=("Arial", 12, "bold"), bg="white")
        form_frame.pack(fill='x', padx=10, pady=10)
        
        input_frame = tk.Frame(form_frame, bg="white")
        input_frame.pack(fill='x', padx=20, pady=20)
        
        tk.Label(input_frame, text="Customer:", font=("Arial", 11), bg="white").grid(row=0, column=0, padx=10, pady=10, sticky='w')
        self.mgt_pay_customer = ttk.Combobox(input_frame, width=30, state="readonly")
        self.mgt_pay_customer.grid(row=0, column=1, padx=10, pady=10, sticky='ew')
        
        tk.Label(input_frame, text="Service Type:", font=("Arial", 11), bg="white").grid(row=1, column=0, padx=10, pady=10, sticky='w')
        self.mgt_pay_service = ttk.Combobox(input_frame, values=["Collection", "Recycling", "Penalty", "Extra Pickup"], width=30, state="readonly")
        self.mgt_pay_service.grid(row=1, column=1, padx=10, pady=10, sticky='ew')
        self.mgt_pay_service.current(0)
        
        tk.Label(input_frame, text="Amount ($):", font=("Arial", 11), bg="white").grid(row=2, column=0, padx=10, pady=10, sticky='w')
        self.mgt_pay_amount = tk.Entry(input_frame, font=("Arial", 11), width=32)
        self.mgt_pay_amount.grid(row=2, column=1, padx=10, pady=10, sticky='ew')
        
        input_frame.columnconfigure(1, weight=1)
        
        tk.Button(
            form_frame,
            text="📋 Create Pending Payment",
            font=("Arial", 12, "bold"),
            bg="#F39C12",
            fg="white",
            relief=tk.FLAT,
            padx=20,
            pady=10,
            cursor="hand2",
            command=self.mgt_create_pending_payment
        ).pack(pady=15)
        
        # Action Buttons
        btn_frame_pay = tk.Frame(self.content_frame, bg=self.bg_color)
        btn_frame_pay.pack(fill='x', padx=10, pady=5)
        
        tk.Button(
            btn_frame_pay,
            text="🗑️ Delete Selected Payment",
            font=("Arial", 10, "bold"),
            bg=self.danger_color,
            fg="white",
            relief=tk.FLAT,
            padx=15,
            pady=5,
            cursor="hand2",
            command=self.delete_selected_payment
        ).pack(side='left', padx=5)
        
        # Payment History
        history_frame = tk.LabelFrame(self.content_frame, text="All Payments", font=("Arial", 12, "bold"), bg="white")
        history_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.mgt_pay_tree = ttk.Treeview(history_frame, columns=("ID", "Customer", "Amount", "Service", "Status", "Date"), show='headings', height=15)
        for col in ["ID", "Customer", "Amount", "Service", "Status", "Date"]:
            self.mgt_pay_tree.heading(col, text=col)
            self.mgt_pay_tree.column(col, width=150)
        self.mgt_pay_tree.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Update combos and refresh
        res_list = [f"{r.resident_id} - {r.full_name}" for r in self.system.residents]
        self.mgt_pay_customer['values'] = res_list
        self.refresh_mgt_payments()
    
    def delete_selected_payment(self):
        """Delete selected payment"""
        selection = self.mgt_pay_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a payment to delete")
            return
        
        item = self.mgt_pay_tree.item(selection[0])
        transaction_id = item['values'][0]
        
        # Confirm deletion
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete payment {transaction_id}?"):
            if self.system.delete_transaction(transaction_id):
                self.refresh_mgt_payments()
                messagebox.showinfo("Success", f"Payment {transaction_id} deleted successfully!")
            else:
                messagebox.showerror("Error", "Payment not found")
    
    def mgt_create_pending_payment(self):
        """Create pending payment for customer by management"""
        customer_str = self.mgt_pay_customer.get()
        service = self.mgt_pay_service.get()
        amount_str = self.mgt_pay_amount.get().strip()
        
        if not customer_str:
            messagebox.showerror("Validation Error", "Please select a customer")
            return
        
        # Validate amount
        is_valid, result = validate_amount(amount_str)
        if not is_valid:
            messagebox.showerror("Validation Error", result)
            return
        
        amount = result
        
        rid = customer_str.split(" - ")[0]
        resident = next((r for r in self.system.residents if r.resident_id == rid), None)
        
        if resident:
            # Generate sequential ID
            tid = self.system.generate_transaction_id()
            # Create pending payment (status="Pending")
            transaction = Transaction(tid, resident, amount, service, status="Pending")
            self.system.create_pending_payment(transaction)
            self.refresh_mgt_payments()
            self.mgt_pay_amount.delete(0, 'end')
            messagebox.showinfo("Success", f"Pending payment of ${amount:.2f} created for {resident.full_name}!\nResident can now pay it from their payment tab.")
        else:
            messagebox.showerror("Error", "Customer not found")
    
    def refresh_mgt_payments(self):
        """Refresh management payments list"""
        for item in self.mgt_pay_tree.get_children():
            self.mgt_pay_tree.delete(item)
        
        for t in self.system.transactions:
            p_name = t.payer.full_name if hasattr(t.payer, 'full_name') else str(t.payer)
            status = getattr(t, 'status', 'Paid' if t.payment_date else 'Pending')
            date = t.payment_date if t.payment_date else "N/A"
            self.mgt_pay_tree.insert("", "end", values=(t.transaction_id, p_name, f"${t.amount:.2f}", t.service_type, status, date))
    
    def logout(self):
        """Logout and return to login page"""
        # Save data before logout
        self.system.save_data()
        
        # Close current window
        self.root.destroy()
        
        # Open login window
        login_root = tk.Tk()
        login = LoginWindow(login_root, self.system)
        login_root.mainloop()
    
    def save_data(self):
        """Save all data"""
        self.system.save_data()
        messagebox.showinfo("Success", "All data saved successfully!")

# ==================== MAIN ENTRY ====================
def main():
    """Main entry point"""
    root = tk.Tk()
    system = WasteManagementSystem()
    system.load_data()
    
    login = LoginWindow(root, system)
    root.mainloop()

if __name__ == "__main__":
    main()
