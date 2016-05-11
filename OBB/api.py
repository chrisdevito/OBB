# -*- coding: utf-8 -*-

import time
from .utils import eigh
try:
    from maya import cmds
    from maya import OpenMaya
except:
    pass

try:
    from scipy.spatial import ConvexHull
    hullMethod = True
except:
    RuntimeWarning("Unable to load scipy."
                   "The from_hull method will not be available.")
    hullMethod = False


def timeit(method):
    """
    Decorator to time function evaluation.
    Prints "method (args, kwargs) time.sec"
    """
    def timed(*args, **kwargs):

        ts = time.time()
        result = method(*args, **kwargs)
        te = time.time()

        print '%r (%r, %r) %2.2f sec' % \
              (method.__name__, args, kwargs, te-ts)
        return result

    return timed


class OBB(object):
    """
    :class:`OBB` Oriented Bounding Box Class.

    Requires an input meshName.
    """
    meshName = None

    def __init__(self, meshName=None, method=0):

        if not meshName:
            raise RuntimeError("No mesh set in class.")

        self.shapeName = self.getShape(meshName)
        self.fnMesh = self.getMFnMesh(self.shapeName)

        # Get data we need to calculate OBB.
        self.points = self.getPoints(self.fnMesh)
        self.triangles = self.getTriangles(self.fnMesh)

        if method == 0:
            eigenVectors, center, obb_extents = self.build_from_points()

        elif method == 1:
            eigenVectors, center, obb_extents = self.build_from_triangles()

        elif method == 2:
            eigenVectors, center, obb_extents = self.build_from_hull()

        else:
            raise RuntimeError("Method unsupported! Please use 0(from_points),"
                               " 1(from_triangles), or 2(from_hull).")

        # Naturally aligned axis for x, y, z.
        self.eigenVectors = eigenVectors

        # Center point.
        self._center = center

        # Extents (length) of the bounding in x, y, z.
        self._obb_extents = obb_extents

        self.boundPoints = self.get_bounding_points()

        self._width = (self.boundPoints[1] - self.boundPoints[0]).length()
        self._height = (self.boundPoints[2] - self.boundPoints[0]).length()
        self._depth = (self.boundPoints[6] - self.boundPoints[0]).length()
        self._matrix = self.getMatrix()

    @property
    def width(self):
        """
        Property width of the bounding box.
        """
        return self._width

    @property
    def height(self):
        """
        Property height of the bounding box.
        """
        return self._height

    @property
    def depth(self):
        """
        Property depth of the bounding box.
        """
        return self._depth

    @property
    def volume(self):
        """
        Property volume of bounding box.
        """
        return self._width * self._height * self._depth

    @property
    def matrix(self):
        """
        Property matrix of the bounding box.
        """
        return self._matrix

    @property
    def center(self):
        """
        Property center of the bounding box.

        Returns:
            (OpenMaya.MVector)
        """
        return self._center

    @classmethod
    def from_points(cls, meshName=None):
        """
        Bounding box algorithm using vertex points.

        Raises:
            None

        Returns:
            (OBB Instance)
        """
        return cls(meshName=meshName, method=0)

    @classmethod
    def from_triangles(cls, meshName=None):
        """
        Bounding box algorithm using triangles points.

        Raises:
            None

        Returns:
            (OBB Instance)
        """
        return cls(meshName=meshName, method=1)

    @classmethod
    def from_hull(cls, meshName=None):
        """
        Bounding box algorithm using triangles points.

        Raises:
            None

        Returns:
            (OBB Instance)
        """
        if not hullMethod:
            raise RuntimeError(
                "From hull method unavailable because scipy cannot be imported."
                "Please install it if you need it.")
        return cls(meshName=meshName, method=2)

    def create_bounding_box(self, meshName="bounding_GEO"):
        """
        Create the bounding box mesh.

        :param meshName(string): Name of created mesh.

        Raises:
            None

        Returns:
            (string) Cube Transform
        """
        obbCube = cmds.polyCube(constructionHistory=False, name="obb_GEO")[0]

        for ind, pnt in enumerate(self.boundPoints):
            cmds.xform("%s.vtx[%s]" % (obbCube, ind),
                       translation=[pnt.x, pnt.y, pnt.z])

        return obbCube

    def getMatrix(self):
        """
        Gets the matrix representing the transformation of the bounding box.

        Raises:
            None

        Returns:
            (list of floats) Matrix
        """
        m = [(self.eigenVectors[1].x * self._obb_extents.y * 2),
             (self.eigenVectors[1].y * self._obb_extents.y * 2),
             (self.eigenVectors[1].z * self._obb_extents.y * 2),
             0.0,
             (self.eigenVectors[2].x * self._obb_extents.z * 2),
             (self.eigenVectors[2].y * self._obb_extents.z * 2),
             (self.eigenVectors[2].z * self._obb_extents.z * 2),
             0.0,
             (self.eigenVectors[0].x * self._obb_extents.x * 2),
             (self.eigenVectors[0].y * self._obb_extents.x * 2),
             (self.eigenVectors[0].z * self._obb_extents.x * 2),
             0.0,
             self._center.x,
             self._center.y,
             self._center.z,
             1.0]

        # Get the scale.
        mMat = OpenMaya.MMatrix()
        OpenMaya.MScriptUtil.createMatrixFromList(m, mMat)

        if mMat.det4x4() < 0:
            m[8] *= -1
            m[9] *= -1
            m[10] *= -1

        return m

    def get_bounding_points(self):
        """
        Gets the bounding box points from the build.

        Raises:
            None

        Returns:
            (list of MVectors) Bounding box points.
        """
        boundPoints = [(self._center - self.eigenVectors[0] *
                        self._obb_extents.x + self.eigenVectors[1] *
                        self._obb_extents.y + self.eigenVectors[2] *
                        self._obb_extents.z),
                       (self._center - self.eigenVectors[0] *
                        self._obb_extents.x + self.eigenVectors[1] *
                        self._obb_extents.y - self.eigenVectors[2] *
                        self._obb_extents.z),
                       (self._center + self.eigenVectors[0] *
                        self._obb_extents.x + self.eigenVectors[1] *
                        self._obb_extents.y + self.eigenVectors[2] *
                        self._obb_extents.z),
                       (self._center + self.eigenVectors[0] *
                        self._obb_extents.x + self.eigenVectors[1] *
                        self._obb_extents.y - self.eigenVectors[2] *
                        self._obb_extents.z),
                       (self._center + self.eigenVectors[0] *
                        self._obb_extents.x - self.eigenVectors[1] *
                        self._obb_extents.y + self.eigenVectors[2] *
                        self._obb_extents.z),
                       (self._center + self.eigenVectors[0] *
                        self._obb_extents.x - self.eigenVectors[1] *
                        self._obb_extents.y - self.eigenVectors[2] *
                        self._obb_extents.z),
                       (self._center - self.eigenVectors[0] *
                        self._obb_extents.x - self.eigenVectors[1] *
                        self._obb_extents.y + self.eigenVectors[2] *
                        self._obb_extents.z),
                       (self._center - self.eigenVectors[0] *
                        self._obb_extents.x - self.eigenVectors[1] *
                        self._obb_extents.y - self.eigenVectors[2] *
                        self._obb_extents.z)]

        return boundPoints

    def build_from_hull(self):
        """
        Test oriented bounding box algorithm using convex hull points.

        Raises:
            None

        Returns:
            EigenVectors(OpenMaya.MVector)
            CenterPoint(OpenMaya.MVector)
            BoundingExtents(OpenMaya.MVector)
        """
        npPointList = [[self.points[i].x, self.points[i].y, self.points[i].z]
                       for i in xrange(self.points.length())]

        try:
            hull = ConvexHull(npPointList)
        except NameError:
            raise RuntimeError(
                "From hull method unavailable because"
                " scipy cannot be imported."
                "Please install it if you need it.")

        indices = hull.simplices
        vertices = npPointList[indices]
        hullPoints = list(vertices.flatten())
        hullTriPoints = list(indices.flatten())

        hullArray = OpenMaya.MVectorArray()
        for ind in xrange(0, len(hullPoints), 3):
            hullArray.append(
                OpenMaya.MVector(
                    hullPoints[ind], hullPoints[ind+1], hullPoints[ind+2]))

        triPoints = OpenMaya.MIntArray()
        for tri in xrange(len(hullTriPoints)):
            triPoints.append(tri)

        return self.build_from_triangles(points=hullArray, triangles=triPoints)

    def build_from_triangles(self, points=None, triangles=None):
        """
        Test oriented bounding box algorithm using triangles.

        :param points(OpenMaya.MVectorArray): points to represent geometry.
        :param triangles(OpenMaya.MIntArray): points to represent geometry.

        Raises:
            None

        Returns:
            EigenVectors(OpenMaya.MVector)
            CenterPoint(OpenMaya.MVector)
            BoundingExtents(OpenMaya.MVector)
        """
        if not points:
            points = self.points

        if not triangles:
            triangles = self.triangles

        mu = OpenMaya.MVector(0.0, 0.0, 0.0)
        mui = OpenMaya.MVector(0.0, 0.0, 0.0)

        Am, Ai = 0.0, 0.0
        cxx, cxy, cxz, cyy, cyz, czz = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0

        for tInd in xrange(0, triangles.length(), 3):

            p = points[triangles[tInd]]
            q = points[triangles[tInd+1]]
            r = points[triangles[tInd+2]]

            mui = (p + q + r) / 3.0
            Ai = ((q-p) ^ (r-p)).length() * 0.5

            mu += mui * Ai
            Am += Ai

            # these bits set the c terms to Am*E[xx], Am*E[xy], Am*E[xz]....
            cxx += ((9.0 * mui.x * mui.x + p.x * p.x + q.x * q.x + r.x * r.x) *
                    (Ai / 12.0))
            cxy += ((9.0 * mui.x * mui.y + p.x * p.y + q.x * q.y + r.x * r.y) *
                    (Ai / 12.0))
            cxz += ((9.0 * mui.x * mui.z + p.x * p.z + q.x * q.z + r.x * r.z) *
                    (Ai / 12.0))
            cyy += ((9.0 * mui.y * mui.y + p.y * p.y + q.y * q.y + r.y * r.y) *
                    (Ai / 12.0))
            cyz += ((9.0 * mui.y * mui.z + p.y * p.z + q.y * q.z + r.y * r.z) *
                    (Ai / 12.0))

        mu /= Am

        cxx /= Am
        cxy /= Am
        cxz /= Am
        cyy /= Am
        cyz /= Am
        czz /= Am

        cxx -= mu.x * mu.x
        cxy -= mu.x * mu.y
        cxz -= mu.x * mu.z
        cyy -= mu.y * mu.y
        cyz -= mu.y * mu.z
        czz -= mu.z * mu.z

        # Covariance Matrix
        C = [[cxx, cxy, cxz],
             [cxy, cyy, cyz],
             [cxz, cyz, czz]]

        return self.build_from_covariance_matrix(
            cvMatrix=C)

    def build_from_points(self):
        """
        Bounding box algorithm using vertex points.

        Raises:
            None

        Returns:
            EigenVectors(OpenMaya.MVector)
            CenterPoint(OpenMaya.MVector)
            BoundingExtents(OpenMaya.MVector)
        """
        pointSize = float(self.points.length())

        mu = OpenMaya.MVector(0.0, 0.0, 0.0)
        # Calculate the average position of points.
        for p in xrange(int(pointSize)):
            mu += self.points[p] / pointSize

        cxx, cxy, cxz, cyy, cyz, czz = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
        for p in xrange(int(pointSize)):
            p = self.points[p]
            cxx += p.x * p.x - mu.x * mu.x
            cxy += p.x * p.y - mu.x * mu.y
            cxz += p.x * p.z - mu.x * mu.z
            cyy += p.y * p.y - mu.y * mu.y
            cyz += p.y * p.z - mu.y * mu.z
            czz += p.z * p.z - mu.z * mu.z

        # Covariance Matrix
        C = [[cxx, cxy, cxz],
             [cxy, cyy, cyz],
             [cxz, cyz, czz]]

        return self.build_from_covariance_matrix(
            cvMatrix=C)

    def build_from_covariance_matrix(self, cvMatrix=None):
        """
        Build eigen vectors from covariance matrix.

        :param matrix(list of lists): covariance matrix

        Raises:
            None

        Returns:
            None
        """
        # Calculate the natural axes by getting the eigen vectors.
        eigenValues, eigVec = eigh(cvMatrix)

        r = OpenMaya.MVector(eigVec[0][0], eigVec[1][0], eigVec[2][0])
        r.normalize()

        u = OpenMaya.MVector(eigVec[0][1], eigVec[1][1], eigVec[2][1])
        u.normalize()

        f = OpenMaya.MVector(eigVec[0][2], eigVec[1][2], eigVec[2][2])
        f.normalize()

        minim = OpenMaya.MVector(1e10, 1e10, 1e10)
        maxim = OpenMaya.MVector(-1e10, -1e10, -1e10)

        for i in xrange(self.points.length()):
            pnt = self.points[i]

            p_prime = OpenMaya.MVector(
                r * pnt, u * pnt, f * pnt)

            minim = OpenMaya.MVector(
                min(minim.x, p_prime.x),
                min(minim.y, p_prime.y),
                min(minim.z, p_prime.z))
            maxim = OpenMaya.MVector(
                max(maxim.x, p_prime.x),
                max(maxim.y, p_prime.y),
                max(maxim.z, p_prime.z))

        centerPoint = (maxim + minim) * .5
        m_ext = (maxim - minim) * .5

        R = OpenMaya.MVector(r.x, u.x, f.x)
        U = OpenMaya.MVector(r.y, u.y, f.y)
        F = OpenMaya.MVector(r.z, u.z, f.z)

        m_pos = OpenMaya.MVector(
            R * centerPoint, U * centerPoint, F * centerPoint)

        return [r, u, f], m_pos, m_ext

    def getTriangles(self, fnMesh):
        """
        Get the triangles indices.

        :param fnMesh (OpenMaya.MFnMesh): mesh function set.

        Raises:
            None

        Returns:
            (OpenMaya.MIntArray) indices of triangles.
        """
        triangleCounts = OpenMaya.MIntArray()
        triangleVertices = OpenMaya.MIntArray()

        fnMesh.getTriangles(triangleCounts, triangleVertices)

        return triangleVertices

    def getPoints(self, fnMesh):
        """
        Get the points of each vertex.

        :param fnMesh (OpenMaya.MFnMesh): mesh function set.

        Raises:
            None

        Returns:
            (OpenMaya.MVectorArray) list of points.
        """
        mPoints = OpenMaya.MPointArray()
        fnMesh.getPoints(mPoints, OpenMaya.MSpace.kWorld)

        mVecPoints = OpenMaya.MVectorArray()
        [mVecPoints.append(OpenMaya.MVector(mPoints[x]))
         for x in xrange(mPoints.length())]

        return mVecPoints

    def getMFnMesh(self, mesh):
        """
        Gets the MFnMesh of the input mesh.

        :param mesh (str): string name of input mesh.

        Raises:
            `RuntimeError` if not a mesh.
        Returns:
            (OpenMaya.MFnMesh) MFnMesh mesh object.
        """
        mSel = OpenMaya.MSelectionList()
        mSel.add(mesh)

        mDagMesh = OpenMaya.MDagPath()
        mSel.getDagPath(0, mDagMesh)

        try:
            fnMesh = OpenMaya.MFnMesh(mDagMesh)
        except:
            raise RuntimeError("%s is not a mesh.")

        return fnMesh

    def getShape(self,  node):
        """
        Gets the shape node from the input node.

        :param node (str): string name of input node

        Raises:
            `RuntimeError` if no shape node.
        Returns:
            (str) shape node name
        """
        if cmds.nodeType(node) == 'transform':
            shapes = cmds.listRelatives(node, shapes=True)

            if not shapes:
                raise RuntimeError('%s has no shape' % node)

            return shapes[0]

        elif cmds.nodeType(node) == "mesh":
            return node

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
