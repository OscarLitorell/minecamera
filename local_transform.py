
import numpy as np
import math

def primitive_rot_matrix(a, b, a_p, b_p, t):
    
    m = np.zeros((3,3))

    s = math.sin(a)
    c = math.cos(a)
    if a_p != 0:
        m += 1 / a_p * np.array([
            [ s, 0, 0],
            [ 0, 0, 0],
            [-c, 0, 0]
        ])
    else:
        m += t * np.array([
            [c, 0, 0],
            [0, 0, 0],
            [s, 0, 0]
        ])

    s = math.sin(b)
    c = math.cos(b)
    if b_p != 0:
        m += 1 / b_p * np.array([
            [0, 0, 0],
            [0, s, c],
            [0, 0, 0]
        ])
    else:
        m += t * np.array([
            [0, 0,  0],
            [0, c, -s],
            [0, 0,  0]
        ])

    s = math.sin(a + b)
    c = math.cos(a + b)
    if a_p + b_p != 0:
        m += 0.5 / (a_p + b_p) * np.array([
            [0,  s, c],
            [0,  0, 0],
            [0, -c, s]
        ])
    else:
        m += 0.5 * t * np.array([
            [0, c, -s],
            [0, 0,  0],
            [0, s,  c]
        ])

    s = math.sin(a - b)
    c = math.cos(a - b)
    if a_p - b_p != 0:
        m += 0.5 / (a_p - b_p) * np.array([
            [0, -s, c],
            [0,  0, 0],
            [0,  c, s]
        ])
    else:
        m += 0.5 * t * np.array([
            [0, -c, -s],
            [0,  0,  0],
            [0, -s,  c]
        ])

    return m

def local_velocity(a_0, b_0, a_1, b_1, g_0, g_1, t):
    a_p = (a_1 - a_0) / t
    b_p = (b_1 - b_0) / t

    integrated = primitive_rot_matrix(a_1, b_1, a_p, b_p, t) - primitive_rot_matrix(a_0, b_0, a_p, b_p, 0)

    return np.linalg.inv(integrated).dot(g_1 - g_0)

