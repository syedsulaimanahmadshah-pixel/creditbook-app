import sqlite3
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.list import OneLineListItem

Window.size = (360, 640)

# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect("credit_book.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS admin_settings (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS customers (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE)")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT, amount TEXT, status TEXT, date_added TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("SELECT * FROM admin_settings WHERE id = 1")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO admin_settings (id, username, password) VALUES (1, 'admin', '1234')")
    conn.commit()
    conn.close()

# --- DESIGN STRING (KV LANGUAGE) ---
KV = '''
MDScreenManager:
    LoginScreen:
    DashboardScreen:
    AddCustomerScreen:
    AllCustomersScreen:
    RemoveCustomerScreen:
    PaymentsReceivedScreen:
    CustomerDetailScreen:
    SettingsScreen:

<LoginScreen>:
    name: 'login'
    MDBoxLayout:
        orientation: 'vertical'
        padding: 30
        spacing: 20
        MDIconButton:
            icon: "book-open-page-variant"
            pos_hint: {"center_x": .5}
            icon_size: "80sp"
        MDLabel:
            text: "Credit Book 📘"
            font_style: "H5"
            halign: "center"
            bold: True
        MDTextField:
            id: user_input
            hint_text: "Username"
            text: "admin"
            icon_left: "account"
        MDTextField:
            id: pass_input
            hint_text: "Password"
            text: "1234"
            password: True
            icon_left: "lock"
        MDRaisedButton:
            text: "LOGIN"
            pos_hint: {"center_x": .5}
            size_hint_x: 0.8
            on_press: root.validate_login()
        MDLabel:
            id: err_lbl
            text: ""
            halign: "center"
            theme_text_color: "Error"

<DashboardScreen>:
    name: 'dashboard'
    MDBoxLayout:
        orientation: 'vertical'
        padding: 15
        spacing: 10
        MDLabel:
            text: "⚙️ Main Menu Dashboard"
            font_style: "H6"
            bold: True
            size_hint_y: None
            height: 40
        MDGridLayout:
            cols: 2
            spacing: 12
            padding: 5
            MDCard:
                orientation: 'vertical'
                padding: 12
                on_release: app.root.current = 'add_customer_screen'
                MDIconButton:
                    icon: "account-plus"
                    pos_hint: {"center_x": .5}
                MDLabel:
                    text: "Add Customer"
                    halign: "center"
            MDCard:
                orientation: 'vertical'
                padding: 12
                on_release: root.go_to('all_customers_screen')
                MDIconButton:
                    icon: "account-multiple"
                    pos_hint: {"center_x": .5}
                MDLabel:
                    text: "All Customers"
                    halign: "center"
            MDCard:
                orientation: 'vertical'
                padding: 12
                on_release: root.go_to('remove_customer_screen')
                MDIconButton:
                    icon: "account-remove"
                    pos_hint: {"center_x": .5}
                MDLabel:
                    text: "Remove Customer"
                    halign: "center"
            MDCard:
                orientation: 'vertical'
                padding: 12
                on_release: root.go_to('payments_received_screen')
                MDIconButton:
                    icon: "cash-check"
                    pos_hint: {"center_x": .5}
                MDLabel:
                    text: "Payment Log"
                    halign: "center"
            MDCard:
                orientation: 'vertical'
                padding: 12
                on_release: app.root.current = 'settings'
                MDIconButton:
                    icon: "cog"
                    pos_hint: {"center_x": .5}
                MDLabel:
                    text: "Settings Panel"
                    halign: "center"
            MDCard:
                orientation: 'vertical'
                padding: 12
                on_release: app.root.current = 'login'
                MDIconButton:
                    icon: "logout"
                    pos_hint: {"center_x": .5}
                MDLabel:
                    text: "Log Out"
                    halign: "center"

<AddCustomerScreen>:
    name: 'add_customer_screen'
    MDBoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 15
        MDBoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: 50
            MDIconButton:
                icon: "arrow-left"
                on_press: app.root.current = 'dashboard'
            MDLabel:
                text: "➕ Add Customer"
                font_style: "H6"
                bold: True
        MDTextField:
            id: cust_name
            hint_text: "Customer Name"
        MDRaisedButton:
            text: "Save Customer"
            pos_hint: {"center_x": .5}
            on_press: root.save()
        MDLabel:
            id: status
            halign: "center"
        MDBoxLayout:

<AllCustomersScreen>:
    name: 'all_customers_screen'
    MDBoxLayout:
        orientation: 'vertical'
        padding: 15
        spacing: 10
        MDBoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: 50
            MDIconButton:
                icon: "arrow-left"
                on_press: app.root.current = 'dashboard'
            MDLabel:
                text: "👥 Customer Directory"
                font_style: "H6"
                bold: True
        MDScrollView:
            MDList:
                id: list_box

<RemoveCustomerScreen>:
    name: 'remove_customer_screen'
    MDBoxLayout:
        orientation: 'vertical'
        padding: 15
        spacing: 10
        MDBoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: 50
            MDIconButton:
                icon: "arrow-left"
                on_press: app.root.current = 'dashboard'
            MDLabel:
                text: "❌ Tap Name to Delete Profile"
                font_style: "H6"
                bold: True
        MDScrollView:
            MDList:
                id: del_box

<PaymentsReceivedScreen>:
    name: 'payments_received_screen'
    MDBoxLayout:
        orientation: 'vertical'
        padding: 15
        spacing: 10
        MDBoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: 50
            MDIconButton:
                icon: "arrow-left"
                on_press: app.root.current = 'dashboard'
            MDLabel:
                text: "💰 All Payment Logs"
                font_style: "H6"
                bold: True
        MDScrollView:
            MDList:
                id: log_box

<CustomerDetailScreen>:
    name: 'customer_detail'
    MDBoxLayout:
        orientation: 'vertical'
        padding: 15
        spacing: 10
        MDBoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: 50
            MDIconButton:
                icon: "arrow-left"
                on_press: app.root.current = 'all_customers_screen'
            MDLabel:
                id: ledger_title
                text: "Ledger"
                font_style: "H6"
                bold: True
        MDGridLayout:
            cols: 2
            spacing: 10
            size_hint_y: None
            height: 60
            MDTextField:
                id: amt_input
                hint_text: "Amount (Rs)"
            Spinner:
                id: stat_spin
                text: 'Pending'
                values: ('Pending', 'Received')
        MDRaisedButton:
            text: "Save Entry"
            size_hint_x: 1
            on_press: root.save_entry()
        MDLabel:
            text: "📜 Tap Entry below to Delete:"
            bold: True
            size_hint_y: None
            height: 30
        MDScrollView:
            MDList:
                id: hist_box

<SettingsScreen>:
    name: 'settings'
    MDBoxLayout:
        orientation: 'vertical'
        padding: 25
        spacing: 15
        MDBoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: 50
            MDIconButton:
                icon: "arrow-left"
                on_press: app.root.current = 'dashboard'
            MDLabel:
                text: "⚙️ Settings"
                font_style: "H6"
                bold: True
        MDTextField:
            id: new_u
            hint_text: "New Username"
        MDTextField:
            id: new_p
            hint_text: "New Password"
            password: True
        MDRaisedButton:
            text: "Update Profile"
            pos_hint: {"center_x": .5}
            on_press: root.update_fields()
        MDLabel:
            id: msg
            halign: "center"
        MDBoxLayout:
'''

