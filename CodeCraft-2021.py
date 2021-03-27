import numpy as np
import sys
import os
import re
import random
import copy
import time

f='training-2.txt'
def Get_data(path):
    if os.path.exists(path):
        with open(path,'r') as data:
            Lis=data.readlines()
            Sever=[]
            Virtual=[]
            counter=0
            use_Case=[]
            while Lis:
                num=Lis[0].strip().split('\n')[0]
                if num.isdigit():
                    Lis=Lis[1:len(Lis)]
                    last_num=int(num)
                else:
                    add_sentence=Lis[0:last_num]
                    P=[]
                    for i in range(len(add_sentence)):
                        P_1=[]
                        sentence = add_sentence[i]
                        result=re.findall(r'[a-zA-Z0-9.]{1,}',sentence)
                        for r_i in result:
                            if r_i.isdigit():
                                P_1.append(int(r_i))
                            else:
                                P_1.append(r_i)
                        P.append(P_1)
                    if counter==0:
                        Sever=P
                    if counter==1:
                        Virtual=P
                    if counter>1:
                        use_Case.append(P)
                    counter+=1
                    Lis=Lis[last_num:len(Lis)]
    return Sever,Virtual,use_Case

def Get_data_input():
    serves = []
    servers_num = int(sys.stdin.readline())
    for i in range(servers_num):
        temp = sys.stdin.readline()
        temp = re.findall(r'[a-zA-Z0-9.]{1,}', temp)
        serve = [int(i) if i.isdigit() else i for i in temp]
        serves.append(serve)
    virtuals = []
    virtuals_num = int(sys.stdin.readline())
    for i in range(virtuals_num):
        temp = sys.stdin.readline()
        temp = re.findall(r'[a-zA-Z0-9.]{1,}', temp)
        virtual = [int(i) if i.isdigit() else i for i in temp]
        virtuals.append(virtual)
 
    user_requests = []
    days = int(sys.stdin.readline())
    for i in range(days):
        day_num = int(sys.stdin.readline())
        day_requests = []
        for j in range(day_num):
            temp = sys.stdin.readline()
            temp = re.findall(r'[a-zA-Z0-9.]{1,}', temp)
            request = [int(i) if i.isdigit() else i for i in temp]
            day_requests.append(request)
        user_requests.append(day_requests)
    return serves, virtuals, user_requests
#获取数据：服务器、虚拟机、每日操作（按天分开）
#######################################################
server_info,machine_info,day_info = Get_data_input()#Get_data(f)
#######################################################
server_num=len(server_info)
machine_num=len(machine_info)
day_num=len(day_info)
#读取服务器信息
server_dict=dict()#{server_name:[CPU,RAM,cost,cost_day]}
for i in range (server_num):
    server_dict[server_info[i][0]] = [server_info[i][1],server_info[i][2],server_info[i][3],server_info[i][4]]
def generateServer(server_name):
    info = [server_dict[server_name][0]/2,server_dict[server_name][0]/2,server_dict[server_name][1]/2,server_dict[server_name][1]/2,server_dict[server_name][2],server_dict[server_name][3]]
    return server_name, info
#读取虚拟机信息
machine_dict=dict()#{machine_name:[CPU,RAM,type]}
for i in machine_info:
    machine_dict[i[0]]=[i[1],i[2],i[3]]
def generateMachine(machine_name):
    info = [machine_dict[machine_name][0],machine_dict[machine_name][1],machine_dict[machine_name][2]]
    return machine_name, info
server=dict()#{server_id:[server_name,CPU_A,CPU_B,RAM_A,RAM_B]}
machine_server_on=dict()#{machine_id:[machine_name,serverId,A/B(0,1,2)]}
machine_id_name=dict()#{machine_id:[machine_name]}
for i in range(day_num):
    for j in range(len(day_info[i])):
        if day_info[i][j][0] == 'add':
            machine_id_name[day_info[i][j][2]] = day_info[i][j][1]
def purchase_server(server_name,num):
    bought_num = len(server)
    for i in range (num):
        server[bought_num+i]=[generateServer(server_name)[0],generateServer(server_name)[1][0],generateServer(server_name)[1][1],
                                generateServer(server_name)[1][2],generateServer(server_name)[1][3]]
def choose_server(machine_id,server_id,migration,choose_out,n):
    n=int(n)
    machine_name = machine_id_name[machine_id]
    need_info = [machine_dict[machine_name][0],machine_dict[machine_name][1],machine_dict[machine_name][2]]
    if need_info[-1] == 1:
            server[server_id][1]-=need_info[0]/2
            server[server_id][2]-=need_info[0]/2
            server[server_id][3]-=need_info[1]/2
            server[server_id][4]-=need_info[1]/2
            machine_server_on[machine_id]=[machine_name,int(server_id),int(0)]
            if migration == False:
                choose_out[n]=('(%d)' %(server_id))
    elif need_info[-1] == 0:
        if server[server_id][1]>=need_info[0] and server[server_id][3]>=need_info[1]:
            server[server_id][1]-=need_info[0]      
            server[server_id][3]-=need_info[1]
            machine_server_on[machine_id]=[machine_name,server_id,int(1)]
            if migration == False:
                choose_out[n]=('(%d, A)' %(server_id))
        elif server[server_id][2]>=need_info[0] and server[server_id][4]>=need_info[1]:
            server[server_id][2]-=need_info[0]      
            server[server_id][4]-=need_info[1]
            machine_server_on[machine_id]=[machine_name,int(server_id),int(2)]
            if migration == False:
                choose_out[n]=('(%d, B)' %(server_id))
