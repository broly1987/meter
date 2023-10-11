import pandas as pd

# Leer el archivo Excel original
df = pd.read_excel(r"C:\\Users\\slotr\\Downloads\\reporte.xlsx")

# Realizar las operaciones necesarias en el DataFrame (por ejemplo, renombrar columnas y eliminar filas)
df = df.rename(columns={'Base': 'lockname', 'Unnamed: 1': 'Machine', 'Unnamed: 2': 'Bank', 'Unnamed: 3': 'manufacture',"Unnamed: 5":"Brand","Unnamed: 6":"Promo Cost"
,"Unnamed: 7":"Brand","Slot Result WithOut Promo SRD":"Profit","Unnamed: 10":"Total in","Unnamed: 11":"Total Out","Unnamed: 12":"Handpay","Unnamed: 13":"Ticket in","Unnamed: 14":"Ticket out",
    "Unnamed: 15":"Cashless in","Unnamed: 16":"Cashless out","Unnamed: 17":"Bills","Unnamed: 18":"Jackpot","Unnamed: 19":"Cancell credit","Unnamed: 20":"Games",
    "Unnamed: 24":"Promo Ticket"})
#df = df.drop(columns=['LUDOTECH',"Unnamed: 4","Unnamed: 8","Unnamed: 21","Unnamed: 22","Unnamed: 23"])
df = df.drop(index=[0, 1])
print(df.columns)

df["Profit"] = pd.to_numeric(df["Profit"], errors="coerce")
top_10_profit = df.sort_values(by="Profit", ascending=False).head(20)
botom_10_profit = df.sort_values(by="Profit", ascending=True).head(20)
valor_max=df["Profit"].max()
# Calcular la columna 'actual Holding' a partir de las columnas existentes
df["actual Holding"] = (df["Profit"] / df["Total In SRD"]).apply(lambda x: round(x * 100, 2) if not pd.isna(x) else None)

num =int(input("1 if you want to save the file or 2 if you want to print the columns "))

if num == 1 :

    # Crear un escritor de Excel para el nuevo archivo
    with pd.ExcelWriter(r"C:\Users\slotr\Downloads\reporte_nuevo.xlsx", engine="xlsxwriter") as writer:

        # Guardar el DataFrame en una nueva hoja de Excel
        df.to_excel(writer, sheet_name='prueba1', index=False)

    # El nuevo archivo "nuevo_archivo.xlsx" contiene los datos procesados
elif num ==2 :
    print(df)
    print(df["lockname"])
    print(top_10_profit[["lockname", "Profit"]])
    print(botom_10_profit[["lockname", "Profit"]])
else:
    print("none of options are correct")