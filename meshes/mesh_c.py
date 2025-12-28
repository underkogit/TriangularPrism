import bpy
from math import pi, cos, sin

# --- Настройки (изменяемые) ---
spiral_name = "SpiralOnly"
radius = 20.0
pitch = 7
turns = 5
points_per_turn = 32
start_phase = 22
# bevel параметры
bevel_resolution = 1
bevel_depth = 2
# --- /Настройки ---

# Удаляем старую спираль с тем же именем (опционально)
old = bpy.data.objects.get(spiral_name)
if old and old.type == 'CURVE':
    bpy.data.objects.remove(old, do_unlink=True)

# Создаём спираль (Curve)
curve_data = bpy.data.curves.new(spiral_name + "_curve", type='CURVE')
curve_data.dimensions = '3D'
spline = curve_data.splines.new('POLY')
steps = max(3, int(points_per_turn))
total_points = int(steps * turns) + 1
spline.points.add(total_points - 1)
for i in range(total_points):
    angle = 2 * pi * (i / steps) + start_phase
    z = (i / float(steps)) * pitch
    x = radius * cos(angle)
    y = radius * sin(angle)
    spline.points[i].co = (x, y, z, 1.0)
spline.use_cyclic_u = False

curve_obj = bpy.data.objects.new(spiral_name, curve_data)
bpy.context.collection.objects.link(curve_obj)

# Делаем спираль активной и устанавливаем bevel параметры
bpy.context.view_layer.objects.active = curve_obj
bpy.context.object.data.bevel_resolution = bevel_resolution
bpy.context.object.data.bevel_depth = bevel_depth

# Оптимизация отображения
curve_obj.data.resolution_u = 0
curve_obj.data.render_resolution_u = 0

print("Спираль создана:", curve_obj.name)
