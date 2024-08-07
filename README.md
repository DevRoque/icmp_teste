# Teste de ICMP

Fiz esse teste de ICMP no intuito de ajudar no gerenciamento de servidores gerenciados por um banco de dados,
onde será feito os testes de ping em 5 e 5 minutos.
---
Será utilizado as bibliotecas para esse gerenciamento.
```
import sys
import os
import pymysql
import dotenv
from time import sleep
from typing import List
```
Porque essas bibliotecas? Então
- `sys` -> está sendo utilizado para a verificação do sistema operacional se é Windows ou Linux/Mac.
- `os` -> está sendo utilizado para buscar os arquivos env e utilizar os comandos do shell.
- `pymysql` -> está sendo utilizado para efetuar a conexão e o UPDATE no banco de dados.
- `dotenv` -> Usado para carregar as variáveis de ambiente no sistema (para segurança dos dados)
- `sleep` -> Usado para dar uma pausa no script de 5 em 5 minutos >> Evitar sobrecarga pode também usar a bibliotéca threading para melhorar no processo do script, dedicando uma parte apenas do processador para essa tarefa.
- `typing` -> Foi utilizado para facilitar a escrita do script e habilitando as funções necessárias para agilizar o processo.

# FUNÇÕES
- created_list_icmp -> Criar a lista de conexões que tiveram sucesso.
```
def created_list_icmp(list_hosts: List) -> List[bool]:
    for host in list_hosts:
        try:
            command = f"ping {'-n 1 ' if sys.platform.startswith('win') else '-c 1'} {host}"
            response = os.system(command)
            ping_check = True if response == 0 else False
            return ping_check

        except ConnectionError as e:
            print(f'Erro na conexão {host}: {e}')
```
- connetion_mysql -> Faz a conexão com o banco de dados (Mysql)
```
def connection_mysql() -> pymysql.connections.Connection:
    dotenv.load_dotenv()

    connection = pymysql.connect(
        host=os.environ['MYSQL_HOST'],
        user=os.environ['MYSQL_USER'],
        password=os.environ['MYSQL_PASSWORD'],
        database=os.environ['MYSQL_DATABASE'],
    )
    return connection
```
- update_values -> Atualiza o valor ICMP do ID indicado do banco de dados como o ID começa com 1 foi acrescido +1 ao index para sempre iniciar no numero 1
```
def update_values(host_connection: pymysql.connections.Connection, table: str, values: List[bool]) -> None:
        with host_connection.cursor() as cursor:
            for index ,value in enumerate(values):
                cursor.execute(
                    f'UPDATE {table} '
                    f'SET icmp={value} '
                    f'WHERE id={index + 1}'
                    )
                host_connection.commit()
```
