import os
import shutil
o_p = '/home/lijq/data/A/29_r/cf/preanno/60dm/premerge'
p = '/home/lijq/data/A/29_r/cfjsons'
o_p_1 ='/home/lijq/data/A/29_r/cf/preanno/60dm/dmjsons'# r'D:\work\data\microsoft\damian\damian_source\1027data\classfile\ds\gsyshd\x512cut\刮伤黑点'#p#r'D:\work\data\microsoft\damian\damian_source\1027data\classfile\凹凸痕382'

for i in os.listdir(o_p):
    if i.endswith('.json'):
        print('---',)
        name = i.split('.json')[0]
        nn = '{}.json'.format(name)
        #n = '{}.json'.format(name)
        try:
            #print(nn)
            shutil.copy(os.path.join(p,nn),os.path.join(o_p_1,nn))
            #shutil.move(os.path.join(o_p,n),os.path.join(o_p_1,n))
        except:
            print(0)