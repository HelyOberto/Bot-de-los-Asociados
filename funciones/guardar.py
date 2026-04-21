from funciones import *

async def archivo(payload):

    if str(payload.emoji) != "⭐":
        return

    listaArchivos = []

    canal = bot.get_channel(payload.channel_id)
    mensaje = await canal.fetch_message(payload.message_id)
    usuario = bot.get_user(payload.user_id) or await bot.fetch_user(payload.user_id)

    if usuario.bot:
        return
    
    if mensaje.guild == None:
        if str(payload.emoji) == "❌" and mensaje.id in mensajesMD:
            await mensajesMD[mensaje.id].delete()
            del mensajesMD[mensaje.id]
        return

    for archivo in mensaje.attachments:
        bytes = await archivo.read()

        listaArchivos.append(discord.File(io.BytesIO(bytes),filename=archivo.filename))

    fechaFormato = mensaje.created_at.strftime("%d/%m/%Y a las %I:%M %p")

    descripcion = f"> Servidor: **{mensaje.guild.name}**\n> Canal: **{mensaje.channel.name}**\n> Fecha y hora: **{fechaFormato}**\n> Publicado por: **{mensaje.author.display_name} ({mensaje.author.global_name},{mensaje.author.name})**\n> Mensaje original: **{mensaje.jump_url}**"

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


async def fueraDeContexto(payload):
    if str(payload.emoji) != "📸":
        return
    
    listaArchivos = []

    canal = bot.get_channel(payload.channel_id)
    mensaje = await canal.fetch_message(payload.message_id)
    victima = mensaje.author
    victimario = bot.get_user(payload.user_id) or await bot.fetch_user(payload.user_id)

    if victimario.bot:
        return

    match mensaje.guild.id:
        case 1020042170230648852:
            config = canales["senderoContexto"]
        case 1086801840764629093:
            config = canales["escaladaContexto"]
        case _:
            return
        
    if mensaje.id in config["historial"]:
        return

    for archivo in mensaje.attachments:
        bytes = await archivo.read()
        listaArchivos.append(discord.File(io.BytesIO(bytes),filename=archivo.filename))

    async with aiohttp.ClientSession() as session:
        try:
            webhook = Webhook.from_url(config["webhook"],session=session)

            resultado = await webhook.send(
                content=mensaje.content,
                username=victima.display_name,
                avatar_url= victima.display_avatar.url,
                files=listaArchivos,
                wait=True
            )
            config["historial"].append(mensaje.id)

            fechaFormato = mensaje.created_at.strftime("%d/%m/%Y a las %I:%M %p")
            await resultado.reply(f"Tomado por: {victimario.mention}\nFecha orginal: {fechaFormato}")

        except Exception as e:
            print("Uy, yo si queria descontextualizarlo...")
            print(e)