import numpy as np
from PIL import Image as pic

xs,ys = np.ogrid[0:100,0:100]

def create_buffer(shape):
    return np.zeros(shape, dtype=np.uint8)

def get_bounds(pixel, r, buffer_dims):
    x, y = pixel
    hoz_min = np.clip(x-r, 0, buffer_dims[1])
    hoz_max = np.clip(x+r+1, 0, buffer_dims[1])
    vert_min = np.clip(y-r, 0, buffer_dims[0])
    vert_max = np.clip(y+r+1, 0, buffer_dims[0])
    return ((hoz_max, hoz_min),(vert_max,vert_min))

def calculate_projection(a, b, xs, ys):
    dx = b[0] - a[0]
    dy = b[1] - b[1]
    x_offset = xs - a[0]
    y_offset = ys - a[1]
    x_dx = x_offset * dx
    y_dy = y_offset * dy
    t = (x_dx + y_dy) / (dx**2 + dy**2)
    t = np.clip(t, 0, 1)
    return t

def calculate_closest_point(a, b, t):
    dx = b[0] - a[0]
    dy = b[1] - b[1]
    cx = a[0] + t*dx
    cy = a[1] + t*dy
    return cx, cy

def calculate_distance(cx, cy, xs, ys):
    dx = xs - cx
    dy = ys - cy
    return np.hypot(dx,dy)

def mask(dist, r):
    m = dist<r
    return m

def buffer_draw(buffer, a, b, r):
    buffer_dims = buffer.shape
    ((hoz_max1, hoz_min1),(vert_max1,vert_min1)) = get_bounds(a,r,buffer_dims)
    ((hoz_max2, hoz_min2),(vert_max2,vert_min2)) = get_bounds(b,r,buffer_dims)
    hoz_max = max(hoz_max1,hoz_max2)
    hoz_min = min(hoz_min1,hoz_min2)
    vert_max = max(vert_max1,vert_max2)
    vert_min = min(vert_min1,vert_min2)
    draw_to = buffer[vert_min:vert_max,hoz_min:hoz_max]
    ys, xs = np.ogrid[vert_min:vert_max,hoz_min:hoz_max]
    t = calculate_projection(a, b, xs, ys)
    cx, cy = calculate_closest_point(a, b, t)
    dist = calculate_distance(cx, cy, xs, ys)
    m = mask(dist, r)
    draw_to[m] = 255

def save_image(buffer):
    img = pic.fromarray(buffer)
    img.save("img.png")

p1 = (10,16)
p2 = (75,48)
buffer = create_buffer((200,200))
t = calculate_projection(p1, p2, xs, ys)
cx, cy = calculate_closest_point(p1, p2, t)
dist = calculate_distance(cx, cy, xs, ys)
m = mask(dist, 1.01)
print(t)
print(cx, cy)
print(dist)
print(m)
buffer_draw(buffer,p1,p2,10)
save_image(buffer)
