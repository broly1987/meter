import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import smtplib
import imaplib
import email
import threading


# Ventana principal de la aplicación
class ReminderApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Recordatorios")

        # Configurar la interfaz de usuario
        self.message_label = tk.Label(self, text="Mensaje:")
        self.message_entry = tk.Entry(self, width=30)
        self.datetime_label = tk.Label(self, text="Fecha y Hora (YYYY-MM-DD HH:MM):")
        self.datetime_entry = tk.Entry(self, width=20)
        self.email_label = tk.Label(self, text="Correo electrónico:")
        self.email_entry = tk.Entry(self, width=30)
        self.add_button = tk.Button(self, text="Agregar", command=self.add_reminder)
        self.stop_button = tk.Button(self, text="Detener", command=self.stop_reminders)
        self.task_text = tk.Text(self, width=40, height=10)

        # Colocar los elementos en la ventana
        self.message_label.pack()
        self.message_entry.pack()
        self.datetime_label.pack()
        self.datetime_entry.pack()
        self.email_label.pack()
        self.email_entry.pack()
        self.add_button.pack()
        self.stop_button.pack()
        self.task_text.pack()

        # Variables para el estado del programa
        self.reminders = []
        self.running = False

        # Iniciar la aplicación
        self.load_reminders()
        self.check_reminders()
        self.mainloop()

    # Agregar un nuevo recordatorio
    def add_reminder(self):
        message = self.message_entry.get()
        datetime_str = self.datetime_entry.get()
        email = self.email_entry.get()

        if not message or not datetime_str or not email:
            messagebox.showwarning("Error", "Por favor, complete todos los campos.")
            return

        try:
            datetime_obj = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
        except ValueError:
            messagebox.showwarning("Error", "Formato de fecha y hora inválido. Utilice 'YYYY-MM-DD HH:MM'.")
            return

        reminder = {
            "message": message,
            "datetime": datetime_obj,
            "email": email
        }

        self.reminders.append(reminder)
        self.task_text.insert(tk.END,
                              f"Recordatorio agregado:\nMensaje: {message}\nFecha y Hora: {datetime_str}\nEmail: {email}\n\n")
        self.save_reminders()

        # Reiniciar el temporizador si no está en ejecución
        if not self.running:
            self.check_reminders()

    # Guardar los recordatorios en un archivo
    def save_reminders(self):
        with open("reminders.txt", "w") as file:
            for reminder in self.reminders:
                file.write(f"{reminder['message']},{reminder['datetime']},{reminder['email']}\n")

    # Cargar los recordatorios desde el archivo
    def load_reminders(self):
        try:
            with open("reminders.txt", "r") as file:
                for line in file:
                    line = line.strip()
                    if line:
                        message, datetime_str, email = line.split(",")
                        datetime_obj = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
                        reminder = {
                            "message": message,
                            "datetime": datetime_obj,
                            "email": email
                        }
                        self.reminders.append(reminder)
        except FileNotFoundError:
            pass

    # Verificar los recordatorios y enviar notificaciones
    def check_reminders(self):
        def send_email(message, email):
            # Configurar el servidor SMTP y enviar el correo electrónico
            with smtplib.SMTP("smtp.office365.com", 587) as server:
                server.starttls()
                server.login("slotriviera@outlook.com", "Slot1234")  # Reemplaza con tus credenciales de Outlook
                msg = email.message.EmailMessage()
                msg.set_content(message)
                msg["Subject"] = "Recordatorio"
                msg["From"] = "slotriviera@outlook.com"  # Reemplaza con tu correo electrónico de Outlook
                msg["To"] = email
                server.send_message(msg)

        def process_reminder(reminder):
            if reminder["datetime"] <= datetime.now():
                send_email(reminder["email"], reminder["message"])

                self.task_text.insert(tk.END,
                                      f"Tarea realizada:\nMensaje: {reminder['message']}\nFecha y Hora: {reminder['datetime']}\nEmail: {reminder['email']}\n\n")
                self.reminders.remove(reminder)
                self.save_reminders()

        def check_email_thread():
            while self.running:
                for reminder in self.reminders:
                    process_reminder(reminder)
                self.check_email_for_done()
                # Intervalo de comprobación de correos electrónicos (en segundos)
                interval = 60
                threading.Timer(interval, check_email_thread).start()

        # Iniciar el temporizador
        self.running = True
        threading.Thread(target=check_email_thread).start()

    # Verificar si se ha respondido al correo con la palabra "done"
    def check_email_for_done(self):
        # Configurar el servidor IMAP y autenticarse
        mail = imaplib.IMAP4_SSL("outlook.office365.com")
        mail.login("slotriviera@outlook.com", "Slot1234")  # Reemplaza con tus credenciales de Outlook

        # Seleccionar la bandeja de entrada
        mail.select("inbox")

        # Buscar los mensajes sin leer
        status, data = mail.search(None, "UNSEEN")

        if status == "OK":
            for num in data[0].split():
                status, email_data = mail.fetch(num, "(RFC822)")

                if status == "OK":
                    raw_email = email_data[0][1]
                    email_message = email.message_from_bytes(raw_email)

                    # Obtener el remitente y el cuerpo del mensaje
                    sender = email_message["From"]
                    body = ""

                    if email_message.is_multipart():
                        for part in email_message.walk():
                            content_type = part.get_content_type()
                            if content_type == "text/plain":
                                body = part.get_payload(decode=True)
                                break
                    else:
                        body = email_message.get_payload(decode=True)

                    if isinstance(body, bytes):
                        body = body.decode()

                    # Verificar si el mensaje contiene la palabra "done"
                    if "done" in body.lower():
                        self.task_text.insert(tk.END, f"¡Tarea completada por {sender}!\n\n")

                # Marcar el mensaje como leído
                mail.store(num, "+FLAGS", "\\Seen")

        # Cerrar la conexión con el servidor IMAP
        mail.logout()

    # Detener los recordatorios y la aplicación
    def stop_reminders(self):
        self.running = False


# Ejecutar la aplicación
if __name__ == "__main__":
    ReminderApp()
