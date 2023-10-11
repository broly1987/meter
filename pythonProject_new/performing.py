import pandas as pd
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class PerformingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Machine Analysis")
        self.bienvenida_label = tk.Label(root, text="Welcome to the Excel File Processor", font=("Arial", 16, "bold"))
        self.bienvenida_label.pack()

        self.cargar_button = tk.Button(root, text="Load File", command=self.cargar_archivo_and_cargar_datos,
                                       font=("Arial", 12))
        self.cargar_button.pack()

    def mostrar_resultados(self, top_df, bottom_df):

        top_df.rename(columns={'PROMO Ticket in currency Value SRD': 'Promo Ticket'}, inplace=True)
        bottom_df.rename(columns={'PROMO Ticket in currency Value SRD': 'Promo Ticket'}, inplace=True)
        top_df.rename(columns={'Base': 'Lockname'}, inplace=True)
        bottom_df.rename(columns={'Base': 'Lockname'}, inplace=True)
        top_df.rename(columns={'Profit (based on meters) SRD': 'Profit(meters)'}, inplace=True)
        bottom_df.rename(columns={'Profit (based on meters) SRD': 'Profit(meters)'}, inplace=True)
        top_df.rename(columns={'Total Promo Cost SRD SRD': 'Total Promo'},inplace=True)
        bottom_df.rename(columns={'Total Promo Cost SRD SRD':'Total Promo'},inplace=True)
        top_df.rename(columns={'Jackpot meter SRD':'Jackpots'},inplace=True)
        bottom_df.rename(columns={'Jackpot meter SRD': 'Jackpots'}, inplace=True)
        top_window = tk.Toplevel(self.root)
        top_window.title("High and Low Performing")
        top_window.geometry("1200x900")


        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        fig.suptitle("High and Low Performing", fontsize=16)

        top_df.plot(kind='bar', x='Lockname', y='Profit(meters)', ax=axes[0], color='skyblue')
        axes[0].set_title('Best Machines', fontsize=12)
        axes[0].set_ylabel('Profit (based on meters) SRD')
        axes[0].set_xlabel('Lockname')

        bottom_df.plot(kind='bar', x='Lockname', y='Profit(meters)', ax=axes[1], color='salmon')
        axes[1].set_title('Worst Machines', fontsize=12)
        axes[1].set_ylabel('Profit (based on meters) SRD')
        axes[1].set_xlabel('Lockname')

        top_df['Lockname'] = top_df['Lockname'].astype(int)
        bottom_df['Lockname'] = bottom_df['Lockname'].astype(int)
        top_df['Hold'] = top_df['Hold'].round().astype(int).astype(str) + "%"
        bottom_df['Hold'] = bottom_df['Hold'].round().astype(int).astype(str) + "%"

        mejores_label = tk.Label(top_window, text="Top Machines:", font=("Arial", 14, "bold"))
        mejores_label.pack()

        mejores_text = tk.Text(top_window, height=15, width=80)
        mejores_text.pack()
        top_df_subset = top_df[['Lockname', 'Manufacturer', 'Profit(meters)','Promo Ticket','Hold','Total Promo','Jackpots']]

        mejores_text.insert(tk.END, top_df_subset.to_string(index=False))

        peores_label = tk.Label(top_window, text="Worst Machines:", font=("Arial", 14, "bold"))
        peores_label.pack()

        peores_text = tk.Text(top_window, height=15, width=80)
        peores_text.pack()
        bottom_df_subset = bottom_df[['Lockname', 'Manufacturer', 'Profit(meters)','Promo Ticket','Hold','Total Promo','Jackpots']]

        peores_text.insert(tk.END, bottom_df_subset.to_string(index=False))

        canvas = FigureCanvasTkAgg(fig, master=top_window)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack()

    def cargar_datos(self, archivo_path):
        df = pd.read_excel(archivo_path, skiprows=2)

        df = df[df['Profit (based on meters) SRD'].apply(
            lambda x: str(x).replace(',', '').replace('.', '', 1).replace('-', '').replace(' ', '').isdigit())]
        df['Profit (based on meters) SRD'] = pd.to_numeric(df['Profit (based on meters) SRD'], errors='coerce')

        columnas_a_eliminar = [
            'Promo Cashless Out SRD',
            'Promo Cashless In SRD',
            'Games played',
            'Credit Cancel SRD',
            'Cashless Out SRD',
            'Cashless In SRD',
            'Slot Result WithOut Promo SRD',
            'Bank',
            'Machine'
        ]
        df = df.drop(columns=columnas_a_eliminar)

        df['Total Out SRD'] = pd.to_numeric(df['Total Out SRD'], errors='coerce')
        df['Total In SRD'] = pd.to_numeric(df['Total In SRD'], errors='coerce')

        df['Hold'] = ((df['Profit (based on meters) SRD'] / df['Total In SRD']) * 100)

        mejores_maquinas = df.nlargest(10,
                                       'Profit (based on meters) SRD')  # Seleccionar las 10 con los valores más altos
        peores_maquinas = df.nsmallest(10,
                                       'Profit (based on meters) SRD')  # Seleccionar las 10 con los valores más bajos

        self.mostrar_resultados(mejores_maquinas, peores_maquinas)

    def cargar_archivo_and_cargar_datos(self):
        archivo_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
        if archivo_path:
            self.cargar_datos(archivo_path)


if __name__ == "__main__":
    root = tk.Tk()
    app = PerformingApp(root)
    root.mainloop()
