from maya import cmds

def tween(percentage, obj=None, attrs=None, selection=True):
    if not obj and not selection:
        raise ValueError("No object given to tween")
    if not obj:
        obj = cmds.ls(selection=True)[0]

    if not attrs:
        attrs = cmds.listAttr(obj, keyable=True)

    currentTime = cmds.currentTime(query=True)

    for attr in attrs:
        attr_full = '%s.%s' % (obj, attr)
        key_frames = cmds.keyframe(attr_full, query=True)
        if not key_frames:
            continue
        previous_key_frames = []
        for frame in key_frames:
            if frame < currentTime:
                previous_key_frames.append(frame)
        later_key_frames = [frame for frame in key_frames if frame > currentTime]

        if not previous_key_frames and not later_key_frames:
            continue

        if previous_key_frames:
            previous_frame = max(previous_key_frames)
        else:
            previous_frame = None

        next_frame = min(later_key_frames) if later_key_frames else None

        if not previous_frame or not next_frame:
            continue

        previous_value = cmds.getAttr(attr_full, time=previous_frame)
        next_value = cmds.getAttr(attr_full, time=next_frame)

        diff = next_value - previous_value
        weight_diff = (diff * percentage) / 100.0
        current_val = previous_value + weight_diff

        cmds.setKeyframe(attr_full, time=currentTime, value=current_val)

class TweenWindow(object):

    window_name = "TweenerWindow"

    def show(self):
        if cmds.window(self.window_name, query=True, exists=True):
            cmds.deleteUI(self.window_name)
        cmds.window(self.window_name)
        self.buildUI()
        cmds.showWindow()

    def buildUI(self):
        column = cmds.columnLayout()
        cmds.text(label="Use this slider to set the tween amount")
        row = cmds.rowLayout(numberOfColumns=2)
        self.slider = cmds.floatSlider(min=0, max=100, value=50, step=1, changeCommand=tween)
        cmds.button(label="Reset", command=self.reset)
        cmds.setParent(column)
        cmds.button(label="Close", command=self.close)

    def reset(self, *args):
        cmds.floatSlider(self.slider, edit=True, value=50)

    def close(self, *args):
        cmds.deleteUI(self.window_name)
