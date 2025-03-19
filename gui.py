import customtkinter as ctk
from tkinter import filedialog
from test import WissensbasisAPI  # Stelle sicher, dass diese Klasse die Methode create_document_by_file implementiert

def choose_file():
    file_path = filedialog.askopenfilename(
        title="Wähle eine Datei",
        filetypes=[
            ("Markdown files", "*.md"),
            ("Text files", "*.txt"),
            ("PDF files", "*.pdf"),
            ("Word files", "*.doc;*.docx")
        ]
    )
    if file_path:
        file_entry.delete(0, ctk.END)
        file_entry.insert(0, file_path)
        status_label.configure(text="Datei ausgewählt.", text_color="#1f6feb")

def upload_file():
    # Manuelle Eingabe der Wissensbasis-ID
    dataset_id = kb_id_entry.get().strip()
    file_path = file_entry.get().strip()
    
    if not dataset_id or not file_path:
        status_label.configure(text="Fehler: Wissensbasis-ID und Datei erforderlich!", text_color="#DC3545")
        return

    status_label.configure(text="Datei wird hochgeladen...", text_color="#FD7E14")
    root.update()  # Sofortiges Aktualisieren der Statusanzeige
    
    api = WissensbasisAPI(api_key="dataset-XFb2bSp8KyR553cekNo9FIZ6")
    response = api.create_document_by_file(dataset_id, file_path)
    
    if response:
        status_label.configure(text="Upload erfolgreich!", text_color="#198754")
        file_entry.delete(0, ctk.END)
        file_entry.insert(0, "Keine Datei ausgewählt")
    else:
        status_label.configure(text="Upload fehlgeschlagen!", text_color="#DC3545")

# Hauptfenster erstellen
root = ctk.CTk()
root.title("SZI Assistent - Dokumenten Upload")
root.geometry("600x400")
root.resizable(False, False)

# Hauptframe mit modernem Stil
main_frame = ctk.CTkFrame(root, corner_radius=15)
main_frame.pack(pady=20, padx=20, fill="both", expand=True)

# Überschrift
header_label = ctk.CTkLabel(main_frame, text="SZI Assistent", font=("Arial", 24, "bold"))
header_label.pack(pady=(20, 10))

# Wissensbasis-ID manuell eingeben
kb_id_label = ctk.CTkLabel(main_frame, text="Wissensbasis-ID:")
kb_id_label.pack(pady=(10, 0))
kb_id_entry = ctk.CTkEntry(main_frame, width=250, placeholder_text="Geben Sie die Wissensbasis-ID ein")
kb_id_entry.pack(pady=(0, 10))

# Datei-Auswahl
file_label = ctk.CTkLabel(main_frame, text="Datei auswählen:")
file_label.pack(pady=(10, 0))
file_entry = ctk.CTkEntry(main_frame, width=250, placeholder_text="Keine Datei ausgewählt")
file_entry.pack(pady=(0, 10))

browse_button = ctk.CTkButton(main_frame, text="Durchsuchen", command=choose_file)
browse_button.pack()

upload_button = ctk.CTkButton(main_frame, text="Hochladen", command=upload_file, fg_color="red")
upload_button.pack(pady=20)

status_label = ctk.CTkLabel(main_frame, text="Bereit", text_color="#495057")
status_label.pack()

root.mainloop()
