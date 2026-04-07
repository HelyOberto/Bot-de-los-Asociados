from .mensajes import buscarMensaje
from funciones import *

cliente = genai.Client(api_key=llave_IA)

async def traducir(message,config):

    #Debo admiitr que este lo copie y pegue mi amiga gimena, no por flojera (Mas o menos) sino porque sin querer hice modificaciones sin guardar correctamente el codigo origina, no quera tardar mas tiempo

    #Si en un futuro reemplazare el traductor quizas me sirva tenerlo separado
    traductor = GoogleTranslator(source=config["idioma_entrada"], target=config["idioma_salida"])

    mensaje_original = message.content

    if mensaje_original.strip() == "":
        return message.content
    
    #Esto obtiene los links, parece Malbolge xd
    links = re.findall(r'(https?://[^\s]+|www\.[^\s]+)', mensaje_original)

    for link in links:
        mensaje_original = mensaje_original.replace(link,"")

    contexto = ""
    for id in config['historial']:
        contexto += f"{config['historial'][id]['autor']}: {config['historial'][id]['contenido']}\n"

    #¿Como va terminar esto?
    if mensaje_original.strip() != "":
        try:
            respuesta = await cliente.aio.models.generate_content(
            model = "gemma-3-27b-it",

            contents= f"""
                Traduce al idioma '{config['idioma_salida']}'.
                Reglas: 
                - Salida: SOLO el texto traducido. Sin introducciones ni formato (cursiva/negrita).
                - Contexto: Gaming/Discord. Adapta la jerga (slang).
                - Emojis (CÓDIGO TÉCNICO): 
                    - Identifica cadenas con el formato '<:nombre:ID>' o '<a:nombre:ID>' (donde 'ID' es una secuencia larga de números).
                    - ESTRICTAMENTE PROHIBIDO: Traducir el 'nombre', alterar o redondear los números del 'ID', u omitir los símbolos '<', ':', '>'.
                    - TRATAMIENTO: Trátalos como constantes de programación. Deben aparecer exactamente igual en la traducción final, respetando su posición gramatical relativa para que el sentido del mensaje no se pierda.
                    - EMOJIS ESTÁNDAR: Los términos entre dos puntos (ej. :smile:) también deben permanecer intactos.

                Mensajes previos: {contexto}
                Autor del mensaje: {message.author.display_name}
                Mensaje que debes traducir: {mensaje_original}"""
        ).text
        except:
            respuesta = traductor.translate(mensaje_original)

        traduccion = respuesta + "\n" + "\n".join(links)
    else:
        traduccion = "\n".join(links)

    
    #Si el mensasje tiene una respuesta, y si esa respuesta existe, haz algo
    if message.reference and message.reference.resolved:
        contenido_ref = await buscarMensaje(message.reference.resolved.id,buscar="espejo")

        if not contenido_ref:
            contenido_ref = traductor.translate(message.reference.resolved.content)


        # Si el mensaje ya tiene una respuesta, la elimina
        contenido_ref = re.sub(r'^>.*$', '', contenido_ref, flags=re.MULTILINE).strip()

        limite = 100
        contenido_ref = contenido_ref[:limite]

        if len(contenido_ref) == limite:
            contenido_ref += "..."

        #Esto evita que los enlaces de desplieguen en las respuestas
        contenido_ref = re.sub(r'(https?://[^\s]+)', r'<\1>', contenido_ref)

        if message.reference.resolved.webhook_id:
            autor_ref = message.reference.resolved.author.id
            traduccion = f"> {config['respuesta']} <@{autor_ref}>: *{contenido_ref}*\n{traduccion}"
        else:
            autor_ref = message.reference.resolved.author.display_name
            traduccion = f"> {config['respuesta']} **{autor_ref}**: *{contenido_ref}*\n{traduccion}"

    
    return traduccion