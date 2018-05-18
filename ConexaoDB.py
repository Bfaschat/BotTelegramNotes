from pymongo import MongoClient

class Mongo_DB():
    #def __init__(self, conexao, banco, collection):
    #    self.cliente = MongoClient(conexao)
    #    self.banco = self.cliente.banco
    #   self.collection = self.banco.collection

    def __init__(self):
        self.cliente = MongoClient('localhost', 27017)
        self.banco = self.cliente['BotTelegram']
        self.collection = self.banco['Anotacoes']

    def altera_banco(self, banco, collection, host='localhost', porta=27017):
        self.cliente = MongoClient(str(host), int(porta))
        self.banco = self.cliente[str(banco)]
        self.collection = self.banco[str(collection)]

    def consulta(self, titulo):
        ''' 
        Realiza uma consulta (select) no banco.
            titulo : str
                Titulo da anotação
        '''
        try:
            document = self.collection.find_one({'titulo' : titulo})
            return document
        except Exception as ex:
            return ('Erro ao recuperar a nota: {}'.format(ex))

    def all_notes(self):
        '''
        Retorna todas as anotações salvas
        '''
        try:
            anotacoes = self.collection.find({})
            return anotacoes
        except Exception as ex:
            return('Erro ao retornar as anotações: {}'.format(ex))

    def upgrade(self, titulo, anotacao):
        ''' 
        Atualiza uma anotação
            titulo: str
                Titulo da anotacao a ser atualizada
            anotacao: dict
                Nova anotacao
        '''
        try:
            documento = self.collection.find_one_and_update({'titulo':titulo}, 
            {'$inc': {'titulo': anotacao['titulo'], 'anotacao': anotacao['anotacao'], 'autor': anotacao['autor']}})
            return documento
        except Exception as ex:
            return('Ocorreu um erro ao atualizar o arquivo: {}'.format(ex))

    def delete(self, titulo):
        '''
        Deleta uma anotação
            titulo: str
                Titulo da anotação a ser deletada
        '''
        try:
            retorno = self.collection.delete_one({'titulo': titulo})
            return retorno
        except Exception as ex:
            return ('Ocorreu um erro ao deletar a anotação: {}'.format(ex))

    def insert(self, anotacao):
        ''' 
        Cria uma nova anotação
            anotacao: dict
                Anotacao a ser inserida
        '''
        try:
            documento_id = self.collection.insert_one(anotacao).inserted_id
            return('Nota criada! ID: {}'.format(documento_id))
        except Exception as ex:
            return('Erro ao criar a nota: {}'.format(ex))
        
    def model(self):
        '''
        Retorna um modelo de anotacao
        '''
        exemplo = {
              "titulo": "Um exemplo de anotacao",
              "anotacao": "Esse é um exemplo de como deve ser feito o objeto de anotacao",
              "autor": 'Fulano de Tal',
             }
        return exemplo