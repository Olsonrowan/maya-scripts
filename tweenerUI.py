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
