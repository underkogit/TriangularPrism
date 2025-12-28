import bpy
import bmesh
from mathutils import Vector
from math import radians


def create_triangular_prism_with_horizontal_bevel(
    name="Triangular_Prism",
    width=2.0,
    height=1.732,
    depth=2.0,
    location=(0, 0, 0),
    rotation=(0, 0, 0),
    bevel_amount=0.2,
    bevel_segments=3,
    bevel_profile=0.5,
    horizontal_z_tol=1e-3,
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
    obj.rotation_euler = (radians(rotation[0]), radians(rotation[1]), radians(rotation[2]))
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
        if abs(v0.x - v1.x) <= horizontal_z_tol:
            vec = v1 - v0
            zc = abs(vec.normalized().x) if vec.length > 1e-8 else 1.0
            if zc <= max_vertical_component:
                e.select = True

    bmesh.update_edit_mesh(obj.data)
    bpy.ops.mesh.bevel(
        affect="EDGES",
        offset_type="OFFSET",
        offset=bevel_amount,
        offset_pct=0,
        segments=bevel_segments,
        profile=bevel_profile,
        clamp_overlap=True,
        loop_slide=True,
        material=-1,
        mark_seam=False,
        mark_sharp=False,
        harden_normals=False,
        face_strength_mode="NONE",
        miter_outer="SHARP",
        miter_inner="SHARP",
        spread=0.1,
        release_confirm=True,
    )
    bpy.ops.object.mode_set(mode="OBJECT")
    mesh.update()
    return obj


def clear_all():
    for obj in list(bpy.data.objects):
        for coll in list(obj.users_collection):
            try:
                coll.objects.unlink(obj)
            except Exception:
                pass
        try:
            bpy.data.objects.remove(obj, do_unlink=True)
        except Exception:
            pass
    for mesh in list(bpy.data.meshes):
        if mesh.users == 0:
            bpy.data.meshes.remove(mesh)
    for mat in list(bpy.data.materials):
        if mat.users == 0:
            bpy.data.materials.remove(mat)
    for tex in list(bpy.data.textures):
        if tex.users == 0:
            bpy.data.textures.remove(tex)
    for img in list(bpy.data.images):
        if img.users == 0:
            bpy.data.images.remove(img)


if __name__ == "__main__":
    clear_all()
    create_triangular_prism_with_horizontal_bevel(
        name="Prism_Horizontal_Bevel",
        width=2.0,
        height=2.0,
        depth=2.0,
        location=(0, 0, 0),
        rotation=(0, 0, 0),
        bevel_amount=0.2,
        bevel_segments=3,
        bevel_profile=0.5,
        horizontal_z_tol=1e-4,
        max_vertical_component=0.01,
    )