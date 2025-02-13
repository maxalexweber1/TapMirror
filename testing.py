import json

def load_layout_config():
    """Loads the layout configuration from a JSON file and validates it."""
    try:
        with open("layout_config.json", "r") as file:
            config = json.load(file)
            print("✅ Erfolgreich geladen:", json.dumps(config, indent=4))  # Debugging
            return config
    except json.JSONDecodeError as e:
        print(f"❌ JSON-Fehler: {e}")
        return {}
    except Exception as e:
        print(f"❌ Fehler beim Laden von layout_config.json: {e}")
        return {}