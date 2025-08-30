import os
import win32com.client
from datetime import datetime

# 📁 Ruta donde se guardarán los adjuntos (carpeta "adjuntos")
RUTA_ADJUNTOS = os.path.join(os.getcwd(), "adjuntos")
os.makedirs(RUTA_ADJUNTOS, exist_ok=True)

try:
    # 📨 Conectarse a Outlook
    outlook = win32com.client.Dispatch("Outlook.Application")
    namespace = outlook.GetNamespace("MAPI")

    # Verificar que la conexión a la bandeja de entrada sea exitosa
    bandeja_entrada = namespace.GetDefaultFolder(6)  # Bandeja de entrada
    if not bandeja_entrada:
        raise ValueError("No se pudo acceder a la bandeja de entrada")

    correos = bandeja_entrada.Items
    correos.Sort("[ReceivedTime]", True)  # Correos más recientes primero

    # 📅 Fecha de hoy
    hoy = datetime.now().date()

    # 🔍 Verificar si se encontraron correos
    print(f"Se encontraron {len(correos)} correos en la bandeja de entrada.")

    # 🔍 Recorremos los correos de hoy con adjuntos
    for correo in correos:
        if correo.Class == 43:  # 43 = MailItem
            recibido = correo.ReceivedTime.date()

            # Verifica si el correo es de hoy y tiene adjuntos
            if recibido == hoy and correo.Attachments.Count > 0:
                
                # Verificar si el asunto contiene "SEGUIMIENTO CONSUMO"
                print(f"Verificando correo: {correo.Subject}")  # Imprimir el asunto
                if "SEGUIMIENTO CONSUMO" in correo.Subject:
                    print(f"\n📩 Asunto: {correo.Subject}")
                    for adjunto in correo.Attachments:
                        nombre = adjunto.FileName
                        ruta = os.path.join(RUTA_ADJUNTOS, nombre)
                        adjunto.SaveAsFile(ruta)
                        print(f"✅ Guardado: {ruta}")
                else:
                    print(f"✋ No es un correo relevante: {correo.Subject}")

except Exception as e:
    print(f"Error al acceder a Outlook: {e}")


