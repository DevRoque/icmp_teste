import sys
import os
import pymysql
import dotenv
from time import sleep
from typing import List


def connection_mysql() -> pymysql.connections.Connection:
    dotenv.load_dotenv()

    connection = pymysql.connect(
        host=os.environ['MYSQL_HOST'],
        user=os.environ['MYSQL_USER'],
        password=os.environ['MYSQL_PASSWORD'],
        database=os.environ['MYSQL_DATABASE'],
    )
    return connection


def check_ping(response: int) -> bool:
        if response == 0:
            ping_value = True
            return ping_value

        else:
            ping_value = False
            return ping_value

def created_list_icmp(list_hosts: List) -> List[bool]:
    print(list_hosts)
    for host in list_hosts:
        try:
            if sys.platform.startswith('win'):
                command = ("ping -n 1 " + host)
                response = os.system(command)
                ping_check = check_ping(response)
                return ping_check
            else:
                command = ("ping -c 1 " + host)
                response = os.system(command)
                ping_check = check_ping(response)
                return ping_check
        except Exception as e:
            print(f'Erro ao Verificar o host {host}: {e}')

def update_values(host_connection: pymysql.connections.Connection, table: str, values: List[bool]) -> None:
        with host_connection.cursor() as cursor:
            for index ,value in enumerate(values):
                cursor.execute(
                    f'UPDATE {table} '
                    f'SET icmp={value} '
                    f'WHERE id={index + 1}'
                    )
                host_connection.commit()


if __name__ == '__main__':  
    TABLE_NAME = 'anp'
    icmp_value: List[None] = []
    list_hostnames: List = [["google.co33m"], ["cloudflare.com"], ["yahoo.co33m"], ["facebook.com"]]

    while True:
        for host in list_hostnames:
            icmp_value.append(created_list_icmp(host))
        print(icmp_value)

        connection_update = connection_mysql()
        update_values(connection_update, TABLE_NAME, icmp_value)

        sleep(300)

