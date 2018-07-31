#print "asd"
import pickle
try:
    pickle.dump("asd", open("/var/www/t.dump", "w"))
    print "ok"
except:
    print "f"
