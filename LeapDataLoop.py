import sys
import Leap
import bpy


class ModalTimerOperator(bpy.types.Operator):
    """Operator which runs its self from a timer"""
    bl_idname = "wm.modal_timer_operator"
    bl_label = "Modal Timer Operator"

    _timer = None
    _frame_num = 0
    _controller = Leap.Controller()
    _cube = bpy.data.objects['Cube']

    def modal(self, context, event):
        if event.type == 'ESC':
            return self.cancel(context)

        if event.type == 'TIMER':
            frame = self._controller.frame()
            bpy.context.scene.frame_set(self._frame_num)
            self._frame_num += 1
            if not frame.hands.empty:
                hand = frame.hands[0]
                # Check if the hand has any fingers
                fingers = hand.fingers
                #Object Cube move
#                self._cube.location.x = fingers[0].tip_position.x / 10.0
#                self._cube.location.z = fingers[0].tip_position.y / 10.0
#                self._cube.location.y = -fingers[0].tip_position.z / 10.0
                
                #Bones
                #get all Bones
                #Anzahl
                #len(bpy.data.objects['Armature'].pose.bones)
                #Rotate one Pos
                bpy.data.objects['Armature'].pose.bones[0].rotation_quaternion.x = fingers[0].direction.x
                bpy.data.objects['Armature'].pose.bones[0].rotation_quaternion.z = fingers[0].direction.y
                
                
                bpy.data.objects['Armature'].pose.bones[1].rotation_quaternion.x = fingers[1].direction.x
                bpy.data.objects['Armature'].pose.bones[1].rotation_quaternion.z = fingers[1].direction.y
                #bpy.data.objects['Armature'].pose.bones[0].rotation_quaternion.z = fingers[0].direction.z
                print (fingers[1].direction.x)
                
                #Add key Frame
                bpy.data.objects['Armature'].pose.bones[0].keyframe_insert("rotation_quaternion")
        return {'PASS_THROUGH'}

    def execute(self, context):
        self._timer = context.window_manager.event_timer_add(0.1, context.window)
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def cancel(self, context):
        context.window_manager.event_timer_remove(self._timer)
        bpy.data.objects['Armature'].pose.bones[0].rotation_quaternion.x = 0
        bpy.data.objects['Armature'].pose.bones[0].rotation_quaternion.y = 0
        bpy.data.objects['Armature'].pose.bones[0].rotation_quaternion.z = 0
        return {'CANCELLED'}


def register():
    bpy.utils.register_class(ModalTimerOperator)


def unregister():
    bpy.utils.unregister_class(ModalTimerOperator)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.wm.modal_timer_operator()
