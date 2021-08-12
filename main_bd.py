import yadisk
import shutil
import os
import datetime
from subprocess import Popen
import settings


def connect():
    '''Connect'''
    print(f'\n\n\n\n\n\nNow: {datetime.datetime.now()} backup_bd')
    print('Connect to YaDisk')
    token = settings.TOKEN
    try:
        y = yadisk.YaDisk(token=token)
    except:
        print('Error connect')
        return False
    if y.check_token():
        print('Success connect')
        return y
    else:
        print('Error connect')
        return False


def upload(y):
    print('Dump DB')
    try:
        command = f'PGPASSWORD={settings.bd_pass} pg_dump --dbname={settings.bd_name} --username={settings.bd_username} ' \
                  f'--host={settings.bd_host} --file=dump'
        proc = Popen(command, shell=True, )
        proc.wait()
    except:
        print('Error dump')
        return False
    '''Delete old backup, remove trash'''
    try:
        files = list(y.listdir("backup_bd", sort='modified'))
    except:
        y.mkdir('backup_bd')
    try:
        files = list(y.listdir("backup_bd", sort='modified'))
    except:
        print('Error get list files in folder')
        return False
    while len(files) > 60:
        y.remove(files[0]['path'])
        files = list(y.listdir("backup_bd", sort='modified'))
        y.remove_trash(path='')
    '''Upload connect file'''
    with open("dump", "rb") as f:
        try:
            y.upload(f, f"backup_bd/dump_{datetime.datetime.now().strftime('%Y-%m-%d__%H_%M')}")
        except:
            print('Error upload')
    return True


if __name__ == '__main__':
    y = connect()
    if y:
        if upload(y):
            print('End backup!')
