# Simulation of DMV - 
# Where we know the queue size(number of people waiting in the queue), the number of windows in the DMV center
#[[2,20,60],[3,4,500]] --> format - arrival_timestamp, execution_timestamp, tolerence_timestamp


def dmv(cust_ts,numOfWindows,qSize):
    windows = [0 for i in range(0,numOfWindows)]
    result = [0 for i in range(0,numOfWindows)]
    q = []
    free = numOfWindows
    globalts = 0
    idx = 0
    def min_q():
        nonlocal q
        r = float('inf')
        if len(q)>0:
            for i in range(0,len(q)):
                r = min(r,q[i][0])
        return r

    def decrementer(v):
        nonlocal windows
        nonlocal q
        nonlocal free
        for i in range(0,len(windows)):
            if windows[i]==0:
                continue
            windows[i]-=v
            if windows[i]<=v:
                windows[i]=0
                free+=1
        if len(q)>0:
            i = 0
            while i<len(q):
                q[i][0]-=v
                if q[i][0]<=0:
                    q.pop(i)
                    i-=1
                i+=1
    def checkifqueue():
        nonlocal q
        nonlocal free
        if len(q)>0:
            if free>0:
                nxt_cust = q.pop(0)
                for i in range(0,len(windows)):
                    if windows[i]==0:
                        windows[i] = nxt_cust[1]
                        result[i]+=1
                        free-=1
                        return
        return
    def finishup():
        nonlocal q
        nonlocal free
        nonlocal windows
        nonlocal globalts
        while(len(q)>0):
            nxt_ts = min(len(windows),min_q())
            decrementer(nxt_ts)
            checkifqueue()
            globalts+=nxt_ts
            # print(q,windows,result)
        return 

    while(True):
        nxt_ts = min(min(windows),min_q(),cust_ts[idx][0]-globalts)
        if nxt_ts==0:
            nxt_ts = cust_ts[idx][0]-globalts
        decrementer(nxt_ts)
        # print(nxt_ts)
        globalts+=nxt_ts
        checkifqueue()
        if globalts==cust_ts[idx][0]:
            if len(q)<qSize:
                nwCust = cust_ts[idx]
                arr_time,processingTime,tolerenceTime = nwCust
                q.append([tolerenceTime,processingTime])
            idx+=1
        # print(q,windows,result)
        if idx==len(cust_ts):
            finishup()
            print(result)
            return

dmv([[1,30,100],[5,30,150],[7,30,1],[8,30,500]],2,2)