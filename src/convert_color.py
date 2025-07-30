import csv
import sys
import logging
import os

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def hex_to_rgba(hex_color, alpha=1.0):
    try:
        # Remove leading '#' if present
        hex_color = hex_color.strip().lstrip('#')

        # Convert shorthand (#FFF) to full (#FFFFFF)
        if len(hex_color) == 3:
            hex_color = ''.join([c * 2 for c in hex_color])

        if len(hex_color) != 6:
            raise ValueError(f"Invalid hex color: {hex_color}")

        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)

        return f"rgba({r}, {g}, {b}, {alpha})"
    except Exception as e:
        logging.error(f"Error converting {hex_color} to RGBA: {e}")
        return "rgba(0,0,0,1)"  # Default to black if error


def process_csv(input_file, col_hexacolor, delimiter=';'):
    try:
        if not os.path.exists(input_file):
            logging.error(f"File {input_file} does not exist.")
            return

        output_file = "../correspondance_rgba.csv"

        with open(input_file, 'r', newline='', encoding='utf-8') as infile, \
                open(output_file, 'w', newline='', encoding='utf-8') as outfile:

            reader = csv.DictReader(infile, delimiter=delimiter)
            fieldnames = reader.fieldnames + ['RGBA']

            if col_hexacolor not in reader.fieldnames:
                logging.error(f"Column '{col_hexacolor}' not found in CSV headers.")
                return

            writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter=delimiter)
            writer.writeheader()

            for row in reader:
                hex_color = row[col_hexacolor]
                rgba_value = hex_to_rgba(hex_color)
                row['RGBA'] = rgba_value
                writer.writerow(row)

        logging.info(f"Processing complete. Output saved to {output_file}")

    except Exception as e:
        logging.error(f"Error processing CSV: {e}")


if __name__ == "__main__":
    input_csv = "../correspondance.csv"
    col_hexacolor = "Code"
    delimiter = ";"

    process_csv(input_csv, col_hexacolor, delimiter)
