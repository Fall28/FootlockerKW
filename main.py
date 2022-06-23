
import threading
import csv
import time

from requests import session
from FootlockerKW import footLockerKW
from FootlockerKW import login

urls=[]
emails=[]
passes=[]
thread_array=[]
webhook=""
try:
    with open(f'./creds.csv', 'r') as f:
        csv_reader = csv.reader(f)
        next(csv_reader)
        for row in csv_reader:
            emails.append(row[0])
            passes.append(row[1])
except:
    print('task file error')

try:
    with open(f'./urls.csv', 'r') as f:
        csv_reader = csv.reader(f)
        next(csv_reader)
        for row in csv_reader:
            urls.append(row[0])
            
except:
    print('task file error')

try:
    with open(f'./webhook.csv', 'r') as f:
        csv_reader = csv.reader(f)
        next(csv_reader)
        webhook=next(csv_reader)
except:
    print('task file error')



for x in range(len(emails)):
    sesh=login(emails[x],passes[x])
    for y in range(len(urls)):
        k=footLockerKW(urls[y],y+1,sesh,emails[x],str(webhook[0]))
        s=threading.Thread(target=k.monitor)
        thread_array.append(s)



for p in range(len(thread_array)):
    thread_array[p].start()
    print(f'Thread[{p+1}] started')
    time.sleep(0.0001)

for f in range(len(thread_array)):
    thread_array[f].join()
    time.sleep(0.0001)
        

# class t:
#     def __init__(self,email,password,urls):
#         self.session=login(email,password)
#         self.urls=urls
#         self.product_threads=[]
        
#     def shoes(self):
#         for x in range(len(self.urls)):
#             k=footLockerKW(self.urls[x],x+1,self.session)
#             s=threading.Thread(target=k.monitor)
#             self.product_threads.append(s)

#         for y in range(len(self.product_threads)):
#             self.product_threads[y].start()
#             print(f'thread{x+1} started')
#             time.sleep(0.0001)

#         for z in range(len(self.product_threads)):
#             self.product_threads[z].join()
#             time.sleep(0.0001)

# for y in range(len(emails)):
#     k=t(emails[y],passes[y],urls)
#     s=threading.Thread(target=k.shoes)
#     thread_array.append(s)

# for p in range(len(emails)):
#     thread_array[p].start()
#     print(f'Account Thread[{p+1}]')
#     time.sleep(0.0001)

# for f in range(len(emails)):
#     thread_array[f].join()
#     time.sleep(0.0001)






# for i in range(len(emails)):
#     t = threading.Thread(target=login,args=(emails[i],passes[i]))
#     thread_array.append(t)

# for i in range(len(urls)):
#     t = threading.Thread(target=footLockerKW,args=(urls[i],i+1,session))
#     thread_array.append(t)



# thread_array[0].start()

# for i in range(len(thread_array)):
#     thread_array[i].start()
#     time.sleep(0.0001)


# for i in range(len(thread_array)):
#     thread_array[i].join()
#     time.sleep(0.0001)





# try:
#     with open(f'./creds.csv', 'r') as f:
#         csv_reader = csv.reader(f)
#         next(csv_reader)
#         for row in csv_reader:
#             urls.append(row[0])
# except:
#     print('task file error')

# for i in range(len(urls)):
#     t = threading.Thread(target=footLockerKW(urls[i], i+1).start)
#     t.daemon = True
#     thread_array.append(t)

# for i in range(len(thread_array)):
#     thread_array[i].start()
#     time.sleep(0.0001)


# for i in range(len(thread_array)):
#     thread_array[i].join()
#     time.sleep(0.0001)
