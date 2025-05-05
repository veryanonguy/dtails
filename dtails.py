#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import tkinter.messagebox as msgbox
from PIL import ImageTk, Image
import os
import gnupg
from src.commands import *
import webbrowser
import pyudev
import threading
import time

class MyApp(tk.Tk):
    def __init__(self):
        try:
            super().__init__()
            self.title("DTails")

            # Set the theme globally
            style = ttk.Style()
            style.theme_use("breeze")

            # Configure styles for specific widgets if needed
            style.configure("TLabel", font=("Helvetica", 10), background="#f0f0f0", foreground="#333333")
            style.configure("TButton", font=("Helvetica", 10), background="#ffffff", foreground="#000000")
            style.configure("TCheckbutton", font=("Helvetica", 10), background="#f0f0f0", foreground="#333333")
            style.configure("TFrame", padding=5, background="#f0f0f0")
            style.configure("TNotebook", background="#f0f0f0")
            style.configure("TNotebook.Tab", font=("Helvetica", 10, "bold"), background="#e0e0e0", foreground="#333333")
            style.map("TNotebook.Tab", background=[("selected", "#ffffff"), ("active", "#e0e0e0"), ("disabled", "#cccccc")], foreground=[("selected", "#000000"), ("active", "#000000"), ("disabled", "#888888")])
            style.configure("TSeparator", background="#e0e0e0")
            style.configure("Vertical.TScrollbar", background="#e0e0e0", troughcolor="#ffffff", arrowcolor="#000000")
            style.configure("Horizontal.TScrollbar", background="#e0e0e0", troughcolor="#ffffff", arrowcolor="#000000")
            style.map("TButton", background=[("active", "#e0e0e0")], foreground=[("active", "#000000")])

            self.tab_control = ttk.Notebook(self)
            self.gpg = gnupg.GPG()
            self.tab1 = ttk.Frame(self.tab_control)
            self.tab2 = ttk.Frame(self.tab_control)
            self.tab3 = ttk.Frame(self.tab_control)
            self.tab4 = ttk.Frame(self.tab_control)
            self.tab_control.add(self.tab1, text='Select image 💽', state='normal')
            self.tab_control.add(self.tab2, text='Modify and Build the image ⚒️', state='disabled')
            self.tab_control.add(self.tab3, text='Live install 👨‍🔧', state='disabled')
            self.tab_control.add(self.tab4, text='ℹ️', state='normal')
            self.tab_control.pack(expand=1, fill='both')
            self.file_path = tk.StringVar()
            self.checkboxes = []

            ################## Tab 1 ##################
            self.logo_img = Image.open("img/dtails.png")
            self.logo_img = self.logo_img.resize((150, 150))
            self.logo_photo = ImageTk.PhotoImage(self.logo_img)
            logo_label = ttk.Label(self.tab1, image=self.logo_photo)
            logo_label.pack(pady=10)

            text_label = ttk.Label(self.tab1, text="Remaster your Debian-based image with DTails! 👨‍💻")
            text_label.pack(pady=2)

            if os.path.exists("shared_with_chroot"):
                clean_button = ttk.Button(self.tab1, text="Clean old build 🚮", command=remove_directories)
                clean_button.pack()

            separator = ttk.Separator(self.tab1, orient="horizontal")
            separator.pack(fill="x", pady=20)

            self.select_file_button = ttk.Button(self.tab1, text="Select image 💽", command=self.select_file)
            self.select_file_button.pack(pady=10)

            self.label = ttk.Label(self.tab1, textvariable=self.file_path)
            self.label.pack()

            self.select_signature_button = ttk.Button(self.tab1, text="Verify signature 📜", command=self.select_sig, state='disabled')
            self.select_signature_button.pack(pady=10)

            # Labels for verification status
            self.verification_label = ttk.Label(self.tab1, text="", font=("Helvetica", 10, "bold"))
            self.verification_label.pack(pady=10)

            ################## Tab 2 ##################

            # Top Frame
            self.top_frame = ttk.Frame(self.tab2)
            self.top_frame.pack(side="top", fill="x", pady=10)
            self.text_label_tab2 = ttk.Label(self.top_frame, text="Select the software you would like to install or remove.\nBinaries from the original image will remain unmodified.")
            self.text_label_tab2.pack()

            # Separator between Top Frame and Middle Frame
            self.top_separator = ttk.Separator(self.tab2, orient="horizontal")
            self.top_separator.pack(fill="x", pady=10)

            # Middle Frame containing Left and Right Frames
            self.middle_frame = ttk.Frame(self.tab2)
            self.middle_frame.pack(fill="both", expand=True)

            # Left Frame (add software) with Scrollbar
            self.left_frame = ttk.Frame(self.middle_frame)
            self.left_frame.pack(side="left", padx=20, fill="both", expand=True)
            self.left_text = ttk.Label(self.left_frame, text="Add Software ✅", font="bold")
            self.left_text.pack(pady=5)

            self.left_canvas = tk.Canvas(self.left_frame)
            self.left_scrollbar = ttk.Scrollbar(self.left_frame, orient="vertical", command=self.left_canvas.yview)
            self.left_scrollable_frame = ttk.Frame(self.left_canvas)

            self.left_scrollable_frame.bind(
                "<Configure>",
                lambda e: self.left_canvas.configure(
                    scrollregion=self.left_canvas.bbox("all")
                )
            )

            self.left_canvas.create_window((0, 0), window=self.left_scrollable_frame, anchor="nw")
            self.left_canvas.configure(yscrollcommand=self.left_scrollbar.set)

            self.left_canvas.pack(side="left", fill="both", expand=True)
            self.left_scrollbar.pack(side="right", fill="y")

            # Now you can use self.left_scrollable_frame
            self.create_checkbox(self.left_scrollable_frame, "Sparrow Wallet (106MB)", "")
            self.create_checkbox(self.left_scrollable_frame, "Liana Wallet (13.8MB)", "")
            self.create_checkbox(self.left_scrollable_frame, "Bisq (222MB)", "")
            self.create_checkbox(self.left_scrollable_frame, "BIP39 iancoleman (4.34MB)", "")
            self.create_checkbox(self.left_scrollable_frame, "SeedTool (6.58MB)", "")
            self.create_checkbox(self.left_scrollable_frame, "Border Wallets (1.59MB)", "")
            self.create_checkbox(self.left_scrollable_frame, "Whirlpool GUI (327MB)", "")
            self.create_checkbox(self.left_scrollable_frame, "Specter Desktop (197MB)", "")
            self.create_checkbox(self.left_scrollable_frame, "MyCitadel Desktop (4.41MB)", "")
            self.create_checkbox(self.left_scrollable_frame, "Hodl Hodl and RoboSats (~1MB)", "")
            self.create_checkbox(self.left_scrollable_frame, "Mempool.space (~1MB)", "")
            self.create_checkbox(self.left_scrollable_frame, "Briar (221MB)", "")
            self.create_checkbox(self.left_scrollable_frame, "SimpleX Chat (249MB)", "")
            self.create_checkbox(self.left_scrollable_frame, "Rana Nostr pubkeys mining tool (1.46MB)", "")
            self.create_checkbox(self.left_scrollable_frame, "Nostr web clients (~1MB)", "gobbler")
            self.create_checkbox(self.left_scrollable_frame, "Bitcoin Core (45MB)", "")
            self.create_checkbox(self.left_scrollable_frame, "Feather Wallet (22MB)", "")
            self.create_checkbox(self.left_scrollable_frame, "Cake Wallet (77.9MB)", "")

            # Separator between Left and Right Frames
            self.middle_separator = ttk.Separator(self.middle_frame, orient="vertical")
            self.middle_separator.pack(side="left", fill="y", padx=10)

            # Right Frame (Remove Software) with Scrollbar
            self.right_frame = ttk.Frame(self.middle_frame)
            self.right_frame.pack(side="right", padx=20, fill="both", expand=True)
            self.right_text = ttk.Label(self.right_frame, text="Remove Software ❌", font="bold")
            self.right_text.pack(pady=5)

            self.right_canvas = tk.Canvas(self.right_frame)
            self.right_scrollbar = ttk.Scrollbar(self.right_frame, orient="vertical", command=self.right_canvas.yview)
            self.right_scrollable_frame = ttk.Frame(self.right_canvas)

            self.right_scrollable_frame.bind(
                "<Configure>",
                lambda e: self.right_canvas.configure(
                    scrollregion=self.right_canvas.bbox("all")
                )
            )

            self.right_canvas.create_window((0, 0), window=self.right_scrollable_frame, anchor="nw")
            self.right_canvas.configure(yscrollcommand=self.right_scrollbar.set)

            self.right_canvas.pack(side="left", fill="both", expand=True)
            self.right_scrollbar.pack(side="right", fill="y")

            # Now you can use self.right_scrollable_frame
            self.create_checkbox(self.right_scrollable_frame, "Thunderbird (219MB)", "")
            self.create_checkbox(self.right_scrollable_frame, "GIMP (90MB)", "")

            # Separator between Middle Frame and Bottom Frame
            self.bottom_separator = ttk.Separator(self.tab2, orient="horizontal")
            self.bottom_separator.pack(fill="x", pady=10)

            # Bottom Frame
            self.bottom_frame = ttk.Frame(self.tab2)
            self.bottom_frame.pack(side="bottom", pady=10)
            self.next_button2 = ttk.Button(self.bottom_frame, text="Build ⚒️", command=self.get_selected_options)
            self.next_button2.pack()

            ################## Tab 3 ##################
            self.disconnect_button = ttk.Label(self.tab3, text="\nChoose the device name from the list.\nDrive will appear at the right. Please, double check it before continuing")
            self.disconnect_button.pack()

            separator = ttk.Separator(self.tab3, orient="horizontal")
            separator.pack(fill="x", pady=40)

            self.pendrive_var = tk.StringVar(self.tab3)
            self.pendrive_dropdown = ttk.OptionMenu(self.tab3, self.pendrive_var, "No pendrives found")
            self.pendrive_dropdown.pack()

            self.image_label = ttk.Label(self.tab3, text="Please connect a pendrive")
            self.image_label.pack()

            self.connect_button = ttk.Button(self.tab3, text="Install to device", state=tk.DISABLED, command=lambda: install_image_to_device(self.pendrive_var.get()))
            self.connect_button.pack()

            thread = threading.Thread(target=self.update_pendrives)
            thread.daemon = True
            thread.start()

            ################## Tab 4 ##################
            label2_1 = ttk.Label(self.tab4, text='DTails is a tool to remaster live Debian based images.\n\nDread (maintainer): /u/veryanonguy', cursor="center_ptr")
            label2_1.pack(pady=1)
            label2_1.bind("<Button-1>", lambda e: self.copy_to_clipboard("http://dreadytofatroptsdj6io7l3xptbet6onoyno2yv7jicoxknyazubrad.onion/u/veryanonguy"))

            label2 = ttk.Label(self.tab4, text='DTails tool - Made by DT and maintained by veryanonguy with ♥', cursor="hand2")
            label2.pack(pady=10, side="bottom")
            label2.bind("<Button-1>", lambda e: self.callback("https://github.com/veryanonguy/dtails"))

            self.tab_control.tab(1, state="disabled")
            self.tab_control.tab(2, state="disabled")
        except Exception as e:
            msgbox.showerror("Initialization Error", f"An error occurred during initialization: {e}")

    def update_pendrives(self):
        try:
            context = pyudev.Context()
            while True:
                devices = context.list_devices(subsystem='block', ID_BUS='usb')
                self.pendrives = {}
                for device in devices:
                    if not device.get('ID_VENDOR'):
                        print("No USB Manufacturer found on internal database... Using idVendor instead.")
                        self.pendrives[device.get('ID_VENDOR_ID')] = device.device_node
                    else:
                        self.pendrives[device.get('ID_VENDOR')] = device.device_node
                self.after(0, self.update_pendrive_ui, self.pendrives, self.pendrive_dropdown)
                time.sleep(1)  # Sleep for a short duration to reduce CPU usage
        except Exception as e:
            msgbox.showerror("Error", f"Failed to update pendrives: {e}")

    def update_pendrive_ui(self, pendrives, pendrive_dropdown):
        try:
            if pendrives:
                if self.pendrive_var.get() == "":
                    self.pendrive_var.set("Select device")
                pendrive_dropdown['menu'].delete(0, 'end')
                for pendrive, route in pendrives.items():
                    pendrive_dropdown['menu'].add_command(label=pendrive, command=tk._setit(self.pendrive_var, pendrive + " - " + route))
                self.image_label.config(text="Pendrive connected")
                self.connect_button.config(state=tk.NORMAL)
            else:
                self.pendrive_var.set("No pendrives found")
                pendrive_dropdown['menu'].delete(0, 'end')
                pendrive_dropdown['menu'].add_command(label="No pendrives found")
                self.image_label.config(text="Please connect a pendrive")
                self.connect_button.config(state=tk.DISABLED)
        except Exception as e:
            msgbox.showerror("UI Update Error", f"An error occurred while updating the UI: {e}")

    def print_device_node(self):
        try:
            vendor = self.pendrive_var.get()
            device_node = self.pendrives.get(vendor)
            print(device_node)
            # Go to next tab code here
        except Exception as e:
            msgbox.showerror("Device Node Error", f"An error occurred while printing the device node: {e}")

    def disconnect_pendrives(self):
        try:
            context = pyudev.Context()
            devices = context.list_devices(subsystem='block', ID_BUS='usb')
            for device in devices:
                device.unmount()
                device.detach()
        except Exception as e:
            msgbox.showerror("Disconnect Error", f"An error occurred while disconnecting pendrives: {e}")

    def create_checkbox(self, side, text, x_cursor):
        try:
            checkbox_var = tk.IntVar()  # create an IntVar to hold the state of the check-box
            checkbox = ttk.Checkbutton(side, text=text, variable=checkbox_var, cursor=x_cursor)
            checkbox.pack(pady=5, anchor="w")
            self.checkboxes.append((text, checkbox_var))
        except Exception as e:
            msgbox.showerror("Checkbox Creation Error", f"An error occurred while creating a checkbox: {e}")

    def get_selected_options(self):
        try:
            selected_options = []
            selected_options.append("chroot_script") # Add it to be the first executed function
            selected_options.append("add_menu")
            for text, var in self.checkboxes:
                if var.get() == 1:
                    selected_options.append(text.rsplit(' ',1)[0].replace(" ", "_").lower())
            selected_options.append("iso_work") # Added to be the last executed function
            print_green(f"Starting...\n")
            for function in selected_options:
                if function == "iso_work":
                    iso_work_path = self.file_path.get()
                    iso_work(iso_work_path)
                elif '.' in function:
                    #print_green(f"Doing: {function}")
                    function = function.replace(".", "_")
                    function = eval(function)
                    function()
                else:
                    #print_green(f"Doing: {function}")
                    function = eval(function)
                    function()
            if iso_work_path.endswith('.iso'):
                self.tab_control.tab(self.tab3, state="normal")
                self.tab_control.select(self.tab3)
            elif iso_work_path.endswith('.img'):
                self.tab_control.tab(self.tab3, state="normal")
                self.tab_control.select(self.tab3)
        except Exception as e:
            msgbox.showerror("Selection Error", f"An error occurred while getting selected options: {e}")

    def select_file(self):
        try:
            file_path = filedialog.askopenfilename(filetypes=[("Image .iso", "*.iso *.img")])
            if file_path:
                iso_path = file_path
                self.file_path.set(file_path)
                self.select_signature_button.config(state="normal")
        except Exception as e:
            msgbox.showerror("File Selection Error", f"An error occurred while selecting the file: {e}")

    def select_sig(self):
        try:
            sig_path = filedialog.askopenfilename(filetypes=[("Signature .sig", "*.sig")])
            if not sig_path:
                msgbox.showerror("Error", "No signature file selected.")
                return

            sig_publickey = filedialog.askopenfilename(filetypes=[("Public-key .asc", "*.asc *.gpg *.key")])
            if not sig_publickey:
                msgbox.showerror("Error", "No public key file selected.")
                return

            image_path = self.file_path.get()
            if not image_path:
                msgbox.showerror("Error", "No image file selected.")
                return

            # Run GnuPG operations in a separate thread
            thread = threading.Thread(target=self.verify_signature, args=(sig_path, sig_publickey, image_path))
            thread.start()
        except Exception as e:
            msgbox.showerror("Signature Selection Error", f"An error occurred while selecting the signature: {e}")

    def verify_signature(self, sig_path, sig_publickey, image_path):
        try:
            # Import the public key
            with open(sig_publickey, "r") as key_file:
                key_data = key_file.read()
            import_result = self.gpg.import_keys(key_data)
            if not import_result.count:
                self.after(0, lambda: msgbox.showerror("Error", "Failed to import public key."))
                return

            # Set the trust level of the imported key
            fingerprints = import_result.fingerprints
            if fingerprints:
                self.gpg.trust_keys(fingerprints, 'TRUST_FULLY')

            # Verify the image file with the detached signature
            with open(image_path, "rb") as image_file:
                image_data = image_file.read()
            verified = self.gpg.verify_data(sig_path, image_data)

            # Update the UI from the main thread
            self.after(0, self.update_verification_status, verified)
        except Exception as e:
            self.after(0, lambda: msgbox.showerror("GnuPG Error", f"An error occurred during GnuPG operations: {e}"))

    def update_verification_status(self, verified):
        if verified:
            self.verification_label.config(text="Signature is valid.", foreground="green")
            self.tab_control.tab(self.tab2, state="normal")
            self.tab_control.select(self.tab2)
        else:
            self.verification_label.config(text="Signature is not valid.", foreground="red")
            msgbox.showerror("Verification Error", f"Verification failed: {verified.status}")

        if verified:
            print(f"Signature is valid: {verified.username}, {verified.key_id}, {verified.signature_id}, {verified.fingerprint}")
        else:
            print(f"Signature is not valid: {verified.status}")

    def copy_to_clipboard(self, texto):
        try:
            text = texto
            self.clipboard_clear()
            self.clipboard_append(text)
            msgbox.showinfo("Copied", "Copied to clipboard")
        except Exception as e:
            msgbox.showerror("Clipboard Error", f"An error occurred while copying to clipboard: {e}")

    def callback(self, url):
        try:
            webbrowser.open_new(url)
        except Exception as e:
            msgbox.showerror("Browser Error", f"An error occurred while opening the URL: {e}")

if __name__ == '__main__':
    try:
        app = MyApp()
        app.mainloop()
    except Exception as e:
        msgbox.showerror("Application Error", f"An error occurred while running the application: {e}")
