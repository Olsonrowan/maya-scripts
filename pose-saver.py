import maya.cmds as cmds
import functools

saved_poses = {}

def save_pose(*args):
    # Get selected object
    selected_obj = cmds.ls(sl=True)

    if not selected_obj:
        cmds.warning("Please select an object to save pose.")
        return

    result = cmds.promptDialog(title="Save Pose", message="Enter pose name:", button=["Save", "Cancel"],
                                  defaultButton="Save", cancelButton="Cancel", dismissString="Cancel")
    if result == "Cancel":
        return

    pose_name = cmds.promptDialog(query=True, text=True)
    cmds.separator(height=10)

    pose_data = {}
    for axis in ["x", "y", "z"]:
        for xform in ["t", "r", "s"]:
            attr = f"{selected_obj[0]}.{xform}{axis}"
            pose_data[attr] = cmds.getAttr(attr)

    saved_poses[pose_name] = pose_data

    restore_fn = functools.partial(restore_pose, pose_data)
    cmds.button(label=pose_name, command=restore_fn, parent=pose_layout)

def restore_pose(saved_poses, *args):
    selected_obj = cmds.ls(sl=True)

    if not selected_obj:
        cmds.warning("Please select an object to restore pose.")
        return

    pose_data = saved_poses
    if not pose_data:
        cmds.warning(f"No pose found with name '{saved_poses}'.")
        return

    for attr, value in pose_data.items():
        cmds.setAttr(attr, value)


if cmds.window("poseWindow", exists=True):
    cmds.deleteUI("poseWindow")

cmds.window("poseWindow", title="Pose")

pose_layout = cmds.columnLayout(adj=True)

cmds.text(label="Select an object and enter a name for the pose to save, or click a saved pose button to restore it.")
cmds.separator(height=10)
cmds.button(label="Save Pose", command=save_pose)
cmds.separator(height=10)

cmds.showWindow("poseWindow")
