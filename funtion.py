from time import sleep
from os import getenv
from dotenv import load_dotenv
import requests
import json 

load_dotenv()

def move_card(phase_id, card_id, schema="query"):
    url = getenv('URL_REQUEST')
    
    query = 'mutation{moveCardToPhase(input:{ destination_phase_id: %(phase_id)s card_id: %(card_id)s }) {clientMutationId} }' % {
            'phase_id': json.dumps(phase_id),
            'card_id': card_id
          }

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"{getenv('TOKEN')}"
    }

    return requests.post(url, json={schema : query}, headers=headers)



def create_card(pipe_id ,name_card ,mais_informacoes, email,  schema="query"):
    url = getenv('URL_REQUEST')
    
    id_card = '{ clientMutationId card {id, title}}'
    
    query = 'mutation{ createCard(input: { pipe_id: %(pipe_id)s fields_attributes: [{field_id: \"o_que_deve_ser_feito\", field_value: %(name_card)s}{field_id: \"mais_informa_es\", field_value: %(mais_informacoes)s}{field_id: \"email_destinat_rio\", field_value: %(email)s}]})%(id_card)s}' % {
            'pipe_id': json.dumps(pipe_id),
            'name_card': json.dumps(name_card),
            'mais_informacoes': json.dumps(mais_informacoes),
            'email': json.dumps(email),
            'id_card': id_card
          }

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"{getenv('TOKEN')}"
    }
    card_id = requests.post(url, json={schema : query}, headers=headers)
    card_id = json.loads(card_id.text)
    card_id = int(card_id['data']['createCard']['card']['id'])
    return card_id



def delete_card(delete_id, schema="query"):
    url = getenv('URL_REQUEST')
    
    result = '{ success}'
    
    query = ' mutation{ deleteCard(input: {id: %(delete_id)s}) { success}}' % {
            'delete_id': json.dumps(delete_id)
          }

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"{getenv('TOKEN')}"
        }
    result = requests.post(url, json={schema : query}, headers=headers)
    return result.text



def id_card_e_phase(pipe_id, schema="query"):
    url = getenv('URL_REQUEST')

    query = '{pipe(id: %(pipe_id)s) {phases {id name cards { edges {node {id title } } } }}}' % {
        'pipe_id': json.dumps(pipe_id)
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"{getenv('TOKEN')}"
    }

    response = requests.post(url, json={schema : query}, headers=headers)

    ids = response.text
    ids =json.loads(ids)
    phase_final = int(ids['data']['pipe']['phases'][3]['id'])
    phase_cobrar_email = int(ids['data']['pipe']['phases'][2]['id'])
    phase_email = int(ids['data']['pipe']['phases'][1]['id'])
    phases_ids = '{"Email": "%(phase_email)s", "Cobrar email": "%(phase_cobrar_email)s", "Final": "%(phase_final)s"}' % {'phase_email': json.dumps(phase_email),'phase_cobrar_email': json.dumps(phase_cobrar_email), 'phase_final': json.dumps(phase_final)}
    phases_ids = json.loads(phases_ids)
    return phases_ids



def card_id_phase_email(pipe_id, schema="query"):
    card_ids = []

    url = getenv('URL_REQUEST')

    query = '{pipe(id: %(pipe_id)s) {phases {id name cards { edges {node {id title } } } }}}' % {
        'pipe_id': json.dumps(pipe_id)
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"{getenv('TOKEN')}"
        }

    response = requests.post(url, json={schema : query}, headers=headers)
    ids = response.text
    ids = json.loads(ids)
    try:
        ids = ids['data']['pipe']['phases'][1]['cards']['edges']
        for id in ids:
            card_ids.append(int(id['node']['id']))
        
        return card_ids
    except:
        return 'Nenhum card encontrado'



def delete_cards(pipe_id, schema="query"):
    url = getenv('URL_REQUEST')

    query = '{pipe(id: %(pipe_id)s) {phases {id name cards { edges {node {id title } } } }}}' % {
        'pipe_id': json.dumps(pipe_id)
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"{getenv('TOKEN')}"
    }

    response = requests.post(url, json={schema : query}, headers=headers)

    ids = response.text
    ids = json.loads(ids)
    id_cards = ids['data']['pipe']['phases']
    for card in id_cards:
        if card['cards']['edges'] != 0:
            for c in card['cards']['edges']:
                delete_card(delete_id=int(c['node']['id']))



