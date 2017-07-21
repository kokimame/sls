import math

def cd2lx3d(v1, v2, cd, h=2000):
    dst = ((v1[0] - v2[0])**2 + (v1[1] - v2[1])**2 + h**2)**0.5
    cos = h / dst
    return cos * cd / dst ** 2 * 1000**2

# print(dst3dcos((0,0),(2000/1.414,2000/1.414)))

lights_p = [(0, 0, 0), (1800, 0, 1), (3600, 0, 2), (5400, 0, 3),
          (0, 1800, 4), (1800, 1800, 5), (3600, 1800, 6), (5400, 1800, 7),
          (0, 3600, 8), (1800, 3600, 9), (3600, 3600, 10), (5400, 3600, 11)]
init_cd = 0

# multi-means
desks_p = [ (1000, 2150, 900, 0, (5,4,9,8,1,0)), (2200, 2150, 700, 1, (5,6,9,10,1,2)), 
            (3400, 2150, 500, 2, (6,5,10,9,2,1)), (1000, 2850, 700, 3, (9,8,5,4)), 
            (2200, 2850, 500, 4, (9,5,10,6)), (3400, 2850, 300, 5,(10,6,9,5,11))]
"""
# 4-means
desks_p = [ (1000, 2000, 900, 0, (5,4,9,8)), (2200, 2000, 700, 1, (5,6,9,10)), 
            (3400, 2000, 500, 2, (6,5,10,9)), (1000, 2400, 700, 3, (9,8,5,4)), 
            (2200, 2400, 500, 4, (9,5,10,6)), (3400, 2400, 300, 5,(10,6,9,5))]
"""
"""
desks_p = [ 
    (1000, 2000, 900, 0, (5,4,9)), (2200, 2000, 700, 1, (5,6,9)), (3400, 2000, 500, 2, (6,5,10)),
    (1000, 2400, 700, 3, (9,8,5)), (2200, 2400, 500, 4, (9,5,10)), (3400, 2400, 300, 5,(10,6,9,5,7,11))]
"""

class Light:
    def __init__(self, pos, cd, _id):
        self.cd = cd
        self.pos = pos
        self._id = _id

    def next_light(self, diff):
        return Light(pos, cd + diff)

class Desk:
    def __init__(self, pos, glx, _id, nears):
        self.glx = glx
        self.pos = pos
        self._id = _id
        self.nears = nears
        self.err = 0

    # Updating method for cd of nearby lights
    def adjust_n_lights(self, lights):
        n_light = [light for light in lights if light._id in self.nears]
        print("Before adjust", [(light._id,light.cd) for light in n_light])
        for i, light in enumerate(n_light):
            light.cd += -self.err * (len(n_light) - i) 
            light.cd = 0 if light.cd < 0 else light.cd
            light.cd = 2500 if light.cd > 2500 else light.cd
        print("After adjust", [(light._id, light.cd) for light in n_light])

    def adjust_lights(self, lights):
        print("Before adjust", [(light._id,light.cd) for light in lights])
        for light in lights:
            dcd = -self.err / 10 * self.distance_to(light)**2
            print(dcd)
            light.cd += dcd
            light.cd = 0 if light.cd < 0 else light.cd
            light.cd = 2500 if light.cd > 2500 else light.cd
        print("After adjust", [(light._id, light.cd) for light in lights])

    def distance_to(self, light):
        x1, y1 = self.pos
        x2, y2 = light.pos
        x1, y1, x2, y2 = x1/1000, y1/1000, x2/1000, y2/1000
        d =  ((x1-x2)**2 + (y1-y2)**2)**0.5
        print("Desk", self._id, "- Light", light._id, "::", d)
        return d

# Initialize lights and desks
lights = [ Light((light_p[0],light_p[1]), init_cd, light_p[2]) for light_p in lights_p ]
desks = [ Desk((desk_p[0], desk_p[1]), desk_p[2], desk_p[3], desk_p[4]) for desk_p in desks_p]

for _ in range(500):
    print("\n\n*=*=*=*=*=*== Episode ",_," ==*=*=*=*=*=*=*=*")
    sterr = 0
    for desk in desks:
        dlight = 0
        for light in lights:
            dlight += cd2lx3d(desk.pos, light.pos, light.cd)
        desk.err = dlight - desk.glx 
        sterr += desk.err ** 2
        print("Before Desk ID(", desk._id, ") Error: ", desk.err, "(lx)")
        desk.adjust_lights(lights)

        # **************************
        # Check adjusting effect (to be removed)
        # **************************
        dlight = 0
        for light in lights:
            dlight += cd2lx3d(desk.pos, light.pos, light.cd)
        print("After Desk ID(", desk._id, ") Error: ", dlight - desk.glx, "(lx)")
        print("Lx at desk(", desk._id, "):", dlight)
        print()
        # **************************
    print("<<< Square Error: ", sterr, ">>>")

print([desk.err for desk in desks])
[ print("Light ID", light._id, ":", light.cd) for light in lights ]


"""
test_cddict = {0:270,1:270,2:270,3:270,4:2500,5:2462,6:373,7:0,8:2500,9:0,10:0,11:0}
test_lights = [Light((light_p[0], light_p[1]), test_cddict[light_p[2]], light_p[2]) for light_p in lights_p]

for desk in desks:
    dlight = 0
    for light in test_lights:
        dlight += cd2lx3d(desk.pos, light.pos, light.cd)
    print(dlight)
assert False
"""

