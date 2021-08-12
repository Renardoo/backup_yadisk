import yadisk
import shutil
import os
import datetime
import settings


def connect():
    '''Connect'''
    print(f'\n\n\n\n\n\nNow: {datetime.datetime.now()} backup_data')
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

'''Delete old backup, remove trash'''
# files = list(y.listdir("backup", sort='modified'))
# while len(files) > 3:
#     y.remove(files[0]['path'])
#     files = list(y.listdir("backup", sort='modified'))
#     y.remove_trash(path='')
'''Upload connect file'''
# with open("test.jpg", "rb") as f:
#     y.upload(f, "backup/test1.jpg")


def upload(y):
    '''Check missing file, and upload'''
    print('Check files')
    try:
        list_files = list(y.listdir("backup", sort='modified'))
    except:
        y.mkdir('backup')
    try:
        list_files = list(y.listdir("backup", sort='modified'))
    except:
        return False
    files_on_yadisk = [d['name'] for d in list_files]
    path = 'private-media'
    files_on_disk = os.listdir(path)

    print('Upload...')
    count = 0
    for file in files_on_disk:
        if file not in files_on_yadisk:
            with open(os.path.join(path, file), "rb") as f:
                try:
                    y.upload(f, os.path.join('backup', file))
                except:
                    print(f'Error upload {file}!')
                    continue
                count += 1
    print(f'Upload {count} files!')
    return True

if __name__ == '__main__':
    y = connect()
    if y:
        if upload(y):
            print('End backup!')