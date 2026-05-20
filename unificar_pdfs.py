# -*- coding: utf-8 -*-
import os
import sys
import subprocess
import re
import urllib.request
from glob import glob

# =====================================================================
# CONFIGURACIÓN DE ACTUALIZACIÓN
# =====================================================================
VERSION = "1.0.0"

# URL apuntando al nuevo repositorio 'toolfast'
GITHUB_RAW_URL = "https://raw.githubusercontent.com/AlejoColazurda/toolfast/main/unificar_pdfs.py"
# =====================================================================

# Habilitar soporte de colores ANSI en la terminal de Windows
if os.name == 'nt':
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
    except Exception:
        pass

# Colores ANSI
C_GREEN = "\033[92m"
C_CYAN = "\033[96m"
C_YELLOW = "\033[93m"
C_RED = "\033[91m"
C_BOLD = "\033[1m"
C_END = "\033[0m"

# Intentar importar pypdf o PyPDF2 de forma segura. Si no existen, los instala.
try:
    import pypdf
    MERGER_CLASS = pypdf.PdfMerger
except ImportError:
    try:
        import PyPDF2
        if hasattr(PyPDF2, 'PdfMerger'):
            MERGER_CLASS = PyPDF2.PdfMerger
        else:
            MERGER_CLASS = PyPDF2.PdfFileMerger
    except ImportError:
        print(f"{C_YELLOW}Instalando la librería necesaria para manipulación de PDFs...{C_END}")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pypdf"])
            import pypdf
            MERGER_CLASS = pypdf.PdfMerger
            print(f"{C_GREEN}Librería instalada correctamente.{C_END}\n")
        except Exception as e:
            print(f"{C_RED}Error al intentar instalar automáticamente la librería: {e}{C_END}")
            print("Por favor, instala la librería manualmente usando: pip install pypdf")
            sys.exit(1)

def parse_version(v_str):
    """Convierte un string de versión '1.0.0' en una tupla de enteros (1, 0, 0) para comparar."""
    try:
        return tuple(map(int, v_str.split('.')))
    except Exception:
        return (0, 0, 0)

