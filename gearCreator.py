from maya import cmds

class Gear(object):

    def __int__(self):
        self.constructor = None
        self.transform = None
        self.extrude = None

    def createGear(self, teeth=10, length=0.3):
        """
        This function will create a gear with the given paramaeters
        Args:
            teeth: The number of teeth to create
            length: The length of teeth
        Returns:
        A tuple of the transform, constructor and extrude node
        """
        spans = teeth * 2

        self.transform, self.constructor = cmds.polyPipe(subdivisionsAxis=spans)

        sideFaces = range(spans*2, spans*3, 2)

        cmds.select(clear=True)

        for face in sideFaces:
            cmds.select('%s.f[%s]' % (self.transform, face), add=True)

        self.extrude = cmds.polyExtrudeFacet(localTranslateZ=length)[0]


    def changeTeeth(self, teeth=10, length=0.3):
        spans = teeth * 2
        cmds.polyPipe(self.constructor, edit=True,
                      subdivisionsAxis=spans)
        sideFaces = range(spans*2, spans*3, 2)

        faceNames = []

        for face in sideFaces:
            faceName = 'f[%s]' % (face)
            faceNames.append(faceName)
        cmds.setAttr('%s.inputComponents' % (self.extrude), len(faceNames),
                     *faceNames, type="componentList")
        cmds.polyExtrudeFacet(self.extrude, edit=True, ltz=length)