from funciones import *

async def buscarMensaje(messageID,buscar="mensaje",ID=False):

    for clave in canales:
        historial = canales[clave]["historial"]
        mensaje = historial.get(messageID)

        if mensaje:
            if ID:

                if buscar == "canal":
                    return canales[clave]["ID"]
                elif buscar == "espejo":
                    return mensaje["espejo"]

                return mensaje["ID"]
            else:
                if buscar == "canal":
                    return clave
                elif buscar == "espejo":
                    return await buscarMensaje(mensaje["espejo"])

                return mensaje["contenido"]
    
    return False

async def editarMensajeEspejo(before, after):
    #Claro, si la edicion no cambio nada ps no hace nada
    if before.content == after.content:
        return

    #Si no esta en nuestro registro, no lo tomes en cuenta para editar de vuelta
    for valor in canales.values():
        if before.id in valor["historial"]:
            #Esto obtiene el objeto con los datos necesarios del canal para poder saber que hacer exacmente
            config = canales[await buscarMensaje(after.id,buscar="canal")]

            if not config:
                return
            
            try:
                #Esto genera la traduccion nueva tomando en cuenta el nuevo mensaje editado, y el webhook aun sin traducir
                from .traductor import traducir
                nueva_traduccion = await traducir(after,config)
                webhook_a_traducir = valor["historial"][before.id]["espejo"]

                async with aiohttp.ClientSession() as session:
                    #Esta magia negra creo que extrae el webhook de el cliente de la url de de discord de los sueños de Mishu o algo asi
                    webhook = Webhook.from_url(config["webhook_destino"], session=session)

                    # Ya con todo listo, solo edita el mensaje
                    await webhook.edit_message(webhook_a_traducir,content=nueva_traduccion)
            except Exception as e:
                print("¿Debia editar algo? Ah si, me equivoque")
                print(e)