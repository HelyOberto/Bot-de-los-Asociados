from funciones import *
from .traductor import traducir

async def conectar(message,canal_ingles,canal_espanol):
    salidaClave = None
    llegadaClave = None

    #La Doctrina Dry es una cosa
    if message.channel.id == canales[canal_ingles]["ID"]:
        salidaClave = canal_ingles
        salida = canales[canal_ingles]

        llegadaClave = canal_espanol
        llegada = canales[canal_espanol]

    elif message.channel.id == canales[canal_espanol]["ID"]:
        salidaClave = canal_espanol
        salida = canales[canal_espanol]

        llegadaClave = canal_ingles
        llegada = canales[canal_ingles]
    else:
        return
    
    
    

    #Esto evita que bot no se cofunda consigo mismo, me suele pasar cuando me volteo y me miro al espejo
    if message.webhook_id or bot.user == message.author:
        return
    
    try:
        #Esto extrae el webhook del canal y para usarlo
        async with aiohttp.ClientSession() as session:
            webhook =  Webhook.from_url(salida["webhook_destino"],session=session)

            canal_destino = bot.get_channel(llegada["ID"])

            async with canal_destino.typing():
                traduccion = await traducir(message,salida)

                #Aca se agregan los stickers y las imagenes
                for sticker in message.stickers:
                    traduccion += f"\n{sticker.url}"

                for archivo in message.attachments:
                    traduccion += f"\n{archivo.url}"

                if traduccion == "":
                    return
            
            msj_enviado = await webhook.send(
                content=traduccion,
                username= message.author.display_name,
                avatar_url= message.author.display_avatar.url,
                wait=True
            )

        # lista_mensajes_id[message.id] = msj_enviado.id

        #Esto se encarga de actualizar el registo de mensajes
        limite_mensajes_largo = 250

        # canales[salidaClave]["historial"][message.id]=( f"{message.author.display_name}: {message.content}"[:limite_mensajes])
        canales[salidaClave]["historial"][message.id] = {
            "autor": message.author.display_name,
            "contenido": message.content[:limite_mensajes_largo],
            "espejo": msj_enviado.id
        }

        canales[llegadaClave]["historial"][msj_enviado.id] = {
            "autor": message.author.display_name,
            "contenido": traduccion[:limite_mensajes_largo],
            "espejo": message.id
        }
        
        limite_mensajes = 15
        exceso = 5
        for clave in [salidaClave,llegadaClave]:
            if len(canales[clave]["historial"]) >= limite_mensajes:
                mensajes_a_borrar = list(canales[clave]["historial"].keys())[:exceso]

                for mensaje in mensajes_a_borrar:
                    del canales[clave]["historial"][mensaje]
        

    except Exception as e:


        print("Oye Sika, algo fallo en la ejecucion, quizas usar el internet del vecino fue tan buena idea...")
        print(e)

        general_ingles = bot.get_channel(canales[canal_ingles]["ID"])
        general_espanol = bot.get_channel(canales[canal_espanol]["ID"])
            
        if general_ingles:
            # Enviamos el mensaje indicando quién lo dijo originalmente
            await general_ingles.send(f"Hey guy, there is posibily that I've run out of tokens, so I wont be able to translate more for today, sorry")

        if general_espanol:
            await general_espanol.send(f"Oigan chicos, creo que me qude sin tonkens para traducir mas XD, ehm, no podre continuar por hoy, para que lo tengan claro, perdon por las molestias")