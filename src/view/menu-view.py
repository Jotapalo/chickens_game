import os
import subprocess
import threading
import tkinter as tk
from tkinter import ttk, Canvas
from PIL import Image, ImageTk
from src.model.Enum import Enum

class MenuView(tk.Tk):
    def __init__(self, screenName = None, baseName = None, className = "Tk", useTk = True, sync = False, use = None):
        super().__init__(screenName, baseName, className, useTk, sync, use)

        self.param_fps = "100"
        self.param_bullet_speed = "20"
        self.param_debug = "false"

        self.title("Chickens Game")
        self.geometry("735x410")
        self.wm_resizable(False, False)

        # Frame principal
        self.frame_main = tk.Frame(self)
        self.frame_main.configure(background="red")
        self.frame_main.pack(expand=True, anchor="center", fill="both")

        # Canvas que vive en frame principal
        image = Image.open(Enum.resourcePath.FONT)
        photo = ImageTk.PhotoImage(image)
        self.canvas = Canvas(self.frame_main, width=735, height=410)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
        self.canvas.image = photo

        # Create a style object
        style_button = ttk.Style(self.frame_main)
        style_button.theme_use("clam")

        style_button.configure("Custom.TButton",
            font=("Cascadia Code", 12),
            foreground="blue",
            padding=10,
            )

        style_label = ttk.Style(self.frame_main)
        style_label.theme_use("clam")
        style_label.configure("Custom.TLabel",
                    font=("Cascadia Code", 12),
                    foreground="blue",
                    background="black"
                    )

        self.load_main_page()

        
    def load_main_page(self):
        for child in self.canvas.winfo_children():
            child.destroy()
        
        # Configuracion canvas
        self.canvas.grid_columnconfigure(0, weight=1)
        self.canvas.grid_rowconfigure((0, 1), weight=1)
        self.canvas.grid_rowconfigure((2,5), weight=0)
        self.canvas.grid_columnconfigure((1), weight=0)
        
        # botones sobre canvas
        self.button_start_game = ttk.Button(self.canvas, text="iniciar partida", style="Custom.TButton", command=self.load_levels_page)
        self.button_start_game.grid(column=0, row=0)
        self.button_start_game.grid_configure(sticky="s", pady=10)

        self.button_options = ttk.Button(self.canvas, text="configuraciones", style="Custom.TButton", command=self.load_settings_page)
        self.button_options.grid(column=0, row=1)
        self.button_options.grid_configure(sticky="n")

    def load_levels_page(self): 
        levels = ["Level_1", "Level_2", "Level_3"]

        for child in self.canvas.winfo_children():
            child.destroy()

        self.canvas.grid_rowconfigure((0,1), weight=0)

        for i in range(len(levels)):
            button = ttk.Button(self.canvas, text=levels[i].replace("_", " "),
                                 style="Custom.TButton",
                                   command=lambda i=i: self.load_level(levels[i]))
            button.pack(padx=10, pady=10)

        ttk.Button(self.canvas, text="Back", style="Custom.TButton", command=self.load_main_page).pack(padx=10, pady=10)

    def load_settings_page(self):
        for child in self.canvas.winfo_children():
            child.destroy()

        self.canvas.grid_rowconfigure((0,1), weight=0)

        self.canvas.grid_columnconfigure((0,1), weight=1)
        self.canvas.grid_rowconfigure((0,2), weight=1)

        ttk.Label(self.canvas, text="FPS", style="Custom.TLabel").grid(column=0, row=0)
        ttk.Label(self.canvas, text="Bullet speed", style="Custom.TLabel").grid(column=0, row=1)
        ttk.Label(self.canvas, text="Debug", style="Custom.TLabel").grid(column=0, row=2)

        self.entry_fps = tk.Entry(self.canvas)
        self.entry_fps.grid(column=1, row=0)
        self.entry_fps.insert(0, self.param_fps)
        self.entry_bullet_speed = tk.Entry(self.canvas)
        self.entry_bullet_speed.grid(column=1, row=1)
        self.entry_bullet_speed.insert(0, self.param_bullet_speed)
        self.entry_debug = tk.Entry(self.canvas)
        self.entry_debug.grid(column=1, row=2)
        self.entry_debug.insert(0, self.param_debug)


        # Back and save buttons 
        ttk.Button(self.canvas, text="Back", style="Custom.TButton", command=self.load_main_page).grid(column=0, row=3)
        ttk.Button(self.canvas, text="Save", style="Custom.TButton", 
                   command=self.act_parameters).grid(column=1, row=3)

    def act_parameters(self):
        self.param_fps = self.entry_fps.get()
        self.param_bullet_speed = self.entry_bullet_speed.get()
        self.param_debug = self.entry_debug.get()
        self.load_main_page()

    def load_level(self, level_id):
        # Extraer el número del nivel (ej: "Level_1" -> 1)
        level_num = level_id.split("_")[1]

        # Directorio raíz del proyecto (chickens_game)
        project_root = os.path.normpath(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
        )

        # Ocultar el menú mientras se juega
        self.withdraw()

        # Ejecutar el juego en un proceso separado con "py -m src.model.main"
        game_process = subprocess.Popen(
            ["py", "-m", "src.model.main", f"level={level_num}", f"fps={self.param_fps}", f"debug={self.param_debug}", f"bullet_speed{self.param_bullet_speed}"],
            cwd=project_root,
        )

        # Monitorear el proceso del juego en un hilo separado
        monitor_thread = threading.Thread(target=self._wait_for_game, args=(game_process,), daemon=True)
        monitor_thread.start()

    def _wait_for_game(self, game_process):
        # Esperar a que el proceso del juego termine (el jugador cerró la ventana)
        game_process.wait()

        # Programar la destrucción del menú en el hilo principal de Tk
        self.after(0, self.destroy)


if __name__ == "__main__":
    root = MenuView()
    root.mainloop()