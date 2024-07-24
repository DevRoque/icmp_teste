import sys
import os
import pymysql
import dotenv
from time import sleep
from typing import List

# SEMPRE QUE UMA FUNÇÃO FOR CHAMADA SERÁ ENCERRADO A CONEXÃO.
def connection_mysql() -> pymysql.connect:
    # CARREGANDO AS VARIAVEIS DE AMBIENTE
    dotenv.load_dotenv()

    connection = pymysql.connect(
        host=os.environ['MYSQL_HOST'],
        user=os.environ['MYSQL_USER'],
        password=os.environ['MYSQL_PASSWORD'],
        database=os.environ['MYSQL_DATABASE'],
    )
    return connection


def chack_ping(response: int) -> bool:
        # PARA CADA HOST QUE ESTIVER NA LISTA VAI FAZER A VERIFICAÇÃO DA CONEXÃO
        if response == 0:
            # CONEXÃO ONLINE
            ping_value = True
            return ping_value

        else:
            # CONEXÃO OFFILINE
            ping_value = False
            return ping_value


def created_list_icmp(list_host: List) -> List:
    for host in list_host:
        try:
            if sys.platform.startswith('win'):
                command = ("ping -n 1 " + host)
                response = os.system(command)
                ping_check = chack_ping(response)
                return ping_check
            else:
                command = ("ping -c 1 " + host)
                response = os.system(command)
                ping_check = chack_ping(response)
                return ping_check
        except: ...


def update_values(host_connection: pymysql.connect, table: str, values: List) -> None:
    with host_connection:
        with host_connection.cursor() as cursor:
            for index ,value in enumerate(values):
                print()
                cursor.execute(
                    f'UPDATE {table} '
                    f'SET icmp={value} '
                    f'WHERE id={index + 1}'
                )
                host_connection.commit()


if __name__ == '__main__':  
    TABLE_NAME = 'anp'
    icmp_value: List = []
    
    # ALTERE PARA OS IPS HOSTS
    hostname = [["google.com"], ["cloudflare.com"], ["yahoo.com"], ["facebook.com"]]

    for host in hostname:
        icmp_value.append(created_list_icmp(host))
    print(icmp_value)

    # ALTERAR PELOS DADOS DA TABELA DO MYSQL ORIGINAL


    # ATUALIZA A COLUNA ICMP
    connection_update = connection_mysql()
    update_values(connection_update, TABLE_NAME, icmp_value)

    # Executa o código novamente após 5 minutos

