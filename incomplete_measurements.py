from email import iterators
import math

import matplotlib.pyplot as plt
import numpy as np

# x, y, theta
ROBOT_STATE_SIZE = 3
# position, angle, prior
LM_SIZE = 4 

# Covariance
Cx = np.diag([0.5, 0.5, np.deg2rad(30.0)]) ** 2
# R = F_n N F_n^T
R = np.diag([0.5, 0.5, np.deg2rad(30.0)]) ** 2




# The same as in the algorithm we've read about. Should stay the same for us 
def motion_model(x, u):
    F = np.array([[1.0, 0, 0],
                  [0, 1.0, 0],
                  [0, 0, 1.0]])

    B = np.array([[DT * math.cos(x[2, 0]), 0],
                  [DT * math.sin(x[2, 0]), 0],
                  [0.0, DT]])

    x = (F @ x) + (B @ u)
    return x

def prediction_step(xEst, PEst, u):
    xEst[0:ROBOT_STATE_SIZE] = motion_model(xEst, u)

    # d/dR motion_model(R, u)
    jacobi_robot = np.eye(ROBOT_STATE_SIZE) + np.array([
                    [0.0, 0.0, -DT * u[0, 0] * math.sin(xEst[2, 0])],
                   [0.0, 0.0, DT * u[0, 0] * math.cos(xEst[2, 0])],
                   [0.0, 0.0, 0.0]], dtype=float)

    PEst[0:ROBOT_STATE_SIZE, 0:ROBOT_STATE_SIZE] = \
        jacobi_robot @ PEst[0:ROBOT_STATE_SIZE, 0:ROBOT_STATE_SIZE] @ jacobi_robot.T + R

    PEst[0:ROBOT_STATE_SIZE, ROBOT_STATE_SIZE:] = jacobi_robot @ PEst[0:ROBOT_STATE_SIZE, ROBOT_STATE_SIZE:]
    PEst[ROBOT_STATE_SIZE:, 0:ROBOT_STATE_SIZE] = PEst[0:ROBOT_STATE_SIZE, ROBOT_STATE_SIZE:].T

    return xEst, PEst


def observation_model(xEst, landmark):
    v = landmark[3] * np.array(landmark[0], landmark[1])
    return 0

# u -- control
# y -- element from a measurement space
def ekf_slam(xEst, PEst, u, y):
    predicted_position, predicted_covariance = prediction_step(xEst, PEst, u)

    for iz in range(len(y[:, 0])):
        id = y[iz, LM_SIZE]
        nLM = calc_n_lm(xEst)
        
        if id == nLM:
            continue

        z = y[0:LM_SIZE]
        


    return xEst, PEst




DT = 0.1  # time tick [s]
SIM_TIME = 50.0  # simulation time [s]
MAX_RANGE = 4.0  # maximum observation range

#  Simulation parameter -> expected noise based on device parameteres?
Q_sim = np.diag([0.2, np.deg2rad(1.0), 0.02]) ** 2
R_sim = np.diag([1.0, np.deg2rad(10.0)]) ** 2

# landmarks in our world
RFID = np.array([[-1.0, 3.0, 0],
                [2.0, 0.5, 0],
                [2.0, 5.0, 0]
                ])

def calc_n_lm(x):
    n = int((len(x) - ROBOT_STATE_SIZE) / LM_SIZE)
    return n

def pi_2_pi(angle):
    return (angle + math.pi) % (2 * math.pi) - math.pi

# we assume observations are sorted by index
def new_movement_observations():
    posX = 0 
    posY = (0.1)*new_movement_observations.iterator # in every move it moves 1 in Y direction
    posZ = 0
    posAngle = np.pi/2 
    # add noise to gps x-y
    z = np.zeros((0, LM_SIZE+1))

    # we assume robots Z coord never changes
    for i in range(len(RFID[:, 0])):
        dx = RFID[i, 0] - posX
        dy = RFID[i, 1] - posY
        dz = RFID[i, 2] - posZ 
        d = math.hypot(dx, dy)          #real distance
        angle = pi_2_pi(math.atan2(dy, dx) - posAngle) #real angle
        zi = []
        if d <= MAX_RANGE:
            # counting noise for landmarks position
            dn = d + np.random.randn() * Q_sim[0, 0] ** 0.5  # observed distance (real with noise)
            angle_n = angle + np.random.randn() * Q_sim[1, 1] ** 0.5  # observed angke (real with noise)
            dzn = dz + np.random.randn() * Q_sim[2, 2] ** 0.5
            zi = np.array([0, 0, angle_n, 1, i])
            #zi = np.array([d, angle, dz, i])
            z = np.vstack((z, zi))
    
    new_movement_observations.iterator += 1

    u = np.array([1,0])
    
    # add noise to movement so its how we think we're moving (info from wheels or sth)
    u_with_noise = np.array([[
        u[0] + np.random.randn() * R_sim[0, 0] ** 0.5,
        u[1] + np.random.randn() * R_sim[1, 1] ** 0.5]]).T

    return u_with_noise, z
new_movement_observations.iterator = 0


def main():
    print(__file__ + " start!!")

    time = 0.0

    # State Vector [x y yaw v]'
    xEst = np.zeros((ROBOT_STATE_SIZE, 1)) # Gauss mean
    xEst[2,0]= np.pi/2 # only for our simulation
    PEst = np.eye(ROBOT_STATE_SIZE)       # covariance

    xDR = xEst  # Dead reckoning -> simulated position with noise (without observations)

    # history
    hxEst = xEst
    hxDR = hxEst

    while SIM_TIME >= time:
        time += DT
        u, z = new_movement_observations()

        # predicted position based only on movement
        xDR = motion_model(xDR, u)

        xEst, PEst = ekf_slam(xEst, PEst, u, z)

        x_state = xEst[0:ROBOT_STATE_SIZE]

        # store data history
        hxEst = np.hstack((hxEst, x_state))
        hxDR = np.hstack((hxDR, xDR))

        if True:  # pragma: no cover
            plt.cla()
            # for stopping simulation with the esc key.
            plt.gcf().canvas.mpl_connect(
                'key_release_event',
                lambda event: [exit(0) if event.key == 'escape' else None])

            plt.plot(RFID[:, 0], RFID[:, 1], "*k")
            plt.plot(xEst[0], xEst[1], ".r")

            # plot landmark
            for i in range(calc_n_lm(xEst)):
                plt.plot(xEst[ROBOT_STATE_SIZE + i * LM_SIZE],
                         xEst[ROBOT_STATE_SIZE + i * LM_SIZE + 1], "xg")

            plt.plot(hxDR[0, :],
                     hxDR[1, :], "-k")
            plt.plot(hxEst[0, :],
                     hxEst[1, :], "-r")
            plt.axis("equal")
            plt.grid(True)
            plt.pause(0.1)

if __name__ == '__main__':
    main()