from ConexaoDB import Mongo_DB

#banco = Mongo_DB('mongodb://localhost:27017/', 'BotTelegram', 'Anotacoes')
banco = Mongo_DB()

anotacao = {
              "titulo": "TesteUpdade",
              "anotacao": "Essa é a minha anotação",
              "autor": 'William Martins',
             }

banco.altera_banco('localhost', 27017, 'BotTelegram', 'Anotacoes')

retorno = banco.delete('Teste')
print(retorno)