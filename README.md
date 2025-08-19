# 🏆 Case Study: Automating Product Data Import for Sarl Floor and Design

## 🏢 Client Overview

**Company:** Sarl Floor and Design  
**Industry:** Flooring & Interior Design  
**Website:** [floor-and-design.fr](https://floor-and-design.fr)

---

## 🚩 Problem Overview

Sarl Floor and Design needed a streamlined, error-free process to:

- **Import product data** into their Wordpress-based e-commerce site.
- **Apply and manage color variants** for each product, ensuring accurate display and selection for customers.
- **Reduce manual work** and minimize human error in product configuration.

---

## 💡 Solution

We developed a **Python-based automation toolkit** that:

- Reads product and color data from CSV files.
- Generates JSON configuration files compatible with the Wordpress Product Configurator plugin.
- Provides a user-friendly GUI for staff to manage products, images, and color options.
- Ensures consistent naming, URL generation, and color mapping.

---

## 🛠️ Key Features

### 1. **Automated Data Import**
- Reads product and color data from CSV files (`correspondance.csv`, `correspondance_rgba.csv`).
- Converts hex color codes to RGBA for accurate color rendering.

### 2. **GUI Configurator**
- Built with `tkinter` for easy use by non-technical staff.
- Allows entry of product details, image URLs, and color selection.
- Automatically generates valid URLs and product image paths.

### 3. **JSON Generation**
- Produces a `configurator.json` file ready for Wordpress import.
- Ensures all product variants and color options are included.

### 4. **Error Handling & Logging**
- Robust error handling with user-friendly messages.
- Logs all operations to `configurator.log` for traceability.

---

## 🖥️ How It Works

1. **Prepare CSV Files:**  
   - List all products and color codes in `correspondance.csv`.
   - Use `convert_color.py` to generate `correspondance_rgba.csv` with RGBA values.

2. **Run the GUI:**  
   - Launch `main.py` to open the Configurator App.
   - Enter product details, select colors, and review generated URLs.

3. **Generate JSON:**  
   - Submit the form to create `configurator.json`.
   - Import this file into the Wordpress Product Configurator plugin.

---

## 📦 Folder Structure

```
src/
├── configurator.json
├── configurator.log
├── convert_color.py
├── generate_json.py
├── main.py
├── read_color.py
├── __pycache__/
```
- **convert_color.py:** Converts hex color codes to RGBA.
- **read_color.py:** Reads color data from CSV.
- **main.py:** GUI application for product configuration.
- **generate_json.py:** Generates the final JSON for Wordpress import.

---

## 🚀 Impact

- **⏱️ Time Saved:** Reduced manual product setup from hours to minutes.
- **🎨 Consistency:** Ensured all color variants are accurately represented.
- **🔒 Reliability:** Minimized errors and improved data integrity.
- **🧑‍💼 Usability:** Empowered non-technical staff to manage products efficiently.

---

## 📝 Usage Example

```sh

# 1. Launch the GUI
python src/main.py

# 2. Import the generated configurator.json into Wordpress
```

---

## 📞 Contact
**Developer:** Jhon Loyd Pastorin  
**Email:** [jhonloydpastorin.03@gmail.com](mailto:jhonloydpastorin.03@gmail.com)  
**LinkedIn:** [Jhon Loyd Pastorin](www.linkedin.com/in/jhon-loyd-pastorin-a84000107)  
**Portfolio:** [jlpasto-portfolio.vercel.app](https://jlpasto-portfolio.vercel.app)  


