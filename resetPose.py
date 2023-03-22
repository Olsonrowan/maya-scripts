import maya.cmds as cmds

ctrl_names = cmds.ls(selection=True)

for ctrl in ctrl_names:
    try:
        cmds.setAttr(ctrl + ".translateX", 0)
        cmds.setAttr(ctrl + ".translateY", 0)
        cmds.setAttr(ctrl + ".translateZ", 0)

        cmds.setAttr(ctrl + ".rotateX", 0)
        cmds.setAttr(ctrl + ".rotateY", 0)
        cmds.setAttr(ctrl + ".rotateZ", 0)

        cmds.setAttr(ctrl + ".scaleX", 1)
        cmds.setAttr(ctrl + ".scaleY", 1)
        cmds.setAttr(ctrl + ".scaleZ", 1)
    except:
        pass
