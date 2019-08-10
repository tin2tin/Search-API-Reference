import bpy
from bpy.types import Operator

bl_info = {
    "name": "Search API Reference",
    "description": "Search API reference",
    "author": "tintwotin",
    "version": (0, 1),
    "blender": (2, 80, 0),
    "location": "Text Editor > Edit > Search API Reference",
    "wiki_url": "https://github.com/tin2tin/",
    "tracker_url": "",
    "category": "Text Editor"}


class TEXT_OT_api_reference(Operator):
    '''Search API reference'''
    bl_idname = "text.api_reference"
    bl_label = "Search API Reference"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return (context.space_data.text and context.area.type == 'TEXT_EDITOR')

    def execute(self, context):
        st = context.space_data
        s = self.get_selected_text(st.text)
        if s is None:
            bpy.ops.text.select_word()
            s = self.get_selected_text(st.text)
            if s is not None:
                bpy.ops.wm.url_open(url="https://docs.blender.org/api/2.80/search.html?q="+s)
            else:
                self.report({'INFO'}, "Selection is missing")
                return {'CANCELLED'}
        else:
            bpy.ops.wm.url_open(url="https://docs.blender.org/api/2.80/search.html?q="+s)
        return {'FINISHED'}

    def get_selected_text(self, text):
        """"""
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
    self.layout.operator(TEXT_OT_api_reference.bl_idname)


def register():
    bpy.utils.register_class(TEXT_OT_api_reference)
    bpy.types.TEXT_MT_edit.append(panel_append)
    bpy.types.TEXT_MT_toolbox.append(panel_append)


def unregister():
    bpy.utils.unregister_class(TEXT_OT_api_reference)
    bpy.types.TEXT_MT_edit.remove(panel_append)
    bpy.types.TEXT_MT_toolbox.remove(panel_append)


if __name__ == "__main__":
    register()
