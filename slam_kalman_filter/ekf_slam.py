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

# EKF state covariance
Cx = np.diag([0.5, 0.5, np.deg2rad(30.0)]) ** 2
#Qx = np.diag([0.05, 0.05, 0.5]) ** 2

#  Simulation parameter -> expected noise based on device parameteres?
Q_sim = np.diag([0.2, np.deg2rad(1.0), 0.02]) ** 2
R_sim = np.diag([0.05, np.deg2rad(0.05)]) ** 2

DT = 1  # time tick [s]
SIM_TIME = 50.0  # simulation time [s]
STATE_SIZE = 3  # State size [x,y,yaw]
LM_SIZE = 2  # LM state size [x,y]

show_animation = True

# xEst -> [robot's state,landmarks' state]
def ekf_slam(xEst, PEst, u, z):
    # Predict
    S = STATE_SIZE
    G, Fx = jacob_motion(xEst[0:S], u)  #linearization of movement u-> move with noise 
    xEst[0:S] = motion_model(xEst[0:S], u)
    PEst[0:S, 0:S] = G.T @ PEst[0:S, 0:S] @ G + Fx.T @ Cx @ Fx
    initP = np.eye(LM_SIZE)


    # Update
    if(z.size == 0):
        return xEst, PEst

    for iz in range(len(z[:, 0])):  # for each observation
        id = z[iz, LM_SIZE]

        nLM = calc_n_lm(xEst)
        if id == nLM:
            print("New LM")
            # Extend state and covariance matrix
            xAug = np.vstack((xEst, calc_landmark_position(xEst, z[iz, :])))
            PAug = np.vstack((np.hstack((PEst, np.zeros((len(xEst), LM_SIZE)))),
                              np.hstack((np.zeros((LM_SIZE, len(xEst))), initP))))
            xEst = xAug
            PEst = PAug
        else:
            lm = get_landmark_position_from_state(xEst, id)
            y, S, H = calc_innovation(lm, xEst, PEst, z[iz, 0:(LM_SIZE)], int(id))

            print(y)

            K  = (PEst @ H.T) @ np.linalg.inv(S)
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
    #zp[2, 0] = z[2] # Z coord doesnt change since robot is not moving in Z  

    return zp


def get_landmark_position_from_state(x, ind):
    lm = x[STATE_SIZE + LM_SIZE * int(ind): STATE_SIZE + LM_SIZE * int(ind + 1), :]
    return lm

# lm landmark position [x,y,z] where lm is based on previous observations and z is our new observation
def calc_innovation(lm, xEst, PEst, z, LMid):
    posZ = 0 # robots z coord doesnt change is always 0
    delta = lm - xEst[0:2]
    q = (delta.T @ delta)[0, 0] # length of delta squared 
    z_angle = math.atan2(delta[1, 0], delta[0, 0]) - xEst[2, 0] # angle between our front and line from as to the landmark
    zp = np.array([[math.sqrt(q), pi_2_pi(z_angle)]]) # landmark from our perspective - how should it be based on previous observations
    y = (z - zp).T # difference between our new observation and 
    y[1] = pi_2_pi(y[1])
    H = jacob_h(q, delta, xEst, LMid + 1)
    S = H @ PEst @ H.T +Cx[0:2,0:2] # Qx

    return y, S, H


def jacob_h(q, delta, x, i):
    sq = math.sqrt(q)
    G = np.array([[-sq * delta[0, 0], - sq * delta[1, 0], 0, sq * delta[0, 0], sq * delta[1, 0]],
               [delta[1, 0], - delta[0, 0], - q, - delta[1, 0], delta[0, 0]],])

    G = G / q
    nLM = calc_n_lm(x)
    F1 = np.hstack((np.eye(STATE_SIZE), np.zeros((3, LM_SIZE * nLM)))) # 3,3+LM_SIZE * nLM
    F2 = np.hstack((np.zeros((LM_SIZE, STATE_SIZE)), np.zeros((LM_SIZE,  LM_SIZE * (i - 1))),
                    np.eye(LM_SIZE), np.zeros((LM_SIZE, LM_SIZE * (nLM -  i))))) # 3 +2+LM_SIZE * (nLM -1)

    F = np.vstack((F1, F2))

    H = G @ F

    return H

def pi_2_pi(angle):
    return (angle + math.pi) % (2 * math.pi) - math.pi

# to enforce the correccntess of the indexes of the landmarks.
mapping_landmarks_to_indexes = {}

# returns distance, angle and index of the ladnmark
def tuple_to_list(t):
    if t[0] not in mapping_landmarks_to_indexes:
        mapping_landmarks_to_indexes[t[0]] = len(mapping_landmarks_to_indexes)
        # [distance, angle, index]
    return [t[1][1], t[1][0], mapping_landmarks_to_indexes[t[0]]] 

def diagonal_length(x, y):
    return math.sqrt(x**2 + y**2)

# getting observations from the image processing
current_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_path + "/../" + "image_processing/landmarks/")

import generated3dPoints as points
observations = points.points4
for i in range(len(observations)):
    observations[i] = list(filter(lambda point: point[0] in [50] , observations[i]))
real_movement = np.array([[diagonal_length(points.XMOVEMENT, points.ZMOVEMENT) ,points.ROTATION]])

SIM_TIME = len(observations) - 1

# generator for observations and movement possible with noise 
def new_movement_observations():
    if new_movement_observations.iterator >= len(observations):
        return None, None
    new_movement_observations.iterator += 1

    u = real_movement[0]

    
    # add noise to movement so its how we think we're moving (info from wheels or sth)
    u_with_noise = np.array([[
        u[0] + np.random.randn() * R_sim[0, 0] ** 0.5,
        u[1] + np.random.randn() * R_sim[1, 1] ** 0.5]]).T

    observation_current = observations[new_movement_observations.iterator - 1]
    obs = np.array(list(map(tuple_to_list, observation_current)))
    return real_movement.T, obs
new_movement_observations.iterator = 0

def main():
    print("\n" + __file__ + " start!!")

    time = 0.0

    # State Vector [x y yaw v]'
    xEst = np.zeros((STATE_SIZE, 1)) # Gauss mean
    xTrue = np.zeros((STATE_SIZE, 1)) # real position
    PEst = np.eye(STATE_SIZE)       # covariance

    xDR = np.zeros((STATE_SIZE, 1))  # Dead reckoning -> simulated position with noise (without observations)

    # history
    hxEst = np.zeros((STATE_SIZE, 1))
    hxTrue = np.zeros((STATE_SIZE, 1))
    hxDR = np.zeros((STATE_SIZE, 1))

    while SIM_TIME >= time:
        time += DT
        u, z = new_movement_observations()

        xTrue = motion_model(xTrue, real_movement.T) # real position based on real movement
        
        # predicted position based only on movement with noise
        xDR = motion_model(xDR, u)

        xEst, PEst = ekf_slam(xEst, PEst, u, z)

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

            plt.plot(xEst[0], xEst[1], ".r")

            # plot landmark
            for i in range(calc_n_lm(xEst)):
                plt.plot(xEst[STATE_SIZE + i * LM_SIZE],
                         xEst[STATE_SIZE + i * LM_SIZE + 1], "xg")

            #print(hxTrue)
            #print(hxDR)
            #print(hxEst)

            plt.plot(hxTrue[0, :],
                     hxTrue[1, :], "-b")
            plt.plot(hxDR[0, :],
                     hxDR[1, :], "-k")
            plt.plot(hxEst[0, :],
                     hxEst[1, :], "-r")
            plt.axis("equal")
            plt.grid(True)
            plt.pause(5)


if __name__ == '__main__':
    main()