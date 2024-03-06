from pipefy.funtion import delete_card
from os import getenv
import requests
import json

delete_id = 629050362

schema = "query"

url = getenv('URL_REQUEST')

card_id = 635132435 
mais_informacoes = 'NEW TESTE UPDATECARD'
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

lista = ids['data']['cards']['edges']
for c in lista:
    delete_id = int(c['node']['id'])
    print(delete_card(delete_id))
    print()
    


{"query" : "query MyQuery {inbox_emails(card_id: 632206368) {id from to subject body }}"}
#VERIFICAR ATRUBUTOS PARA CRIAR UM CARD
{"query": "{ pipe (id: 302910903){start_form_fields{ id label required type }}}"}

#CREATECARD
{"query": "mutation{ createCard(input: { pipe_id: 302910903 fields_attributes: [{field_id: \"o_que_deve_ser_feito\", field_value: \"Pipefy com python\"}]}){clientMutationId}}"}

#DELETECARD
{"query": "mutation{ deleteCard(input: {id: 628179868}) {success}}"}

#DELETEPHASE
{"query": "mutation { deletePhase(input: {id: 318129941}) {success}}"}

#CREATEPHASE
{"query": "mutation{ createPhase(input:{pipe_id: 302910903, name: \"Create phase python\"}) {phase{ id color }}}"}

#MOVECARDTOPHASE
{"query": "mutation{moveCardToPhase(input:{ destination_phase_id: 318138535 card_id: 628183120 }) {clientMutationId} }"}

#UPDATEPHASE
{"query": "mutation {updatePhase(input:{id: 318138535, name: \"Inicio\"}) {clientMutationId}}"}

# JSON + DEF
'''query = 'mutation { deleteCard(input: { id: %(id)s }) { %(response_fields)s } }' % {
            'id': json.dumps(delete_id),
            'response_fields': response_fields,
          }'''

# Verificar ID cards
{"query": "{ cards(pipe_id: 302910903, search: {title: \"Programa iniciado\"}) { edges { node { fields{ value} title, id }} } }"}
'''
{
  cards(pipe_id: 302910903, search: {title: "Programa iniciado"}) {
    edges {
      node {
        fields {
          value
        }
        title
        id
      }
    }
  }
}
'''

'''query = 'mutation { createInboxEmail(input: {card_id: %(card_id)s, repo_id: %(pipe_id)s, from: "pipe302910903+V7NE9jhe@mail.pipefy.com", subject: %(titulo_email)s, text: %(corpo_email)s, to: %(enviar_para)s}) {inbox_email {id}}}' % {
    'card_id': json.dumps(card_id),
    'pipe_id': json.dumps(pipe_id),
    'titulo_email': json.dumps(titulo),
    'corpo_email': json.dumps(texto)
    'enviar_para': json.dumps(email)

}

query = 'mutation {sendInboxEmail(input: {id: %(id_email)s}) {clientMutationId success}}' % {
    'id_email': json.dumps(id_email)
}'''