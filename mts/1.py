import subprocess
#['killall', '--older-than', '3m', 'python']
#out, err = p.communicate()

import os   
list = os.popen('killall --older-than 3m python').read()