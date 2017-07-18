import rendering

roomw, roomh = 600, 400
scale = roomw / 5400
offx, offy = 100, 50
viewer = rendering.Viewer(roomw + 2 * offx, roomh + 2 * offy)

def int_scale(x):
    return int(x * scale)

for x in range(0, roomw + 1, int_scale(1800)):
    for y in range(0, roomh + 1, int_scale(1800)):
        light = rendering.make_circle(x + offx, y + offy)
        light.set_color(1,.8,0)
        viewer.add_geom(light)


for _ in range(1000):
    viewer.render()
