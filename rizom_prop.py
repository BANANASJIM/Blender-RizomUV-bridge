from enum import auto
from xml.etree.ElementInclude import default_loader
import bpy

class RizomProperties(bpy.types.PropertyGroup):

    temp_fbx_path : bpy.props.StringProperty(name= "Export FBX path", default= "//temp")
    temp_fbx_name : bpy.props.StringProperty(name= "Export FBX name", default= "test.fbx")
    rizomuv_exe_path : bpy.props.StringProperty(name= "RizomUV EXE path", default= "HT_RIZOMUV_EXE") #environ var or absolute path
    method_enum : bpy.props.EnumProperty(
                name= "Method",
                description= "unwrap method",
                items= [('OP0', "Pelt", ""),
                        ('OP1', "Mosaic", ""),
                        ('OP2', "Sharp Edge", ""),
                        ('OP3', "Box", ""),
                        ('OP4', "Custom", "")    
                        ]
                )
    auto_reload_fbx : bpy.props.BoolProperty(name= "Auto Reload FBX" , default= True)
        
    cut_handles : bpy.props.BoolProperty(name= "Cut Handles", default= True)
    link_holes : bpy.props.BoolProperty(name= "Link Holes")

    use_detail_remover : bpy.props.BoolProperty(name= "use detail remover")
    detail_remover : bpy.props.FloatProperty(name= "Detail Remover", default= 0.5, soft_min=0, soft_max= 1.0)
    
    use_stretch_control : bpy.props.BoolProperty(name= "use stretch control")
    stretch_control : bpy.props.FloatProperty(name= "Stretch Control", default= 0.25, soft_min=0, soft_max= 1.0)

    use_reweld_threshold : bpy.props.BoolProperty(name= "use reweld threshold")
    reweld_threshold : bpy.props.FloatProperty(name= "Reweld Threshold", default= 0.01, soft_min=0, soft_max= 10.0)
    reweld_poly_max : bpy.props.IntProperty(name= "Reweld Ploy Max", default= 30, soft_min=1, soft_max= 100)
    reweld_length_max : bpy.props.FloatProperty(name= "Reweld Length Max", default= 1.0, soft_min=0, soft_max= 1.0)

    use_size_limiter : bpy.props.BoolProperty(name= "use size limiter")
    size_limiter : bpy.props.IntProperty(name= "Size Limiter", default= 5, soft_min=1, soft_max= 10)

    #Pelt
    enable_leaf : bpy.props.BoolProperty(name= "Enable Leaf")
    enable_branch : bpy.props.BoolProperty(name= "Enable Branch")
    enable_trunk : bpy.props.BoolProperty(name= "Enable Trunk")

    #Mosaic
    force : bpy.props.FloatProperty(name= "Force", default= 0.25, soft_min= 0.0, soft_max= 1.0)
    fix_revolution_shapes : bpy.props.BoolProperty(name= "Revol Shapes")
    enable_island_count: bpy.props.BoolProperty(name="Enable Island Count")
    island_count : bpy.props.IntProperty(name= "Island Count", default= 5, soft_min=0, soft_max= 100)

    #Sharp Edge
    sharp_edge_angle : bpy.props.FloatProperty(name= "Sharp Edge Angle", default= 70, soft_min= 0, soft_max= 100)

    #Box
    xpos_ypos : bpy.props.BoolProperty(name= "X+Y+", default= True)
    xpos_zpos : bpy.props.BoolProperty(name= "X+Z+", default= True)
    xpos_yneg : bpy.props.BoolProperty(name= "X+Y—", default= True)
    xpos_zneg : bpy.props.BoolProperty(name= "X+Z—", default= True)
    ypos_zpos : bpy.props.BoolProperty(name= "Y+Z+", default= True)
    yneg_zpos : bpy.props.BoolProperty(name= "Y—Z+", default= True)
    yneg_zneg : bpy.props.BoolProperty(name= "Y—Z—", default= True)
    ypos_zneg : bpy.props.BoolProperty(name= "Y+Z—", default= True)
    xneg_ypos : bpy.props.BoolProperty(name= "X—Y+", default= True)
    xneg_zpos : bpy.props.BoolProperty(name= "X—Z+", default= True)
    xneg_yneg : bpy.props.BoolProperty(name= "X—Y—", default= True)
    xneg_zneg : bpy.props.BoolProperty(name= "X—Z—", default= True)

    #TODO Custom
    custom_lua_script : bpy.props.StringProperty(name= "Custom Lua Script",default="")