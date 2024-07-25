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

def created_list_icmp(list_hosts: List) -> List[bool]:
    for host in list_hosts:
        try:
            command = f"ping {'-n 1 ' if sys.platform.startswith('win') else '-c 1'} {host}"
            response = os.system(command)
            ping_check = True if response == 0 else False
            return ping_check

        except ConnectionError as e:
            print(f'Erro na conexão {host}: {e}')

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
    while True:
        TABLE_NAME = 'anp'
        list_hostnames: List = [["google.com"], ["cloudflare.com"], ["yahoo.com"], ["facebook.com"]]
        icmp_value: List[None] = []
        for host in list_hostnames:
            icmp_value.append(created_list_icmp(host))
        print(icmp_value)

        connection_update = connection_mysql()
        update_values(connection_update, TABLE_NAME, icmp_value)

        sleep(300)

