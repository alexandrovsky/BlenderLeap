import sys
import Leap
import bpy


class ModalTimerOperator(bpy.types.Operator):
    """Operator which runs its self from a timer"""
    bl_idname = "wm.modal_timer_operator"
    bl_label = "Modal Timer Operator"

    _timer = None
    _controller = Leap.Controller()
    _cube = bpy.data.objects['Cube']

    def modal(self, context, event):
        if event.type == 'ESC':
            return self.cancel(context)

        if event.type == 'TIMER':
            frame = self._controller.frame()
            #print(frame)
            if not frame.hands.empty:
                hand = frame.hands[0]
                # Check if the hand has any fingers
                fingers = hand.fingers
                self._cube.location.x = fingers[0].tip_position.x / 10.0
                self._cube.location.z = fingers[0].tip_position.y / 10.0
                self._cube.location.y = -fingers[0].tip_position.z / 10.0

        return {'PASS_THROUGH'}

    def execute(self, context):
        self._timer = context.window_manager.event_timer_add(0.1, context.window)
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def cancel(self, context):
        context.window_manager.event_timer_remove(self._timer)
        return {'CANCELLED'}


def register():
    bpy.utils.register_class(ModalTimerOperator)


def unregister():
    bpy.utils.unregister_class(ModalTimerOperator)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.wm.modal_timer_operator()
