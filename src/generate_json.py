import json
import uuid

class ConfiguratorJSONGenerator:
    def __init__(self, title, base_price, config_style, form, group_layer_image, sections_data):
        self.title = title
        self.base_price = base_price
        self.config_style = config_style
        self.form = form
        self.group_layer_image = group_layer_image  # dict: image_id, src, width, height
        self.sections_data = sections_data  # list of sections
        self.editor_images = {}

    def _generate_uid(self):
        return uuid.uuid4().hex[:4] + "-" + uuid.uuid4().hex[:4]

    def _build_group_layer(self):
        group_layer_uid = self._generate_uid()
        child_uid = self._generate_uid()

        # Add to editor images
        self.editor_images[str(self.group_layer_image["image_id"])] = {
            "uid": child_uid,
            "key": "image",
            "src": self.group_layer_image["src"],
            "width": self.group_layer_image["width"],
            "height": self.group_layer_image["height"]
        }

        return {
            "name": "Group Layer 1",
            "uid": group_layer_uid,
            "type": "group",
            "actions": {"open": True, "show": True, "lock": False},
            "children": [
                {
                    "name": "Image 1",
                    "uid": child_uid,
                    "type": "image",
                    "actions": {"open": False, "show": True, "lock": False},
                    "settings": {
                        "control_type": "icon",
                        "active": True,
                        "views": {"front": {"image": self.group_layer_image["image_id"]}}
                    }
                }
            ],
            "settings": {
                "control_type": "icon",
                "required": True,
                "hide_control": True
            }
        }

    def _build_sections(self):
        sections = []
        for section in self.sections_data:
            section_uid = self._generate_uid()
            children_list = []

            for idx, img in enumerate(section["children"], start=1):
                child_uid = self._generate_uid()
                children_list.append({
                    "name": f"Image {idx}",
                    "uid": child_uid,
                    "type": "image",
                    "actions": {"open": False, "show": False},
                    "settings": {
                        "control_type": "color",
                        "views": {"front": {"image": img["image_id"]}},
                        "color": img["color"]
                    }
                })

                # Add to editor images
                self.editor_images[str(img["image_id"])] = {
                    "uid": child_uid,
                    "key": "image",
                    "src": img["src"],
                    "width": img["width"],
                    "height": img["height"]
                }

            sections.append({
                "name": section["name"],
                "uid": section_uid,
                "type": "group",
                "actions": {"open": True, "show": True},
                "children": children_list,
                "settings": {
                    "custom_class": section["custom_class"],
                    "control_type": "icon"
                }
            })
        return sections

    def generate(self):
        components = [self._build_group_layer()] + self._build_sections()

        config_data = {
            "title": self.title,
            "type": "amz_configurator",
            "settings": {
                "_wpc_data_version": "3.4",
                "_wpc_config_style": self.config_style,
                "_wpc_form": "cart-form",
                "_wpc_base_price": self.base_price,
                "_wpc_components": components,
                "_wpc_editor_images": self.editor_images
            }
        }
        return config_data

    def save_to_file(self, filename):
        data = self.generate()
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"✅ JSON saved to {filename}")
