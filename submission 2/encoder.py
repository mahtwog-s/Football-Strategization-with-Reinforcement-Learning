import argparse
import numpy as np

parser = argparse.ArgumentParser()

def str_to_coord(str1):
    b1 =np.array(((int(str1[:2])-1)//4,(int(str1[:2])-1)%4))
    b2 =np.array(((int(str1[2:4])-1)//4,(int(str1[2:4])-1)%4))
    r =np.array(((int(str1[4:6])-1)//4,(int(str1[4:6])-1)%4))
    p = int(str1[-1])
    return b1,b2,r,p

def coord_to_str(b1,b2,r,p):
    str1 = ''
    str1 += f"{int(b1[0]*4+b1[1]+1):02d}"
    str1 += f"{int(b2[0]*4+b2[1]+1):02d}"
    str1 += f"{int(r[0]*4+r[1]+1):02d}"
    str1 += str(p)
    return str1

def toggle(current_value):
    if current_value == 1:
        current_value = 2
    else:
        current_value = 1
    return current_value

def lies_btwn(p1,p2,r):
    dist = np.sqrt(np.square(p1[0]-p2[0]) + np.square(p1[1]-p2[1]))
    dist1 = np.sqrt(np.square(p1[0]-r[0]) + np.square(p1[1]-r[1]))
    dist2 = np.sqrt(np.square(r[0]-p2[0]) + np.square(r[1]-p2[1]))
    if dist != 0:
        if dist == (dist1 + dist2):
            return True
    return False









if __name__ == "__main__":
    parser.add_argument('--opponent', type = str, default = "data/football/test-1.txt",required=True)
    parser.add_argument("--p",type=float,default=0.1)
    parser.add_argument("--q",type=float,default=0.7)
    args = parser.parse_args()
    p = args.p
    q = args.q
    file = open(args.opponent,'r')
    f = file.readlines()[1:]
    file.close()
    states = [x.split()[0] for x in f]
    num_states = len(states)+2
    num_actions = 10
    print('numStates {}'.format(num_states))
    print('numActions {}'.format(num_actions))
    print('end {} {}'.format(8192,8193))
    state_dict = {string: index for index, string in enumerate(states)}
    actions = [i for i in range(10)]
    
    for i in range(len(f)):
        opp_moves = [float(x) for x in f[i].split()[1:]]
        curr_b1, curr_b2, curr_r, curr_p = str_to_coord(states[i])
        new_b1, new_b2, new_r, new_p = 0,0,0,0
        sas = {}
        strs = []
        for j in range(len(opp_moves)):
            if opp_moves[j] > 0:
                if j==0:
                    new_r = curr_r + np.array((0,-1))
                elif j==1:
                    new_r = curr_r + np.array((0,1))
                elif j==2:
                    new_r = curr_r + np.array((-1,0))
                else:
                    new_r = curr_r + np.array((1,0))

                for a in actions:
                    if a<4:
                        new_p = curr_p
                        new_b2 = curr_b2
                        if a == 0:
                            new_b1 = curr_b1 + np.array((0,-1))
                        elif a == 1:
                            new_b1 = curr_b1 + np.array((0,1))
                        elif a == 2:
                            new_b1 = curr_b1 + np.array((-1,0))
                        else:
                            new_b1 = curr_b1 + np.array((1,0))

                        if (np.min(new_b1) < 0) or (np.max(new_b1) > 3):
                            if (i,a,8193) not in sas.keys():
                                sas[(i,a,8193)] = opp_moves[j]*1
                            else:
                                sas[(i,a,8193)] += opp_moves[j]*1
                            
                        elif curr_p == 1:
                            if np.array_equal(new_r,new_b1) or (np.array_equal(curr_b1,new_r) and np.array_equal(curr_r,new_b1)):

                                if (i,a,8193) not in sas.keys():
                                    sas[(i,a,8193)] = opp_moves[j]*(0.5+p)
                                else:
                                    sas[(i,a,8193)] += opp_moves[j]*(0.5+p)
                                
                                strs.append('transition {} {} {} {} {}'.format(i,a,state_dict[coord_to_str(new_b1,new_b2,new_r,new_p)],0,opp_moves[j]*(0.5-p)))
                                
                            else:

                                if (i,a,8193) not in sas.keys():
                                    sas[(i,a,8193)] = opp_moves[j]*(2*p)
                                else:
                                    sas[(i,a,8193)] += opp_moves[j]*(2*p)
                                strs.append('transition {} {} {} {} {}'.format(i,a,state_dict[coord_to_str(new_b1,new_b2,new_r,new_p)],0,opp_moves[j]*(1-(2*p))))
                                
                        elif curr_p == 2:

                            if (i,a,8193) not in sas.keys():
                                sas[(i,a,8193)] = opp_moves[j]*(p)
                            else:
                                sas[(i,a,8193)] += opp_moves[j]*(p)
                            strs.append('transition {} {} {} {} {}'.format(i,a,state_dict[coord_to_str(new_b1,new_b2,new_r,new_p)],0,opp_moves[j]*(1-p)))
                            
                        
                    elif a<8:
                        new_p = curr_p
                        new_b1 = curr_b1

                        if a == 4:
                            new_b2 = curr_b2 + np.array((0,-1))
                        elif a == 5:
                            new_b2 = curr_b2 + np.array((0,1))
                        elif a == 6:
                            new_b2 = curr_b2 + np.array((-1,0))
                        else:
                            new_b2 = curr_b2 + np.array((1,0))

                        if (np.min(new_b2) < 0) or (np.max(new_b2) > 3):
                            if (i,a,8193) not in sas.keys():
                                sas[(i,a,8193)] = opp_moves[j]*1
                            else:
                                sas[(i,a,8193)] += opp_moves[j]*1
                            
                        elif curr_p == 2:
                            if np.array_equal(new_r,new_b2) or (np.array_equal(curr_b2,new_r) and np.array_equal(curr_r,new_b2)):

                                if (i,a,8193) not in sas.keys():
                                    sas[(i,a,8193)] = opp_moves[j]*(0.5+p)
                                else:
                                    sas[(i,a,8193)] += opp_moves[j]*(0.5+p)
                                strs.append('transition {} {} {} {} {}'.format(i,a,state_dict[coord_to_str(new_b1,new_b2,new_r,new_p)],0,opp_moves[j]*(0.5-p)))
                               
                            else:
                                if (i,a,8193) not in sas.keys():
                                    sas[(i,a,8193)] = opp_moves[j]*(2*p)
                                else:
                                    sas[(i,a,8193)] += opp_moves[j]*(2*p)
                                strs.append('transition {} {} {} {} {}'.format(i,a,state_dict[coord_to_str(new_b1,new_b2,new_r,new_p)],0,opp_moves[j]*(1-(2*p))))
                               
                        elif curr_p == 1:

                            if (i,a,8193) not in sas.keys():
                                sas[(i,a,8193)] = opp_moves[j]*(p)
                            else:
                                sas[(i,a,8193)] += opp_moves[j]*(p)
                            strs.append('transition {} {} {} {} {}'.format(i,a,state_dict[coord_to_str(new_b1,new_b2,new_r,new_p)],0,opp_moves[j]*(1-p)))
                            
                    
                    elif a == 8:
                        new_p = toggle(curr_p)
                        new_b1 = curr_b1
                        new_b2 = curr_b2
                        prob = q - 0.1*np.max((abs(new_b1[0]-new_b2[0]),abs(new_b1[1]-new_b2[1])))

                        if lies_btwn(new_b1,new_b2,new_r) and (new_b1[0] == new_b2[0]) and (new_b1[0] == new_r[0]):

                            if (i,a,8193) not in sas.keys():
                                sas[(i,a,8193)] = opp_moves[j]*(1-(prob/2))
                            else:
                                sas[(i,a,8193)] += opp_moves[j]*(1-(prob/2))
                            strs.append('transition {} {} {} {} {}'.format(i,a,state_dict[coord_to_str(new_b1,new_b2,new_r,new_p)],0,opp_moves[j]*prob/2))
                            
                        
                        elif (new_b1[1] == new_b2[1]) and (new_b1[1] == new_r[1]) and lies_btwn(new_b1,new_b2,new_r):
        
                            if (i,a,8193) not in sas.keys():
                                sas[(i,a,8193)] = opp_moves[j]*(1-(prob/2))
                            else:
                                sas[(i,a,8193)] += opp_moves[j]*(1-(prob/2))
                            strs.append('transition {} {} {} {} {}'.format(i,a,state_dict[coord_to_str(new_b1,new_b2,new_r,new_p)],0,opp_moves[j]*prob/2))
                            
                        elif (np.sum(new_b1) == np.sum(new_b2)) and (np.sum(new_b1) == np.sum(new_r)) and lies_btwn(new_b1,new_b2,new_r):
            
                            if (i,a,8193) not in sas.keys():
                                sas[(i,a,8193)] = opp_moves[j]*(1-(prob/2))
                            else:
                                sas[(i,a,8193)] += opp_moves[j]*(1-(prob/2))
                            strs.append('transition {} {} {} {} {}'.format(i,a,state_dict[coord_to_str(new_b1,new_b2,new_r,new_p)],0,opp_moves[j]*prob/2))
                            
                        elif (new_b1[0]-new_b1[1] == new_b2[0]-new_b2[1]) and (new_b1[0]-new_b1[1] == new_r[0]-new_r[1]) and lies_btwn(new_b1,new_b2,new_r):

                            if (i,a,8193) not in sas.keys():
                                sas[(i,a,8193)] = opp_moves[j]*(1-(prob/2))
                            else:
                                sas[(i,a,8193)] += opp_moves[j]*(1-(prob/2))
                            strs.append('transition {} {} {} {} {}'.format(i,a,state_dict[coord_to_str(new_b1,new_b2,new_r,new_p)],0,opp_moves[j]*prob/2))
                         
                        else:
                            if (i,a,8193) not in sas.keys():
                                sas[(i,a,8193)] = opp_moves[j]*(1-prob)
                            else:
                                sas[(i,a,8193)] += opp_moves[j]*(1-prob)
                            strs.append('transition {} {} {} {} {}'.format(i,a,state_dict[coord_to_str(new_b1,new_b2,new_r,new_p)],0,opp_moves[j]*prob))
                                                                 

                    else:
                        new_b1 = curr_b1
                        new_b2 = curr_b2
                        new_p = curr_p
                        if curr_p == 1:
                            prob = q - 0.2*(3-new_b1[1])
                        else:
                            prob = q - 0.2*(3-new_b2[1])
                        
                        if np.array_equal(new_r,np.array((1,3))) or np.array_equal(new_r,np.array((2,3))):
                            if (i,a,8192) not in sas.keys():
                                sas[(i,a,8192)] = opp_moves[j]*(prob/2)
                            else:
                                sas[(i,a,8192)] += opp_moves[j]*(prob/2)
                            
                            if (i,a,8193) not in sas.keys():
                                sas[(i,a,8193)] = opp_moves[j]*(1-(prob/2))
                            else:
                                sas[(i,a,8193)] += opp_moves[j]*(1-(prob/2))
                            
                        else:
                            if (i,a,8192) not in sas.keys():
                                sas[(i,a,8192)] = opp_moves[j]*(prob)
                            else:
                                sas[(i,a,8192)] += opp_moves[j]*(prob)

                            if (i,a,8193) not in sas.keys():
                                sas[(i,a,8193)] = opp_moves[j]*(1-prob)
                            else:
                                sas[(i,a,8193)] += opp_moves[j]*(1-prob)
                            
        for trans in sas.keys():
            if trans[2] == 8192:
                strs.append('transition {} {} {} {} {}'.format(trans[0],trans[1],8192,1,sas[trans]))
            elif trans[2] == 8193:
                strs.append('transition {} {} {} {} {}'.format(trans[0],trans[1],8193,0,sas[trans]))
        
        strs.sort()
        for output in strs:
            print(output)

    print('mdptype episodic')
    print('discount 1')
                        



