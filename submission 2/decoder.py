import argparse
import numpy as np

parser = argparse.ArgumentParser()



if __name__ == "__main__":
    parser.add_argument('--value-policy', type = str, default = "value.txt",required=True)
    parser.add_argument("--opponent",type=str,default="data/football/test-1.txt")
    args = parser.parse_args()
    opp_file = open(args.opponent,'r')
    opp_f = opp_file.readlines()[1:]
    opp_file.close()
    states = [x.split()[0] for x in opp_f]
    val_file = open(args.value_policy,'r')#,encoding='utf-16')
    val_f = val_file.readlines()
    val_file.close()
    val = [x.split()[0] for x in val_f]
    action = [x.split()[1] for x in val_f]
    for i in range(len(states)):
        print('{} {} {:.6f}'.format(states[i],action[i],float(val[i]))) 