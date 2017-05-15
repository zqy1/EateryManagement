import random

rand = random.randint(1000, 9999)
print "函数外：" + rand


def ax():
    rand = random.randint(1000, 9999)
    print "函数内" + rand
