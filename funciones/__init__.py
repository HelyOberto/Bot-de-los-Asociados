import discord
from discord import Webhook
from discord.ext import commands
from deep_translator import GoogleTranslator
from google import genai
import re
import aiohttp 
import os
from dotenv import load_dotenv

load_dotenv()

llave_IA = os.getenv("LLAVE_IA")
llave_Discord = os.getenv("LLAVE_DISCORD")


# Vale, entonces esto le dice a Discord que por favor me deje leer los mensajes de los usarios por favorcito
intents = discord.Intents.default()
intents.message_content = True

#Esto declara el objeto que sera el bot... Creo
bot = commands.Bot(command_prefix="$",intents=intents)

mensajes_respondiendo = {
    "en": "Responding to: ",
    "es": "Respondiendo a: "
}

canales = {

    "escaladaIngles" : {
        "ID": 1428833199320076379,
        "idioma_entrada": "en",
        "idioma_salida": "es",
        "webhook_destino": "",
        "historial" : {}
    },

    "escaladaEspanol" : {
        "ID": 1086801841754472580,
        "idioma_entrada": "es",
        "idioma_salida": "en",
        "webhook_destino": "",
        "historial" : {}
    },

    "senderoIngles" : {
        "ID": 1490930083161182440,
        "idioma_entrada": "en",
        "idioma_salida": "es",
        "webhook_destino": "",
        "historial" : {}
    },

    "senderoEspanol" : {
        "ID": 1020042170230648854,
        "idioma_entrada": "es",
        "idioma_salida": "en",
        "webhook_destino": "",
        "historial" : {}
    }
}

for clave in canales:
    canal_idioma = canales[clave]["idioma_salida"]
    canales[clave]["respuesta"] = mensajes_respondiendo[canal_idioma]

    canales[clave]["webhook_destino"] = os.getenv(clave)