def choose_server_migration(machine_id,server_id,migration,migration_out,n): 
    n=int(n)
    machine_name = machine_id_name[machine_id]
    need_info = [machine_dict[machine_name][0],machine_dict[machine_name][1],machine_dict[machine_name][2]]
    if need_info[-1] == 1:
            server[server_id][1]-=need_info[0]/2
            server[server_id][2]-=need_info[0]/2
            server[server_id][3]-=need_info[1]/2
            server[server_id][4]-=need_info[1]/2
            machine_server_on[machine_id]=[machine_name,int(server_id),int(0)]
            if migration == True:
                migration_out[n]=('(%s, %d)' %(machine_id,server_id))
    elif need_info[-1] == 0:
        if server[server_id][1]>=need_info[0] and server[server_id][3]>=need_info[1]:
            server[server_id][1]-=need_info[0]      
            server[server_id][3]-=need_info[1]
            machine_server_on[machine_id]=[machine_name,server_id,int(1)]
            if migration == True:
                migration_out[n]=('(%s, %d, A)' %(machine_id,server_id))
        elif server[server_id][2]>=need_info[0] and server[server_id][4]>=need_info[1]:
            server[server_id][2]-=need_info[0]      
            server[server_id][4]-=need_info[1]
            machine_server_on[machine_id]=[machine_name,int(server_id),int(2)]
            if migration == True:
                migration_out[n]=('(%s, %d, B)' %(machine_id,server_id))
    return migration_out,n

def delete_server(machine_id,server_id):
    machine_name = machine_id_name[machine_id]
    need_info = [machine_dict[machine_name][0],machine_dict[machine_name][1],machine_dict[machine_name][2]]
    if machine_server_on[machine_id][-1] == 0:
        server[server_id][1]+=need_info[0]/2
        server[server_id][2]+=need_info[0]/2
        server[server_id][3]+=need_info[1]/2
        server[server_id][4]+=need_info[1]/2
        del machine_server_on[machine_id]
    elif machine_server_on[machine_id][-1] == 1:
        server[server_id][1]+=need_info[0]      
        server[server_id][3]+=need_info[1]
        del machine_server_on[machine_id]
    else:
        server[server_id][2]+=need_info[0]      
        server[server_id][4]+=need_info[1]
        del machine_server_on[machine_id]
def can_use_server(machine_id):
    can_use_A=dict()
    can_use_B=dict()
    can_use_server=dict()
    machine_name = machine_id_name[machine_id]
    need_info = generateMachine(machine_name)[1]
    if need_info[-1] == 1:
        can_use_A = {k: v for k, v in server.items() if v[1]>=need_info[0]/2 and v[2]>=need_info[0]/2 and v[3]>=need_info[1]/2 and v[4]>=need_info[1]/2}
        if can_use_A != {}:
            return sorted(can_use_A.keys())[0]
        else:
            purchase_server(myserver, 1)
            can_use_A = {k: v for k, v in server.items() if v[1]>=need_info[0]/2 and v[2]>=need_info[0]/2 and v[3]>=need_info[1]/2 and v[4]>=need_info[1]/2}
            return sorted(can_use_A.keys())[0]
    else:
        can_use_A = {k: v for k, v in server.items() if v[1]>=need_info[0] and v[3]>=need_info[1]}
        can_use_B = {k: v for k, v in server.items() if v[2]>=need_info[0] and v[4]>=need_info[1]}
        if can_use_A=={} and can_use_B=={}:
            purchase_server(myserver, 1)
            can_use_A = {k: v for k, v in server.items() if v[1]>=need_info[0] and v[3]>=need_info[1]}
            can_use_B = {k: v for k, v in server.items() if v[2]>=need_info[0] and v[4]>=need_info[1]}
            return min(sorted(can_use_A.keys())[0],sorted(can_use_B.keys())[0])
        elif can_use_A=={}:
            return sorted(can_use_B.keys())[0]
        elif can_use_B=={}:
            return sorted(can_use_A.keys())[0]   
        else:
            return min(sorted(can_use_A.keys())[0],sorted(can_use_B.keys())[0])
add_machine_id_all=dict()#{n:machine_id}
machine_n=0
for i in range(day_num):
    for j in day_info[i]:
        if j[0] == 'add':
            add_machine_id_all[machine_n]=j[-1]
            machine_n+=1
