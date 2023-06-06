from time import time

a = [1 for i in range(1000000)]
def f1():
    for i in range(len(a)):
        a[i] /= 2

# compare with multiplication
def f2():
    for i in range(len(a)):
        a[i] *= 0.5

point_dict = {'f1': 0, 'f2': 0, 'tie': 0}

# compare f1 and f2, give a point to the faster one
n = 10000
for i in range(n):
    t1 = time()
    f1()
    t1 = time() - t1
    t2 = time()
    f2()
    t2 = time() - t2
    if t1 < t2:
        point_dict['f1'] += 1
    elif t2 < t1:
        point_dict['f2'] += 1
    else:
        point_dict['tie'] += 1

# print results
print('After {} iterations:'.format(n))
for k, v in point_dict.items():
    print('{}: {} points'.format(k, v))
    