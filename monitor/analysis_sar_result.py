#-*-coding:utf-8
import os
import sys

listCPU = []
listNET = []
listSOCK = []
listRAM = []

def getOutFilePath():
    return os.path.join(  os.getcwd(), 'mon_summary.txt')

def analisys(srcFile):
    global listCPU
    global listNET
    global listSOCK
    global listRAM

    print('소스 파일 : ', srcFile)

    f = open(srcFile, 'r', encoding='utf-8')
    line = f.readline()

    isTitle = True
    cate = ""

    while True:
        line = f.readline()
        if not line: break

        arr = line.split()
        if len(arr)  is 0:
            isTitle = True
            continue

        if isTitle is True:
            if "CPU" in arr:
                cate = "CPU"
            elif "IFACE" in arr:
                cate = "NET"
            elif "totsck" in arr:
                cate = "SOCK"
            elif "kbmemused" in arr:
                cate = "RAM"

            isTitle = False
        else:
            if cate is "CPU":
                listCPU.append( (arr, line) ) 
            if cate is "NET":
                listNET.append( (arr, line) ) 
            if cate is "SOCK":
                listSOCK.append( (arr, line) ) 
            if cate is "RAM":
                listRAM.append( (arr, line) ) 
        
        print(line)
    f.close()



def writeSummaryCPU_common(title, writeMode, keyIndexList, TopCount):
    global listCPU
    localList = []

    for tup in listCPU:
        key = 0.0
        for idx in keyIndexList:
            key +=  float(tup[0][idx])
        localList.append((key, tup[1]))

    localList = sorted(localList, key=lambda dataTuple: dataTuple[0], reverse=True)
    localList = localList[0:TopCount]

    f = open(getOutFilePath(), writeMode, encoding='utf-8')
    f.write(title + "\n" )
    f.write('00시 00분 00초     CPU     %user     %nice   %system   %iowait    %steal     %idle\n' )
    
    for line in localList:
        f.write(line[1] )
    f.write('\n')
    f.close()


SubjectStringMap = {
    'CPU': '00시 00분 00초     CPU     %user     %nice   %system   %iowait    %steal     %idle',
    'RAM': '00시 00분 00초 kbmemfree kbmemused  %memused kbbuffers  kbcached  kbcommit   %commit  kbactive   kbinact   kbdirty',
    'NET': '21시 36분 15초     IFACE   rxpck/s   txpck/s    rxkB/s    txkB/s   rxcmp/s   txcmp/s  rxmcst/s',
    'SOCK': '21시 36분 20초    totsck    tcpsck    udpsck    rawsck   ip-frag    tcp-tw',
}

def writeSummary_common(subjectStringKey, title, writeMode, keyIndexList, TopCount, listTotal):
    localList = []

    offset = 2

    for tup in listTotal:
        key = 0.0
        for idx in keyIndexList:
            key +=  float(tup[0][idx + offset])
        localList.append((key, tup[1]))

    localList = sorted(localList, key=lambda dataTuple: dataTuple[0], reverse=True)
    localList = localList[0:TopCount]

    f = open(getOutFilePath(), writeMode, encoding='utf-8')
    f.write(title + "\n" )
    f.write(SubjectStringMap[subjectStringKey] + '\n' )
    
    for line in localList:
        f.write(line[1] )
    f.write('\n')
    f.close()


def writeSummary():
    offset = 0
    writeSummary_common("CPU", "상위 CPU 사용량", 'w', (1,2), 50, listCPU)
    writeSummary_common("CPU", "상위 CPU I/O Wait", 'a', (4,), 50, listCPU)
    writeSummary_common("CPU", "상위 CPU System Call", 'a', (3,), 50, listCPU)

    writeSummary_common("RAM", "상위 RAM 사용량", 'a', (1,), 50, listRAM)

    writeSummary_common("NET", "상위 Netowk 초당 수신한 bytes", 'a', (3,), 50, listNET)
    writeSummary_common("NET", "상위 Netowk 초당 송신한 bytes", 'a', (4,), 50, listNET)

    writeSummary_common("SOCK", "상위 TCP 소켓 사용수", 'a', (1,), 50, listSOCK)
    writeSummary_common("SOCK", "상위 UDP 소켓 시용수", 'a', (2,), 50, listSOCK)

if 2 > len(sys.argv):
    print('분석할 파일을 입력해 주세요. ex> python analysis_sar_result.py targetFile.txt')
else:
    srcFile = sys.argv[1]
    if os.path.isfile(srcFile):
        analisys(srcFile)

        writeSummary()

        print('Output File Path : ', getOutFilePath() )
    else:
        print('파일을 찾을 수 없습니다.')


