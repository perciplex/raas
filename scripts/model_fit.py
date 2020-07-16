from sympy import *
import numpy as np
from sympy.utilities.lambdify import lambdify
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from traj_produce import get_traj


def get_min_obj(traj):

    alpha, beta, drag = symbols("alpha, beta, drag", real=True)

    # theta, gamma, thetadot = symbols("theta, gamma, thetadot", real=True)
    u = symbols("u", real=True)

    dt = 0.05
    A = Matrix([[1, alpha * dt, dt], [0, alpha, 1]])
    # A = Matrix([[1, alpha * dt, dt * (1 - drag)], [0, alpha, (1 - drag)]])
    B = Matrix([dt * beta, beta])

    print(A.shape)
    print(B.shape)

    opt_vars = [alpha, beta]

    C = Matrix(opt_vars)

    # print(C.shape)

    # x = Matrix([[theta], [gamma], [thetadot]])

    min_obj = Matrix([0])

    for step in traj:

        # [action, theta, np.sin(theta + np.pi), thdot]
        u = step["u"]
        x_next = Matrix(step["s_next"])
        s = step["s"]
        gamma = np.sin(s[0] + np.pi)
        x = Matrix([[s[0]], [gamma], [s[1]]])

        """
        print("x:", x.shape)
        print("x_next:", x_next.shape)
        print("(A * x + B * u):", (A * x + B * u).shape)
        print("x:", x)
        print("x_next:", x_next)
        print(A)
        print(B)
        print(u)
        print("(A * x + B * u):", (A * x + B * u))
        """

        step_error = Matrix([(x_next - (A * x + B * u)).norm() ** 2])

        min_obj += step_error

    # print(min_obj)
    obj_fn = lambdify(opt_vars, min_obj)

    J = min_obj.jacobian(C)
    H = J.jacobian(C)
    print("\nH: ", H)

    J_fn = lambdify(opt_vars, J)
    # print(J_fn(*np.zeros(len(opt_vars))))

    cur_vars = 0.01 * np.random.randn(len(opt_vars))
    J_evald = J_fn(*cur_vars)
    step = -((H.inv()) * J_evald.transpose())

    optimal_vals = Matrix(cur_vars) + step

    opt_vals = [x[0] for x in optimal_vals.tolist()]
    print("\noptimal_vals: ", opt_vals)

    alpha_sol = opt_vals[0]
    beta_sol = opt_vals[1]

    l_sol = (-3 * 10 * dt) / (2 * alpha_sol)
    m_sol = (3 * dt) / (beta_sol * l_sol ** 2)

    print("\n\nValues found:")
    print("alpha = {:.2f}".format(alpha_sol))
    print("beta = {:.2f}".format(beta_sol))
    print("l = {:.2f}".format(l_sol))
    print("m = {:.2f}".format(m_sol))

    """
    x = np.linspace(-1, 1, 50)
    y = np.linspace(-0.5, 0.5, 50)

    X, Y = np.meshgrid(x, y)
    Z = obj_fn(X, Y)[0][0]

    plt.close("all")

    # fig = plt.figure()
    # ax = plt.axes(projection="3d")
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection="3d")
    ax.plot_surface(X, Y, Z, cmap=cm.coolwarm)
    ax.set_xlabel("alpha")
    ax.set_ylabel("beta")
    plt.show()
    """

    """
    obj_fn = lambdify(opt_vars, min_obj)
    obj_val = obj_fn(*opt_vals)[0][0]
    print("\nJ: ", J.shape)
    print(J)
    print(H)
    print("\nstep: ", step)
    print("\nObjective value: ", type(float(obj_val)))
    return float(obj_val)
    """


traj = get_traj()
get_min_obj(traj)
