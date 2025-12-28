import bpy
import bmesh
from math import radians
from mathutils import Vector


class MESH_OT_add_prism(bpy.types.Operator):
    bl_idname = "mesh.add_prism_with_bevel"
    bl_label = "Add Triangular Prism (with horizontal bevel)"
    bl_options = {'REGISTER', 'UNDO'}

    width: bpy.props.FloatProperty(name="Width", default=10, min=0.01)
    height: bpy.props.FloatProperty(name="Height", default=10, min=0.01)
    depth: bpy.props.FloatProperty(name="Depth", default=5, min=0.01)
    bevel_amount: bpy.props.FloatProperty(
        name="Bevel Amount", default=0.2, min=0.0)
    bevel_segments: bpy.props.IntProperty(
        name="Bevel Segments", default=3, min=0, max=20)
    enter_editmode: bpy.props.BoolProperty(
        name="Enter Edit Mode", default=False)

    def execute(self, context):
        create_triangular_prism_with_horizontal_bevel(
            name="Prism_Horizontal_Bevel",
            width=self.width,
            height=self.height,
            depth=self.depth,
            location=(0, 0, 0),
            rotation=(0, 0, 0),
            bevel_amount=self.bevel_amount,
            bevel_segments=self.bevel_segments,
            bevel_profile=0.5,
            horizontal_x_tol=1e-3,
            max_vertical_component=0.01,
        )
        return {'FINISHED'}

    def invoke(self, context, event):
        return self.execute(context)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "width")
        layout.prop(self, "height")
        layout.prop(self, "depth")
        layout.prop(self, "bevel_amount")
        layout.prop(self, "bevel_segments")
        layout.prop(self, "enter_editmode")


def menu_func_prism(self, context):
    self.layout.operator(MESH_OT_add_prism.bl_idname, icon='MESH_CUBE')


def create_triangular_prism_with_horizontal_bevel(
    name="Triangular_Prism",
    width=10,
    height=8,
    depth=4,
    location=(0, 0, 0),
    rotation=(0, 0, 0),
    bevel_amount=0.2,
    bevel_segments=3,
    bevel_profile=0.5,
    horizontal_x_tol=1e-3,
    max_vertical_component=0.1,
):
    half_w = width / 2.0
    verts = [
        (-half_w, -height / 3.0, 0.0),
        (half_w, -height / 3.0, 0.0),
        (0.0, height * 2.0 / 3.0, 0.0),
        (-half_w, -height / 3.0, depth),
        (half_w, -height / 3.0, depth),
        (0.0, height * 2.0 / 3.0, depth),
    ]
    faces = [(0, 1, 2), (3, 5, 4), (0, 3, 4, 1), (1, 4, 5, 2), (2, 5, 3, 0)]

    mesh = bpy.data.meshes.new(f"{name}_Mesh")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    obj.location = location
    obj.rotation_euler = (
        radians(rotation[0]),
        radians(rotation[1]),
        radians(rotation[2]),
    )

    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)

    if bevel_amount <= 0:
        mesh.update()
        return obj

    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_mode(type="EDGE")
    bpy.ops.mesh.select_all(action="DESELECT")

    bm = bmesh.from_edit_mesh(obj.data)
    bm.edges.ensure_lookup_table()

    for e in bm.edges:
        v0, v1 = e.verts[0].co, e.verts[1].co

        if abs(v0.x - v1.x) <= horizontal_x_tol:
            vec = v1.co - v0.co if False else (v1 - v0)
            if vec.length > 1e-8:
                vertical_component = abs(vec.normalized().x)
            else:
                vertical_component = 0.0
            if vertical_component <= max_vertical_component:
                e.select = True

    bmesh.update_edit_mesh(obj.data)

    bpy.ops.mesh.bevel(
        affect="EDGES",
        offset_type="OFFSET",
        offset=bevel_amount,
        segments=bevel_segments,
        profile=bevel_profile,
        clamp_overlap=True,
        loop_slide=True,
        release_confirm=True,
    )

    bpy.ops.object.mode_set(mode="OBJECT")
    mesh.update()
    return obj
