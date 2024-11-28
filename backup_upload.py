#!/usr/bin/python3

import os
import datetime
import tarfile
import pysftp
import hashlib


sourceDir = ""          # source directory 
remote_host = ""        # remote server IP
remote_user = ""        # SSH username
remote_port = ""        # SSH port
remote_key = ""         # SSH keyfile
remote_dir = ""         # directory where the backup files to be stored on the remote server


def genArchiveName(directory_name):
    timeStamp = datetime.datetime.now().strftime("%d-%m-%Y-%H:%M:%S")
    return {"local": f"/tmp/{directory_name}-{timeStamp}.tar.gz", "remote": f"{remote_dir}/{directory_name}-{timeStamp}.tar.gz"}

def uploadBackup(backupFile, remoteFile):
    cnopts = pysftp.CnOpts()
    with pysftp.Connection(host=remote_host, private_key=remote_key, port=remote_port, username=remote_user, cnopts=cnopts) as sftp:
        sftp.put(backupFile, remoteFile)
        return sftp.execute(f"md5sum {remoteFile} | cut -d ' ' -f1")[0].decode('utf-8').rstrip('\n')

def removeBackupFile(remoteFilename):
    cnopts = pysftp.CnOpts()
    with pysftp.Connection(host=remote_host, private_key=remote_key, port=remote_port, username=remote_user, cnopts=cnopts) as sftp:
        sftp.remove(remoteFilename)
        return True

def getHash(archiveName):
    md5sum = hashlib.md5()
    with open(archiveName, 'rb') as fh:
        while True:
            data = fh.read(1024000)
            if data:
                md5sum.update(data)
            else:
                return md5sum.hexdigest()
                break


for directory in os.listdir(sourceDir):

    absPath = os.path.join(sourceDir, directory)
    backup_name = genArchiveName(directory)
    archiveName = backup_name["local"]
    currentDir = os.getcwd()

    if os.path.isdir(absPath):
        with tarfile.open(archiveName,'w:gz') as tar:
            os.chdir(absPath)
            tar.add('.')
            os.chdir(currentDir)
    else:
        with tarfile.open(archiveName,'w:gz') as tar:
            os.chdir(sourceDir)
            tar.add(directory)
            os.chdir(currentDir)
    remoteFilename = backup_name["remote"]
    hashBeforeUpload = getHash(archiveName)
    hashAfterUpload = uploadBackup(archiveName, remoteFilename)

    if hashAfterUpload == hashBeforeUpload:
        print(f"hash values of source and destination files matched")
        print(f"Hash value before upload: {hashBeforeUpload}")
        print(f"Hash value after upload: {hashAfterUpload}")
        print(f"upload completed: {archiveName} --> {remoteFilename}")
        os.remove(archiveName)
        print(f"backup file removed from source host")
    else:
        print(f"hash value of the files {archiveName} and {remoteFilename} don't match so removing the file from the remote server")
        if removeBackupFile(remoteFilename):
            print(f"remote backup file {remoteFilename} removed.")