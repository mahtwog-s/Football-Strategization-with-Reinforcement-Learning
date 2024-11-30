import argparse
from types import new_class
import numpy as np
import pulp

parser = argparse.ArgumentParser()

def master_arr(path):
    f = open(path,'r')#,encoding='utf-16')
    lines = f.readlines()
    f.close()
    m_arr = []
    numStates = 0
    numActions = 0
    endStates = []
    curr_states = []
    curr_ac = []
    discount = 0 
    for line in lines:
        x = line.split()
        if x[0] == 'numStates':
            numStates = int(x[1])
        elif x[0] == 'numActions':
            numActions = int(x[1])
            m_arr = [[] for s in range(numStates)]
        elif x[0] == 'end':
            if int(x[1]) != -1:
                endStates = [int(s) for s in x[1:]]
        elif x[0] == 'transition':
            if int(x[1]) not in curr_states:
                curr_states.append(int(x[1]))
                curr_ac = []
            if int(x[2]) not in curr_ac:
                curr_ac.append(int(x[2]))
                m_arr[int(x[1])].append([int(x[2]),(int(x[3]),float(x[4]),float(x[5]))])
            else:
                m_arr[int(x[1])][-1].append((int(x[3]),float(x[4]),float(x[5])))
        elif x[0] == 'discount':
            discount = float(x[1])
    return m_arr,discount,endStates

def value_iteration(m_arr,disc):
    val_stat = [0]*len(m_arr)
    val_pol = [0]*len(m_arr)
    l2_diff = np.inf
    while l2_diff >= 1e-10:
        ind = 0
        new_val_stat = [0]*len(m_arr)
        for s in m_arr:
            if bool(s):
                q = []
                for a in s:
                    qsum = 0
                    for trans in a[1:]:
                        qsum += trans[2]*(trans[1]+(disc*val_stat[trans[0]]))
                    q.append(qsum)
                new_val_stat[ind] = np.max(q)
                val_pol[ind] = s[np.argmax(q)][0]
            ind += 1
        l2_diff = np.linalg.norm(np.array(new_val_stat) - np.array(val_stat))
        val_stat = new_val_stat
    return val_stat, val_pol
        

def get_policy(path):
    f = open(path,'r')
    lines = f.readlines()
    f.close()
    actions = []
    for line in lines:
        actions.append(int(line))
    return actions

def eval_val_func(m_arr,pol,disc,ends):
    vk = [0]*len(m_arr)
    while True:
        vk1 = [0]*len(m_arr)
        for s in range(len(m_arr)):
            if s in ends:
                vk1[s] = 0
            else:
                possib_ac = [i[0] for i in m_arr[s]]
                if pol[s] not in possib_ac:
                    vk1[s] = 0
                else:
                    a = m_arr[s][possib_ac.index(pol[s])]
                    qsum = 0
                    for trans in a[1:]:
                        qsum += trans[2]*(trans[1]+(disc*vk[trans[0]]))
                    vk1[s] = qsum
        if np.linalg.norm(np.array(vk1) - np.array(vk)) <= 1e-10:
            return vk1
        vk = vk1
    return vk

def hpi(m_arr,disc,ends):
    new_pol = [0]*len(m_arr)
    for s in range(len(m_arr)):
        if s not in ends:
            new_pol[s] = m_arr[s][0][0]
    pol = [np.nan]*len(m_arr)
    while (pol != new_pol):
        pol = new_pol
        val_stat = eval_val_func(m_arr,pol,disc,ends)
        ind = 0
        new_pol = [0]*len(m_arr)
        new_val_stat = [0]*len(m_arr)
        for s in m_arr:
            if bool(s):
                q = []
                p = []
                for a in s:
                    if a[0] != pol[ind]:
                        qsum = 0
                        for trans in a[1:]:
                            qsum += trans[2]*(trans[1]+(disc*val_stat[trans[0]]))
                        q.append(qsum)
                        p.append(a[0])
                if (np.max(q) > val_stat[ind]) and (np.max(q)-val_stat[ind])>=1e-10:
                    new_pol[ind] = p[np.argmax(q)]
                    new_val_stat[ind] = np.max(q)
                else:
                    new_pol[ind] = pol[ind]
                    new_val_stat[ind] = val_stat[ind]
            ind += 1
        if np.linalg.norm(np.array(new_val_stat) - np.array(val_stat)) <= 1e-10:
            break
    return eval_val_func(m_arr,new_pol,disc,ends), new_pol

def lp(m_arr,disc):
    prob = pulp.LpProblem('Optimal_Value_Func',pulp.LpMinimize)
    vars = [pulp.LpVariable('V'+str(i)) for i in range(len(m_arr))]
    prob += pulp.lpSum(vars)
    ind = 0
    for s in m_arr:
        if bool(s):
            for a in s:
                q = []
                for trans in a[1:]:
                    q.append(trans[2]*(trans[1]+(disc*vars[trans[0]])))
                prob += (vars[ind] >= pulp.lpSum(q))
        else:
            prob += (vars[ind] >= 0)
        ind += 1
    optimization_result = prob.solve(pulp.PULP_CBC_CMD(msg=0))
    val_func = [pulp.value(x) for x in vars]
    ind = 0
    pol = [0]*len(m_arr)
    for s in m_arr:
        if bool(s):
            q = []
            for a in s:
                qsum = 0
                for trans in a[1:]:
                    qsum += trans[2]*(trans[1]+(disc*val_func[trans[0]]))
                q.append(qsum)
            pol[ind] = s[np.argmax(q)][0]
        ind+=1
    return val_func, pol

        
        
    



if __name__ == "__main__":
    parser.add_argument('--mdp', type = str, required=True, )
    parser.add_argument("--algorithm",type=str,default="lp")
    parser.add_argument("--policy",type=str)
    args = parser.parse_args()
    
    master_array,gam,endstats = master_arr(args.mdp)
    if args.policy:
        pol = get_policy(args.policy)
        val_func = eval_val_func(master_array,pol,gam,endstats)

    else:
        if args.algorithm == 'vi':
            val_func, pol = value_iteration(master_array,gam)
        elif args.algorithm == 'hpi':
            val_func, pol = hpi(master_array,gam,endstats)
        elif args.algorithm == 'lp':
            val_func, pol = lp(master_array,gam)        
    
    for i in range(len(pol)):
        print('{:.6f} {}'.format(val_func[i],pol[i]))