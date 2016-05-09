=====
Usage
=====

Here's a simple api usage example with the 3 methods.

.. code-block:: python
    :name: helloWorld.py

    from maya import cmds
    from OBB.api import OBB

    if __name__ == '__main__':

        mesh = cmds.ls(selection=True)

        if len(mesh) == 0:
            raise RuntimeError("Nothing selected!")

        obbBoundBoxPnts = OBB.from_points(mesh)
        obbCube = cmds.polyCube(
            constructionHistory=False, name="pointMethod_GEO")[0]
        cmds.xform(obbCube, matrix=obbBoundBoxPnts.matrix)
        print(obbBoundBoxPnts.volume)

        obbBoundBoxTris = OBB.from_triangles(mesh)
        obbCube = cmds.polyCube(
            constructionHistory=False, name="triangleMethod_GEO")[0]
        cmds.xform(obbCube, matrix=obbBoundBoxTris.matrix)
        print(obbBoundBoxTris.volume)

        obbBoundBoxHull = OBB.from_hull(mesh)
        obbCube = cmds.polyCube(
            constructionHistory=False, name="hullMethod_GEO")[0]
        cmds.xform(obbCube, matrix=obbBoundBoxHull.matrix)
        print(obbBoundBoxHull.volume)
