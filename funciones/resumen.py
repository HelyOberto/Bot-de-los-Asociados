from funciones import *

async def resumir(texto, promt= "Comprime este texto en un parrafo resumido, manten el tiempo verbal y la persona, no me respondas a mi, solo comprime:"):

    respuesta = False
    try:
        resumen = await co.chat(message=promt +"\n\n" + texto)
        respuesta = resumen.text
    except Exception as e:
        print(e)

    return respuesta