# TITULODOPROJETO

# BackEnd

*O sistema de trilha de conhecimento tem como objetivo produzir conhecimentos
necessário para o desenvolvimento de competências, que proporciona ao usuário o
aprendizado contínuo através de múltiplas formas de aperfeiçoamento pessoal,
profissional, integrando ao seu planejamento de carreira. Por meio de trilhas de
cursos de interesse do usuário que ao final lhe habilitará ao conhecimento
necessário para determinada tecnologia ou área.*

## Considerações Iniciais

Essas instruções serão necessárias para configuração e execução do projeto em sua maquina local para desenvolvimento e possíveis casos de testes.
Antes de tudo, visualize o arquivo abaixo sobre como você realizará a configuração do projeto para execução oficial.
	
### Pré-requisitos

*EXEMPLO DE REQUERIMENTOS BÁSICOS PARA UMA APLICAÇÃO, É INTERESSANTE QUE AO LADO DA TECNOLOGIA, INFORME A SUA VERSÃO.*

	- Python 3.7.2
	- Django 2.2.0
	- SQLite 3.24.0

### Instalando

É necessário ter instalado em sua máquina o Python 3.6.3 ou superior que é disponibilizado no site oficial 
do Python (https://www.python.org/downloads/). Antes de finalizar confira em suas Variações de Ambiente do Windows e verifique
que o Python encontra-se configurado em sua "path". Posteriormente, tem-se necessário criar e configurar a sua própria máquina virtual de 
desenvolvimento para que as ferramentas de projeto não se instalem em suas respectivas máquinas permanentemente.

```
	Criar a virtual enviroment:
		--> python -m venv (nomeDaEnviroment)
	Ativar a enviroment criada:
		--> (nomeDaEnviroment)/Scripts/activate
	Instalar o requirements.txt:
	    --> pip install -r requirements.txt
	Atualizar as migrações do banco de dados:
	    --> python manage.py makemigrations
	Construir o banco de dados da aplicação:
	    --> python manage.py migrate
```

## Executando os testes

Para executar os testes. Será necessário alguns passos a mais, seguem abaixo a sequência dos mesmos:
	
```
	Acessar a pasta do projetos:
		--> cd PASTADOPROJETO
	Executar o arquivo manage.py:
		--> python manage.py runserver
	Abrir o navegador e acessar o link de localhost:
		--> localhost:8000
	Credenciais para acesso ao sistema:
	    --> Matrícula: 000
	    --> Senha: 123
```

## Construído com

* [Python](https://www.python.org/) - Linguagem de Programação	
* [Django](https://www.djangoproject.com/) - Framework Python
* [PyCharm](https://www.jetbrains.com/pycharm/) - IDE

## Autores

* **Alysson Morais** - *Desenvolvedor Back-End* - [@alyssonmorais](https://gitlab.com/alyssonmorais/)
* **Carlos Barreto** - *Desenvolvedor Back-End* - [@CarlosACBarreto](https://gitlab.com/CarlosACBarreto)
* **Diogo Alves** - *Desenvolvedor Back-End* - [@diogo84](https://gitlab.com/diogo84)
* **Gabriel Sérgio** - *Desenvolvedor Back-End* - [@gabrielgscm](https://gitlab.com/gabrielgscm)
* **Joice Emilly** - *Desenvolvedor Back-End* - [@joiceemilly](https://gitlab.com/joiceemilly)
* **Nathalie Kato** - *Desenvolvedor Back-End* - [@katonathalie](https://gitlab.com/katonathalie)

# Desenvolvedor back-end

Descrição de back-end.

- [ ] Codificação do sistema
- [ ] Documentação técnica

Visualize também um grafico sobre as nossas constribuições [Grafico](https://gitlab.com/repositoriodafabrica/pi19_1_fabrica_trilha/graphs/back-end) sobre quem participou deste projeto.

## Licença

Este projeto tem licença administrada pela Fábrica de Software do Centro Universitário de João Pessoa.
