import requests
import json

# Importar a biblioteca Telebot - Acessar o Terminal de sua IDE (Seja local ou virtual) e rodar esse script: pip install telebot
import telebot

# Para conseguir o Token de sua API é necessário ter acesso ao Telegrem e por lá inicicar um conversa com BotFather Verificado
# Após a criação de seu Bot será exposto seu Token API para utilização!

# Insira sua API token na linha abaixo, caso possua dificuldade para requisitar seu token API, assista ao vídeo https://www.youtube.com/watch?v=OO3a7tJEJ1I&t=1s
bot = telebot.TeleBot('SUA_API_TOKEN_AQUI')

@bot.message_handler(commands=['start', 'help'])

def send_welcome(message):
    bot.reply_to(message, " 🌐</> Seja bem vindo ao meu 'Proxy Checker Bot' 🤖</> "
                          "\n\nBot voltado a validação de Proxys, fazendo o uso request a API ipinfo.io em execução com a APIBot do Telegram! ^-^"
                          "\n\nPor favor, informe um proxy no formato 'IP:PORT' ou 'IP' 👉")

@bot.message_handler(func=lambda message: True)

def check_proxy(message):

    proxy = message.text.strip()

    # Chama a API ipinfo.io para obter detalhes do endereço IP
    url = f"https://ipinfo.io/{proxy}/json"

    response = requests.get(url)

    # Verifica se a chamada da API foi bem-sucedida
    if response.status_code == 200:

        data = json.loads(response.text)

        # Verifique se o endereço IP é válido
        if "ip" in data:

            # Extrai os detalhes do endereço IP
            ip = data["ip"]
            cidade = data["city"] if "city" in data else ""
            regiao = data["region"] if "region" in data else ""
            pais = data["country"] if "country" in data else ""
            postal = data["postal"] if "postal" in data else ""
            fuso = data["timezone"] if "timezone" in data else ""
            org = data["org"] if "org" in data else ""
            host = data["hostname"] if "hostname" in data else ""

            # Retorna ao usuário o resultado formatado de sua pesquisa
            result = (f"✅ PROXY VÁLIDO 🥳\n"
                      f"\n⤷ Endereço de IP: {ip}"
                      f"\n⤷ Cidade: {cidade}"
                      f"\n⤷ Região: {regiao}"
                      f"\n⤷ País: {pais}"
                      f"\n⤷ Código Postal: {postal}"
                      f"\n⤷ Fuso horário: {fuso}"
                      f"\n⤷ Organização: {org}"
                      f"\n⤷ Hostname (Domínio): {host}"
                      f"\n\nVisite meu Github github.com/pedrozand 🤘")
            bot.reply_to(message, result)

        else:
            bot.reply_to(message, "❌ PROXY INVÁLIDO 😭"
                                  "\n\nPor favor, envie um proxy válido no formato 'IP:PORT' ou 'IP'")

    else:
        bot.reply_to(message, f"😵 Erro ao verificar o proxy: {response.text}")

bot.polling()