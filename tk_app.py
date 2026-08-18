from __future__ import annotations
import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
import threading
import queue
import logging
from pathlib import Path
from PIL import Image, ImageDraw
import pystray
from guardianx.core.scanner import scan_paths
from guardianx.core.quarantine import QuarantineManager

class GuardianXGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("GuardianX Community - Panel de Control")
        self.root.geometry("750x550")
        self.root.configure(bg="#1e1e1e")
        self.log_queue = queue.Queue()
        self.root.protocol("WM_DELETE_WINDOW", self.hide_to_tray)
        self.build_ui()
        self.setup_tray_icon()
        self.root.after(100, self.process_log_queue)

    def build_ui(self):
        header = tk.Frame(self.root, bg="#007acc", height=50)
        header.pack(fill=tk.X)
        tk.Label(header, text="🛡️ GuardianX Community", fg="white", bg="#007acc", font=("Arial", 16, "bold")).pack(pady=10)

        status_frame = tk.Frame(self.root, bg="#1e1e1e")
        status_frame.pack(pady=10, padx=20, fill=tk.X)
        self.status_label = tk.Label(status_frame, text="Estado: Protección Activa", fg="#4caf50", bg="#1e1e1e", font=("Arial", 12, "bold"))
        self.status_label.pack(side=tk.LEFT)

        btn_frame = tk.Frame(self.root, bg="#1e1e1e")
        btn_frame.pack(pady=5, padx=20, fill=tk.X)
        tk.Button(btn_frame, text="📂 Escanear Carpeta", command=self.scan_folder, bg="#333333", fg="white", font=("Arial", 10), relief=tk.FLAT).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="🗑️ Ver Cuarentena", command=self.view_quarantine, bg="#333333", fg="white", font=("Arial", 10), relief=tk.FLAT).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="🔄 Actualizar Firmas", command=self.update_signatures, bg="#333333", fg="white", font=("Arial", 10), relief=tk.FLAT).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="▼ Ocultar", command=self.hide_to_tray, bg="#333333", fg="white", font=("Arial", 10), relief=tk.FLAT).pack(side=tk.RIGHT, padx=5)

        log_frame = tk.Frame(self.root, bg="#1e1e1e")
        log_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        tk.Label(log_frame, text="Eventos en Tiempo Real:", fg="white", bg="#1e1e1e", font=("Arial", 10, "bold")).pack(anchor=tk.W)
        self.log_viewer = scrolledtext.ScrolledText(log_frame, bg="#000000", fg="#00ff00", font=("Consolas", 10), insertbackground="white")
        self.log_viewer.pack(fill=tk.BOTH, expand=True)
        self.log_viewer.config(state=tk.DISABLED)

    def setup_tray_icon(self):
        image = Image.new('RGB', (64, 64), color=(30, 30, 30))
        draw = ImageDraw.Draw(image)
        draw.rectangle([16, 16, 48, 48], fill=(0, 122, 204))
        menu = pystray.Menu(
            pystray.MenuItem("Mostrar Panel", self.show_from_tray, default=True),
            pystray.MenuItem("Salir", self.quit_app)
        )
        self.tray_icon = pystray.Icon("GuardianX", image, "GuardianX Antivirus", menu)
        self.tray_thread = threading.Thread(target=self.tray_icon.run, daemon=True)
        self.tray_thread.start()

    def hide_to_tray(self):
        self.root.withdraw()

    def show_from_tray(self, icon=None, item=None):
        self.root.after(0, self.root.deiconify)

    def quit_app(self, icon=None, item=None):
        self.tray_icon.stop()
        self.root.after(0, self.root.destroy)

    def add_log(self, message: str):
        self.log_queue.put(message)

    def process_log_queue(self):
        while not self.log_queue.empty():
            log_line = self.log_queue.get()
            self.log_viewer.config(state=tk.NORMAL)
            self.log_viewer.insert(tk.END, f"{log_line}\n")
            self.log_viewer.see(tk.END)
            self.log_viewer.config(state=tk.DISABLED)
        self.root.after(100, self.process_log_queue)

    def scan_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.add_log(f"[*] Iniciando escaneo manual en: {folder}")
            threading.Thread(target=self._run_scan, args=(folder,), daemon=True).start()

    def _run_scan(self, folder: str):
        try:
            findings = scan_paths([folder])
            if findings:
                for f in findings:
                    self.add_log(f"[!] Amenaza: {f.threat} en {f.path}")
            else:
                self.add_log("[+] Escaneo completado. Sin amenazas detectadas.")
        except Exception as e:
            self.add_log(f"[ERROR] Fallo en escaneo: {e}")

    def view_quarantine(self):
        try:
            qm = QuarantineManager()
            items = qm.list_items()
            if not items:
                messagebox.showinfo("Cuarentena", "No hay archivos en cuarentena.")
                return
            info = "Archivos en cuarentena:\n\n"
            for item in items:
                info += f"• {item['threat']}\n  Original: {item['original_path']}\n  Fecha: {item['quarantined_at']}\n\n"
            messagebox.showinfo("Cuarentena", info)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo leer la cuarentena: {e}")

    def update_signatures(self):
        self.add_log("[*] Descargando actualizaciones de firmas...")
        threading.Thread(target=self._run_update, daemon=True).start()

    def _run_update(self):
        try:
            from guardianx.core.updater import update_signatures
            result = update_signatures()
            self.add_log(f"[+] Firmas actualizadas: v{result['version']} ({result['rules']} reglas, {result['hashes']} hashes)")
        except Exception as e:
            self.add_log(f"[ERROR] No se pudieron actualizar las firmas: {e}")

class QueueLogHandler(logging.Handler):
    def __init__(self, log_queue):
        super().__init__()
        self.log_queue = log_queue
    def emit(self, record):
        self.log_queue.put(self.format(record))
        
    def quit_app(self, icon=None, item=None):
    self.tray_icon.stop()
    # Si guardaste una referencia al hilo de ResidentGuard, detén su evento aquí:
    # if self.guard: self.guard.stop()
    self.root.after(0, self.root.destroy)
