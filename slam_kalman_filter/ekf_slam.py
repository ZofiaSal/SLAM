"""
Extended Kalman Filter SLAM example

author: Atsushi Sakai (@Atsushi_twi)
"""

from email import iterators
import math

import matplotlib.pyplot as plt
import numpy as np

import sys
import os
sys.path.append('/Users/laplasjan/Documents/Studia/informatyka/sem5/zpp/slam100/SLAM/image_processing/test_data_sets/staircase')
import output

# EKF state covariance
Cx = np.diag([0.5, 0.5, np.deg2rad(30.0)]) ** 2
Cx2 = np.diag([0.5, 0.5, 0.5, np.deg2rad(30.0)]) ** 2
#Qx = np.diag([0.05, 0.05, 0.5]) ** 2

#  Simulation parameter -> expected noise based on device parameteres?
Q_sim = np.diag([0.2, np.deg2rad(1.0), 0.02]) ** 2
R_sim = np.diag([1.0, np.deg2rad(10.0)]) ** 2

# landmarks in our world
# RFID = np.array([[-1.0, 3.0, 0],
#                 [2.0, 0.5, 0],
#                 [2.0, 5.0, 0]
#                 ])

DT = 0.1  # time tick [s]
SIM_TIME = 50.0  # simulation time [s]
MAX_RANGE = 4.0  # maximum observation range
M_DIST_TH = 2.0  # Threshold of Mahalanobis distance for data association.
STATE_SIZE = 3  # State size [x,y,yaw]
LM_SIZE = 3  # LM state size [x,y,z]

show_animation = True

def calc_movement():
    return np.array([17.35*np.sin(10*2*np.pi/360)*2, - np.pi / 9])


def search_correspond_landmark_id(xAug, PAug, zi):
     """
     Landmark association with Mahalanobis distance
     """

     nLM = calc_n_lm(xAug)

     min_dist = []

     for i in range(nLM):
         lm = get_landmark_position_from_state(xAug, i)
         y, S, H = calc_innovation(lm, xAug, PAug, zi, i)
         min_dist.append(y.T @ np.linalg.inv(S) @ y)

     min_dist.append(M_DIST_TH)  # new landmark

     min_id = min_dist.index(min(min_dist))

     return min_id



# xEst -> [robot's state,landmarks' state]
def ekf_slam(xEst, PEst, u, z):
    # Predict
    S = STATE_SIZE
    G, Fx = jacob_motion(xEst[0:S], u)  #linearization of movement u-> move with noise 
    xEst[0:S] = motion_model(xEst[0:S], u)
    PEst[0:S, 0:S] = G.T @ PEst[0:S, 0:S] @ G + Fx.T @ Cx @ Fx
    initP = np.eye(LM_SIZE)


    # Update
    for iz in range(len(z[:, 0])):  # for each observation
        #id = z[iz, LM_SIZE]
        id = search_correspond_landmark_id(xEst, PEst, z[iz, 0:LM_SIZE])

        nLM = calc_n_lm(xEst)
        if id == nLM:
            #print("New LM")
            # Extend state and covariance matrix
            xAug = np.vstack((xEst, calc_landmark_position(xEst, z[iz, :])))
            PAug = np.vstack((np.hstack((PEst, np.zeros((len(xEst), LM_SIZE)))),
                              np.hstack((np.zeros((LM_SIZE, len(xEst))), initP))))
            xEst = xAug
            PEst = PAug
        lm = get_landmark_position_from_state(xEst, id)
        y, S, H = calc_innovation(lm, xEst, PEst, z[iz, 0:(LM_SIZE)], int(id))

        K = (PEst @ H.T) @ np.linalg.inv(S)
        xEst = xEst + (K @ y)
        PEst = (np.eye(len(xEst)) - (K @ H)) @ PEst

    xEst[2] = pi_2_pi(xEst[2])

    return xEst, PEst

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


def calc_n_lm(x):
    n = int((len(x) - STATE_SIZE) / LM_SIZE)
    return n

# u -> move with noise x -> state
def jacob_motion(x, u):
    Fx = np.hstack((np.eye(STATE_SIZE), np.zeros(
        (STATE_SIZE, LM_SIZE * calc_n_lm(x)))))

    jF = np.array([[0.0, 0.0, -DT * u[0, 0] * math.sin(x[2, 0])],
                   [0.0, 0.0, DT * u[0, 0] * math.cos(x[2, 0])],
                   [0.0, 0.0, 0.0]], dtype=float)

    G = np.eye(STATE_SIZE) + Fx.T @ jF @ Fx

    return G, Fx,

# zp = [x,y,z]
def calc_landmark_position(x, z):
    zp = np.zeros((LM_SIZE, 1))

    zp[0, 0] = x[0, 0] + z[0] * math.cos(x[2, 0] + z[1])
    zp[1, 0] = x[1, 0] + z[0] * math.sin(x[2, 0] + z[1])
    zp[2, 0] = z[2] # Z coord doesnt change since robot is not moving in Z  

    return zp


def get_landmark_position_from_state(x, ind):
    lm = x[STATE_SIZE + LM_SIZE * int(ind): STATE_SIZE + LM_SIZE * int(ind + 1), :]
    return lm

# lm landmark position [x,y,z] where lm is based on previous observations and z is our new observation
def calc_innovation(lm, xEst, PEst, z, LMid):
    posZ = 0 # robots z coord doesnt change is always 0
    delta = lm - np.matrix([xEst[0,0], xEst[1,0], 0]).T
    q = (delta.T @ delta)[0, 0] # length of delta squared 
    z_angle = math.atan2(delta[1, 0], delta[0, 0]) - xEst[2, 0] # angle between our front and line from as to the landmark
    zp = np.array([[math.sqrt(q), pi_2_pi(z_angle), 0]]) # landmark from our perspective - how should it be based on previous observations
    y = (z - zp).T # difference between our new observation and 
    y[1] = pi_2_pi(y[1])
    H = jacob_h(q, delta, xEst, LMid + 1)
    S = H @ PEst @ H.T +Cx2[0:3,0:3] # Qx

    return y, S, H


