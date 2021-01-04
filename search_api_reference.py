import bpy
from bpy.types import Operator
from bpy.props import (
    EnumProperty,StringProperty
)

bl_info = {
    "name": "Search Online Reference",
    "description": "Search online reference",
    "author": "tintwotin, 1C0D",
    "version": (1, 5),
    "blender": (2, 90, 0),
    "location": "Text Editor > Edit > Search Online",
    "wiki_url": "https://github.com/tin2tin/Search-API-Reference",
    "tracker_url": "",
    "category": "Text Editor"}


class TEXT_OT_online_reference(Operator):
    '''Search for current word or selection online'''
    bl_idname = "text.online_reference"
    bl_label = "Search Online"
    bl_options = {"REGISTER", "UNDO"}

    type: EnumProperty(
        name="Search Online",
        description="Search for current word or selection online",
        options={'ENUM_FLAG'},
        items=(
             ('API', "API Reference", "Search the API reference"),
             ('PYTHON', "Python Reference", "Search the Python reference"),
             ('STACKEXCHANGE', "Stack Exchange", "Search Stack Exchange"),
             ('SOURCECODE', "Source Code", "Blender Source Code"),
             ('GITHUB', "Github", "Github"),
             ),
             default={'API'},
        )
        
    s: StringProperty(default='')

    def execute(self, context): 
        
        s=self.s        

        if context.area.type == 'TEXT_EDITOR' and context.space_data.text:  
            
            text = context.space_data.text
            s = self.get_selected_text(text)
            
            if s is None:
                bpy.ops.text.select_word()
                s = self.get_selected_text(text)

        if context.area.type == 'CONSOLE':
            
            s=self.s            
            sc=context.space_data 
            
            if sc.select_start==sc.select_end or sc.select_start==sc.select_end+1:
                self.report({'WARNING'}, "Selection is missing")

                return {'CANCELLED'}
            else:
                bpy.ops.console.copy() 
                s = bpy.context.window_manager.clipboard                    
                
        if context.area.type == 'INFO':
        
            s=self.s            
            sc=context.space_data    
            bpy.ops.info.report_copy()
            s = bpy.context.window_manager.clipboard

        if self.type == {'API'}:
            bpy.ops.wm.url_open(url="https://docs.blender.org/api/current/search.html?q="+s)
        if self.type == {'STACKEXCHANGE'}:
            bpy.ops.wm.url_open(url="https://blender.stackexchange.com/search?q="+s)
        if self.type == {'PYTHON'}:
            bpy.ops.wm.url_open(url="https://docs.python.org/3/search.html?q="+s)
        if self.type == {'SOURCECODE'}:
            bpy.ops.wm.url_open(url="https://developer.blender.org/diffusion/B/browse/master/?grep="+s)
        if self.type == {'GITHUB'}:
            bpy.ops.wm.url_open(url="https://www.google.com/search?q=intext%3A%22"+s+"%22+ext%3Apy+bpy+site%3Agithub.com")
            #bpy.ops.wm.url_open(url="https://github.com/search?l=Python&q="+s+"&type=code")

        return {'FINISHED'}


    def get_selected_text(self, text):

        current_line = text.current_line
        select_end_line = text.select_end_line

        current_character = text.current_character
        select_end_character = text.select_end_character

        # if there is no selected text return None
        if current_line == select_end_line:
            if current_character == select_end_character:
                return None
            else:
                return current_line.body[min(current_character, select_end_character):max(current_character, select_end_character)]

        text_return = None
        writing = False
        normal_order = True  # selection from top to bottom

        for line in text.lines:
            if not writing:
                if line == current_line:
                    text_return = current_line.body[current_character:] + "\n"
                    writing = True
                    continue
                elif line == select_end_line:
                    text_return = select_end_line.body[select_end_character:] + "\n"
                    writing = True
                    normal_order = False
                    continue
            else:
                if normal_order:
                    if line == select_end_line:
                        text_return += select_end_line.body[:select_end_character]
                        break
                    else:
                        text_return += line.body + "\n"
                        continue
                else:
                    if line == current_line:
                        text_return += current_line.body[:current_character]
                        break
                    else:
                        text_return += line.body + "\n"
                        continue

        return text_return


def panel_append(self, context):
    self.layout.separator()
    self.layout.operator_menu_enum("text.online_reference", "type")
    
#see all actions in info    
def update_toggle_see_all_actions(self, context):
    
    bpy.app.debug_wm ^= True

bpy.types.Scene.toggle_see_all_actions = bpy.props.BoolProperty(
    update=update_toggle_see_all_actions
)    
    
def panel1_append(self, context):

    self.layout.separator()
    row = self.layout.row()
    row.prop(context.scene, "toggle_see_all_actions", text="see all actions", icon='HIDE_OFF', toggle=True)


def register():
    bpy.utils.register_class(TEXT_OT_online_reference)
    bpy.types.TEXT_MT_edit.append(panel_append)
    bpy.types.TEXT_MT_context_menu.append(panel_append)
    bpy.types.CONSOLE_MT_context_menu.append(panel_append)
    bpy.types.INFO_MT_context_menu.append(panel_append)
    bpy.types.INFO_HT_header.append(panel1_append)
    bpy.types.CONSOLE_MT_console.append(panel_append)


def unregister():
    bpy.utils.unregister_class(TEXT_OT_online_reference)
    bpy.types.TEXT_MT_edit.remove(panel_append)
    bpy.types.TEXT_MT_context_menu.remove(panel_append)
    bpy.types.CONSOLE_MT_context_menu.remove(panel_append)    
    bpy.types.INFO_MT_context_menu.remove(panel_append)
    bpy.types.INFO_HT_header.remove(panel1_append)    
    bpy.types.CONSOLE_MT_console.remove(panel_append)


if __name__ == "__main__":
    register()
