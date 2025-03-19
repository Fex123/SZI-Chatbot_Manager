import customtkinter as ctk
from tkinter import filedialog
from api_connection import WissensbasisAPI  
import os
import json

def choose_file():
    # Open a file dialog to select one or more files
    file_paths = filedialog.askopenfilenames(
        title="Wähle eine oder mehrere Dateien",
        filetypes=[
            ("Markdown files", "*.md"),
            ("Text files", "*.txt"),
            ("PDF files", "*.pdf"),
            ("Word files", "*.doc;*.docx")
        ]
    )
    if file_paths:
        file_entry.delete(0, ctk.END)
        file_entry.insert(0, ";".join(file_paths))
        status_label.configure(text="Dateien ausgewählt.", text_color="#1f6feb")

def upload_file():
    # Process file upload and update status based on the API response
    dataset_id = kb_id_entry.get().strip()
    api_key = api_key_entry.get().strip()  # Get API Key from new field
    files_text = file_entry.get().strip()
    
    if not dataset_id or not files_text or not api_key:
        status_label.configure(text="Fehler: Wissensbasis-ID, API Key und Datei erforderlich!", text_color="#DC3545")
        return

    # Save the new dataset ID and API Key permanently
    save_config({"dataset_id": dataset_id, "api_key": api_key})

    status_label.configure(text="Dateien werden hochgeladen...", text_color="#FD7E14")
    root.update()
    
    api = WissensbasisAPI(api_key=api_key)  # Use entered API key
    file_paths = [fp.strip() for fp in files_text.split(";") if fp.strip()]
    all_success = True
    for file_path in file_paths:
        response = api.create_document_by_file(dataset_id, file_path)
        if not response:
            all_success = False
    
    if all_success:
        status_label.configure(text="Alle Uploads erfolgreich!", text_color="#198754")
        file_entry.delete(0, ctk.END)
        file_entry.insert(0, "Keine Datei ausgewählt")
    else:
        status_label.configure(text="Mindestens ein Upload fehlgeschlagen!", text_color="#DC3545")

# Add helper function to get a writable config path
def get_config_path():
    import os
    appdata = os.getenv("APPDATA")
    config_folder = os.path.join(appdata, "SZI-Assistent")
    if not os.path.exists(config_folder):
        os.makedirs(config_folder)
    return os.path.join(config_folder, "config.json")

# Modify load_config() to use the writable path
def load_config():
    config_path = get_config_path()
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            return json.load(f)
    return {}

# Modify save_config() to use the writable path
def save_config(config):
    config_path = get_config_path()
    with open(config_path, "w") as f:
        json.dump(config, f)

# Create and configure the main application window, then run the GUI loop
root = ctk.CTk()
root.title("SZI Assistent - Dokumenten Upload")
root.geometry("600x500")  # increased height to prevent bottom cutoff
root.resizable(False, False)

main_frame = ctk.CTkFrame(root, corner_radius=15)
main_frame.pack(pady=20, padx=20, fill="both", expand=True)

header_label = ctk.CTkLabel(main_frame, text="SZI Assistent", font=("Arial", 24, "bold"))
header_label.pack(pady=(20, 10))

kb_id_label = ctk.CTkLabel(main_frame, text="Wissensbasis-ID:")
kb_id_label.pack(pady=(10, 0))
# Added show parameter to mask the dataset id
kb_id_entry = ctk.CTkEntry(main_frame, width=250, placeholder_text="Geben Sie die Wissensbasis-ID ein", show="*")
kb_id_entry.pack(pady=(0, 10))

# New API Key input field with masked text
api_key_label = ctk.CTkLabel(main_frame, text="API Key:")
api_key_label.pack(pady=(10, 0))
api_key_entry = ctk.CTkEntry(main_frame, width=250, placeholder_text="Enter your API Key", show="*")
api_key_entry.pack(pady=(0, 10))

file_label = ctk.CTkLabel(main_frame, text="Datei auswählen:")
file_label.pack(pady=(10, 0))
file_entry = ctk.CTkEntry(main_frame, width=250, placeholder_text="Keine Datei ausgewählt")
file_entry.pack(pady=(0, 10))

browse_button = ctk.CTkButton(main_frame, text="Durchsuchen", command=choose_file)
browse_button.pack()

upload_button = ctk.CTkButton(main_frame, text="Hochladen", command=upload_file, fg_color="red")
upload_button.pack(pady=20)

# Revert status label styling with white text
status_label = ctk.CTkLabel(main_frame, text="Bereit", text_color="white")
status_label.pack()

# Load saved config and pre-fill the entries if available
config = load_config()
if "dataset_id" in config:
    kb_id_entry.delete(0, ctk.END)
    kb_id_entry.insert(0, config["dataset_id"])
if "api_key" in config:
    api_key_entry.delete(0, ctk.END)
    api_key_entry.insert(0, config["api_key"])

root.mainloop()
