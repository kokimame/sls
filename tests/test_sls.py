import rendering

ROOMW, ROOMH = 600, 400
SCALE = ROOMW / 5400
OFFX, OFFY = 100, 50
viewer = rendering.Viewer(ROOMW + 2 * OFFX, ROOMH + 2 * OFFY)

lights_p = [(0, 0, 0), (1800, 0, 1), (3600, 0, 2), (5400, 0, 3),
          (0, 1800, 4), (1800, 1800, 5), (3600, 1800, 6), (5400, 1800, 7),
          (0, 3600, 8), (1800, 3600, 9), (3600, 3600, 10), (5400, 3600, 11)]
init_cd = 0

desks_p = [ 
    (1000, 2150, 900, 0, (5,4,9,8,1,0)), (2200, 2150, 700, 1, (5,6,9,10,1,2)), 
    (3400, 2150, 500, 2, (6,5,10,9,2,1)),(1000, 2850, 700, 3, (9,8,5,4)), 
    (2200, 2850, 500, 4, (9,5,10,6)), (3400, 2850, 300, 5,(10,6,9,5,7,11))]

def cd2lx3d(v1, v2, cd, h=2000):
    dst = ((v1[0] - v2[0])**2 + (v1[1] - v2[1])**2 + h**2)**0.5
    cos = h / dst
    return cos * cd / dst ** 2 * 1000**2

class Light:
    MAXCD = 2500 # Maximum value of candela
    def __init__(self, pos, cd, _id):
        self.cd = cd
        self.pos = pos
        self._id = _id
        x, y = pos
        x, y = x * SCALE, y * SCALE
        self.shape = rendering.make_circle(x + OFFX, y + OFFY)
        self.set_color()
        viewer.add_geom(self.shape)

    def update_cd(self, dcd):
        self.cd += dcd
        self.cd = 0 if self.cd < 0 else self.cd
        self.cd = Light.MAXCD if self.cd > Light.MAXCD else self.cd
        self.set_color()
    
    def set_color(self):
        color_scale = self.cd / Light.MAXCD
        rgb = (color_scale, color_scale, 0)
        self.shape.set_color(*rgb)

class Desk:
    W, H = 1200, 700
    Ws, Hs = 1200 * SCALE, 700 * SCALE
    def __init__(self, pos, glx, _id, nears):
        self.glx = glx
        self.pos = pos
        self._id = _id
        self.nears = nears
        self.err = 0
        x, y = pos
        x, y = x * SCALE, y * SCALE
        lx, rx = x - Desk.Ws/2 + OFFX, x + Desk.Ws/2 + OFFX
        by, ty = y - Desk.Hs/2 + OFFY, y + Desk.Hs/2 + OFFY
        shape = rendering.FilledPolygon([(lx,by),(lx,ty),(rx,ty),(rx,by)])
        shape.set_color(0.8,0.1,0.7)
        viewer.add_geom(shape)
        viewer.draw_polyline([(lx,by),(lx,ty),(rx,ty),(rx,by)])

    # Updating method for cd of nearby lights
    def adjust_light(self, lights):
        n_light = [light for light in lights if light._id in self.nears]
        sign = 1 if self.err < 0 else -1
        for i, light in enumerate(n_light):
            dcd = sign * abs(self.err)/ 10 * (len(n_light) - i) 
            light.update_cd(dcd)

    def set_err(self, err):
        pass


# Initialize lights and desks
desks = [ Desk((desk_p[0], desk_p[1]), desk_p[2], desk_p[3], desk_p[4]) for desk_p in desks_p]
lights = [ Light((light_p[0],light_p[1]), init_cd, light_p[2]) for light_p in lights_p ]

for _ in range(50):
    sterr = 0
    for desk in desks:
        dlight = 0
        for light in lights:
            dlight += cd2lx3d(desk.pos, light.pos, light.cd)
        desk.err = dlight - desk.glx 
        desk.adjust_light(lights)
        viewer.render()


[ print("Light ID", light._id, ":", light.cd) for light in lights ]

#print([desk.err for desk in desks])

