from funciones import *
from funciones.traductor import traducir
from funciones.coneccion import conectar
from funciones.mensajes import *

# Quizas me hubiera sido mas utilo haber conocido esta funcion antes, no importa
#El arroba lo que hace es algo asi como agregarle una funcion ya existente al principo de otra, en en este caso on_ready... Bastante curioso
@bot.event
async def on_ready():
    print(f"Buenas gente, aca estamos como {bot.user} sirviendo a la causa!")

#Supongo que cuando el bot recibe un mensaje, ejecuta esta funcion
#Ahora que lo veo mejor, message se supone que va ser un objeto entero con mucha info, no solo un string, lo cual tiene sentido
@bot.event
async def on_message(message):

    await conectar(message,"escaladaIngles","escaladaEspanol")

    await conectar(message,"senderoIngles","senderoEspanol")
    
    #Esto hace que el bot escuche la funcion, eh, supongo que lo que hace es hacerlo esperar hasta que todo se cumpla
    await bot.process_commands(message)

@bot.event
async def on_message_edit(before, after):
    
    await editarMensajeEspejo(before,after)
    



bot.run(llave_Discord)