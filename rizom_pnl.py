import bpy

from bpy.types import Panel

class OBJECT_PT_RIZOM_Panel(Panel):
    bl_idname = "OBJECT_PT_rizomUV"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "RizomUV"
    bl_category = "RizomUV"

    def draw(self, context):

        layout = self.layout
        props = context.scene.rizom_props
        
        row = layout.row()
        col = row.column()
    
        col = row.column()
        col.prop(props, "temp_fbx_path")
        col.prop(props, "temp_fbx_name")
        col.prop(props, "rizomuv_exe_path")

        row = layout.row()
        row.prop(props, "method_enum",expand= True)


        if props.method_enum == "OP0" :
            row = layout.row()
            row.prop(props, "enable_leaf")
            row.prop(props, "enable_branch")
            row.prop(props, "enable_trunk")

        if props.method_enum == "OP1" :
            row1 = layout.row()
            row1.prop(props, "force" , slider= True)
            row1.enabled = not props.enable_island_count
            row2 = layout.row()
            row2.prop(props, "fix_revolution_shapes")
            row3 = layout.row()
            row3.prop(props, "enable_island_count")
            col = row3.column()
            col.prop(props, "island_count", slider= True)
            col.enabled = props.enable_island_count

        if props.method_enum == "OP2" :
            row = layout.row()
            row.prop(props, "sharp_edge_angle", slider= True)
            
        if props.method_enum == "OP3" :
            row = layout.row()
            row.prop(props, "xpos_ypos")
            row.prop(props, "xpos_zpos")
            row.prop(props, "xpos_yneg")
            row.prop(props, "xpos_zneg")
            row.prop(props, "ypos_zpos")
            row.prop(props, "yneg_zpos")
            row = layout.row()
            row.prop(props, "yneg_zneg")
            row.prop(props, "ypos_zneg")
            row.prop(props, "xneg_ypos")
            row.prop(props, "xneg_zpos")
            row.prop(props, "xneg_yneg")
            row.prop(props, "xneg_zneg")

        #TODO Cusmtom
        if props.method_enum == "OP4" :
            row = layout.row()
            row.prop(props, "custom_lua_script", text= "Custom Lua Script")
            

        layout.row().label(text= "Advanced :")
        row = layout.row()
        row.prop(props, "cut_handles")
        row.prop(props, "link_holes")

        row = layout.row()
        col = row.column()
        col.prop(props, "use_detail_remover", text= "")
        col = row.column()
        col.enabled = props.use_detail_remover
        col.prop(props, "detail_remover", slider= True)

        row = layout.row()
        col = row.column()
        col.prop(props, "use_stretch_control", text= "")
        col = row.column()
        col.enabled = props.use_stretch_control
        col.prop(props, "stretch_control", slider= True)

        row = layout.row()
        col = row.column()
        col.prop(props, "use_reweld_threshold", text= "")
        col = row.column()
        col.enabled = props.use_reweld_threshold
        col.prop(props, "reweld_threshold", slider= True)
        col.prop(props, "reweld_poly_max", slider= True)
        col.prop(props, "reweld_length_max", slider= True)

        row = layout.row()
        col = row.column()
        col.prop(props, "use_size_limiter", text= "")
        col = row.column()
        col.enabled = props.use_size_limiter
        col.prop(props, "size_limiter", slider= True)


        row = layout.row()
        row.prop(props, "auto_reload_fbx",text= "Auto Reload FBX")
        row.operator("object.export_temp_fbx",text = "export temp FBX")

class OBJECT_PT_RIZOM_optimize(Panel):
    bl_idname = "OBJECT_RIZOM_optimize"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "RizomUV Optimize"
    bl_category = "RizomUV"
    bl_parent_id = "OBJECT_PT_rizomUV"

    def draw(self, context):

        layout = self.layout
        props = context.scene.rizom_props

        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        col = layout.column()
        col.prop(props, "use_optimization")
        sub = col.column()
        sub.enabled = props.use_optimization

        sub.prop(props, "use_origin_uv")
        sub.prop(props, "iterations", slider= True)
        sub.prop(props, "optimization_force", slider= True)
        sub.prop(props, "angle_distance_mix", slider= True)

        col = sub.column(align=True)
        
        col.prop(props, "fill_holes")
        col.prop(props, "prevent_flips")
        col.prop(props, "prevent_overlaps")




