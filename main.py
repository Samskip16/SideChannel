import numpy as np
import scipy.io as sio
import matplotlib.pyplot as plt


def xor(val1, val2):
    return val1 ^ val2


def s_box(val):
    switch = {
        0: 12,
        1: 5,
        2: 6,
        3: 11,
        4: 9,
        5: 0,
        6: 10,
        7: 13,
        8: 3,
        9: 14,
        10: 15,
        11: 8,
        12: 4,
        13: 7,
        14: 1,
        15: 2
    }

    return switch.get(val, 0)


def hw(x):
    return bin(x).count("1")


def attack(nr):
    inn = sio.loadmat('in.mat')['in']

    val_pred = np.empty((nr, 16), dtype=int)
    val_power = np.empty((nr, 16), dtype=int)
    corr_arr = np.empty((6990, 16))
    totals = dict()

    for i in range(0, nr):
        for j in range(0, 16):
            inn_val = inn[i][0]
            val_pred[i, j] = s_box(xor(inn_val, j))

    for i in range(0, nr):
        for j in range(0, 16):
            val = val_pred[i][j]
            val_power[i, j] = hw(val)

    traces = sio.loadmat('traces.mat')['traces'][:nr, :]
    print(traces.shape)

    for i in range(0, 16):
        total = 0
        for j in range(0, 6990):
            cor = abs(np.multiarray.correlate(traces[:, j], val_power[:, i]))
            total += cor

            corr_arr[j][i] = cor

        totals[str(i)] = total

    sorted_t = sorted(totals.items(), key=lambda kv: kv[1])
    best_k = int(sorted_t[15][0])

    print(best_k)

    lines = plt.plot(corr_arr, 'b')
    plt.setp(lines[best_k], color='r')
    plt.show()


attack(2)