all_CPU=all_RAM=ALL_C_R=0
for i in range(day_num):
    for j in day_info[i]:
        if j[0] == 'add':
           all_CPU+=machine_dict[j[1]][0]
           all_RAM+=machine_dict[j[1]][1]
ALL_C_R = all_CPU/all_RAM
def min_cost(a):#寻找最小成本
    keys = list()
    max_id = ''
    for i in a.keys():
        keys.append(i)
        for j in a.keys():
            if j not in keys:
                #if ALL_C_R-0.05<=a[i][0]/a[i][1]<=ALL_C_R+0.05 and ALL_C_R-0.05<=a[j][0]/a[j][1]<=ALL_C_R+0.05:
                if 0.8<=a[i][0]/a[i][1]<=0.9 and 0.8<=a[j][0]/a[j][1]<=0.9:
                    if (int(a[i][2])+600*int(a[i][3]))/(int(a[i][0])+int(a[i][1]))<(int(a[j][2])+600*int(a[j][3]))/(int(a[j][0])+int(a[j][1])):
                        max_id = i
                    if (int(a[i][2])+600*int(a[i][3]))/int(a[i][0])+int(a[i][1])>=(int(a[j][2])+600*int(a[j][3]))/(int(a[j][0])+int(a[j][1])):
                        max_id = j
    return max_id
myserver = min_cost(server_dict)
myserver_info = server_dict[myserver]
all_CPU=0
all_RAM=0
most_CPU=0
most_RAM=0
for i in range(int(day_num)):
    for j in day_info[i]:
        if j[0] == 'add':
            all_CPU+=machine_dict[j[1]][0]
            all_RAM+=machine_dict[j[1]][1]
            if most_CPU<=all_CPU:
                most_CPU=all_CPU
            if most_RAM<=all_RAM:
                most_RAM=all_RAM
        else:
            all_CPU-=machine_dict[machine_id_name[j[1]]][0]
            all_RAM-=machine_dict[machine_id_name[j[1]]][1]
    
buy_num = int(max(most_CPU/myserver_info[0],most_RAM/myserver_info[1]))+1
'''
def migrate():
    migration_out=dict()
    count=0
    for i in list(machine_server_on.keys()[-int(len(machine_server_on)*0.005):]):
        if can_use_server(i)<machine_server_on[i][1]:
            delete_server(i,machine_server_on[i][1])
            choose_server_migration(i,can_use_server(i),True,migration_out,count)
            count+=1
    print(f'(migration, {count})')
    for j in range(count):
        print(migration_out[j])
    return
'''             
def main():
    print('(purchase, 1)')
    print(f'({myserver}, {buy_num})')
    print('(migration, 0)')
    sys.stdout.flush()
    purchase_server(myserver, buy_num)
    N=0
    choose_out=dict()
    for j in day_info[0]:
        if j[0] == 'add':
            choose_server(j[-1],can_use_server(j[-1]),False,choose_out,N)
            N+=1
        else:
            delete_server(j[-1],machine_server_on[j[-1]][1])
    for p in range(N):
        print(choose_out[p])
    sys.stdout.flush()
    for i in range(1,int(day_num)):
        N=0
        choose_out=dict()
        pre_server_num = len(server)
        if i%20 == 0:
            migration_out=dict()
            count=0
            a=list(machine_server_on.keys())
            for q in a[-int(len(machine_server_on)*0.02):]:
            #a.reverse()
            #for q in a[0:int(len(machine_server_on)*0.02)]:
                if count >= int(len(machine_server_on)*0.005):
                    break
                elif can_use_server(q)<machine_server_on[q][1]:
                    delete_server(q,machine_server_on[q][1])
                    choose_server_migration(q,can_use_server(q),True,migration_out,count)
                    count+=1        
            for j in day_info[i]:
                if j[0] == 'add':
                    choose_server(j[-1],can_use_server(j[-1]),False,choose_out,N)
                    N+=1  
                else:
                    delete_server(j[-1],machine_server_on[j[-1]][1])
            now_server_num = len(server)
            if now_server_num-pre_server_num>0:
                print('(purchase, 1)')
                print(f'({myserver}, {now_server_num-pre_server_num})')
            else:
                print('(purchase, 0)')
            print(f'(migration, {count})')
            for j in range(count):
                print(migration_out[j])
            for p in range(N):
                print(choose_out[p])
        else:
            for j in day_info[i]:
                if j[0] == 'add':
                    choose_server(j[-1],can_use_server(j[-1]),False,choose_out,N)
                    N+=1  
                else:
                    delete_server(j[-1],machine_server_on[j[-1]][1])
            now_server_num = len(server)
            if now_server_num-pre_server_num>0:
                print('(purchase, 1)')
                print(f'({myserver}, {now_server_num-pre_server_num})')
            else:
                print('(purchase, 0)')
            print(f'(migration, 0)')
            for p in range(N):
                print(choose_out[p])
        sys.stdout.flush()
    
if __name__ == "__main__":
    main()
