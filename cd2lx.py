import numpy as np

"""
Write test case
"""
def cd2lx(cd, sx, ex, h=2):
    x = abs(sx - ex)
    diag = np.sqrt(x**2 + h**2)
    cos = h / diag
    return cos * cd / diag ** 2


m400 = []
o700 = []
step = 20

# 0 976 2500
# 0 1325 2000
cd1, cd2, cd3 = 0, 976, 2500
print(cd2lx(cd1, 0.3, 0.6) + cd2lx(cd2, 1.5, 0.6) + cd2lx(cd3, 2.7, 0.6))
print(cd2lx(cd1, 0.3, 1.8) + cd2lx(cd2, 1.5, 1.8) + cd2lx(cd3, 2.7, 1.8))

for cd1 in range(0, 2001, step):
    for cd2 in range(0, 2001, step):
        for cd3 in range(0, 2001, step):
            m400.append([cd2lx(cd1, 0.3, 0.6) + cd2lx(cd2, 1.5, 0.6) + cd2lx(cd3, 2.7, 0.6),
                            (cd1, cd2, cd3)])
            o700.append([cd2lx(cd1, 0.3, 1.8) + cd2lx(cd2, 1.5, 1.8) + cd2lx(cd3, 2.7, 1.8),
                            (cd1, cd2, cd3)])
    print(cd1)

_min = 9999
for i in range(len(m400)):
    if(abs(400 - m400[i][0] + 700 - o700[i][0]) < _min):
        _min = abs(400 - m400[i][0] + 700 - o700[i][0])
        min_data = m400[i] + o700[i]



print(min_data)
