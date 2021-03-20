import numpy as np
f=open('training-1.txt',mode='r')
line = f.read().strip().split("\n")
lineR=np.asarray(line)
for i in range(len(lineR)):
    if '(' in lineR[i]:
        lineR[i] = lineR[i].replace('(','').replace(')','')
meaning = 0
for i in range(len(lineR)):
    if np.shape(lineR[i].split(","))==(1,):
        meaning += 1
        if meaning == 1:
            server_num = lineR[i].split(",")[0]
        elif meaning == 2:
            machine_num = lineR[i].split(",")[0]
        elif meaning == 3:
            day_num = lineR[i].split(",")[0]
#获取三个列表
server_info = lineR[1:1+int(server_num),]
machine_info = lineR[2+int(server_num):2+int(server_num)+int(machine_num),]
day_info = lineR[3+int(server_num)+int(machine_num):,]
day_op=[]
for i in range(len(day_info)):
    if day_info[i].split(", ")[0] == 'add' or day_info[i].split(", ")[0] == 'del':
        day_op.append(day_info[i])
#读取服务器信息
def generateServer(server_name):
    for i in range (int(server_num)):
        if server_info[i].split(", ")[0] == server_name:
            cpu_cores = int(server_info[i].split(", ")[1])
            memory_size = int(server_info[i].split(", ")[2])
            server_cost = int(server_info[i].split(", ")[3])
            power_cost = int(server_info[i].split(", ")[4])
            return np.array([server_name,cpu_cores//2 ,cpu_cores//2,memory_size//2,memory_size//2,server_cost,power_cost])
#读取虚拟机信息
def generateMachine(machine_name):
    for i in range (int(machine_num)):
        if machine_info[i].split(", ")[0] == machine_name:
            cpu_cores_ = int(machine_info[i].split(", ")[1])
            memory_size_ = int(machine_info[i].split(", ")[2])
            machine_type_ = int(machine_info[i].split(", ")[3])
            info1 = [cpu_cores_, memory_size_, machine_type_]
            return np.array([machine_name, cpu_cores_, memory_size_, machine_type_])
machine_name_id = []
for i in range(len(day_info)):
    if day_info[i].split(", ")[0] == 'add':
        machine_name = day_info[i].split(", ")[1]
        machine_id = day_info[i].split(", ")[2]
        machine_name_id.append([machine_name,machine_id])
machine_name_id = np.array(machine_name_id)
def Request(day_start,day_end):
    vm = []
    for i in range(int(day_start),int(day_end)):
        if day_op[i].split(", ")[0] == 'add':
            add_machine = day_op[i].split(", ")[1]
            machine_id = day_op[i].split(", ")[2]
            add_machine_info = generateMachine(add_machine)
            vm.append(np.hstack([add_machine_info,np.array(machine_id),1]))     
        elif day_op[i].split(", ")[0] == 'del':
            machine_id = day_op[i].split(", ")[1]
            for j in range (len(machine_name_id)):
                if machine_name_id[j][1] == machine_id:
                    del_machine = machine_name_id[j][0]
                    del_machine_info = generateMachine(del_machine)
                    vm.append(np.hstack([del_machine_info,np.array(machine_id),0]))
    return np.array(vm)
p = []
def buy_server(server,num):
    for i in range(int(server_num)):
        if  server == server_info[i].split(', ')[0]:
            for j in range (num):
                p.append(generateServer(server))
    return np.array(p)
machine_server_on=['0','0','0','0']
#machine_server_on=np.array([])
def choose_server(machineName,serverId,vmId): 
    global machine_server_on
    need_info = generateMachine(machineName)
    need_cpu = float(need_info[1])
    need_mem = float(need_info[2])
    need_type = int(need_info[3])
    serverId = int(serverId)
    if need_type == 1:
        if float(p[serverId][1])>=need_cpu//2 and float(p[serverId][2])>=need_cpu//2 and float(p[serverId][3])>=need_mem//2 and float(p[serverId][4])>=need_mem//2:
            p[serverId][1] = float(p[serverId][1]) - need_cpu//2
            p[serverId][2] = float(p[serverId][2]) - need_cpu//2
            p[serverId][3] = float(p[serverId][3]) - need_mem//2
            p[serverId][4] = float(p[serverId][4]) - need_mem//2
            #machine_server_on.append([machineName,serverId,12])
            machine_server_on=np.row_stack((machine_server_on,[0,0,0,0]))
            machine_server_on[-1][0]=machineName
            machine_server_on[-1][1]=serverId
            machine_server_on[-1][2]=12
            machine_server_on[-1][3]=vmId
            #machine_server_on=np.row_stack(machine_server_on,np.array([machineName,serverId,12]))
            return True
        else:
            return False
    elif need_type == 0:
        if float(p[serverId][1]) >= need_cpu and float(p[serverId][3]) >= need_mem:
            p[serverId][1] = float(p[serverId][1])-need_cpu
            p[serverId][3] = float(p[serverId][3])-need_mem
            #machine_server_on.append([machineName,serverId,1])
            machine_server_on=np.row_stack((machine_server_on,[0,0,0,0]))
            machine_server_on[-1][0]=machineName
            machine_server_on[-1][1]=serverId
            machine_server_on[-1][2]=1
            machine_server_on[-1][3]=vmId
            #machine_server_on=np.row_stack(machine_server_on,np.array([machineName,serverId,1]))
            return True
        elif float(p[serverId][2]) >= need_cpu and float(p[serverId][4]) >= need_mem:
            p[serverId][2] = float(p[serverId][2])-need_cpu
            p[serverId][4] = float(p[serverId][4])-need_mem
            #machine_server_on.append([machineName,serverId,2])
            machine_server_on=np.row_stack((machine_server_on,[0,0,0,0]))
            machine_server_on[-1][0]=machineName
            machine_server_on[-1][1]=serverId
            machine_server_on[-1][2]=2
            machine_server_on[-1][3]=vmId
            #machine_server_on=np.row_stack(machine_server_on,np.array([machineName,serverId,2]))
            return True
        else:
            return False
def delete_machine(machineName,serverId,vmId):
    global machine_server_on
    need_info = generateMachine(machineName)
    need_cpu = float(need_info[1])
    need_mem = float(need_info[2])
    need_type = int(need_info[3])
    serverId = int(serverId)
    l = int(np.argwhere(machine_server_on[:,3]==str(vmId)))
    if need_type == 1:
        p[serverId][1] = float(p[serverId][1])+need_cpu/2
        p[serverId][2] = float(p[serverId][2])+need_cpu/2
        p[serverId][3] = float(p[serverId][3])+need_mem/2
        p[serverId][4] = float(p[serverId][4])+need_mem/2
        machine_server_on=np.delete(machine_server_on,l,axis=0)
    elif need_type == 0:
        if machine_server_on[l][2] == '1':# and machine_server_on[i][1] == str(serverId) and machine_server_on[i][0] == machineName:
            p[serverId][1] = float(p[serverId][1])+need_cpu
            p[serverId][3] = float(p[serverId][3])+need_mem
            machine_server_on=np.delete(machine_server_on,l,axis=0)
        elif machine_server_on[l][2] == '2':# and machine_server_on[i][1] == str(serverId) and machine_server_on[i][0] == machineName:
            p[serverId][2] = float(p[serverId][2])+need_cpu
            p[serverId][4] = float(p[serverId][4])+need_mem
            machine_server_on=np.delete(machine_server_on,l,axis=0)
day_n=[]
for i in range(len(day_info)):
    if day_info[i].split(", ")[0] != 'add' and day_info[i].split(", ")[0] != 'del':
        day_n.append(day_info[i])
day_n = list(map(int, day_n))
day_n_add = [sum(day_n[:y]) for y in range(1, len(day_n) + 1)]
day_n_add.insert(0,0)
buy_server('hostUY41I',2500)
print('(purchase, 2500)')
print('(hostUY41I, 2500)')
print('(migration, 0)')
out=[]
all_info=['0',0]
n_server = len(p)
for i in range(int(day_num)):#int(day_num)
    for j in Request(day_n_add[i],day_n_add[i+1]):
        if j[-1] == '1':
            for u in range(n_server):
                if choose_server(j[0],u,j[4]) == True:
                    all_info=np.row_stack((all_info,[0,0]))
                    all_info[-1,0] = j[4]
                    all_info[-1,1] = u
                    out.append(machine_server_on[-1,1:3])
                    break
        if j[-1] == '0':
            u=int(np.argwhere(all_info[:,0]==j[4]))
            delete_machine(j[0],int(all_info[u,1]),j[4])
            all_info=np.delete(all_info,u,axis=0)
    out.append(['day',i+1])

def main():
    for i in out:
        if i[0] == 'day' and i[1] < int(day_num):#int(day_num)
            print('(purchase, 0)')
            print('(migration, 0)')
        else:
            if i[1] == '1':
                print("(%d, A)" %(int(i[0])))
            elif i[1] == '2':
                print("(%d, B)" %(int(i[0])))
            elif i[1] == '12':
                print("(%d)" %(int(i[0])))
    pass


if __name__ == "__main__":
    main()
