import yadisk

'''Connect'''
token = 'TOKEN'
y = yadisk.YaDisk(token=token)

'''Delete old backup, remove trash'''
files = list(y.listdir("backup", sort='modified'))
while len(files) > 3:
    y.remove(files[0]['path'])
    files = list(y.listdir("backup", sort='modified'))
    y.remove_trash(path='')

'''Upload connect file'''
with open("test.jpg", "rb") as f:
    y.upload(f, "backup/test1.jpg")