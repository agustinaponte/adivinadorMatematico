import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import random
import threading
import time
from PIL import Image, ImageTk

ctk.set_default_color_theme("blue")
verdeUS21="#006756"

class AdivinadorApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Adivinador Mágico Grupal")
        self.root.minsize(900, 600)           # Works from 800x1000
        self.root.state('zoomed')             # Start maximized
        self.root.configure(fg_color=verdeUS21)

        # Variables
        self.a = 0
        self.b = 0
        self.S = [2, 3, 4, 5, 6, 7, 8, 9]
        self.estudiante_actual = 1
        self.resultados = []

        self.setup_ui()
        self.mostrar_bienvenida()

    def setup_ui(self):
        # === ROOT GRID ===
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # === TITLE ===
        title_frame = ctk.CTkFrame(self.root, fg_color=verdeUS21)
        title_frame.grid(row=0, column=0, pady=(15, 5), sticky="ew")
        title_frame.grid_columnconfigure(0, weight=1)
        title_frame.grid_columnconfigure(1, weight=0)

        # Título a la izquierda
        self.title_label = ctk.CTkLabel(
            title_frame,
            text="Adivinador Mágico",
            font=ctk.CTkFont(size=36, weight="bold")
        )
        self.title_label.grid(row=0, column=0, sticky="w", padx=(20, 10))

        # Cargar y mostrar logo a la derecha
        try:
            logo_image = Image.open("logoUS21.jpg")
            logo_image = logo_image.resize((174, 75), Image.Resampling.LANCZOS)
            self.logo_photo = ImageTk.PhotoImage(logo_image)

            self.logo_label = ctk.CTkLabel(
                title_frame,
                image=self.logo_photo,
                text=""
            )
            self.logo_label.grid(row=0, column=1, sticky="e", padx=(0, 20))
        except Exception as e:
            print(f"No se pudo cargar el logo: {e}")
            # Opción fallback: mostrar texto si falla la imagen
            fallback = ctk.CTkLabel(title_frame, text="LOGO", font=ctk.CTkFont(size=20))
            fallback.grid(row=0, column=1, sticky="e", padx=(0, 20))

        # === MAIN CONTAINER ===
        main_container = ctk.CTkFrame(self.root)
        main_container.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        main_container.grid_rowconfigure(0, weight=1)
        main_container.grid_columnconfigure(0, weight=1)
        main_container.grid_columnconfigure(1, weight=0)  # sidebar
        main_container.configure(fg_color=verdeUS21)

        # === CONTENT FRAME (SCROLLABLE) ===
        self.content_scroll = ctk.CTkFrame(main_container, fg_color="transparent")
        self.content_scroll.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        self.content_scroll.grid_columnconfigure(0, weight=1)

        # === SIDEBAR (FIXED WIDTH, SCROLLABLE) ===
        self.sidebar = ctk.CTkFrame(
            main_container, width=300, corner_radius=15
        )
        self.sidebar.grid_columnconfigure(0, weight=1)

        self.sidebar_title = ctk.CTkLabel(
            self.sidebar,
            text="PASOS MÁGICOS",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#FFD700"
        )
        self.sidebar_title.pack(pady=(20, 10), anchor="w", padx=20)

        self.pasos_labels = []
        for _ in range(5):
            lbl = ctk.CTkLabel(
                self.sidebar,
                text="",
                font=ctk.CTkFont(size=16),
                anchor="w",
                justify="left",
                wraplength=260  # Fits inside 300px width
            )
            lbl.pack(pady=8, padx=20, fill="x")
            self.pasos_labels.append(lbl)

        # === FOOTER ===
        self.footer = ctk.CTkFrame(self.root, height=70)
        self.footer.grid(row=2, column=0, sticky="ew", pady=(10, 15))
        self.footer.grid_columnconfigure(0, weight=1)
        self.footer.grid_columnconfigure(1, weight=1)
        self.footer.configure(fg_color=verdeUS21)

        self.btn_finalizar = ctk.CTkButton(
            self.footer,
            text="Finalizar juego",
            fg_color="#C41E3A",
            font=ctk.CTkFont(size=16, weight="bold"),
            command=self.mostrar_final,
            height=50
        )
        self.btn_finalizar.grid(row=0, column=0, padx=15, pady=10, sticky="ew")

        self.btn_reiniciar = ctk.CTkButton(
            self.footer,
            text="Reiniciar",
            fg_color="#2E8B57",
            font=ctk.CTkFont(size=16, weight="bold"),
            command=self.mostrar_bienvenida,
            height=50
        )
        self.btn_reiniciar.grid(row=0, column=1, padx=15, pady=10, sticky="ew")

    def limpiar_contenido(self):
        for widget in self.content_scroll.winfo_children():
            widget.destroy()

    def mostrar_sidebar(self):
        self.sidebar.grid(row=0, column=1, sticky="ns", padx=(10, 0))
        self.actualizar_sidebar()

    def ocultar_sidebar(self):
        self.sidebar.grid_remove()

    def actualizar_sidebar(self):
        pasos = [
            "Piensen un número",
            f"× {self.a}",
            f"+ {self.a * self.b}",
            f"÷ {self.a}",
            "→ Díganme el resultado"
        ]
        for lbl, texto in zip(self.pasos_labels, pasos):
            lbl.configure(text=texto)

    def iniciar_juego(self):
        self.a = random.choice(self.S)
        self.b = random.choice(self.S)
        self.estudiante_actual = 1
        self.resultados = []
        self.mostrar_instrucciones()

    def mostrar_bienvenida(self):
        self.ocultar_sidebar()
        self.limpiar_contenido()

        frame = ctk.CTkFrame(self.content_scroll)
        frame.pack(fill="both", expand=True, padx=40, pady=40)
        frame.grid_columnconfigure(0, weight=1)

        lbl = ctk.CTkLabel(
            frame,
            text="¡Bienvenidos al show de magia matemática!\n\n"
                 "Voy a adivinar el número que piensa CADA estudiante...\n"
                 "¡sin que me digan nada!",
            font=ctk.CTkFont(size=28),
            justify="center",
            wraplength=700
        )
        lbl.grid(row=0, column=0, pady=30)

        btn = ctk.CTkButton(
            frame,
            text="¡Empezar el Truco!",
            font=ctk.CTkFont(size=20, weight="bold"),
            command=self.iniciar_juego,
            height=60
        )
        btn.grid(row=1, column=0, pady=40)

    def mostrar_instrucciones(self):
        self.limpiar_contenido()

        frame = ctk.CTkFrame(self.content_scroll)
        frame.pack(fill="both", expand=True, padx=30, pady=30)
        frame.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(
            frame,
            text="Primero piensen un número",
            font=ctk.CTkFont(size=26, weight="bold")
        )
        title.grid(row=0, column=0, pady=(20, 15))

        pasos = [
            f"Multipliquen su número por {self.a}",
            f"Sumen {self.a * self.b} al resultado",
            f"Dividan todo entre {self.a}",
            "¡Listo! Ahora me dicen el resultado final."
        ]

        for i, paso in enumerate(pasos):
            lbl = ctk.CTkLabel(
                frame,
                text=paso,
                font=ctk.CTkFont(size=22),
                anchor="w",
                justify="left",
                wraplength=700
            )
            lbl.grid(row=i+1, column=0, pady=12, sticky="w", padx=40)

        btn = ctk.CTkButton(
            frame,
            text="¡Entendido! Empezar a adivinar",
            font=ctk.CTkFont(size=18, weight="bold"),
            command=self.recolectar_resultado,
            height=60
        )
        btn.grid(row=len(pasos)+1, column=0, pady=50)

    def recolectar_resultado(self):
        self.limpiar_contenido()
        self.mostrar_sidebar()
        
        frame = ctk.CTkFrame(self.content_scroll)
        frame.pack(fill="both", expand=True, padx=50, pady=50)
        frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            frame,
            text=f"Estudiante {self.estudiante_actual}",
            font=ctk.CTkFont(size=32, weight="bold")
        ).grid(row=0, column=0, pady=30)

        ctk.CTkLabel(
            frame,
            text="Ingresa tu resultado final:",
            font=ctk.CTkFont(size=20)
        ).grid(row=1, column=0, pady=15)

        self.entry = ctk.CTkEntry(
            frame,
            placeholder_text="Ej: 15.0",
            font=ctk.CTkFont(size=24),
            height=55,
            justify="center"
        )
        self.entry.grid(row=2, column=0, pady=25, sticky="ew", padx=100)
        self.entry.focus()

        btn = ctk.CTkButton(
            frame,
            text="¡Adivinar mi número!",
            font=ctk.CTkFont(size=18, weight="bold"),
            command=self.procesar_resultado,
            height=60
        )
        btn.grid(row=3, column=0, pady=40)

        self.entry.bind("<Return>", lambda e: self.procesar_resultado())

    def procesar_resultado(self):
        try:
            y = float(self.entry.get().strip())
            x = y - self.b
            if not x.is_integer:
                raise ValueError
            x = int(x)
            if x>=0:
                raise ValueError
            self.resultados.append((self.estudiante_actual, x))
            self.mostrar_adivinando(x)
        except:
            messagebox.showerror("Error", "Por favor ingresa un número natural.")
            return

    def mostrar_adivinando(self, numero):
        self.limpiar_contenido()

        frame = ctk.CTkFrame(self.content_scroll)
        frame.pack(fill="both", expand=True, padx=50, pady=60)
        frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            frame,
            text="Pensando... calculando ondas mentales...",
            font=ctk.CTkFont(size=26)
        ).grid(row=0, column=0, pady=50)

        self.progress = ctk.CTkProgressBar(frame, height=35)
        self.progress.grid(row=1, column=0, sticky="ew", padx=100, pady=30)
        self.progress.set(0)

        def animar():
            for i in range(1, 101):
                time.sleep(0.02)
                self.progress.set(i / 100)
                self.root.update_idletasks()
            self.revelar_numero(numero)

        threading.Thread(target=animar, daemon=True).start()

    def revelar_numero(self, numero):
        self.limpiar_contenido()

        frame = ctk.CTkFrame(self.content_scroll)
        frame.pack(fill="both", expand=True, padx=40, pady=40)
        frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            frame,
            text=f"¡TU NÚMERO ES EL {numero}!",
            font=ctk.CTkFont(size=60, weight="bold"),
            text_color="#FFD700"
        ).grid(row=0, column=0, pady=60)

        ctk.CTkLabel(
            frame,
            text="¡Magia matemática!",
            font=ctk.CTkFont(size=26)
        ).grid(row=1, column=0, pady=20)

        btn = ctk.CTkButton(
            frame,
            text="Siguiente estudiante",
            font=ctk.CTkFont(size=18, weight="bold"),
            command=lambda: [
                setattr(self, 'estudiante_actual', self.estudiante_actual + 1),
                self.recolectar_resultado()
            ],
            height=60
        )
        btn.grid(row=2, column=0, pady=50)

    def mostrar_final(self):
        self.limpiar_contenido()

        if not self.resultados:
            messagebox.showinfo("Sin datos", "No se adivinó ningún número.")
            return

        frame = ctk.CTkFrame(self.content_scroll)
        frame.pack(fill="both", expand=True, padx=30, pady=30)
        frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            frame,
            text="¡Fin del espectáculo!",
            font=ctk.CTkFont(size=32, weight="bold")
        ).grid(row=0, column=0, pady=30)

        ctk.CTkLabel(
            frame,
            text=f"Se adivinaron {len(self.resultados)} número(s):",
            font=ctk.CTkFont(size=22)
        ).grid(row=1, column=0, pady=20)

        for i, (est, num) in enumerate(self.resultados):
            ctk.CTkLabel(
                frame,
                text=f"Estudiante {est} → {num}",
                font=ctk.CTkFont(size=20),
                anchor="w",
                wraplength=700
            ).grid(row=i+2, column=0, pady=8, padx=50, sticky="w")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = AdivinadorApp()
    app.run()