# --- SCREEN CLASSES (PURE PYTHON LOGIC) ---
class LoginScreen(MDScreen):
    def validate_login(self):
        u = self.ids.user_input.text.strip()
        p = self.ids.pass_input.text.strip()
        conn = sqlite3.connect("credit_book.db")
        cursor = conn.cursor()
        cursor.execute("SELECT username, password FROM admin_settings WHERE id = 1")
        db_u, db_p = cursor.fetchone()
        conn.close()
        if u == db_u and p == db_p:
            self.ids.err_lbl.text = ""
            self.manager.current = 'dashboard'
        else:
            self.ids.err_lbl.text = "❌ Galat Details!"

class DashboardScreen(MDScreen):
    def go_to(self, sname):
        self.manager.current = sname
        self.manager.get_screen(sname).load_data()

class AddCustomerScreen(MDScreen):
    def save(self):
        name = self.ids.cust_name.text.strip()
        if name:
            conn = sqlite3.connect("credit_book.db")
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO customers (name) VALUES (?)", (name,))
                conn.commit()
                self.ids.status.text = f"✅ {name} Saved!"
                self.ids.cust_name.text = ""
            except sqlite3.IntegrityError:
                self.ids.status.text = "❌ Name already exists!"
            conn.close()

class AllCustomersScreen(MDScreen):
    def load_data(self):
        self.ids.list_box.clear_widgets()
        conn = sqlite3.connect("credit_book.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM customers ORDER BY name ASC")
        for row in cursor.fetchall():
            item = OneLineListItem(text=row[0])
            item.bind(on_release=self.view_ledger)
            self.ids.list_box.add_widget(item)
        conn.close()

    def view_ledger(self, instance):
        det = self.manager.get_screen('customer_detail')
        det.current_customer = instance.text
        det.setup()
        self.manager.current = 'customer_detail'

