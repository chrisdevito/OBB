from math import sqrt


def eigh(a, tol=1.0e-9):
    """
    Calculates the eigenValues and vectors using jacobi method.
    Code configured without numpy from http://goo.gl/U3m7nX

    Returns:
        (list of 3 floats) EigenValues
        (3x3 list of floats) EigenVectors

    Raises:
        None
    """
    # Find largest off-diag. element a[k][l]
    def maxElem(a):
        n = len(a)
        aMax = 0.0
        for i in xrange(n-1):
            for j in xrange(i+1, n):
                if abs(a[i][j]) >= aMax:
                    aMax = abs(a[i][j])
                    k = i
                    l = j
        return aMax, k, l

    # Rotate to make a[k][l] = 0
    def rotate(a, p, k, l):
        n = len(a)
        aDiff = a[l][l] - a[k][k]
        if abs(a[k][l]) < abs(aDiff) * 1.0e-36:
            t = a[k][l] / aDiff
        else:
            phi = aDiff/(2.0 * a[k][l])
            t = 1.0/(abs(phi) + sqrt(phi**2 + 1.0))
            if phi < 0.0:
                t = -t
        c = 1.0/sqrt(t**2 + 1.0)
        s = t*c
        tau = s/(1.0 + c)
        temp = a[k][l]
        a[k][l] = 0.0
        a[k][k] = a[k][k] - t * temp
        a[l][l] = a[l][l] + t * temp
        for i in xrange(k):      # Case of i < k
            temp = a[i][k]
            a[i][k] = temp - s*(a[i][l] + tau*temp)
            a[i][l] = a[i][l] + s*(temp - tau*a[i][l])
        for i in xrange(k+1, l):  # Case of k < i < l
            temp = a[k][i]
            a[k][i] = temp - s*(a[i][l] + tau*a[k][i])
            a[i][l] = a[i][l] + s*(temp - tau*a[i][l])
        for i in xrange(l+1, n):  # Case of i > l
            temp = a[k][i]
            a[k][i] = temp - s*(a[l][i] + tau*temp)
            a[l][i] = a[l][i] + s*(temp - tau*a[l][i])
        for i in xrange(n):      # Update transformation matrix
            temp = p[i][k]
            p[i][k] = temp - s*(p[i][l] + tau*p[i][k])
            p[i][l] = p[i][l] + s*(temp - tau*p[i][l])

    # Set limit on number of rotations
    n = len(a)
    maxRot = 5*(n**2)

    p = [[1.0,  0.0,  0.0],
         [0.0,  1.0,  0.0],
         [0.0,  0.0,  1.0]]

    # Jacobi rotation loop
    for i in xrange(maxRot):

        aMax, k, l = maxElem(a)

        if aMax < tol:
            return [a[i][i] for i in xrange(len(a))], p

        rotate(a, p, k, l)