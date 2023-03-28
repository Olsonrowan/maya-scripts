import maya.cmds as cmds
import functools

# A dictionary to store the saved poses
saved_poses = {}

# A function to save the current pose of a selected object
def save_pose(*args):
    selected_obj = cmds.ls(sl=True)

    # Check if an object is selected
    if not selected_obj:
        cmds.warning("Please select an object to save pose.")
        return

    # Prompt the user to enter a name for the pose
    result = cmds.promptDialog(title="Save Pose", message="Enter pose name:", button=["Save", "Cancel"],
                                  defaultButton="Save", cancelButton="Cancel", dismissString="Cancel")
    if result == "Cancel":
        return

    # Get the pose name from the prompt dialog
    pose_name = cmds.promptDialog(query=True, text=True)
    cmds.separator(height=10)

    # Create a dictionary to store the pose data
    pose_data = {}
    for axis in ["x", "y", "z"]:
        for xform in ["t", "r", "s"]:
            attr = f"{selected_obj[0]}.{xform}{axis}"
            pose_data[attr] = cmds.getAttr(attr)

    # Add the pose data to the dictionary of saved poses
    saved_poses[pose_name] = pose_data

    # Create a button to restore the saved pose
    restore_fn = functools.partial(restore_pose, pose_data)
    cmds.button(label=pose_name, command=restore_fn, parent=pose_layout)

# A function to restore a saved pose of a selected object
def restore_pose(saved_poses, *args):
    selected_obj = cmds.ls(sl=True)

    # Check if an object is selected
    if not selected_obj:
        cmds.warning("Please select an object to restore pose.")
        return

    # Get the pose data from the saved_poses dictionary
    pose_data = saved_poses
    if not pose_data:
        cmds.warning(f"No pose found with name '{saved_poses}'.")
        return

    # Restore the pose by setting the attributes to the saved values
    for attr, value in pose_data.items():
        cmds.setAttr(attr, value)

# Check if the window already exists and delete it if it does
if cmds.window("poseWindow", exists=True):
    cmds.deleteUI("poseWindow")

# Create a new window to display the saved poses
cmds.window("poseWindow", title="Pose")

# Create a layout for the saved poses
pose_layout = cmds.columnLayout(adj=True)

# Add some instructions for the user
cmds.text(label="Select an object and enter a name for the pose to save, or click a saved pose button to restore it.")
cmds.separator(height=10)

# Add a button to save the current pose
cmds.button(label="Save Pose", command=save_pose)

# Add a separator and display the window
cmds.separator(height=10)
cmds.showWindow("poseWindow")