def jacob_h(q, delta, x, i):
    sq = math.sqrt(q)
    #print(delta)
    G = np.array(
        [
            [-sq * delta[0, 0]  , - sq * delta[1, 0], 0     , sq * delta[0, 0]  , sq * delta[1, 0], 0],
            [delta[1, 0]        , - delta[0, 0]     , - q   , - delta[1, 0]     , delta[0, 0], 0],
            [0,0,1,0,0, 0]
        ])

    G = G / q
    nLM = calc_n_lm(x)
    F1 = np.hstack((np.eye(STATE_SIZE), np.zeros((LM_SIZE, LM_SIZE * nLM)))) # 3,3+LM_SIZE * nLM
    F2 = np.hstack((np.zeros((LM_SIZE, STATE_SIZE)), np.zeros((LM_SIZE,  LM_SIZE * (i - 1))),
                    np.eye(LM_SIZE), np.zeros((LM_SIZE, LM_SIZE * (nLM -  i))))) # 3 +2+LM_SIZE * (nLM -1)

    F = np.vstack((F1, F2))

    H = G @ F

    return H

def pi_2_pi(angle):
    return (angle + math.pi) % (2 * math.pi) - math.pi


# we assume observations are sorted by index
def new_movement_observations(u):
    # posX = 0 
    # posY = (0.1)*new_movement_observations.iterator # in every move it moves 1 in Y direction
    # posZ = 0
    # posAngle = np.pi/2 
    # # add noise to gps x-y
    # z = np.zeros((0, LM_SIZE+1))

    # # landmarks in our world
    # RFID = np.array([[-1.0, 3.0,0],
    #                  [2.0, 0.5, 0],
    #                  [2.0, 5.0,0]
    #                  ])

    # # we assume robots Z coord never changes
    # for i in range(len(RFID[:, 0])):
    #     dx = RFID[i, 0] - posX
    #     dy = RFID[i, 1] - posY
    #     dz = RFID[i, 2] - posZ 
    #     d = math.hypot(dx, dy)          #real distance
    #     angle = pi_2_pi(math.atan2(dy, dx) - posAngle) #real angle
    #     zi = []
    #     if d <= MAX_RANGE:
    #         # counting noise for landmarks position
    #         dn = d + np.random.randn() * Q_sim[0, 0] ** 0.5  # observed distance (real with noise)
    #         angle_n = angle + np.random.randn() * Q_sim[1, 1] ** 0.5  # observed angle (real with noise)
    #         dzn = dz + np.random.randn() * Q_sim[2, 2] ** 0.5
    #         zi = np.array([dn, angle_n, dz, i])
    #         #zi = np.array([d, angle, dz, i])
    #         z = np.vstack((z, zi))
    
    new_movement_observations.iterator += 1

    #u = np.array([17.35*np.sin(10*2*np.pi/360)*2, - np.pi / 9])
    
    # add noise to movement so its how we think we're moving (info from wheels or sth)
    u_with_noise = np.array([[
        u[0] + np.random.randn() * R_sim[0, 0] ** 0.5,
        u[1] + np.random.randn() * R_sim[1, 1] ** 0.5]]).T

    return u_with_noise, output.output[new_movement_observations.iterator]
new_movement_observations.iterator = 0

import time
def main():
    print(__file__ + " start!!")

    time2 = 0.0

    # State Vector [x y yaw v]'
    xEst = np.zeros((STATE_SIZE, 1)) # Gauss mean
    xEst[2,0]= 0 # np.pi/2 # only for our simulation
    PEst = np.eye(STATE_SIZE)       # covariance
    xTrue = np.zeros((STATE_SIZE, 1)) # real position

    xDR = xEst  # Dead reckoning -> simulated position with noise (without observations)

    # history
    hxEst = xEst
    hxDR = hxEst
    hxTrue = xTrue

    t = 1
    while len(output.output) >= t:
        t += 1
        u = calc_movement()
        xTrue = motion_model(xTrue, u)
        u, z = new_movement_observations(u)

        # predicted position based only on movement
        xDR = motion_model(xDR, u)

        #xEst, PEst = ekf_slam(xEst, PEst, u, z)

        x_state = xEst[0:STATE_SIZE]

        # store data history
        hxEst = np.hstack((hxEst, x_state))
        hxDR = np.hstack((hxDR, xDR))
        hxTrue = np.hstack((hxTrue, xTrue))

        if show_animation:  # pragma: no cover
            plt.cla()
            # for stopping simulation with the esc key.
            plt.gcf().canvas.mpl_connect(
                'key_release_event',
                lambda event: [exit(0) if event.key == 'escape' else None])

            #plt.plot(RFID[:, 0], RFID[:, 1], "*k")
            plt.plot(xEst[0], xEst[1], ".r")

            # plot landmark
            for i in range(calc_n_lm(xEst)):
                plt.plot(xEst[STATE_SIZE + i * LM_SIZE],
                         xEst[STATE_SIZE + i * LM_SIZE + 1], "xg")

            plt.plot(hxDR[0, :],
                     hxDR[1, :], "-k")
            plt.plot(hxEst[0, :],
                     hxEst[1, :], "-r")
            plt.plot(hxTrue[0, :],
                      hxTrue[1, :], "-b")

            plt.axis("equal")
            plt.grid(True)
            plt.pause(1)


if __name__ == '__main__':
    main()