import numpy as np
import sys
import os
import re
import random
import copy
import time

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
server_info,machine_info,day_info = Get_data_input()
#######################################################
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
def choose_server(machine_id,server_id):
    machine_name = machine_id_name[machine_id]
    need_info = generateMachine(machine_name)[1]
    if need_info[-1] == 1:
            server[server_id][1]-=need_info[0]/2
            server[server_id][2]-=need_info[0]/2
            server[server_id][3]-=need_info[1]/2
            server[server_id][4]-=need_info[1]/2
            machine_server_on[machine_id]=[machine_name,int(server_id),int(0)]
            print('(%d)' %(server_id))
    elif need_info[-1] == 0:
        if server[server_id][1]>=need_info[0] and server[server_id][3]>=need_info[1]:
            server[server_id][1]-=need_info[0]      
            server[server_id][3]-=need_info[1]
            machine_server_on[machine_id]=[machine_name,server_id,int(1)]
            print('(%d, A)' %(server_id))
        elif server[server_id][2]>=need_info[0] and server[server_id][4]>=need_info[1]:
            server[server_id][2]-=need_info[0]      
            server[server_id][4]-=need_info[1]
            machine_server_on[machine_id]=[machine_name,int(server_id),int(2)]
            print('(%d, B)' %(server_id))
def delete_server(machine_id,server_id):
    machine_name = machine_id_name[machine_id]
    need_info = generateMachine(machine_name)[1]
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
        return sorted(can_use_A.keys())[0]
    else:
        can_use_A = {k: v for k, v in server.items() if v[1]>=need_info[0] and v[3]>=need_info[1]}
        can_use_B = {k: v for k, v in server.items() if v[2]>=need_info[0] and v[4]>=need_info[1]}
        return min(sorted(can_use_A.keys())[0],sorted(can_use_B.keys())[0])
add_machine_id_all=dict()#{n:machine_id}
machine_n=0
for i in range(day_num):
    for j in day_info[i]:
        if j[0] == 'add':
            add_machine_id_all[machine_n]=j[-1]
            machine_n+=1
server_dict=dict()#{server_name:[CPU,RAM,cost,cost_day]}
for i in range (server_num):
    server_dict[server_info[i][0]] = [server_info[i][1],server_info[i][2],server_info[i][3],server_info[i][4]]

def main():
    print('(purchase, 1)')
    print('(host9T6VX, 4000)')
    print('(migration, 0)')
    purchase_server('host9T6VX',4000)
    for j in day_info[0]:
        if j[0] == 'add':
            choose_server(j[-1],can_use_server(j[-1]))
        else:
            delete_server(j[-1],machine_server_on[j[-1]][1])
    for i in range(1,day_num):
        print('(purchase, 0)')
        print('(migration, 0)')
        for j in day_info[i]:
            if j[0] == 'add':
                choose_server(j[-1],can_use_server(j[-1]))
            else:
                delete_server(j[-1],machine_server_on[j[-1]][1])
    pass


if __name__ == "__main__":
    main()
