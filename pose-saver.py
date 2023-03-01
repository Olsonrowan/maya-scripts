from maya import cmds

axis = ["x", "y", "z"]
xform = ["t", "r", "s"]

for ax in axis:
	for xf in xform:
		print(xf, ax)

if cmds.getAttr(f'{cmds.ls(sl=1)[0]}.sx', lock=True):
	print('Its locked')
else:
	print('Unlocked')

selectedObj = cmds.ls(sl=True)

attrVal = cmds.getAttr(f'{selectedObj[0]}.rx')

cmds.setAttr(f'{selectedObj[0]}.rx', attrVal)

cmds.select('ControlSet')
ctrlList = cmds.ls(sl=True)
