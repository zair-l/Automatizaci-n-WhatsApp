from fastapi import FastAPI, UploadFile, File
import pytesseract
from PIL import Image
import cv2, numpy as np, io, re
from datetime import datetime

app = FastAPI()

def preprocesar_imagen(image_bytes):
    nparr = np.frombuffer(image_bytes, np.uint8)
    img   = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    gray  = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    return thresh

def extraer_datos(texto):
    texto_limpio = " ".join(texto.split())
    monto_match = re.search(r'[S58B]/\.?\s*(\d+(?:[.,]\d{1,2})?)', texto_limpio, re.IGNORECASE)
    oper_match = re.search(r'(?:operaci[oó]n|nro\.?\s*de|transacci[oó]n)[:\s]+(\d+)', texto_limpio, re.IGNORECASE)
    fecha_match = re.search(r'(\d{2}/\d{2}/\d{4})', texto_limpio)
    monto = monto_match.group(1).replace(',', '.') if monto_match else None
    
    return {
        "monto":      monto,
        "operacion":  oper_match.group(1) if oper_match else None,
        "fecha":      fecha_match.group(1) if fecha_match else datetime.now().strftime('%d/%m/%Y'),
        "tipo":       "Yape" if "yape" in texto.lower() else 
                      "Plin" if "plin" in texto.lower() else "Desconocido",
        "texto_raw":  texto
    }

@app.post("/procesar-imagen")
async def procesar_imagen(file: UploadFile = File(...)):
    contenido = await file.read()
    img_proc  = preprocesar_imagen(contenido)
    texto     = pytesseract.image_to_string(img_proc, lang='spa')
    datos     = extraer_datos(texto)
    datos["valido"] = datos["monto"] is not None
    return datos