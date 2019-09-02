#2 requests por segundo
#250 requests en 3 minutos
#800 requests en 10 minutos
#1500 requests 13 minutos
#2000 requests 23 minutos
#2500 requests media hora
#3000 requests 35 minutos

import codecs
import requests

path = "C:/Python2710/"

url = "https://api.meaningcloud.com/sentiment-2.1"
text_value = ''
headers = {'content-type': 'application/x-www-form-urlencoded'}

input_file = path + 'DiaNaranja.txt'
output_file = path + 'ListaAnalisisDiaNaranja2.tsv'
text_file = open(input_file, "r")
indice=0

with codecs.open(input_file, "r", encoding="latin-1") as f:
    with codecs.open(output_file, "a", encoding="latin-1") as fs:
        fs.write('Id\tUser_name\tScore\tConfidence\tAgreement\tSubjectivity\tIrony\n')
        for line in f:
            try:
                line = str((line).replace("\n", "").strip())
                currentline = line.split("\t")
                text_value = str(currentline[3])
                idtuit = str(currentline[1])
                idtuit = idtuit.strip()
                user = str(currentline[2])

                indice = indice + 1
                payload = "key=d4a5f6f2c0a3a01a3e938f8e470d46bd&lang=es&txt=" + text_value + "&txtf=plain&model=Modelo1&ud=diccionario" #diccionario y modelo personalziado
                #payload = "key=c35c88dcb4ba4e96d5407429b10fbbe8&lang=es&txt=text_value&txtf=plain"
                #payload = "key=d4a5f6f2c0a3a01a3e938f8e470d46bd&lang=es&txt=" + text_value + "&txtf=plain&model=general" #diccionario y modelo general
                response = requests.request("POST", url, data=payload, headers=headers)
                print(indice, text_value) #impresión en consola para verificar progreso
                score = response.json().get('score_tag')
                conf = response.json().get('confidence')
                agree = response.json().get('agreement')
                subj = response.json().get('subjectivity')
                irony = response.json().get('irony')
                fs.write(idtuit + '\t' +
                user + '\t' +
                score + '\t' +
                conf + '\t' +
                agree + '\t' +
                subj + '\t' +
                irony + '\n')

            except:
                continue