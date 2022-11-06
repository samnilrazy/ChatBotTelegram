# ----------------------------
import requests              #|📕Bibliotecas
import telebot               #|
import sqlite3               #| ☕Codigo criado e modificado por Sam // Wevelly
import time                  #|
import random
# ----------------------------



try:
    connection = sqlite3.connect('files/database.db')

    cursor = connection.cursor()

    data = """CREATE TABLE `Mensagens` (
`ID` INTEGER NOT NULL,
`Msg` TEXT  NOT NULL,
`Reply` TEXT  NOT NULL
);
INSERT INTO `Mensagens` (`ID`, `Msg`, `Reply`) VALUES
(1, 'Olá', '/start'), (2, 'Hello!', '/start')"""

    cursor.executescript(data)


    #cursor.execute("SELECT * FROM Followers_Usuarios")
    #print(cursor.fetchall())
    cursor.close()

    r = True
except Exception as e:
    r = False
    print(e)





file = open("files/token.txt")
data = str(file.read()).split()[2:3]
API = str(data).replace('"', "").replace("[", "").replace("]", "").replace("'", "")


if API == "":
    print("Erro: você não definiu o token do bot em files/token.txt")
    exit()
else:
    r = False


bot = telebot.TeleBot(API)



@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    chatid = str(call.message.chat.id)
    user_id = chatid
    mensagem = call.message
    username = str(mensagem.chat.username)
    nome = str(call.from_user.first_name)
    bot.send_chat_action(chatid, "typing")
    bot.reply_to(mensagem, "Hello World")



def verificar(mensagem):
    return True


@bot.message_handler(func=verificar)
def responderall(mensagem):
    texto_msg = mensagem.text
    chatid = mensagem.chat.id

    try:
        msg_resp = mensagem.reply_to_message.json['text']
    except:
        msg_resp = ""



    connection2 = sqlite3.connect('files/database.db')

    cursor2 = connection2.cursor()

    cursor2.execute(f"SELECT Msg FROM Mensagens WHERE Reply = '{texto_msg}' ORDER BY RANDOM() LIMIT 1")
    r2 = str(cursor2.fetchall())
    
    #print(r2) # [('Olá',)]
    if msg_resp == "":
        r = False
    else:
        cursor2.execute(f"SELECT * FROM Mensagens WHERE Msg = '{texto_msg}'")
        rr = str(cursor2.fetchall())

        if rr == "[]":
            cursor2.execute(f"INSERT INTO Mensagens (ID, Msg, Reply) VALUES ('0', '{texto_msg}', '{msg_resp}')")
            connection2.commit()
        else:
            r = False


    if r2 == "[]":
        r = False
    else:
        resposta = str(r2).replace("[('", "").replace("',)]", "")
        #print(resposta)
        
        one_or_two = random.randint(1, 2)

        if one_or_two == 1:
            bot.reply_to(mensagem, f"<b>{resposta}</b>", parse_mode="HTML")
        else:
            bot.send_message(chatid, f"<b>{resposta}</b>", parse_mode="HTML")







bot.polling()