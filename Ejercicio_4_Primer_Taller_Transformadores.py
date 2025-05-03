import tkinter as tk
from tkinter import ttk
import math

class TransformerGUI:
    def __init__(self, master):
        self.master = master
        master.title("Transformer Analysis")

        # Variables de entrada
        self.V_oc = tk.DoubleVar()
        self.I_oc = tk.DoubleVar()
        self.P_oc = tk.DoubleVar()
        self.V_sc = tk.DoubleVar()
        self.I_sc = tk.DoubleVar()
        self.P_sc = tk.DoubleVar()
        self.V_rated_primary = tk.DoubleVar()
        self.V_rated_secondary = tk.DoubleVar()
        self.S_rated = tk.DoubleVar()
        self.other_PF = tk.DoubleVar(value=0.8)

        # Parámetros del circuito equivalente
        self.Rc = tk.DoubleVar()
        self.Xm = tk.DoubleVar()
        self.Req_lv = tk.DoubleVar()
        self.Xeq_lv = tk.DoubleVar()

        # Crear interfaz
        self.create_widgets()

    def create_widgets(self):
        # Frame de entrada
        input_frame = ttk.Frame(self.master, padding="10")
        input_frame.grid(row=0, column=0, sticky=tk.W)

        # Prueba de vacío
        ttk.Label(input_frame, text="Prueba de Vacío (LV):").grid(row=0, column=0, columnspan=2, sticky=tk.W)
        ttk.Label(input_frame, text="V_oc (V):").grid(row=1, column=0, sticky=tk.W)
        ttk.Entry(input_frame, textvariable=self.V_oc, width=10).grid(row=1, column=1)
        ttk.Label(input_frame, text="I_oc (A):").grid(row=2, column=0, sticky=tk.W)
        ttk.Entry(input_frame, textvariable=self.I_oc, width=10).grid(row=2, column=1)
        ttk.Label(input_frame, text="P_oc (W):").grid(row=3, column=0, sticky=tk.W)
        ttk.Entry(input_frame, textvariable=self.P_oc, width=10).grid(row=3, column=1)

        # Prueba de corto
        ttk.Label(input_frame, text="Prueba de Corto (HV):").grid(row=4, column=0, columnspan=2, sticky=tk.W)
        ttk.Label(input_frame, text="V_sc (V):").grid(row=5, column=0, sticky=tk.W)
        ttk.Entry(input_frame, textvariable=self.V_sc, width=10).grid(row=5, column=1)
        ttk.Label(input_frame, text="I_sc (A):").grid(row=6, column=0, sticky=tk.W)
        ttk.Entry(input_frame, textvariable=self.I_sc, width=10).grid(row=6, column=1)
        ttk.Label(input_frame, text="P_sc (W):").grid(row=7, column=0, sticky=tk.W)
        ttk.Entry(input_frame, textvariable=self.P_sc, width=10).grid(row=7, column=1)

        # Parámetros nominales
        ttk.Label(input_frame, text="Parámetros Nominales:").grid(row=8, column=0, columnspan=2, sticky=tk.W)
        ttk.Label(input_frame, text="V_primario (V):").grid(row=9, column=0, sticky=tk.W)
        ttk.Entry(input_frame, textvariable=self.V_rated_primary, width=10).grid(row=9, column=1)
        ttk.Label(input_frame, text="V_secundario (V):").grid(row=10, column=0, sticky=tk.W)
        ttk.Entry(input_frame, textvariable=self.V_rated_secondary, width=10).grid(row=10, column=1)
        ttk.Label(input_frame, text="S_rated (VA):").grid(row=11, column=0, sticky=tk.W)
        ttk.Entry(input_frame, textvariable=self.S_rated, width=10).grid(row=11, column=1)

        # Factor de potencia adicional
        ttk.Label(input_frame, text="Otro FP (d):").grid(row=12, column=0, sticky=tk.W)
        ttk.Entry(input_frame, textvariable=self.other_PF, width=10).grid(row=12, column=1)

        # Botones
        ttk.Button(input_frame, text="Calcular Circuito Equivalente (a)", command=self.calcular_equivalente).grid(row=13, column=0, columnspan=2, pady=5)
        ttk.Button(input_frame, text="VR 0.65 Atraso (b)", command=lambda: self.calcular_vr(0.65, 'atraso')).grid(row=14, column=0, columnspan=2, pady=2)
        ttk.Button(input_frame, text="VR 0.75 Adelanto (c)", command=lambda: self.calcular_vr(0.75, 'adelanto')).grid(row=15, column=0, columnspan=2, pady=2)
        ttk.Button(input_frame, text="VR Otro FP (d)", command=self.calcular_vr_otro).grid(row=16, column=0, columnspan=2, pady=2)

        # Resultados del circuito equivalente
        result_frame = ttk.Frame(self.master, padding="10")
        result_frame.grid(row=0, column=1, sticky=tk.W)
        ttk.Label(result_frame, text="Circuito Equivalente:").grid(row=0, column=0, columnspan=2, sticky=tk.W)
        ttk.Label(result_frame, text="Rc (Ω):").grid(row=1, column=0, sticky=tk.W)
        ttk.Label(result_frame, textvariable=self.Rc).grid(row=1, column=1)
        ttk.Label(result_frame, text="Xm (Ω):").grid(row=2, column=0, sticky=tk.W)
        ttk.Label(result_frame, textvariable=self.Xm).grid(row=2, column=1)
        ttk.Label(result_frame, text="Req_lv (Ω):").grid(row=3, column=0, sticky=tk.W)
        ttk.Label(result_frame, textvariable=self.Req_lv).grid(row=3, column=1)
        ttk.Label(result_frame, text="Xeq_lv (Ω):").grid(row=4, column=0, sticky=tk.W)
        ttk.Label(result_frame, textvariable=self.Xeq_lv).grid(row=4, column=1)

        # Área de texto para regulación
        self.vr_text = tk.Text(self.master, wrap=tk.WORD, width=50, height=15)
        self.vr_text.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    def calcular_equivalente(self):
        try:
            # Obtener valores
            V_oc = self.V_oc.get()
            I_oc = self.I_oc.get()
            P_oc = self.P_oc.get()
            V_sc = self.V_sc.get()
            I_sc = self.I_sc.get()
            P_sc = self.P_sc.get()
            V_prim = self.V_rated_primary.get()
            V_sec = self.V_rated_secondary.get()
            S_rated = self.S_rated.get()

            # Calcular Rc y Xm
            Rc = (V_oc ** 2) / P_oc
            S_oc = V_oc * I_oc
            Q_oc = math.sqrt(S_oc ** 2 - P_oc ** 2)
            Xm = (V_oc ** 2) / Q_oc

            # Calcular Req y Xeq en HV
            Req_hv = P_sc / (I_sc ** 2)
            Zsc_hv = V_sc / I_sc
            Xeq_hv = math.sqrt(Zsc_hv ** 2 - Req_hv ** 2)

            # Convertir a LV
            a = V_prim / V_sec
            Req_lv = Req_hv / (a ** 2)
            Xeq_lv = Xeq_hv / (a ** 2)

            # Actualizar variables
            self.Rc.set(round(Rc, 4))
            self.Xm.set(round(Xm, 4))
            self.Req_lv.set(round(Req_lv, 6))  # Valores pequeños
            self.Xeq_lv.set(round(Xeq_lv, 6))
        except Exception as e:
            self.vr_text.insert(tk.END, f"Error: {str(e)}\n")

    def calcular_vr(self, fp, tipo):
        try:
            Req = self.Req_lv.get()
            Xeq = self.Xeq_lv.get()
            V_sec = self.V_rated_secondary.get()
            S_n = self.S_rated.get()

            # Calcular ángulo
            theta = math.acos(fp) if tipo == 'atraso' else -math.acos(fp)
            sin_theta = math.sin(theta)

            # Cargas
            cargas = [0.4, 0.6, 0.8, 1.0, 1.2]
            resultados = []

            for carga in cargas:
                S = S_n * carga
                I = S / V_sec
                V_nl = V_sec

                # Términos
                term1 = I * (Req * fp + Xeq * sin_theta)
                term2 = I * (Req * math.sin(theta) - Xeq * math.cos(theta))

                discriminante = V_nl**2 - term2**2
                if discriminante < 0:
                    vr = "N/A"
                else:
                    V_load = -term1 + math.sqrt(discriminante)
                    vr = ((V_nl - V_load) / V_load) * 100 if V_load != 0 else "N/A"
                    vr = round(vr, 2) if isinstance(vr, float) else vr

                resultados.append(f"{int(carga*100)}%: {vr}%")

            # Mostrar resultados
            self.vr_text.delete(1.0, tk.END)
            self.vr_text.insert(tk.END, f"Regulación de Voltaje (FP={fp} {tipo}):\n")
            self.vr_text.insert(tk.END, "\n".join(resultados) + "\n")
        except Exception as e:
            self.vr_text.insert(tk.END, f"Error: {str(e)}\n")

    def calcular_vr_otro(self):
        fp = self.other_PF.get()
        self.calcular_vr(fp, 'atraso')  # Asumir atraso por defecto

# Iniciar GUI
root = tk.Tk()
app = TransformerGUI(root)
root.mainloop()