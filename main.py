import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QAction, QIcon #Importando recurso específico de icones
from PyQt6.QtCore import Qt  # Importando Qt do PyQt6.QtCore
from validate_docbr import cpf
import requests


class JanelaPrincipal(QMainWindow): #classe principal que vai conter elementos  
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Minha Janela PyQt6")
       # self.setFixedSize(self.size())
        self.setGeometry(500, 150, 365, 300)# (borda esquerda, superior,largura, altura )
       # self.showFullScreen() #coloca a janela em fullScreen
        self.setWindowIcon(QIcon('s.png')) #apontando para imagem que está no mesmo diretório
        self.interface()
        #self.show()# faz a tela ser exibida
    
    '''Define o layout e os widgets, incluindo o campo de entrada para o CEP, o 
    botão de consulta e a label para exibir os resultados.'''
    def interface(self):
        #Widget principal
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        
        #layout principal 
        layout = QVBoxLayout(central_widget)

        #campo para a entrada de de cep
        self.cep_label = QLabel('Digite seu cep:',self)
        self.cep_input = QLineEdit(self)
        self.cep_input.setInputMask('00000-000')  # Define a máscara para CEP
        layout.addWidget(self.cep_label)
        layout.addWidget(self.cep_input)

        #botão para realizar a busca do cep
        self.botao_cep = QPushButton('Consultar CEP', self)
        self.botao_cep.clicked.connect(self.consulta_cep)
        layout.addWidget(self.botao_cep)

        #label para aparecer as informações do CEP
        self.resultado_cep = QLabel('',self)
        layout.addWidget(self.resultado_cep)

        self.cpf_label = QLabel('Digite seu cpf:',self)
        self.data_label = QLabel('digite sua data de nascimento: ',self)
        self.cpf_input = QLineEdit(self)
        self.data_input = QLineEdit(self)
        self.data_input.setInputMask('00/00/0000')
        self.cpf_input.setInputMask('000.000.000-00')  # Define a máscara para CEP
        layout.addWidget(self.cpf_label)
        layout.addWidget(self.cpf_input)
        layout.addWidget(self.data_label)
        layout.addWidget(self.data_input)

        #botão para realizar a busca do cep
        self.botao_cpf = QPushButton('Consultar CPF', self)
        self.botao_cpf.clicked.connect(self.consulta_cpf)
        layout.addWidget(self.botao_cpf)

        #label para aparecer as informações do CEP
        self.resultado_cpf = QLabel('',self)
        layout.addWidget(self.resultado_cpf)

        self.show()

    def consulta_cep(self):
        cep = self.cep_input.text().strip().replace('-','') #replace: substitui o - por vazio

        #len: verifica a quantidade de caracteres
        if len(cep)!=8 or not cep.isdigit():
            QMessageBox.warning(self,"Atenção","Por favor insira um CEP válido(8 digitos).")
            return
        
        try: #recebendo a resposta da API e atribuindo a variável
            resposta = requests.get(f'https://viacep.com.br/ws/{cep}/json/')
            resposta.raise_for_status()

            dados = resposta.json()
            #print(type(dados)) tipo dicionário

            if 'erro' in dados:
                self.resultado_cep.setText('CEP não encontrado.')
            else:
                # recebendo os resultados da api e atribuindo em forma de string para endereco
                endereco = (
                    f"Logradouro: {dados.get('logradouro')}\n"
                    f"Bairro: {dados.get('bairro')}\n"
                    f"Cidade: {dados.get('localidade')}\n"
                    f"Estado: {dados.get('uf')}\n"
                )
                self.resultado_cep.setText(endereco)

        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, 'Erro', f'Erro ao consultar CEP: {e}')







qt = QApplication(sys.argv) #variavel qt instanciando a classe QApplication: permite usar recursos do SO
app = JanelaPrincipal() #instaciando a classe
sys.exit(qt.exec()) #encerra totalmente a aplicação assim que fechada
