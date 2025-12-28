from math import pi, cos, sin, radians
import bpy


class MESH_OT_add_spiral(bpy.types.Operator):
    bl_idname = "mesh.add_spiral_with_bevel"
    bl_label = "Add Spiral (with bevel)"
    bl_options = {'REGISTER', 'UNDO'}

    spiral_name: bpy.props.StringProperty(name="Name", default="SpiralOnly")
    radius: bpy.props.FloatProperty(name="Radius", default=20.0, min=0.01)
    pitch: bpy.props.FloatProperty(name="Pitch", default=7.0, min=0.0)
    turns: bpy.props.IntProperty(name="Turns", default=5, min=1)
    points_per_turn: bpy.props.IntProperty(
        name="Points per Turn", default=32, min=3)
    start_phase: bpy.props.FloatProperty(name="Start Phase", default=22.0)
    bevel_resolution: bpy.props.IntProperty(
        name="Bevel Resolution", default=1, min=1)
    bevel_depth: bpy.props.FloatProperty(
        name="Bevel Depth", default=2.0, min=0.0)
    squeeze: bpy.props.IntProperty(name="Squeeze", default=0, min=0, max=100)

    def execute(self, context):
        create_spiral(
            name=self.spiral_name,
            radius=self.radius,
            pitch=self.pitch,
            turns=self.turns,
            points_per_turn=self.points_per_turn,
            start_phase=self.start_phase,
            bevel_resolution=self.bevel_resolution,
            bevel_depth=self.bevel_depth,
            squeeze=self.squeeze
        )
        return {'FINISHED'}

    def invoke(self, context, event):
        return self.execute(context)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "spiral_name")
        layout.prop(self, "radius")
        layout.prop(self, "pitch")
        layout.prop(self, "turns")
        layout.prop(self, "points_per_turn")
        layout.prop(self, "start_phase")
        layout.prop(self, "bevel_resolution")
        layout.prop(self, "bevel_depth")
        layout.prop(self, "squeeze")


def menu_func_spiral(self, context):
    self.layout.operator(MESH_OT_add_spiral.bl_idname, icon='CURVE_BEZCURVE')


def create_spiral(
    name="Spiral",
    radius=20.0,
    pitch=7,
    turns=5,
    points_per_turn=32,
    start_phase=22,
    bevel_resolution=1,
    bevel_depth=2,
    squeeze=0,
):
    curve_data = bpy.data.curves.new(name + "_curve", type='CURVE')
    curve_data.dimensions = '3D'
    spline = curve_data.splines.new('POLY')

    steps_per_turn = max(3, int(points_per_turn))
    total_steps = int(steps_per_turn * max(1, int(turns)))
    total_points = total_steps + 1
    spline.points.add(total_points - 1)

    # предрасчёт смещения фазы
    phase_rad = radians(start_phase)

    for i in range(total_points):
        t = i / total_steps  # от 0.0 до 1.0
        angle = 2 * pi * (t * turns) + phase_rad
        z = t * (pitch * turns)

        # squeeze: сужаем на начале и в конце
        # целевая минимальная шкала в середине сужаемой области = 1 - squeeze/100
        s = squeeze / 100.0
        if s <= 0.0:
            squeeze_factor = 1.0
        else:
            # расстояние до ближайшего конца (в нормированном [0,1])
            dist_to_end = min(t, 1.0 - t)
            # ширина зоны сужения — половина кривой (0..0.5). Можно изменить при желании.
            # нормализуем dist_to_end в диапазон 0..1 на интервале [0, 0.5]
            norm = min(1.0, dist_to_end / 0.5)
            # на концах norm ~0 => фактор = 1 - s ; в центре norm ~1 => фактор = 1.0
            squeeze_factor = (1.0 - s) + s * norm

        x = radius * squeeze_factor * cos(angle)
        y = radius * squeeze_factor * sin(angle)
        spline.points[i].co = (x, y, z, 1.0)

    spline.use_cyclic_u = False

    curve_obj = bpy.data.objects.new(name, curve_data)
    bpy.context.collection.objects.link(curve_obj)

    bpy.context.view_layer.objects.active = curve_obj
    curve_obj.data.bevel_resolution = max(1, int(bevel_resolution))
    curve_obj.data.bevel_depth = max(0.0, float(bevel_depth))

    curve_obj.data.resolution_u = 0
    curve_obj.data.render_resolution_u = 0

    print("Спираль создана:", curve_obj.name)
