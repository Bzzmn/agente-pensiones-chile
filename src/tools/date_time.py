import pytz
from datetime import datetime

def get_current_time(_=None):
    # Definir la zona horaria de Santiago, Chile
    chile_tz = pytz.timezone('America/Santiago')
    
    # Obtener la fecha y hora actual en esa zona
    now = datetime.now(chile_tz)
    
    # Formatear la fecha y hora según el formato deseado
    formatted_time = now.strftime("%Y-%m-%d %H:%M:%S %Z")
    return formatted_time

if __name__ == "__main__":
    print("La hora actual en Chile es:", get_current_time())