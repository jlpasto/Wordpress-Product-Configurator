import csv
import logging
import os


def read_color_csv(file_path, delimiter=';'):
    couleur_list = []
    rgba_color_list = []
    couleur_rgba_dict = {}

    try:
        # Check if file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(file_path, 'r', newline='', encoding='utf-8-sig') as csvfile:
            try:
                reader = csv.DictReader(csvfile, delimiter=delimiter)
                print("Detected columns:", reader.fieldnames)

                # Check if required columns exist
                if 'Couleur' not in reader.fieldnames or 'RGBA' not in reader.fieldnames:
                    raise KeyError("CSV must contain 'Couleur' and 'RGBA' columns.")

                for row in reader:
                    couleur = str(row['Couleur']).strip()
                    rgba = str(row['RGBA']).strip()
                    couleur_list.append(couleur)
                    rgba_color_list.append(rgba)
                    couleur_rgba_dict[couleur] = rgba  # ✅ key-value pair

                logging.info(f"Successfully read {len(couleur_list)} color entries from {file_path}")

            except csv.Error as e:
                logging.error(f"CSV parsing error: {e}")
                raise ValueError(f"CSV parsing error: {e}")

    except FileNotFoundError as e:
        logging.error(e)
        print(f"Error: {e}")
    except KeyError as e:
        logging.error(e)
        print(f"Error: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        print(f"Unexpected error: {e}")

    return couleur_list, rgba_color_list, couleur_rgba_dict


# # Example usage
# if __name__ == "__main__":
#     file_path = '../correspondance_rgba.csv'  # replace with your CSV file path
#     couleur_list, rgba_color_list = read_color_csv(file_path)

#     # Export the lists to be used in other scripts
#     print("couleur_list =", couleur_list)
#     print("rgba_color_list =", rgba_color_list)
