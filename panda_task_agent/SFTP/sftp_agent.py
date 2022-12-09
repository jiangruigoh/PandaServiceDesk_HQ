# SFTP AGENT
"""
Version No: 1
Release Date: 1 September 2021 
KKSC
"""
import pysftp
import sys
import os
from panda_task_agent.md5_checksum import *
from fastapi import HTTPException


class SFTP_Connection(object):
    def __init__(self):
        self.hostname = None
        self.username = None
        self.pwd = None
        self.remoteFilePath = None # Define the file that you want to download from the remote directory
        self.localFilePath = None # Define the local path where the file will be saved
        self.filename = None
        self.port = 22

    def connect(self):
        try:
            self.__sftp = pysftp.Connection(host=self.hostname, username=self.username, password=self.pwd, port=self.port)
            #print("Connection succesfully stablished ... ")
        except:
            print("Connection Failure.")
            e = sys.exc_info()
            # print("Exception: {0}".format(e))
            return {
                "status": 421,
                "message": str(e)
            }
            

    def download(self):
        try:
            source = os.path.join(self.remoteFilePath, self.filename)
            destination = os.path.join(self.localFilePath, self.filename)
            dest_path_fle = os.path.join(self.remoteFilePath, self.filename)
            # print(self.__sftp.pwd)
            # print(source)
            # print(destination)
            self.__sftp.get(source, destination)
            #print(self.__sftp.lstat(dest_path_fle))
            return {
                "status": 200,
                "message": "Succesfully Downloaded File"
            }
        except:
            e = sys.exc_info()
            # print("Exception: {0}".format(e))
            return {
                "status": 404,
                "message": str(e)
            }

    def upload(self):
        try:
            destination = os.path.join(self.remoteFilePath, self.filename)
            #destination = self.remoteFilePath
            source = os.path.join(self.localFilePath, self.filename)
            dest_path_fle = os.path.join(self.remoteFilePath, self.filename)
            #print(source)
            #print(destination)
            # self.__sftp.cd(destination)
            #print(self.__sftp.pwd)
            self.__sftp.put(source, remotepath=destination)
            #print(self.__sftp.lstat(dest_path_fle))
            
            return {
                "status": 200,
                "message": "Succesfully Uploaded File at: " + str(destination)
            }
        except:
            e = sys.exc_info()
            # print("Exception: {0}".format(e))
            return {
                "status": 404,
                "message": str(e)
            }
    
    def dir_checkpoint_remote(self):
        status = "Remote Directory exist"
        try:
            res = self.__sftp.exists(self.remoteFilePath)
            if res != True:
                self.__sftp.makedirs(self.remoteFilePath, mode=777)
                status = "Created new remote directory: " + str(self.remoteFilePath)
        except Exception as e:
            # print(str(e))
            return str(e)
        return status
    
    def file_checkpoint_remote(self):
        status = "Remote File Does not exist"
        abs_path = os.path.join(self.remoteFilePath, self.filename)
        try:
            #print(abs_path)
            res = self.__sftp.exists(abs_path)
            #print(res)
            if res == True:
                status = "File already Exist: " + str(abs_path) + " Proceed delete file to be renewed"
                self.__sftp.remove(abs_path)
            return status
        except Exception as e:
            # print(str(e))
            return str(e)

    
    def dir_checkpoint_local(self):
        status = "Remote Directory exist"
        try:
            res = os.path.exists(self.localFilePath)
            if res == False:
                os.mkdir(self.localFilePath)
                status = "New path directory created: " + str(self.localFilePath)
            return status
        except Exception as e:
            # print(str(e))
            raise HTTPException(status_code=422, detail=str(e))
        
    def filename_checkpoint_local(self):
        path = os.path.join(self.localFilePath, self.filename)
        try:
            f = open(path)
            # f.readlines()
            f.close()
            return "Local Path and File exist"
        except IOError as e:
            print("Local File not accessible")
            raise HTTPException(status_code=422, detail=str(e))


    def check_integrity_remote(self):
        path = os.path.join(self.remoteFilePath, self.filename)
        try:
            md5_hash = hashlib.md5()
            remote_file_stat = self.__sftp.open(path, "rb")
            content = remote_file_stat.read()
            md5_hash.update(content)
            digest = md5_hash.hexdigest()
            return digest
        except IOError as e:
            print("Remote File not accessible for md5 Checksum check")
            raise HTTPException(status_code=422, detail=str(e))
    
    def check_integrity_local(self):
        local_file_stat = cal_checksum(self.filename, self.localFilePath)
        return local_file_stat
    
    def close_session(self):
        self.__sftp.close() # Close Connection

    


