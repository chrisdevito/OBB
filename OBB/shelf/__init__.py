import os
from maya import mel
from maya import cmds

from OBB.packages.Qt import QtGui

from functools import partial
from collections import OrderedDict

this_package = os.path.abspath(os.path.dirname(__file__))
shelf_path = partial(os.path.join, this_package)

buttons = OrderedDict({
    'OBB_BoundingBox': {
        'command': (
            "from maya import cmds\n"
            "from OBB.api import OBB\n"
            "meshes = cmds.ls(selection=True)\n"
            "if len(meshes) == 0:\n"
            "   raise RuntimeError(\"Nothing selected!\")\n"
            "for mesh in meshes:\n"
            "   obbBoundBoxPnts = OBB.from_points(mesh)\n"
            "   obbCube = cmds.polyCube(ch=False,\n"
            "                           name=\"{}_BBOX\".format(mesh))[0]\n"
            "   cmds.xform(obbCube, matrix=obbBoundBoxPnts.matrix)"
        ),
        'sourceType': 'python',
        'style': 'iconOnly',
        'image': shelf_path('OBB_boundingBox.png'),
        'annotation': 'AOV Matte management',
        'enableCommandRepeat': False,
        'flat': True,
        'enableBackground': False,
    },
    'OBB_Lattice': {
        'command': (
            "from maya import cmds\n"
            "from OBB.api import OBB\n"
            "meshes = cmds.ls(selection=True)\n"
            "if len(meshes) == 0:\n"
            "   raise RuntimeError(\"Nothing selected!\")\n"
            "for mesh in meshes:\n"
            "   obbBoundBoxPnts = OBB.from_points(mesh)\n"
            "   lattice = cmds.lattice(dv=(2, 2, 2),\n"
            "                          objectCentered=True,\n"
            "                          name=\"{}_LATTICEBOX\".format(mesh))\n"
            "   cmds.xform(lattice[1], matrix=obbBoundBoxPnts.matrix)\n"
            "   cmds.xform(lattice[2], matrix=obbBoundBoxPnts.matrix)"
        ),
        'sourceType': 'python',
        'style': 'iconOnly',
        'image': shelf_path('OBB_lattice.png'),
        'annotation': 'Oriented Bounding Box',
        'enableCommandRepeat': False,
        'flat': True,
        'enableBackground': False,
    },
    'documentation': {
        'command': (
            "import webbrowser\n"
            "webbrowser.open('https://obb.readthedocs.org')"
        ),
        'sourceType': 'python',
        'style': 'iconOnly',
        'image': shelf_path('OBB_docs.png'),
        'annotation': 'documentation',
        'enableCommandRepeat': False,
        'flat': True,
        'enableBackground': False,
    }
})


def create_shelf():
    """
    Create the OBB shelf

    Raises:
        None

    Returns:
        None
    """

    tab_layout = mel.eval('$pytmp=$gShelfTopLevel')
    shelf_exists = cmds.shelfLayout('OBB', exists=True)

    if shelf_exists:
        cmds.deleteUI('OBB', layout=True)

    shelf = cmds.shelfLayout('OBB', parent=tab_layout)

    for button, kwargs in buttons.items():

        img = QtGui.QImage(kwargs['image'])
        kwargs['width'] = img.width()
        kwargs['height'] = img.height()

        cmds.shelfButton(label=button, parent=shelf, **kwargs)

    # Fix object 0 error.
    shelves = cmds.shelfTabLayout(tab_layout, query=True, tabLabelIndex=True)

    for index, shelf in enumerate(shelves):
        cmds.optionVar(stringValue=("shelfName%d" % (index + 1), str(shelf)))


create_shelf()