def comprobar_actualizaciones(silencioso=False):
    """Consulta la URL de GitHub en busca de una versión superior del script."""
    if not silencioso:
        print(f"\n{C_YELLOW}Buscando actualizaciones en GitHub...{C_END}")
    
    try:
        req = urllib.request.Request(
            GITHUB_RAW_URL, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            codigo_remoto = response.read().decode('utf-8')
            
        match = re.search(r'VERSION\s*=\s*["\']([^"\']+)["\']', codigo_remoto)
        if match:
            version_remota = match.group(1)
            
            if parse_version(version_remota) > parse_version(VERSION):
                print(f"\n{C_GREEN}{C_BOLD}¡Nueva versión disponible! ({version_remota}){C_END}")
                print(f"Tu versión actual es: {VERSION}")
                
                confirmacion = input("¿Deseas actualizar el programa ahora mismo? (S/N, por defecto S): ").strip().upper()
                if confirmacion in ('S', 'SI', ''):
                    ruta_local = os.path.abspath(__file__)
                    
                    with open(ruta_local, 'w', encoding='utf-8') as f:
                        f.write(codigo_remoto)
                        
                    print(f"\n{C_GREEN}{C_BOLD}¡Actualización exitosa!{C_END}")
                    print(f"Se ha instalado la versión {C_BOLD}{version_remota}{C_END}. Por favor, vuelve a iniciar el programa.")
                    sys.exit(0)
            else:
                if not silencioso:
                    print(f"{C_GREEN}¡Ya tienes la última versión instalada! (v{VERSION}){C_END}")
        else:
            if not silencioso:
                print(f"{C_RED}No se pudo leer la versión en el servidor remoto.{C_END}")
    except Exception as e:
        if not silencioso:
            print(f"{C_RED}Error al conectar con GitHub para buscar actualizaciones: {e}{C_END}")
            print(f"Asegúrate de que el repositorio 'toolfast' esté creado en tu cuenta y sea público.")

def print_header():
    print(f"\n{C_CYAN}{C_BOLD}" + "="*60)
    print(f"        UNIFICADOR DE ARCHIVOS PDF - v{VERSION}         ")
    print("="*60 + f"{C_END}")

def unificar_carpeta():
    print_header()
    print(f"{C_BOLD}--- OPCIÓN 1: Unificar una carpeta completa ---{C_END}\n")
    
    carpeta_origen = input(f"Ingresa la ruta de la carpeta con los PDFs: ").strip().strip('"')
    if not carpeta_origen:
        print(f"{C_RED}Ruta no válida.{C_END}")
        return
        
    carpeta_origen = os.path.abspath(carpeta_origen)
    if not os.path.exists(carpeta_origen):
        print(f"{C_RED}Error: La carpeta '{carpeta_origen}' no existe.{C_END}")
        return
        
    nombre_salida = input(f"Nombre o ruta del PDF resultante (ej: unificado.pdf): ").strip().strip('"')
    if not nombre_salida:
        nombre_salida = "unificado.pdf"
        
    if not nombre_salida.lower().endswith(".pdf"):
        nombre_salida += ".pdf"
        
    if not os.path.isabs(nombre_salida):
        archivo_salida = os.path.join(carpeta_origen, nombre_salida)
    else:
        archivo_salida = nombre_salida
        
    archivo_salida = os.path.abspath(archivo_salida)
    
    patron = os.path.join(carpeta_origen, "*.pdf")
    archivos_pdf = glob(patron)
    archivos_pdf = [f for f in archivos_pdf if os.path.abspath(f) != archivo_salida]
    
    if not archivos_pdf:
        print(f"{C_YELLOW}No se encontraron archivos PDF en la carpeta '{carpeta_origen}'.{C_END}")
        return
        
    archivos_pdf.sort(key=lambda x: os.path.basename(x).lower())
    
    ejecutar_unificacion(archivos_pdf, archivo_salida)

def unificar_seleccion_manual():
    print_header()
    print(f"{C_BOLD}--- OPCIÓN 2: Seleccionar archivos manualmente ---{C_END}\n")
    print("Ingresa las rutas de los archivos PDF uno por uno en el orden en que deseas unificarlos.")
    print("Cuando termines de ingresar archivos, escribe 'listo' o 'fin'.\n")
    
    archivos_pdf = []
    while True:
        entrada = input(f"Ruta del PDF #{len(archivos_pdf) + 1} (o 'listo'): ").strip().strip('"')
        if entrada.lower() in ('listo', 'fin', ''):
            break
            
        archivo_abs = os.path.abspath(entrada)
        if not os.path.exists(archivo_abs):
            print(f"{C_RED}Error: El archivo no existe en la ruta especificada.{C_END}")
        elif not archivo_abs.lower().endswith(".pdf"):
            print(f"{C_YELLOW}Advertencia: El archivo debe ser un archivo PDF.{C_END}")
        else:
            archivos_pdf.append(archivo_abs)
            print(f"{C_GREEN}Agregado correctamente.{C_END}")
            
    if not archivos_pdf:
        print(f"{C_YELLOW}No ingresaste ningún archivo.{C_END}")
        return
        
    archivo_salida = input(f"\nIngresa la ruta completa del PDF de salida (ej: C:\\salida.pdf): ").strip().strip('"')
    if not archivo_salida:
        print(f"{C_RED}Ruta de salida no válida.{C_END}")
        return
        
    if not archivo_salida.lower().endswith(".pdf"):
        archivo_salida += ".pdf"
        
    archivo_salida = os.path.abspath(archivo_salida)
    
    ejecutar_unificacion(archivos_pdf, archivo_salida)

def ejecutar_unificacion(archivos_pdf, archivo_salida):
    print(f"\n{C_CYAN}Archivos a unificar ({len(archivos_pdf)}):{C_END}")
    for idx, f in enumerate(archivos_pdf, 1):
        print(f" {idx}. {os.path.basename(f)} ({os.path.dirname(f)})")
        
    confirmacion = input(f"\n¿Confirmas la unificación de estos archivos? (S/N, por defecto S): ").strip().upper()
    if confirmacion not in ('S', 'SI', ''):
        print(f"{C_YELLOW}Operación cancelada.{C_END}")
        return
        
    print(f"\n{C_YELLOW}Unificando archivos...{C_END}")
    merger = MERGER_CLASS()
    
    for pdf in archivos_pdf:
        try:
            merger.append(pdf)
        except Exception as e:
            print(f"{C_RED}Error al agregar {os.path.basename(pdf)}: {e}{C_END}")
            merger.close()
            return
            
    try:
        directorio_salida = os.path.dirname(archivo_salida)
        if directorio_salida and not os.path.exists(directorio_salida):
            os.makedirs(directorio_salida, exist_ok=True)
            
        merger.write(archivo_salida)
        print(f"\n{C_GREEN}{C_BOLD}¡Éxito! PDF unificado guardado en:{C_END}")
        print(f"--> {C_BOLD}{archivo_salida}{C_END}")
    except Exception as e:
        print(f"{C_RED}Error al guardar el PDF unificado: {e}{C_END}")
    finally:
        merger.close()

def menu_principal():
    try:
        comprobar_actualizaciones(silencioso=True)
    except Exception:
        pass

    while True:
        print_header()
        print(f"Selecciona una opción:")
        print(f" {C_GREEN}1.{C_END} Unificar todos los PDFs de una carpeta (orden alfabético)")
        print(f" {C_GREEN}2.{C_END} Unificar PDFs seleccionándolos manualmente uno a uno")
        print(f" {C_GREEN}3.{C_END} Buscar actualizaciones del programa")
        print(f" {C_GREEN}4.{C_END} Salir")
        
        opcion = input(f"\nOpción (1-4): ").strip()
        
        if opcion == "1":
            unificar_carpeta()
        elif opcion == "2":
            unificar_seleccion_manual()
        elif opcion == "3":
            comprobar_actualizaciones(silencioso=False)
        elif opcion == "4":
            print(f"\n{C_CYAN}¡Hasta luego!{C_END}")
            break
        else:
            print(f"{C_RED}Opción no válida. Por favor, selecciona una opción entre 1 y 4.{C_END}")
            
        input(f"\nPresiona {C_BOLD}Enter{C_END} para volver al menú...")
        os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] in ('--update', '-u'):
            comprobar_actualizaciones(silencioso=False)
            sys.exit(0)
            
        if len(sys.argv) < 3:
            print(f"{C_RED}Uso: unificarpdfs <ruta_carpeta_origen> <ruta_pdf_salida>{C_END}")
            print(f"O bien: unificarpdfs --update (para buscar actualizaciones)")
            sys.exit(1)
            
        carpeta = sys.argv[1]
        salida = sys.argv[2]
        
        carpeta_abs = os.path.abspath(carpeta)
        if not os.path.exists(carpeta_abs):
            print(f"{C_RED}Error: La carpeta '{carpeta}' no existe.{C_END}")
            sys.exit(1)
            
        patron = os.path.join(carpeta_abs, "*.pdf")
        pdfs = glob(patron)
        
        salida_abs = os.path.abspath(salida)
        pdfs = [p for p in pdfs if os.path.abspath(p) != salida_abs]
        
        if not pdfs:
            print(f"{C_YELLOW}No se encontraron PDFs en la carpeta '{carpeta}'.{C_END}")
            sys.exit(1)
            
        pdfs.sort(key=lambda x: os.path.basename(x).lower())
        
        print(f"Unificando {len(pdfs)} PDFs en {salida_abs}...")
        merger = MERGER_CLASS()
        for pdf in pdfs:
            merger.append(pdf)
        merger.write(salida_abs)
        merger.close()
        print(f"{C_GREEN}¡Éxito! PDF unificado creado.{C_END}")
    else:
        menu_principal()
