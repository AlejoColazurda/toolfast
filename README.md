# toolfast

**toolfast** es una navaja suiza de herramientas CLI interactiva desarrollada en Python y diseñada especialmente para facilitar tareas administrativas y de oficina del día a día de forma 100% automatizada.

Desarrollado por: **Alejo Colazurda**

---

## 🛠️ Herramientas Incluidas

1. **Gestión de PDFs:**
   * **Unificar PDFs:** Combina todos los PDFs de una carpeta en un único archivo (orden alfabético).
   * **Separar PDFs:** Extrae rangos de páginas específicos o guarda cada página por separado.
   * **Comprimir PDFs:** Reduce el tamaño físico de los archivos optimizando los flujos internos.
   * **Extractor de Texto:** Extrae y guarda el contenido de texto embebido en un documento PDF a un archivo `.txt`.

2. **Conversor de Formatos Inteligente:**
   * Conversión mutua entre formatos de imagen: **PNG, JPG, WEBP, BMP**.
   * Conversión rápida de **Imágenes a PDF**.
   * Conversión de **Excel (.xlsx) a CSV** y **CSV a Excel (.xlsx)**.
   * *Validación Inteligente:* Si pides una conversión imposible, la consola te avisará en rojo y te sugerirá una opción viable de inmediato.

3. **Herramientas de Oficina y Organización:**
   * **Renombrado Masivo:** Agrega prefijos, sufijos, reemplaza palabras o numera archivos de una carpeta en lote.
   * **Organizador Automático de Carpetas:** Limpia y ordena tu carpeta de Descargas (o cualquier directorio) clasificando los archivos sueltos en carpetas automáticas (`PDFs`, `Imagenes`, `Planillas_Excel`, `Documentos`, `Comprimidos`).

4. **Buscador de Actualizaciones Integrado:**
   * Actualiza el script en segundos directo desde GitHub.

---

## 🚀 Instalación Rápida (Windows)

Para instalar **toolfast** por primera vez en cualquier computadora, abre el **Símbolo del sistema (cmd)** o **PowerShell** y ejecuta este comando de una sola línea:

```cmd
powershell -ExecutionPolicy Bypass -Command "[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.SecurityProtocolType]::Tls12; iwr -useb https://raw.githubusercontent.com/AlejoColazurda/toolfast/main/instalar_toolfast.ps1 | iex"
```

O bien, si tienes la carpeta del repositorio descargada, haz doble clic en `instalar.bat`.

---

## 💻 Cómo se Usa

Una vez finalizada la instalación, **abre una NUEVA ventana de cmd o PowerShell** y escribe:

```cmd
toolfast
```

Sigue las instrucciones interactivas del menú en pantalla para realizar todas tus tareas administrativas rápido y sin esfuerzo.