class RemoveCustomerScreen(MDScreen):
    def load_data(self):
        self.ids.del_box.clear_widgets()
        conn = sqlite3.connect("credit_book.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM customers ORDER BY name ASC")
        for row in cursor.fetchall():
            item = OneLineListItem(text=f"Delete: {row[0]}")
            item.bind(on_release=lambda x, name=row[0]: self.remove(name))
            self.ids.del_box.add_widget(item)
        conn.close()

    def remove(self, name):
        conn = sqlite3.connect("credit_book.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM customers WHERE name = ?", (name,))
        cursor.execute("DELETE FROM payments WHERE customer_name = ?", (name,))
        conn.commit()
        conn.close()
        self.load_data()

class PaymentsReceivedScreen(MDScreen):
    def load_data(self):
        self.ids.log_box.clear_widgets()
        conn = sqlite3.connect("credit_book.db")
        cursor = conn.cursor()
        cursor.execute("SELECT customer_name, amount, status FROM payments ORDER BY id DESC")
        for row in cursor.fetchall():
            self.ids.log_box.add_widget(OneLineListItem(text=f"{row[0]} | Rs.{row[1]} | {row[2]}"))
        conn.close()

class CustomerDetailScreen(MDScreen):
    current_customer = ""
    def setup(self):
        self.ids.ledger_title.text = f"Ledger: {self.current_customer}"
        self.load_history()

    def save_entry(self):
        amt = self.ids.amt_input.text.strip()
        stat = self.ids.stat_spin.text
        if amt:
            conn = sqlite3.connect("credit_book.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO payments (customer_name, amount, status) VALUES (?, ?, ?)", (self.current_customer, amt, stat))
            conn.commit()
            conn.close()
            self.ids.amt_input.text = ""
            self.load_history()

    def load_history(self):
        self.ids.hist_box.clear_widgets()
        conn = sqlite3.connect("credit_book.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, amount, status FROM payments WHERE customer_name = ? ORDER BY id DESC", (self.current_customer,))
        for row in cursor.fetchall():
            item = OneLineListItem(text=f"Rs. {row[1]} ({row[2]}) [Tap to Delete]")
            item.bind(on_release=lambda x, eid=row[0]: self.del_entry(eid))
            self.ids.hist_box.add_widget(item)
        conn.close()

    def del_entry(self, eid):
        conn = sqlite3.connect("credit_book.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM payments WHERE id = ?", (eid,))
        conn.commit()
        conn.close()
        self.load_history()

class SettingsScreen(MDScreen):
    def update_fields(self):
        u = self.ids.new_u.text.strip()
        p = self.ids.new_p.text.strip()
        if u and p:
            conn = sqlite3.connect("credit_book.db")
            cursor = conn.cursor()
            cursor.execute("UPDATE admin_settings SET username = ?, password = ? WHERE id = 1", (u, p))
            conn.commit()
            conn.close()
            self.ids.msg.text = "✅ Success!"
            self.ids.new_u.text = ""
            self.ids.new_p.text = ""

# --- MAIN ENGINE ---
class CreditBookApp(MDApp):
    def build(self):
        init_db()
        self.theme_cls.primary_palette = "Blue"
        return Builder.load_string(KV)

if __name__ == '__main__':
    CreditBookApp().run()