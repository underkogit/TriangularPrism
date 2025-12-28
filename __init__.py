# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import sys
import bpy
from .meshes.mesh_prism import *
from .meshes.mesh_box import *
from .meshes.mesh_spiral import *
from . import auto_load
bl_info = {
    "name": "Add Mesh: Triangular Prism + Menu",
    "author": "UnderKo",
    "version": (1, 0, 1),
    "blender": (4, 0, 0),
    "location": "Shift+A -> Mesh",
    "description": "Adds an item to Add→Mesh and creates a triangular prism with a horizontal fold",
    "category": "Add Mesh"
}
auto_load.init()

classes = (MESH_OT_add_prism, MESH_OT_add_box, MESH_OT_add_spiral)


def register():
    auto_load.register()

    print("auto_load.register")
    for fcls in classes:
        bpy.utils.register_class(fcls)
    bpy.types.VIEW3D_MT_mesh_add.append(menu_func_prism)
    bpy.types.VIEW3D_MT_mesh_add.append(menu_func_box)
    bpy.types.VIEW3D_MT_mesh_add.append(menu_func_spiral)


def unregister():
    auto_load.unregister()

    print("auto_load.unregister")
    bpy.types.VIEW3D_MT_mesh_add.remove(menu_func_prism)
    bpy.types.VIEW3D_MT_mesh_add.remove(menu_func_box)
    bpy.types.VIEW3D_MT_mesh_add.remove(menu_func_spiral)
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
