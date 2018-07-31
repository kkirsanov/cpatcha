import subprocess
from os import unlink


def capcha(filepath):
    #try:
    #    f = open('./digits', "w")
    #    f.write('tessedit_char_whitelist 0123456789')
    #    f.close()
    #except:
    #    pass
    process = subprocess.Popen(['tesseract', filepath, filepath], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT)
    process.communicate()
    process.wait()
    #return str(dir(process))#filepath   
    txt = open(filepath + ".txt", "r")
    txt = "".join(txt.readlines())
    t1 = txt.replace("\n", "")
    #print filepath
    unlink(filepath + ".txt")
    txt = filter(lambda x:x in '0123456789', txt)
    
    if len(txt) == 4:
        return txt
    else:
        return "FAIL: " + t1

#mini test
cnt = 0
if __name__ == '__main__':
    import time
    data = []
    for x in range(0, 20):
        t0 = time.time()
        num = capcha('~/workspace/LMM/cap/capbee_%d.png' % x)
        if "FAIL" in num:
            print x, num
            cnt += 1
        delta = time.time() - t0
        data.append(delta)
        
    print sum(data), sum(data) / len(data)

