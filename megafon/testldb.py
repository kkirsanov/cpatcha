import leveldb

db = leveldb.LevelDB('/home/kkirsanov/db')

import time

# single put
t = time.time()
for x in range(1000000):
    db.Put('hello' + str(x), 'world')
# print db.Get('hello')
print time.time() - t