def verificar_email(card_id, schema="query"):
    url = getenv('URL_REQUEST')

    query = 'query MyQuery {inbox_emails(card_id: %(card_id)s) {id from to subject body }}' % {
        'card_id': json.dumps(card_id)
    } 
    

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"{getenv('TOKEN')}"
        }

    response = requests.post(url, json={schema : query}, headers=headers)
    ids = response.text
    ids = json.loads(ids)
    email = ids['data']['inbox_emails']
    for verificar in email:
        if verificar['from'] != 'pipe302910903+V7NE9jhe@mail.pipefy.com':
            if verificar['subject'].count('Maquina se encontra com percentual baixo') == 1:
                texto = verificar['body']
                texto = texto.split('\n')
                texto = texto[0].lower().count('tem um toner para repor quando este acabar')
                if texto == 1:
                    return 'Pode excluir o card ai cria'
            else:
                texto = verificar['body']
                texto = texto.split('\n')
                texto = texto[0].lower().count('toner trocado')
                if texto == 1:
                    return 'Pode excluir o card ai cria'
        else:
            return 'Não pode excluir o card cria'



def verificar_subject_email(card_id, schema="query"):
    url = getenv('URL_REQUEST')

    query = 'query MyQuery {inbox_emails(card_id: %(card_id)s) {id from to subject body }}' % {
        'card_id': json.dumps(card_id)
    } 
    

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"{getenv('TOKEN')}"
        }

    response = requests.post(url, json={schema : query}, headers=headers)
    ids = response.text
    ids = json.loads(ids)
    email = ids['data']['inbox_emails']
    for verificar in email:
            if verificar['subject'].count('Maquina se encontra com percentual baixo') == 1:
                return 'Estou entrando em contato novamente para verificar se tem ou não toner para repor quando o toner com porcentagem baixo acabar?'
            else:
                return 'O toner já foi trocado, preciso saber para excluir este processo!'



def updatecard(card_id, mais_informacoes,  schema="query"):
    url = getenv('URL_REQUEST')

    query = 'mutation {updateCardField( input: {card_id: %(card_id)s, field_id: "mais_informa_es", new_value: %(mais_informacoes)s} ) {   clientMutationId  success }}' % {
        'card_id': json.dumps(card_id),
        'mais_informacoes': json.dumps(mais_informacoes)
    }
    
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"{getenv('TOKEN')}"
        }

    response = requests.post(url, json={schema : query}, headers=headers)
    ids = response.text
    ids = json.loads(ids)
    return ids



def main(lista_toner):
    lista_toner = converter_to_int(lista_toner)
    for toner in lista_toner:
        if toner == 0:
            phases = id_card_e_phase(pipe_id=302910903)
            card_id = create_card(pipe_id=302910903, name_card=f'Maquina se encontra com toner zerado {toner}', mais_informacoes='O toner do local {localidade} está sem toner {O toner que está com percentual baixo} ', email='lg.nunes.souza2006@gmail.com')
            move_card(phase_id=int(phases['Email']), card_id=card_id)
        elif toner <= 10:
            phases = id_card_e_phase(pipe_id=302910903)
            card_id = create_card(pipe_id=302910903, name_card=f'Maquina se encontra com percentual baixo {toner}', mais_informacoes='O toner do local {localidade} está com percentual baixo no toner {O toner que está com percentual baixo}, tem alguma toner no estoque para colocar no lugar quando acabar? ', email='lg.nunes.souza2006@gmail.com')
            move_card(phase_id=int(phases['Email']), card_id=card_id)
    card_ids = card_id_phase_email(pipe_id=302910903)
    if len(card_ids) != 0:
        while True:
            sleep(60)
            for card_id in card_ids:
                result = verificar_email(card_id=card_id)
                if result == 'Pode excluir o card ai cria':
                    print('Pode memo né ? se for errado o bagulho vai ficar loco em!')
                    move_card(phase_id=int(phases['Final']), card_id=card_id)
                    card_ids.remove(card_id)
                else:
                    new_texto = verificar_subject_email(card_id)
                    updatecard(card_id, new_texto)
                    move_card(phase_id=int(phases['Cobrar email']), card_id=card_id)
            if len(card_ids) == 0:
                break



def converter_to_int(lista):
    new_lista = []
    numero_int = []
    for porcento in lista:
        numero_int.clear()
        for numero in porcento:
            if numero != '%':
                numero_int.append(numero)
        new_lista.append(int(''.join(numero_int)))
    return new_lista



if __name__ == "__main__":
    delete_cards(pipe_id=302910903)
    lista = ['36%', '34%', '40%', '50%', '10%', '5%', '0%']
    main(lista)