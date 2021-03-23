import numpy as np
import sys
import os
import re
import random
import numpy as np
import copy
import time
f='training-1.txt'
#获取数据：服务器、虚拟机、每日操作（按天分开）
def Get_data(path):
    if os.path.exists(path):
        with open(path,'r') as data:
            Lis=data.readlines()
            Server=[]
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
                        Server=P
                    if counter==1:
                        Virtual=P
                    if counter>1:
                        use_Case.append(P)
                    counter+=1
                    Lis=Lis[last_num:len(Lis)]
    return Server,Virtual,use_Case
server_info,machine_info,day_info = Get_data(f)
server_num=len(server_info)
machine_num=len(machine_info)
day_num=len(day_info)
#读取服务器信息
def generateServer(server_name):
    for i in range (server_num):
        if server_info[i][0] == server_name:
            cpu_cores = server_info[i][1]
            memory_size = server_info[i][2]
            server_cost = server_info[i][3]
            power_cost = server_info[i][4]
            info = [cpu_cores/2,cpu_cores/2,memory_size/2,memory_size/2,server_cost,power_cost]
            return server_name, info
 #读取虚拟机信息
def generateMachine(machine_name):
    for i in range (machine_num):
        if machine_info[i][0] == machine_name:
            cpu_cores_ = machine_info[i][1]
            memory_size_ = machine_info[i][2]
            machine_type_ = machine_info[i][3]
            info = [cpu_cores_,memory_size_,machine_type_]
            return machine_name, info
server=dict()#{server_id:[server_name,CPU_A,CPU_B,RAM_A,RAM_B]}
machine_server_on=dict()#{machine_id:[machine_name,serverId,A/B]}
machine_id_name=dict()#{machine_id:[machine_name]}
for i in range(day_num):
    for j in range(len(day_info[i])):
        if day_info[i][j][0] == 'add':
            machine_id_name[day_info[i][j][2]] = day_info[i][j][1]
def purchase_server(server_name,num):
    bought_num = len(server)
    p=[]
    for i in range (num):
        server[bought_num+i]=[generateServer(server_name)[0],generateServer(server_name)[1][0],generateServer(server_name)[1][1],
                                generateServer(server_name)[1][2],generateServer(server_name)[1][3]]
    p.append([server_name,num])
    return p
purchase_server('hostUY41I',3000)
def choose_server(machine_id,server_id):
    machine_name = machine_id_name[machine_id]
    need_info = generateMachine(machine_name)[1]
    if need_info[-1] == 1:
            server[server_id][1]-=need_info[0]/2
            server[server_id][2]-=need_info[0]/2
            server[server_id][3]-=need_info[1]/2
            server[server_id][4]-=need_info[1]/2
            machine_server_on[machine_id]=[machine_name,int(server_id),int(0)]
            return True
    elif need_info[-1] == 0:
        if server[server_id][1]>=need_info[0] and server[server_id][3]>=need_info[1]:
            server[server_id][1]-=need_info[0]      
            server[server_id][3]-=need_info[1]
            machine_server_on[machine_id]=[machine_name,server_id,int(1)]
            return True
        elif server[server_id][2]>=need_info[0] and server[server_id][4]>=need_info[1]:
            server[server_id][2]-=need_info[0]      
            server[server_id][4]-=need_info[1]
            machine_server_on[machine_id]=[machine_name,int(server_id),int(2)]
            return True
def delete_server(machine_id,server_id):
    machine_name = machine_id_name[machine_id]
    need_info = generateMachine(machine_name)[1]
    if machine_id in machine_server_on.keys():
        if need_info[-1] == 1:
            server[server_id][1]+=need_info[0]/2
            server[server_id][2]+=need_info[0]/2
            server[server_id][3]+=need_info[1]/2
            server[server_id][4]+=need_info[1]/2
            del machine_server_on[machine_id]
        else:
            if machine_server_on[machine_id][-1] == 1:
                server[server_id][1]+=need_info[0]      
                server[server_id][3]+=need_info[1]
                del machine_server_on[machine_id]
            else:
                server[server_id][2]+=need_info[0]      
                server[server_id][4]+=need_info[1]
                del machine_server_on[machine_id]
    else:
        return False
def can_use_server(machine_id):
    can_use_A=dict()
    can_use_B=dict()
    can_use_server=dict()
    machine_name = machine_id_name[machine_id]
    need_info = generateMachine(machine_name)[1]
    if need_info[-1] == 1:
        can_use_A = {k: v for k, v in server.items() if v[1]>=need_info[0]/2 and v[2]>=need_info[0]/2 and v[3]>=need_info[1]/2 and v[4]>=need_info[1]/2}
        sorted(can_use_A.keys())[0]
        return sorted(can_use_A.keys())[0]
    else:
        can_use_A = {k: v for k, v in server.items() if v[1]>=need_info[0] and v[3]>=need_info[1]}
        can_use_B = {k: v for k, v in server.items() if v[2]>=need_info[0] and v[4]>=need_info[1]}
        return min(sorted(can_use_A.keys())[0],sorted(can_use_B.keys())[0])

#from tqdm import tqdm
for i in range(day_num):
    for j in day_info[i]:
        if j[0] == 'add':
            choose_server(j[-1],can_use_server(j[-1]))
        if j[0] == 'del':
            delete_server(j[-1],machine_server_on[j[-1]][1])
