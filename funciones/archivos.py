from funciones import *

async def guardarArchivo(payload):

    listaArchivos = []

    canal = bot.get_channel(payload.channel_id)
    mensaje = await canal.fetch_message(payload.message_id)
    usuario = bot.get_user(payload.user_id) or await bot.fetch_user(payload.user_id)

    if mensaje.guild == None:
        if str(payload.emoji) == "❌" and mensaje.id in mensajesMD:
            await mensajesMD[mensaje.id].delete()
            del mensajesMD[mensaje.id]
        return

    if usuario.bot:
        return

    poseeLinks = bool(re.search(r'https?://\S+|www\.\S+',mensaje.content))

    if str(payload.emoji) != "⭐" or (not(mensaje.attachments) and not(poseeLinks)):
        return
    
    for archivo in mensaje.attachments:
        bytes = await archivo.read()

        listaArchivos.append(discord.File(io.BytesIO(bytes),filename=archivo.filename))

    descripcion = f"> Servidor: **{mensaje.guild.name}**\n> Canal: **{mensaje.channel.name}**\n> Fecha y hora: **{mensaje.created_at}**\n> Publicado por: **{mensaje.author.display_name} ({mensaje.author.global_name},{mensaje.author.name})**\n> Mensaje original: **{mensaje.jump_url}**"

    if mensaje.content != "":
        descripcion += f'\n{mensaje.content}'

    try:   
        directorio = os.path.dirname(__file__)
        indicacion = os.path.join(directorio,"..","imagenes","indicaciones.png")

        if usuario.id not in usuariosConMD:
            await usuario.send('Recciona con una "❌" para borrar cualquiera de los archivos\n\nTambien puedes puedes filtras las imagenes por nombre u usuario usando el buscador nativo de discord\n------------------------------------------------')
            usuariosConMD.append(usuario.id)

        mensajeResultado = await usuario.send(descripcion,files=listaArchivos)
        mensajesMD[mensajeResultado.id] = mensajeResultado
        recortarRegistro(mensajesMD,exceso=1)

    except:
        instruccion = await canal.send(f'{usuario.mention} Para poder guardar los mensajes en tu MD debes tener configurado **en tu perfil** en la seccion de **Permisos de interacción** la opcion de **Mensajes directos** activa al menos para este servidor:',file=discord.File(indicacion))

        await asyncio.sleep(20)

        await instruccion.delete()