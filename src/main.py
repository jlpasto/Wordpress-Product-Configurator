import tkinter as tk
from tkinter import ttk, messagebox
from read_color import read_color_csv
from generate_json import ConfiguratorJSONGenerator
import logging
import json

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

        #couleur_list, rgba_color_list, couleur_rgba_dict = read_color_csv(CORRESPONDANCE_RGBA_DIR)
        # self.couleur_list = couleur_list
        # self.rgba_color_list = rgba_color_list
        # self.couleur_rgba_dict = couleur_rgba_dict
        

        try:
            self.create_global_settings()
            self.create_group_layer()
            self.create_submit_button()
            logging.info("Application initialized successfully.")
        except Exception as e:
            logging.error(f"Error initializing application: {e}")
            messagebox.showerror("Error", f"Failed to initialize application: {e}")

    # --- Section 1: Global Settings ---
    def create_global_settings(self):
        global_frame = ttk.LabelFrame(self.root, text="Global Settings", padding=(10, 5))
        global_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(global_frame, text="Name a Configurator:").grid(row=0, column=0, sticky="w")
        self.config_name = ttk.Entry(global_frame, width=40)
        self.config_name.grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(global_frame, text="Choose Style:").grid(row=1, column=0, sticky="w")
        self.style_var = tk.StringVar(value="Accordion Style 2")
        styles = ["Style 1", "Style 2", "Style 3", "Accordion Style 1", "Accordion Style 2", "Popover"]
        self.style_combo = ttk.Combobox(global_frame, values=styles, textvariable=self.style_var, state="readonly")
        self.style_combo.grid(row=1, column=1, padx=5, pady=2)

        ttk.Label(global_frame, text="Custom CSS:").grid(row=2, column=0, sticky="w")
        self.custom_css = ttk.Entry(global_frame, width=40)
        self.custom_css.grid(row=2, column=1, padx=5, pady=2)

        ttk.Label(global_frame, text="Custom JS:").grid(row=3, column=0, sticky="w")
        self.custom_js = ttk.Entry(global_frame, width=40)
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
        group_frame = ttk.LabelFrame(self.root, text="Group Layer 1", padding=(10, 5))
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
            motif_num_var = tk.StringVar()

            motif_entry = self._create_labeled_entry(img_frame, "Motif Name:", 0, motif_var)

            # Motif Num Dropdown
            motif_num_list = ['Background', 'Motif 1', 'Motif 2', 'Motif 3', 'Motif 4', 'Motif 5', 'Motif 6', 'Motif 7', 'Motif 8', 'Motif 9', 'Motif 10']

            ttk.Label(img_frame, text="Motif Num:").grid(row=1, column=0, sticky="w")
            color_combo = ttk.Combobox(img_frame, values=motif_num_list, textvariable=motif_num_var, state="readonly")
            color_combo.grid(row=1, column=1, padx=5, pady=2)
            color_combo.current(0)  # Default to Background


            date_entry = self._create_labeled_entry(img_frame, "Date Uploaded (YYYY/MM):", 2, date_var)
            width_entry = self._create_labeled_entry(img_frame, "Width:", 3)
            height_entry = self._create_labeled_entry(img_frame, "Height:", 4)

            # Color Dropdown
            couleur_list, rgba_color_list, couleur_rgba_dict = read_color_csv(CORRESPONDANCE_RGBA_DIR)
            ttk.Label(img_frame, text="Sample Color:").grid(row=5, column=0, sticky="w")
            color_combo = ttk.Combobox(img_frame, values=couleur_list, textvariable=color_var, state="readonly")
            color_combo.grid(row=5, column=1, padx=5, pady=2)
            color_combo.current(0)  # Default to first color

            # Product Image URL (readonly)
            ttk.Label(img_frame, text="Product Image URL:").grid(row=6, column=0, sticky="w")
            product_img_url = ttk.Entry(img_frame, width=60, state="readonly")
            product_img_url.grid(row=6, column=1, padx=5, pady=2)

            field_set = {
                "motif": motif_var,
                "motif_num" : motif_num_var,
                "date": date_var,
                "color": color_var,
                "width": width_entry,
                "height": height_entry,
                "product_url": product_img_url
            }
            self.image_fields.append(field_set)

            # Trace updates (motif, date, color)
            motif_var.trace_add("write", lambda *args, f=field_set: self.update_product_url(f))
            date_var.trace_add("write", lambda *args, f=field_set: self.update_product_url(f))
            color_var.trace_add("write", lambda *args, f=field_set: self.update_product_url(f))

            logging.info(f"Added image input set #{len(self.image_fields)}")
        except Exception as e:
            logging.error(f"Error adding image fields: {e}")
            messagebox.showerror("Error", f"Failed to add image fields: {e}")

    # --- Auto-update Product Image URL ---
    def update_product_url(self, fields):
        motif_name = fields["motif"].get().strip()
        motif_num = fields["motif_num"].get().strip()
        date_uploaded = fields["date"].get().strip()
        color = fields["color"].get().strip()
        #image_name = self.replace_spaces_with_dash(f"{motif_name}-{motif_num}-{color}.png")
        image_name = self.replace_spaces_with_dash(f"{motif_name}-{motif_num}")

        url_value = ""
        if motif_name and date_uploaded and color and motif_num:
            url_value = f"{BASE_URL}/{date_uploaded}/{image_name}"

        fields["product_url"].config(state="normal")
        fields["product_url"].delete(0, tk.END)
        fields["product_url"].insert(0, url_value)
        fields["product_url"].config(state="readonly")


    def _create_labeled_entry(self, parent, label_text, row, text_var=None):
        ttk.Label(parent, text=label_text).grid(row=row, column=0, sticky="w")
        entry = ttk.Entry(parent, width=40, textvariable=text_var)
        entry.grid(row=row, column=1, padx=5, pady=2)
        return entry

    def create_submit_button(self):
        submit_btn = ttk.Button(self.root, text="Submit", command=self.submit_form)
        submit_btn.pack(pady=10)

    def submit_form(self):
        try:
            data = {
                "Configurator Name": self.config_name.get(),
                "Style": self.style_var.get(),
                "Custom CSS": self.custom_css.get(),
                "Custom JS": self.custom_js.get(),
                "Form": self.form_var.get(),
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
                        "Product URL": f"{BASE_URL}/{img["date"].get()}/{img["motif"].get()}-{img["motif_num"].get()}".replace(" ", "-"),
                        "Motif": img["motif"].get(),
                        "Motif No": img["motif_num"].get(),
                        "Date": img["date"].get(),
                    }
                    for i, img in enumerate(self.image_fields)
                ]
            }




            group_layer_image = {
                "image_id": 100000,
                "src": data["Group Layer Image URL"],
                "width": 2437, # change this use variable
                "height": 2560
            }

            sections_data = []
            couleur_list, rgba_color_list, couleur_rgba_dict = read_color_csv(CORRESPONDANCE_RGBA_DIR)
            # Loop through data_list and build sections_data
            for section in data["Sections"]:
                section = {
                    "name": section["Section No"],
                    "custom_class": section["Custom Class"],
                    "children": [
                        {"image_id": 100000 + j, 
                         "src": f"{section["Product URL"]}-{couleur}.png", 
                         "width": f"{section["Width"]}", 
                         "height":  f"{section["Height"]}", 
                         "color": rgba}
                        for j, (couleur, rgba) in enumerate(couleur_rgba_dict.items())  # ✅ iterate key-value pairs
                    ],
    
                }
                sections_data.append(section)

            logging.info(f"Sections data: {len(sections_data)}")

            generator = ConfiguratorJSONGenerator(
                title=data["Configurator Name"],
                base_price=data["Base Price"],
                config_style=data["Custom CSS"],
                form = data["Form"], 
                group_layer_image=group_layer_image,
                sections_data=sections_data
                )
            
            # ✅ Generate JSON data
            json_data = generator.generate()
            print(json.dumps(json_data, indent=2))

            # ✅ Save to file
            generator.save_to_file("configurator.json")

            logging.info(f"Form submitted: {data}")
            messagebox.showinfo("Success", "Form submitted successfully! Check configurator.log for details.")
        except Exception as e:
            logging.error(f"Error submitting form: {e}")
            messagebox.showerror("Error", f"Failed to submit form: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = ConfiguratorApp(root)
    root.mainloop()
