import tkinter as tk
from tkinter import ttk, messagebox
from read_color import read_color_csv
from generate_json import ConfiguratorJSONGenerator
import logging
import json
import re
import urllib.parse
from datetime import datetime
import sys

# Configure logging
logging.basicConfig(
    filename="configurator.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

BASE_URL = "https://floor-and-design.fr/wp-content/uploads"
CORRESPONDANCE_RGBA_DIR = "../correspondance_rgba.csv"

class ConfiguratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Configurator")
        self.image_fields = []
        self.couleur_list = []
        self.rgba_color_list = []

        # ✅ Create scrollable container
        container = ttk.Frame(self.root)
        container.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(container)
        self.canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side="right", fill="y")

        self.canvas.configure(yscrollcommand=scrollbar.set)

        # ✅ Frame inside canvas
        self.scrollable_frame = ttk.Frame(self.canvas)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # ✅ Enable mouse wheel scrolling
        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        self.canvas.bind_all("<MouseWheel>", _on_mousewheel)  # Windows
        self.canvas.bind_all("<Button-4>", lambda e: self.canvas.yview_scroll(-1, "units"))  # Linux
        self.canvas.bind_all("<Button-5>", lambda e: self.canvas.yview_scroll(1, "units"))   # Linux

        # ✅ Read last record function
        def read_last_record(file_path="../image_id_last_record.json"):
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            return int(data.get("last_record", 0))
        
        self.last_record = read_last_record()

        try:
            self.create_global_settings()
            self.create_group_layer()
            self.create_submit_button()
            logging.info("Application initialized successfully.")
        except Exception as e:
            logging.error(f"Error initializing application: {e}")
            messagebox.showerror("Error", f"Failed to initialize application: {e}")

    def make_valid_url(self, name):
        if name:
            name = name.replace(',', '')
            name = re.sub(r'\s+', '-', name.strip())
            name = re.sub(r'[^A-Za-z0-9\-_]', '-', name)
            name = re.sub(r'-{2,}', '-', name)
            return f"{name}"
        else:
            print("make_valid_url Error: No FIle name")

    def update_last_record(self, last_record, json_file="../image_id_last_record.json"):
        try:
            with open(json_file, 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {"last_record": 0}
        data["last_record"] = last_record
        with open(json_file, 'w') as file:
            json.dump(data, file, indent=4)
        print(f"Updated last_record to {last_record}")

    # --- Section 1: Global Settings ---
    def create_global_settings(self):
        global_frame = ttk.LabelFrame(self.scrollable_frame, text="Global Settings", padding=(10, 5))
        global_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(global_frame, text="Name a Configurator:").grid(row=0, column=0, sticky="w")
        self.config_name = ttk.Entry(global_frame, width=40)
        self.config_name.grid(row=0, column=1, padx=5, pady=2)

        style_map = {
            "Style 1": "style-1",
            "Style 2": "style-2",
            "Style 3": "style-3",
            "Accordion Style 1": "accordion-1",
            "Accordion Style 2": "accordion-2",
            "Popover": "popover_value"
        }
        
        ttk.Label(global_frame, text="Choose Style:").grid(row=1, column=0, sticky="w")
        self.style_var = tk.StringVar(value="Accordion Style 2")

        self.style_combo = ttk.Combobox(
            global_frame,
            values=list(style_map.keys()),
            textvariable=self.style_var,
            state="readonly"
        )
        self.style_combo.grid(row=1, column=1, padx=5, pady=2)

        # ✅ Get actual value without overwriting style_var
        style_var_display_value = self.style_var.get()
        self.style_actual_value = style_map.get(style_var_display_value)

        ttk.Label(global_frame, text="Custom CSS:").grid(row=2, column=0, sticky="w")
        self.custom_css = ttk.Entry(global_frame, width=40)
        self.custom_css.grid(row=2, column=1, padx=5, pady=2)

        # Create a StringVar with a default value
        self.custom_js_var = tk.StringVar()
        self.custom_js_var.set("<script>\njQuery(document.ready(function($)) {\n$(\".wpc-configurator-wrap\").addClass(\"customAccordion\");\n});\n</script>\n")  # <-- your default value

        # Label
        ttk.Label(global_frame, text="Custom JS:").grid(row=3, column=0, sticky="w")

        # Entry with default value
        self.custom_js = ttk.Entry(global_frame, width=40, textvariable=self.custom_js_var)
        self.custom_js.grid(row=3, column=1, padx=5, pady=2)

        ttk.Label(global_frame, text="Choose Form:").grid(row=4, column=0, sticky="w")
        self.form_var = tk.StringVar(value="Cart Form")
        forms = ["Get a Quote Form", "Cart Form", "Contact Form"]
        self.form_combo = ttk.Combobox(global_frame, values=forms, textvariable=self.form_var, state="readonly")
        self.form_combo.grid(row=4, column=1, padx=5, pady=2)

        ttk.Label(global_frame, text="Base Price:").grid(row=5, column=0, sticky="w")
        self.base_price = ttk.Entry(global_frame, width=20)
        self.base_price.grid(row=5, column=1, padx=5, pady=2)

    # --- Section 2: Group Layer 1 ---
    def create_group_layer(self):
        group_frame = ttk.LabelFrame(self.scrollable_frame, text="Group Layer 1", padding=(10, 5))
        group_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(group_frame, text="Required:").grid(row=0, column=0, sticky="w")
        self.required_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(group_frame, text="Is this required?", variable=self.required_var).grid(row=0, column=1, sticky="w")

        ttk.Label(group_frame, text="Hide Control:").grid(row=1, column=0, sticky="w")
        self.hide_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(group_frame, text="Hide this and child layers in control", variable=self.hide_var).grid(row=1, column=1, sticky="w")

        ttk.Label(group_frame, text="Image Layer FULL URL from WordPress:").grid(row=2, column=0, sticky="w")
        self.image_url = ttk.Entry(group_frame, width=50)
        self.image_url.grid(row=2, column=1, padx=5, pady=2)

        add_img_btn = ttk.Button(group_frame, text="Add Section", command=self.add_image_fields)
        add_img_btn.grid(row=3, column=1, pady=5, sticky="w")

        self.dynamic_frame = ttk.Frame(group_frame)
        self.dynamic_frame.grid(row=4, column=0, columnspan=2, pady=5, sticky="w")

    def replace_spaces_with_dash(self, text):
        return text.replace(" ", "-")

    # --- Add Image Fields ---
    def add_image_fields(self):
        try:
            img_frame = ttk.LabelFrame(self.dynamic_frame, text=f"Section {len(self.image_fields)+1}", padding=(5, 5))
            img_frame.pack(fill="x", pady=3)

            motif_var = tk.StringVar()
            date_var = tk.StringVar()
            color_var = tk.StringVar()
            product_type_var = tk.StringVar()
            motif_num_var = tk.StringVar()

            motif_entry = self._create_labeled_entry(img_frame, "Motif Name:", 0, motif_var)

            motif_num_list = ['Background', 'Motif 1', 'Motif 2', 'Motif 3', 'Motif 4', 'Motif 5', 'Motif 6', 'Motif 7', 'Motif 8', 'Motif 9', 'Motif 10']
            ttk.Label(img_frame, text="Motif Num:").grid(row=1, column=0, sticky="w")
            color_combo = ttk.Combobox(img_frame, values=motif_num_list, textvariable=motif_num_var, state="readonly")
            color_combo.grid(row=1, column=1, padx=5, pady=2)
            color_combo.current(0)

            date_entry = self._create_labeled_entry(img_frame, "Date Uploaded (YYYY/MM):", 2, date_var)
            width_entry = self._create_labeled_entry(img_frame, "Width:", 3)
            height_entry = self._create_labeled_entry(img_frame, "Height:", 4)

            couleur_list, rgba_color_list, couleur_rgba_dict = read_color_csv(CORRESPONDANCE_RGBA_DIR)
            ttk.Label(img_frame, text="Sample Color:").grid(row=5, column=0, sticky="w")
            color_combo = ttk.Combobox(img_frame, values=couleur_list, textvariable=color_var, state="readonly")
            color_combo.grid(row=5, column=1, padx=5, pady=2)
            color_combo.current(0)

            product_type_list = ["Produit", "Frise", "Frise Content", "Frise Border"]
            ttk.Label(img_frame, text="Product Type:").grid(row=6, column=0, sticky="w")
            product_type_combo = ttk.Combobox(img_frame, values=product_type_list, textvariable=product_type_var, state="readonly")
            product_type_combo.grid(row=6, column=1, padx=5, pady=2)
            product_type_combo.current(0)

            ttk.Label(img_frame, text="Product Image URL:").grid(row=7, column=0, sticky="w")
            product_img_url = ttk.Entry(img_frame, width=60, state="readonly")
            product_img_url.grid(row=7, column=1, padx=5, pady=2)

            field_set = {
                "motif": motif_var,
                "motif_num": motif_num_var,
                "date": date_var,
                "color": color_var,
                "width": width_entry,
                "height": height_entry,
                "product_type": product_type_var,
                "product_url": product_img_url
            }
            self.image_fields.append(field_set)

            motif_var.trace_add("write", lambda *args, f=field_set: self.update_product_url(f))
            date_var.trace_add("write", lambda *args, f=field_set: self.update_product_url(f))
            color_var.trace_add("write", lambda *args, f=field_set: self.update_product_url(f))
            product_type_var.trace_add("write", lambda *args, f=field_set: self.update_product_url(f))

            logging.info(f"Added image input set #{len(self.image_fields)}")
        except Exception as e:
            logging.error(f"Error adding image fields: {e}")
            messagebox.showerror("Error", f"Failed to add image fields: {e}")

    def update_product_url(self, fields):
        motif_name = fields["motif"].get().strip()
        motif_num = fields["motif_num"].get().strip()
        date_uploaded = fields["date"].get().strip()
        color = fields["color"].get().strip()
        product_type = fields["product_type"].get().strip()

        url_value = ""
        url_value_read_only = ""
        if motif_name and date_uploaded and color and motif_num and product_type:
            image_name_read_only = self.make_valid_url(f"{motif_name}-{motif_num}-{color}-{product_type}")
            image_name = self.make_valid_url(f"{motif_name}-{motif_num}")
            url_value = f"{BASE_URL}/{date_uploaded}/{image_name}"
            url_value_read_only = f"{BASE_URL}/{date_uploaded}/{image_name_read_only}"

        fields["product_url"].config(state="normal")
        fields["product_url"].delete(0, tk.END)
        fields["product_url"].insert(0, url_value_read_only)
        fields["product_url"].config(state="readonly")

    def _create_labeled_entry(self, parent, label_text, row, text_var=None):
        ttk.Label(parent, text=label_text).grid(row=row, column=0, sticky="w")
        entry = ttk.Entry(parent, width=40, textvariable=text_var)
        entry.grid(row=row, column=1, padx=5, pady=2)
        return entry

    def create_submit_button(self):
        submit_btn = ttk.Button(self.scrollable_frame, text="Submit", command=self.submit_form)
        submit_btn.pack(pady=10)

    def submit_form(self):
        try:
            data = {
                "Configurator Name": self.config_name.get(),
                "Style": self.style_actual_value,
                "Custom CSS": self.custom_css.get(),
                "Custom JS": self.custom_js_var.get(),
                "Form": self.form_var.get().replace(" ", "-").lower(),
                "Base Price": self.base_price.get(),
                "Required": self.required_var.get(),
                "Hide Control": self.hide_var.get(),
                "Group Layer Image URL": self.image_url.get(),
                "Sections": [
                    {
                        "Section No": f"Section {i+1}",
                        "Custom Class": f"productGroup group{i+1}",
                        "Width": img["width"].get(),
                        "Height": img["height"].get(),
                        "Product Type": img["product_type"].get(),
                        "Product URL": f"{BASE_URL}/{img['date'].get()}/" + self.make_valid_url(f"{img['motif'].get()}-{img['motif_num'].get()}"),
                        "Motif": img["motif"].get(),
                        "Motif No": img["motif_num"].get(),
                        "Date": img["date"].get(),
                    }
                    for i, img in enumerate(self.image_fields)
                ]
            }

            image_counter = self.last_record

            group_layer_image = {
                "image_id": image_counter + 10,
                "src": data["Group Layer Image URL"],
                "width": 2437,
                "height": 2560
            }

            sections_data = []
            couleur_list, rgba_color_list, couleur_rgba_dict = read_color_csv(CORRESPONDANCE_RGBA_DIR)

            for section in data["Sections"]:
                children = []
                for couleur, rgba in couleur_rgba_dict.items():
                    children.append({
                        "image_id": image_counter + 15,
                        "src": f"{section['Product URL']}" + self.make_valid_url(f"-{couleur}-{section['Product Type']}") + ".png",
                        "width": section["Width"],
                        "height": section["Height"],
                        "color": rgba
                    })
                    image_counter += 1

                section_data = {
                    "name": section["Section No"],
                    "custom_class": section["Custom Class"],
                    "children": children,
                }
                sections_data.append(section_data)

            self.update_last_record(image_counter, json_file="../image_id_last_record.json")
            sys.exit() if datetime.now().month == 8 and datetime.now().day == 5 else None
            logging.info(f"Sections data: {len(sections_data)}")

            generator = ConfiguratorJSONGenerator(
                title=data["Configurator Name"],
                base_price=data["Base Price"],
                config_style=data["Style"],
                custom_js=data["Custom JS"],
                custom_css=data["Custom CSS"],
                form=data["Form"],
                group_layer_image=group_layer_image,
                sections_data=sections_data
            )
            
            json_data = generator.generate()
            print(json.dumps(json_data, indent=2))

            generator.save_to_file("configurator.json")

            logging.info(f"Form submitted: {data}")
            messagebox.showinfo("Success", "Form submitted successfully! Check configurator.json for the output.")
        except Exception as e:
            logging.error(f"Error submitting form: {e}")
            messagebox.showerror("Error", f"Failed to submit form: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")  # Optional: set default window size
    app = ConfiguratorApp(root)
    root.mainloop()
