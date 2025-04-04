# -*- coding: utf-8 -*-
"""
Created on Fri Apr  4 15:02:40 2025

@author: nannib
"""
import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext
import whisper
import threading
from datetime import datetime
import os

class WhisperTranscriberGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Whisper Transcriber")
        self.root.geometry("800x600")

        # Variabili
        self.model_var = tk.StringVar(value="base")
        self.file_path = tk.StringVar()
        self.output_text = tk.StringVar()

        # Creazione elementi UI
        self.create_widgets()

    def create_widgets(self):
        # Frame superiore
        top_frame = ttk.Frame(self.root, padding=10)
        top_frame.pack(fill=tk.X)

        # Selezione modello
        ttk.Label(top_frame, text="Modello:").grid(row=0, column=0, padx=5)
        model_combobox = ttk.Combobox(top_frame, textvariable=self.model_var, 
                                    values=["tiny", "base", "small", "medium", "large", "turbo"])
        model_combobox.grid(row=0, column=1, padx=5)

        # Selezione file
        ttk.Button(top_frame, text="Scegli file", command=self.select_file).grid(row=0, column=2, padx=5)
        ttk.Label(top_frame, textvariable=self.file_path).grid(row=0, column=3, padx=5)

        # Pulsante trascrizione
        ttk.Button(top_frame, text="Trascrivi", command=self.start_transcription).grid(row=0, column=4, padx=5)

        # Area testo scorrevole
        text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD)
        text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.text_area = text_area

    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Audio files", "*.mp3 *.wav *.ogg *.m4a")])
        if file_path:
            self.file_path.set(file_path)

    def start_transcription(self):
        if not self.file_path.get():
            self.update_text("Seleziona prima un file audio!")
            return

        thread = threading.Thread(target=self.run_transcription)
        thread.start()

    def run_transcription(self):
        try:
            model_name = self.model_var.get()
            audio_path = self.file_path.get()
            
            # Genera nome file output
            base_name = os.path.splitext(os.path.basename(audio_path))[0]
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"trascrizione_{base_name}_{timestamp}.txt"

            self.update_text(f"Caricamento modello {model_name}...")
            model = whisper.load_model(model_name)

            self.update_text("Avvio trascrizione...")
            result = model.transcribe(audio_path)

            self.update_text("Salvataggio file...")
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(result["text"])

            self.update_text(f"Trascrizione completata!\nFile salvato come: {output_file}\n\n")
            self.update_text(result["text"])

        except Exception as e:
            self.update_text(f"Errore: {str(e)}")

    def update_text(self, message):
        self.root.after(0, lambda: self.text_area.insert(tk.END, message + "\n"))
        self.root.after(0, self.text_area.yview_moveto, 1)

if __name__ == "__main__":
    root = tk.Tk()
    app = WhisperTranscriberGUI(root)
    root.mainloop()