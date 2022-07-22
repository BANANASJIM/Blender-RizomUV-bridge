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

bl_info = {
    "name" : "RizomUV",
    "author" : "Jim",
    "description" : "RizomUV bridge",
    "blender" : (3, 2, 0),
    "version" : (0, 0, 1),
    "location" : "View3D",
    "warning" : "",
    "category" : "Generic"
}


import bpy

from .rizom_op import Apply_All_Op , Export_Temp_FBX
from .rizom_pnl import OBJECT_PT_RIZOM_Panel
from .rizom_prop import RizomProperties

classes = (RizomProperties, Apply_All_Op, OBJECT_PT_RIZOM_Panel, Export_Temp_FBX)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.rizom_props = bpy.props.PointerProperty(type= RizomProperties)
        

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.rizom_props

if __name__ == "__main__":
    register()

