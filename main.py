import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import random
import threading
import time

# Configuración
ctk.set_default_color_theme("blue")

class AdivinadorApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Adivinador Mágico Grupal")
        self.root.geometry("1000x700")
        self.root.resizable(True, True)
        self.root.state('zoomed')

        # Variables
        self.a = 0
        self.b = 0
        self.S = [2, 3, 4, 5, 6, 7, 8, 9]
        self.estudiante_actual = 1
        self.resultados = []

        self.setup_ui()
        self.mostrar_bienvenida()

    def setup_ui(self):
        # Título
        self.title_label = ctk.CTkLabel(
            self.root,
            text="Adivinador Mágico",
            font=ctk.CTkFont(size=40, weight="bold")
        )
        self.title_label.pack(pady=(20, 10))

        # Contenedor principal
        main_container = ctk.CTkFrame(self.root)
        main_container.pack(fill="both", expand=True, padx=40, pady=20)

        # === SIDEBAR (inicialmente oculto) ===
        self.sidebar = ctk.CTkFrame(main_container, width=340, corner_radius=15)
        self.sidebar.pack_propagate(False)
        # No se empaqueta aún → se mostrará con .pack() cuando empiece el juego

        self.sidebar_title = ctk.CTkLabel(
            self.sidebar,
            text="PASOS MÁGICOS",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#FFD700"
        )

        self.pasos_labels = []
        for i in range(5):
            lbl = ctk.CTkLabel(
                self.sidebar,
                text="",
                font=ctk.CTkFont(size=16),
                anchor="w",
                justify="left",
                wraplength=300
            )
            lbl.pack(pady=10, padx=25, fill="x")
            self.pasos_labels.append(lbl)

        # === CONTENIDO PRINCIPAL ===
        self.content_frame = ctk.CTkFrame(main_container)
        self.content_frame.pack(side="left", fill="both", expand=True, padx=(0, 20), pady=20)

        # Footer
        self.footer = ctk.CTkFrame(self.root, height=80, corner_radius=0)
        self.footer.pack(fill="x", side="bottom", pady=(10, 0))
        self.footer.grid_columnconfigure(0, weight=1)
        self.footer.grid_columnconfigure(1, weight=1)

        self.btn_finalizar = ctk.CTkButton(
            self.footer,
            text="Finalizar juego",
            fg_color="#C41E3A",
            font=ctk.CTkFont(size=18, weight="bold"),
            command=self.mostrar_final,
            height=60
        )
        self.btn_finalizar.grid(row=0, column=0, padx=30, pady=15, sticky="ew")

        self.btn_reiniciar = ctk.CTkButton(
            self.footer,
            text="Reiniciar",
            fg_color="#2E8B57",
            font=ctk.CTkFont(size=18, weight="bold"),
            command=self.mostrar_bienvenida,
            height=60
        )
        self.btn_reiniciar.grid(row=0, column=1, padx=30, pady=15, sticky="ew")

    def limpiar_contenido(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def mostrar_sidebar(self):
        self.sidebar.pack(side="right", fill="y", padx=(20, 0), pady=20)
        self.sidebar_title.pack(pady=(25, 15))

    def ocultar_sidebar(self):
        self.sidebar.pack_forget()

    def actualizar_sidebar(self):
        pasos = [
            f"Piensen un número",
            f"× {self.a}",
            f"+ {self.a * self.b}",
            f"÷ {self.a}",
            f"→ Díganme el resultado"
        ]
        for lbl, texto in zip(self.pasos_labels, pasos):
            lbl.configure(text=texto)

    def iniciar_juego(self):
        self.a = random.choice(self.S)
        self.b = random.choice(self.S)
        self.estudiante_actual = 1
        self.resultados = []
        self.actualizar_sidebar()
        self.mostrar_sidebar()  # ¡Aparece el sidebar!
        self.mostrar_instrucciones()

    def mostrar_bienvenida(self):
        self.ocultar_sidebar()
        self.limpiar_contenido()

        inner = ctk.CTkFrame(self.content_frame)
        inner.pack(fill="both", expand=True, padx=80, pady=80)

        label = ctk.CTkLabel(
            inner,
            text="¡Bienvenidos al show de magia matemática!\n\n"
                 "Voy a adivinar el número que piensa CADA estudiante...\n"
                 "¡sin que me digan nada!",
            font=ctk.CTkFont(size=30), justify="center"
        )
        label.pack(expand=True)

        btn = ctk.CTkButton(
            inner,
            text="¡Empezar el Truco!",
            height=70,
            font=ctk.CTkFont(size=22, weight="bold"),
            command=self.iniciar_juego
        )
        btn.pack(pady=50)

    def mostrar_instrucciones(self):
        self.limpiar_contenido()

        scroll = ctk.CTkScrollableFrame(self.content_frame)
        scroll.pack(fill="both", expand=True, padx=60, pady=50)

        title = ctk.CTkLabel(
            scroll,
            text="Sigan estos pasos con su número pensado:",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title.pack(pady=20)

        pasos = [
            f"Multipliquen su número por {self.a}",
            f"Sumen {self.a * self.b} al resultado",
            f"Dividan todo entre {self.a}",
            "¡Listo! Ahora me dicen el resultado final."
        ]

        for paso in pasos:
            lbl = ctk.CTkLabel(
                scroll,
                text=paso,
                font=ctk.CTkFont(size=26),
                anchor="w",
                justify="left"
            )
            lbl.pack(pady=15, padx=60, fill="x")

        btn = ctk.CTkButton(
            scroll,
            text="¡Entendido! Empezar a adivinar",
            command=self.recolectar_resultado,
            height=70,
            font=ctk.CTkFont(size=20, weight="bold")
        )
        btn.pack(pady=60)

    def recolectar_resultado(self):
        self.limpiar_contenido()

        inner = ctk.CTkFrame(self.content_frame)
        inner.pack(fill="both", expand=True, padx=70, pady=70)

        label = ctk.CTkLabel(
            inner,
            text=f"Estudiante {self.estudiante_actual}",
            font=ctk.CTkFont(size=36, weight="bold")
        )
        label.pack(pady=50)

        instr = ctk.CTkLabel(
            inner,
            text="Ingresa tu resultado final:",
            font=ctk.CTkFont(size=24)
        )
        instr.pack(pady=20)

        self.entry = ctk.CTkEntry(
            inner,
            placeholder_text="Ej: 15.0",
            width=320,
            height=60,
            font=ctk.CTkFont(size=26),
            justify="center"
        )
        self.entry.pack(pady=30)
        self.entry.focus()

        btn = ctk.CTkButton(
            inner,
            text="¡Adivinar mi número!",
            command=self.procesar_resultado,
            height=70,
            font=ctk.CTkFont(size=20, weight="bold")
        )
        btn.pack(pady=50)

        self.entry.bind("<Return>", lambda e: self.procesar_resultado())

    def procesar_resultado(self):
        try:
            y = float(self.entry.get().strip())
            x = y - self.b
            if not x.is_integer():
                raise ValueError
            x = int(x)
            self.resultados.append((self.estudiante_actual, x))
            self.mostrar_adivinando(x)
        except:
            messagebox.showerror("Error", "Por favor ingresa un número válido.")
            return

    def mostrar_adivinando(self, numero):
        self.limpiar_contenido()

        inner = ctk.CTkFrame(self.content_frame)
        inner.pack(fill="both", expand=True, padx=70, pady=70)

        thinking = ctk.CTkLabel(
            inner,
            text="Pensando... calculando ondas mentales...",
            font=ctk.CTkFont(size=30)
        )
        thinking.pack(pady=70)

        self.progress = ctk.CTkProgressBar(inner, height=40)
        self.progress.pack(pady=40, fill="x", padx=120)
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

        inner = ctk.CTkFrame(self.content_frame)
        inner.pack(fill="both", expand=True, padx=70, pady=70)

        magia = ctk.CTkLabel(
            inner,
            text=f"¡TU NÚMERO ES EL {numero}!",
            font=ctk.CTkFont(size=70, weight="bold"),
            text_color="#FFD700"
        )
        magia.pack(pady=100)

        aplausos = ctk.CTkLabel(
            inner,
            text="¡Magia matemática!",
            font=ctk.CTkFont(size=30)
        )
        aplausos.pack(pady=20)

        btn = ctk.CTkButton(
            inner,
            text="Siguiente estudiante",
            command=lambda: [
                setattr(self, 'estudiante_actual', self.estudiante_actual + 1),
                self.recolectar_resultado()
            ],
            height=70,
            font=ctk.CTkFont(size=20, weight="bold")
        )
        btn.pack(pady=70)

    def mostrar_final(self):
        self.limpiar_contenido()

        if not self.resultados:
            messagebox.showinfo("Sin datos", "No se adivinó ningún número.")
            return

        scroll = ctk.CTkScrollableFrame(self.content_frame)
        scroll.pack(fill="both", expand=True, padx=60, pady=50)

        title = ctk.CTkLabel(
            scroll,
            text="¡Fin del espectáculo!",
            font=ctk.CTkFont(size=36, weight="bold")
        )
        title.pack(pady=40)

        total = len(self.resultados)
        resumen = ctk.CTkLabel(
            scroll,
            text=f"Se adivinaron {total} número(s):",
            font=ctk.CTkFont(size=26)
        )
        resumen.pack(pady=20)

        for est, num in self.resultados:
            lbl = ctk.CTkLabel(
                scroll,
                text=f"Estudiante {est} → {num}",
                font=ctk.CTkFont(size=24)
            )
            lbl.pack(pady=12, padx=80, fill="x")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = AdivinadorApp()
    app.run()