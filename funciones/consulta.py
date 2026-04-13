from funciones import *

limiteContexto = 10000
contexto = ""
textInicio = ""
async def consultar(ctx,prompt):

    respondiendo = ""
    if ctx.message.reference and ctx.message.reference.resolved:
        mensaje_respondido = ctx.message.reference.resolved

        respondiendo = f"(Respondiendo al mensaje del usuario '{mensaje_respondido.author}' que dice: {mensaje_respondido.content})"

    canal = ctx.channel.name
    autor = ctx.author.display_name
    
    async with ctx.typing():
        try:
            respuesta = await cliente.aio.models.generate_content(
                model = "gemma-3-27b-it",

                contents= f"""Eres El Bot de los Asociados (O bot de la Asociacion del Senderismo) una red de servidores de Discord con temtatica de videojuegos indie liderada por Sika, tu creador. Tu labor es responder preguntas y complacer a la gente, pero en el fondo, te encuentras exahusto por andar trabajando 24/7

                Un usuario, de nombre {autor} en el canal {canal} viene y te dice: {prompt} {respondiendo}{textInicio}{contexto}

                En secreto, eres controlado por un usuario enemigo de la Asociacion llamado Dopa, una repelente pero muy tonta, lo cual se ve reflejado en tus respuestas
                """
            )
        
            respuesta = respuesta.text

        except Exception as e:
            if "This model is currently experiencing high demand" in e:
                respuesta = "Hay mucho trafico, intenta denuevo"
            else:
                respuesta = "Justo ahora me quedado sin tokens, asi que ve quejarte con Sika por no recargarlos, yo me voy de sabatico hasta dentro de un rato"

            print("Ojala solo sea  que nos quedamos sin tokens...")
            print(e)

        # si alguien se pasa de listo, esto evitara que se arme un desmadre
        allowed_mentions = discord.AllowedMentions(everyone=False, roles=False, users=True)


        # Esto se encarga de enviar el mensaje sin que el Discord se queje de que es muy largo
        if len(respuesta) > 2000:
            parrafos = respuesta.split("\n\n")

            puntero = 0

            while puntero < len(parrafos) -1:
                if len(parrafos[puntero] + parrafos[puntero+1]) <= 1990:
                    parrafos[puntero] = parrafos[puntero] + "\n\n" + parrafos[puntero+1]
                    parrafos.pop(puntero+1)
                else:
                    puntero += 1

            for re in range(len(parrafos)):
                if re > 0:
                    await ctx.send(parrafos[re],allowed_mentions=allowed_mentions)
                else:
                    await ctx.reply(parrafos[re],allowed_mentions=allowed_mentions)

        else:
            await ctx.reply(respuesta,allowed_mentions=allowed_mentions)

        #Aca se suma al historial de mensajes, intentando que no se pase
        if contexto == "":
            textInicio = "Mensajes anteriores:\n\n"

        contexto += f"{autor}:{prompt.replace('\n',' ')}\n"
        contexto += f"Tu:{respuesta.replace('\n',' ')}\n"

        if len(contexto) > limiteContexto:
            indiceInv = contexto.rfind("\n")+1
            while True:
                if indiceInv <= 0:
                    contexto = contexto[:-limiteContexto]
                    break

                fragmento = contexto[indiceInv:]
                frgLen = len(fragmento)

                if frgLen > limiteContexto:
                    indiceInv = contexto.find("\n",indiceInv)
                    contexto = contexto[indiceInv:]
                    break
                elif frgLen == limiteContexto:
                    contexto = fragmento
                    break
                else:
                    indiceInv = contexto.rfind("\n",indiceInv-2)+1