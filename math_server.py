from subprocess import Popen,STDOUT,PIPE
from threading import Thread
import socket


class ProcessOutputThread(Thread):
    def __init__(self,proc,conn,addr):
        Thread.__init__(self)
        self.proc = proc
        self.conn = conn
        self.addr = addr
    def run(self):
        while self.proc.poll() is None:
            try:
                self.conn.sendall(self.proc.stdout.readline())
            except Exception as e:
                print(e)
                conn.close(addr[0])
                


class MathServerThread(Thread):
    def __init__(self,conn,addr):
        Thread.__init__(self)
        self.conn = conn
        self.addr = addr
    
    def run(self):
        try:
            proc = Popen(['bc'],stdin=PIPE,stderr=STDOUT,stdout=PIPE)
            out_thread = ProcessOutputThread(proc,self.conn,self.addr)
            out_thread.start()
            while proc.poll() is None:
                    query = self.conn.recv(BUFFER_SIZE)
                    #query = input("Enter expression -> ") +'\n'
                    query = query.decode().strip()
                    if not query:
                        break
                    elif query == "exit" or query == "quit":
                        proc.kill()
                        self.conn.close()
                        break
                    query = query+'\n'
                    
                    #if not query:
                        #break
                    proc.stdin.write(query.encode())
                    proc.stdin.flush()
                    #print(proc.stdout.readline().decode().strip())
        except Exception as e:
            print(e)
            proc.kill()
            self.conn.close()   
        #print(proc.stdout.readline())

HOST = ''
PORT = 1444
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
s.bind((HOST,PORT))
s.listen()

while True:
    conn,addr = s.accept()
    if addr[0] in conn:#To avoid denial of service attack a client can have only one connection
        print("Client {} rejected for misusing server ".format(addr[0]))
        conn.close()
    print("Client {} connected with {}".format(addr[0],addr[1]))
    t = MathServerThread(conn,addr)
    t.start()