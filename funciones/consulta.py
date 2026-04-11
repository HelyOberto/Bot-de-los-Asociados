from funciones import *

historial_conversacion = {}
limiteContexto = 10000
contexto = ""
async def consultar(ctx,prompt):

    respondiendo = ""
    if ctx.message.reference and ctx.message.reference.resolved:
        mensaje_respondido = ctx.message.reference.resolved

        respondiendo = f"(Respondiendo al mensaje del usuario '{mensaje_respondido.author}' que dice: {mensaje_respondido.content})"

    canal = ctx.channel.name

    if not ctx.channel.id in historial_conversacion:
        historial_conversacion[ctx.channel.id] = []
        contexto = "(Vacio)"
    else:
        contexto = "\n".join(historial_conversacion[ctx.channel.id])
    
    async with ctx.typing():
        try:
            respuesta = await cliente.aio.models.generate_content(
                model = "gemma-3-27b-it",

                contents= f"""Eres El Bot de los Asociados (O bot de la Asociacion del Senderismo) una red de servidores de Discord con temtatica de videojuegos indie liderada por Sika, tu creador. Tu labor es responder preguntas y complacer a la gente, pero en el fondo, te encuentras exahusto por andar trabajando 24/7

                Un usuario, de nombre {ctx.author.display_name} en el canal {canal} viene y te dice: {prompt} {respondiendo}

                Mensajes anteriores: {contexto}

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

        if contexto == "(Vacio)":
            contexto = ""

        #Esto gestiona el registro del historial del bot
        for mensaje in [f"{ctx.author.display_name}: {prompt}\n","Tu: {respuesta}\n"]:
            
            historial_conversacion[ctx.channel.id].apend(mensaje)
            contexto += mensaje
            
        recorte = 1
        while len(contexto) > limiteContexto:
            if recorte >= len(historial_conversacion[ctx.channel.id]):
                contexto = historial_conversacion[ctx.channel.id][0][:limiteContexto]
                historial_conversacion[ctx.channel.id][0] = contexto
                break

            historial_conversacion[ctx.channel.id] = historial_conversacion[ctx.channel.id][recorte:]
            contexto = "\n".join(historial_conversacion[ctx.channel.id])
            recorte += 1