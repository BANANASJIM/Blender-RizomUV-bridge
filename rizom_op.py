from tabnanny import check
from typing import Final
import bpy
import os
import platform
import subprocess
import tempfile
from bpy.types import Operator

class Apply_All_Op(Operator):
    bl_idname = "object.apply_all_mods"
    bl_label = "Apply all"
    bl_description = "none"

    @classmethod
    def poll(cls, context):
        obj = context.object

        if obj is not None:
            if obj.mode == "OBJECT":
                return True

        return False
    
    def execute(self, context):
        
        active_obj = context.view_layer.objects.active

        for mod in active_obj.modifiers:
            bpy.ops.object.modifier_apply(modifier=mod.name)

        return {"FINISHED"}

class Export_Temp_FBX(Operator):
    bl_idname = "object.export_temp_fbx"
    bl_label = "export FBX"
    bl_description = "export FBX"

    @classmethod
    def poll(cls, context):
        obj = context.object

        if obj is not None:
            if obj.mode == "OBJECT":
                return True

        return False
       

    def execute(self, context):
        props = context.scene.rizom_props
        export_file_name = props.temp_fbx_name
        export_filepath = props.temp_fbx_path
        rizomuv_exe_path = props.rizomuv_exe_path

        #Pelt Method
        if props.method_enum == 'OP0':
            print("Method : Pelt")
            leaf = props.enable_leaf
            branch = props.enable_branch
            trunk = props.enable_trunk

            seg_levels_array = []
            if leaf: 
                seg_levels_array.append("1")

            if branch: 
                seg_levels_array.append("2")

            if trunk: 
                seg_levels_array.append("3")
            seg_levels = ",".join(seg_levels_array)

        #Mosaic Method
        if props.method_enum == 'OP1':
            print("Method : Mosaic")
            developability = props.force
            fix_revolution_shapes = props.fix_revolution_shapes
            enable_island_count = props.enable_island_count
            island_count = props.island_count

        #Sharp Shape Method
        if props.method_enum == 'OP2':
            print("Method : Sharp Shape")
            sharp_edge_angle = props.sharp_edge_angle

        #Box Method
        if props.method_enum == 'OP3':
            print("Method : Box")
            bounds = []
            parm_val = {"xpos_ypos":'"XPYP"',
                        "xpos_zpos":'"XPZP"',
                        "xpos_yneg":'"XPYM"',
                        "xpos_zneg":'"XPZM"',
                        "ypos_zpos":'"YPZP"',
                        "yneg_zpos":'"YMZP"',
                        "yneg_zneg":'"YMZM"',
                        "ypos_zneg":'"YPZM"',
                        "xneg_ypos":'"XMYP"',
                        "xneg_zpos":'"XMZP"',
                        "xneg_yneg":'"XMYM"',            
                        "xneg_zneg":'"XMZM"',            
                        }
            for parm in parm_val:
                if getattr(props,parm):
                    bounds.append(parm_val[parm])

        select_handles = props.cut_handles
        select_hole_links = props.link_holes

        on_detail_remover = props.use_detail_remover
        detail_remover = props.detail_remover

        on_stretch_control = props.use_stretch_control
        stretch_control = props.stretch_control

        on_reweld = props.use_reweld_threshold
        reweld_threshold = props.reweld_threshold
        reweld_poly_max = props.reweld_poly_max
        reweld_length_max = props.reweld_length_max

        on_size_limiter = props.use_size_limiter
        size_limiter = props.size_limiter

        pipes_cutter = "false"
        if select_hole_links:
            pipes_cutter = "true"
        
        handle_cutter = "false"
        if select_handles:
            handle_cutter = "true"    

        #############Lua Script Generate############

        script = ""
        script += 'ZomSelect({'
        script += 'PrimType="Edge"'
        script += ', Select=true'
        script += ', ResetBefore=true'
        script += ', ProtectMapName="Protect"'
        script += ', FilterIslandVisible=true'

        #Pelt Script Generate
        if props.method_enum == 'OP0':
            script += ', Auto={Skeleton={Open=true'

            if len(seg_levels_array):
                script += ', SegLevels={ ' + seg_levels + '}'
            script += '}'

        #Mosaic Script Generate
        if props.method_enum == 'OP1':
            revolution_shapes = "false"
            if fix_revolution_shapes:
                revolution_shapes = "true"

            if enable_island_count:
                developability = 0

            script += ', Auto={QuasiDevelopable={Developability=' + str(developability)
            script += ', FitCones=' + revolution_shapes
            script += ', IslandPolyNBMin=1' 
            
            if enable_island_count: 
                script += ', IslandsNB=' + str(island_count)

            script += '}'
        
        #Sharp Shape Script Generate
        if props.method_enum == 'OP2':
            script += ', Auto={SharpEdges={AngleMin=' + str(sharp_edge_angle)
            script += '}'

        #Box Script Generate
        if props.method_enum == 'OP3':
            if len(bounds):
                script += ', Auto={Box={ActiveEdges={ '
                script += ",".join(bounds) 
                script += '}}'


        script += ', PipesCutter=' + pipes_cutter
        script += ', HandleCutter=' + handle_cutter 

        if on_stretch_control:   
            script += ', StretchLimiter=true, Quality=' + str(stretch_control)

        if on_detail_remover:       
            script += ', Smooth={Iterations=2, Force=' + str(detail_remover) + '}'

        if on_size_limiter:     
            script += ', SizeLimiter={LengthRatio='+ str(size_limiter)+ '}'
            
        if on_reweld:     
            script += ', ReWeld={Threshold=' + str(reweld_threshold) + ', PolyMax=' \
            + str(reweld_poly_max) + ', LenghtMax=' + str(reweld_length_max) + '}'

        script += '}})\n'


        script += 'ZomCut({'
        script += 'PrimType="Edge"'
        script += '})\n'

        script += 'ZomUnfold({'
        script += 'PrimType="Edge"'
        script += ', MinAngle=1e-005'
        script += ', Mix=1'
        script += ', Iterations=1'
        script += ', PreIterations=5'
        script += ', StopIfOutOFDomain=false'
        script += ', RoomSpace=0'
        script += ', PinMapName="Pin"'
        script += ', ProcessNonFlats=true'
        script += ', ProcessSelection=true'
        script += ', ProcessAllIfNoneSelected=true'
        script += ', ProcessJustCut=true'
        script += ', BorderIntersections=true'
        script += ', TriangleFlips=true'
        script += '})\n'


        script += 'ZomIslandGroups({'
        script += 'Mode="DistributeInTilesEvenly"'
        script += ', MergingPolicy=8322'
        script += ', GroupPath="RootGroup"'
        script += '})'


        script += 'ZomPack({'
        script += 'ProcessTileSelection=false'
        script += ', RecursionDepth=1'
        script += ', RootGroup="RootGroup"'
        script += ', Scaling={Mode=2}'
        script += ', Rotate={}'
        script += ', Translate=true'
        script += ', LayoutScalingMode=2'
        script += '})\n'

        ##############Lua Script Generate############

        #存放初步的脚本
        old_script = script

        ############### Export FBX ##################

        #如果不是路径则是环境变量
        if not os.path.exists(rizomuv_exe_path):
            rizomuv_exe_path = os.environ[rizomuv_exe_path]
        print("RizomUV : " + rizomuv_exe_path)

        export_filepath = bpy.path.abspath(export_filepath)
        isExists = os.path.exists(export_filepath)
        if not isExists:
            os.makedirs(export_filepath)

        export_filepath += "\\"
        export_filepath += export_file_name
        print("Export File : " + export_filepath)
        bpy.ops.export_scene.fbx(filepath=export_filepath, use_selection=True)

        ############### Export FBX ##################

        
        autoLoad    = True
        autoSave    = True
        autoQuit    = True
        clearUVs    = True
        enableLua   = False
        rizomPath   = rizomuv_exe_path
        exportFile  = export_filepath
        luaString = ""

        luascript = '''
                    loadString
                    selectionString
                    luaString
                    saveString
                    quitString
                    '''

        script = luascript

        selString = ""
        #TODO group selection 
        script = script.replace("selectionString", selString)

        loadString = ""
        if autoLoad:
            if clearUVs:
                loadString = 'ZomLoad({File={Path="odfilepath", ImportGroups=true, XYZ=true}, NormalizeUVW=true})'
            else:
                loadString = 'ZomLoad({File={Path="odfilepath", ImportGroups=true, XYZUVW=true, UVWProps=true}, NormalizeUVW=true})'
        script = script.replace("loadString", loadString.replace("odfilepath", exportFile.replace("\\" , "/")))

        saveString = ""
        if autoSave:
            saveString = 'ZomSave({File={Path="odfilepath", UVWProps=true}, __UpdateUIObjFileName=true})'
        script = script.replace("saveString", saveString.replace("odfilepath", exportFile.replace("\\", "/")))

        quitString = ""
        if autoQuit:
            quitString = 'ZomQuit()'
        script = script.replace("quitString", quitString)    

        lua = ""

        if enableLua:
            lua = luaString
        else:
            lua = old_script
        
        script = script.replace("luaString", lua) 
        
        
        if lua != "": 
            f = open(tempfile.gettempdir() + os.sep + "riz.lua", "w")
            f.write(script)
            f.close()    
            cmd = '"' + rizomPath + '" -i -cfi "' + tempfile.gettempdir() + os.sep + "riz.lua" + '"'
            if platform.system() == "Windows":
                subprocess.call(cmd, shell=False)
            else:
                os.system('open -W "' + rizomPath + '" --args -i -cfi "'+tempfile.gettempdir() + os.sep + 'riz.lua"')

        print("Final lua : " + script)

        #reload fbx
        if props.auto_reload_fbx :
            bpy.ops.import_scene.fbx(filepath=export_filepath)
        return {"FINISHED"}
