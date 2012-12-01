import time, thread

from ftplib import FTP

thread_counter = 0;
ftp_lock = thread.allocate_lock()
def create_thread(fun, args):    
    def thread_fun(args):
        fun(*args)
        global thread_counter
        thread_counter -= 1
        
    global thread_counter
    thread_counter += 1
    thread.start_new_thread(thread_fun,(args,))

def wait_thread():
    while thread_counter > 0:
        time.sleep(1)
    
def ftp_work(name, con):
    print name, " is waiting"
    global ftp_lock
    while 1:
        with ftp_lock:
            ftp_locked_work(name,con)        
        
def ftp_locked_work(name,con):
    print name, " now working"
    ftp = FTP(con['host'],con['user'], con['pass'])
    file_local = open('file.txt', 'wb')     
    ftp.retrbinary('RETR file.txt',file_local.write)
    file_local.close() 
    
    
    file_local = open('file.txt', 'ab')
    file_local.write(name + "\r\n")
    file_local.close()

    file_local = open("file.txt", "rb")
    ftp.storlines("STOR file.txt", file_local)
    file_local.close()
    ftp.quit()    
    print name, " stopped working"
    
if __name__ == "__main__":
    con = {}
    con['host'] = 'ftp.uznam.org'
    con['user'] = 'soltys-pw'
    con['pass'] = 'qwerty1'
    
    create_thread(ftp_work,("#1 Thread",con,))
    create_thread(ftp_work,("#2 Thread",con,))
    
    print "main thread awaits"
    wait_thread()
    print "done"
