import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

CONTACTS_FILE = "contacts.json"


class ContactManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Manager (codsoft) by sourabh sisodia")
        self.contacts = []
        self.load_contacts()

        # ui setup hai by sourabh
        self.search_var = tk.StringVar()
        tk.Label(root, text="Search:").grid(row=0, column=0, sticky="w", padx=5)
        tk.Entry(root, textvariable=self.search_var).grid(row=0, column=1, padx=5)
        tk.Button(root, text="Search", command=self.search_contact).grid(row=0, column=2, padx=5)
        tk.Button(root, text="Add Contact", command=self.add_contact_window).grid(row=0, column=3, padx=5)

        self.contact_listbox = tk.Listbox(root, width=70)
        self.contact_listbox.grid(row=1, column=0, columnspan=4, padx=10, pady=10)
        self.contact_listbox.bind('<<ListboxSelect>>', self.on_select)

        self.display_contacts()

    def load_contacts(self):
        if os.path.exists(CONTACTS_FILE):
            with open(CONTACTS_FILE, 'r') as f:
                self.contacts = json.load(f)

    def save_contacts(self):
        with open(CONTACTS_FILE, 'w') as f:
            json.dump(self.contacts, f, indent=4)

    def display_contacts(self, filtered=None):
        self.contact_listbox.delete(0, tk.END)
        for idx, contact in enumerate(filtered if filtered else self.contacts):
            self.contact_listbox.insert(tk.END, f"{contact['name']} - {contact['phone']}")

    def add_contact_window(self, contact=None, index=None):
        win = tk.Toplevel(self.root)
        win.title("Edit Contact" if contact else "Add Contact")

        fields = ["Name", "Phone", "Email", "Address"]
        entries = {}

        for i, field in enumerate(fields):
            tk.Label(win, text=field + ":").grid(row=i, column=0, padx=5, pady=5, sticky='e')
            entry = tk.Entry(win, width=40)
            entry.grid(row=i, column=1, padx=5, pady=5)
            entries[field.lower()] = entry

        if contact:
            for key in entries:
                entries[key].insert(0, contact[key])

        def save():
            new_contact = {k: e.get().strip() for k, e in entries.items()}
            if not new_contact["name"] or not new_contact["phone"]:
                messagebox.showerror("Error", "Name and Phone are required.")
                return

            if index is not None:
                self.contacts[index] = new_contact
            else:
                self.contacts.append(new_contact)

            self.save_contacts()
            self.display_contacts()
            win.destroy()

        tk.Button(win, text="Save", command=save).grid(row=5, column=0, columnspan=2, pady=10)

    def on_select(self, event):
        selection = self.contact_listbox.curselection()
        if selection:
            index = selection[0]
            selected_contact = self.contacts[index]

            action = messagebox.askquestion("Action", "Would you like to Edit or Delete this contact?", icon='question', type='yesno')
            if action == 'yes':
                self.add_contact_window(contact=selected_contact, index=index)
            else:
                confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this contact?")
                if confirm:
                    self.contacts.pop(index)
                    self.save_contacts()
                    self.display_contacts()

    def search_contact(self):
        keyword = self.search_var.get().strip().lower()
        if not keyword:
            self.display_contacts()
            return

        filtered = [
            c for c in self.contacts
            if keyword in c['name'].lower() or keyword in c['phone']
        ]
        self.display_contacts(filtered)


if __name__ == "__main__":
    root = tk.Tk()
    app = ContactManagerApp(root)
    root.mainloop()
