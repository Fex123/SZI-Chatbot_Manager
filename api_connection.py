import os
import requests
import json

class WissensbasisAPI:
    def __init__(self, api_key):
        # Initialize API connection with base URL, headers, and default chunk rule
        self.api_url = "http://localhost:3100/v1"
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        self.default_chunk_rule = {
            "rules": {
                "pre_processing_rules": [],
                "segmentation": {
                    "separator": "#",
                    "max_tokens": 1000
                }
            },
            "mode": "custom"
        }

    def create_document_by_file(self, dataset_id, file_path, doc_name=None, process_rule=None):
        # Upload document as file with optional custom processing rule
        """
        Uploadt ein Dokument als Datei und übernimmt die Einstellungen im process_rule.
        Falls kein doc_name angegeben wird, nutzt er den Dateinamen aus file_path.
        """
        if doc_name is None:
            doc_name = os.path.basename(file_path)
        
        url = f"{self.api_url}/datasets/{dataset_id}/document/create-by-file"
        if process_rule is None:
            process_rule = self.default_chunk_rule
        
        data_field = {
            "name": doc_name,
            "indexing_technique": "high_quality",
            "process_rule": process_rule
        }
        
        files = {
            "data": (None, json.dumps(data_field), "text/plain"),
            "file": open(file_path, "rb")
        }
        headers = self.headers.copy()
        headers.pop("Content-Type", None)
        response = requests.post(url, files=files, headers=headers)
        try:
            data = response.json()
        except ValueError:
            data = response.text

        if response.status_code in (200, 201):
            print("Dokument erfolgreich erstellt (Datei)!")
            return data
        else:
            print("Fehler beim Erstellen des Dokuments per Datei:", data)
            return None

# Example usage of WissensbasisAPI
api = WissensbasisAPI(api_key="dataset-MIUuX7XZOXZ3tg0oIyyW4IUW")
dataset_id = "c646b92d-0186-488b-95a0-e5907cc11294"

custom_rule = {
    "rules": {
        "pre_processing_rules": [
            {"id": "remove_extra_spaces", "enabled": True},
            {"id": "remove_urls_emails", "enabled": True}
        ],
        "segmentation": {
            "separator": "#",
            "max_tokens": 1000
        }
    },
    "mode": "custom"
}
