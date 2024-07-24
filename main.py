import tkinter as tk
from tkinter import messagebox, scrolledtext
import json
import jsonschema
from genson import SchemaBuilder

# Function to generate JSON schema
def generate_schema(json_data):
    try:
        data = json.loads(json_data)
        builder = SchemaBuilder()
        builder.add_object(data)
        schema = builder.to_schema()
        return schema
    except json.JSONDecodeError as e:
        messagebox.showerror("Error", f"Invalid JSON: {e}")
    except Exception as e:
        messagebox.showerror("Error", f"Schema generation failed: {e}")
    return None

# Function to validate JSON against schema
def validate_json(json_data, schema):
    try:
        data = json.loads(json_data)
        validator = jsonschema.Draft7Validator(schema)
        errors = list(validator.iter_errors(data))
        if errors:
            error_messages = "\n".join(str(e.message) for e in errors)
            messagebox.showerror("Validation Errors", error_messages)
        else:
            messagebox.showinfo("Success", "JSON is valid!")
    except json.JSONDecodeError as e:
        messagebox.showerror("Error", f"Invalid JSON: {e}")
    except Exception as e:
        messagebox.showerror("Error", f"Validation failed: {e}")

# Function to handle the Generate Schema button
def on_generate_schema():
    json_data = json_input.get("1.0", tk.END).strip()
    schema = generate_schema(json_data)
    if schema:
        schema_output.delete("1.0", tk.END)
        schema_output.insert(tk.END, json.dumps(schema, indent=4))

# Function to handle the Validate JSON button
def on_validate_json():
    json_data = json_input.get("1.0", tk.END).strip()
    schema = schema_output.get("1.0", tk.END).strip()
    try:
        schema = json.loads(schema)
        validate_json(json_data, schema)
    except json.JSONDecodeError as e:
        messagebox.showerror("Error", f"Invalid Schema: {e}")

# Main window setup
root = tk.Tk()
root.title("JSON Schema Generator")

# Input JSON text area
tk.Label(root, text="Input JSON:").pack()
json_input = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=10)
json_input.pack()

# Buttons
tk.Button(root, text="Generate Schema", command=on_generate_schema).pack()
tk.Button(root, text="Validate JSON", command=on_validate_json).pack()

# Output schema text area
tk.Label(root, text="Generated Schema:").pack()
schema_output = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=10)
schema_output.pack()

# Run the application
root.mainloop()
