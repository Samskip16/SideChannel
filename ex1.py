import numpy as np
import scipy.io as sio
from bokeh.plotting import figure
from bokeh.io import show


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


def hw(val):
    return bin(val).count("1")


def process_row_correlation(corr_mtrx):
    d = dict()

    for i in range(0, 16):
        row_corr_data = corr_mtrx[i, :]
        correlation = np.max(np.abs(row_corr_data))
        d[correlation] = i

    row_correlation = np.arange(16)
    for i, (key, value) in enumerate(sorted(d.items(), reverse=True)):
        row_correlation[i] = value

    return row_correlation


def plot_row_correlation(row_correlation, max_row, nr_of_traces):
    colors = []
    for i in row_correlation:
        colors.append('red' if i == max_row else 'blue')

    inc_one = lambda x: x + 1
    legend = 'Row correlation per candidate ' + str(nr_of_traces) + ' power traces attack'

    plot = figure(plot_width=900, plot_height=600)
    plot.vbar(x=np.arange(1, 17), top=inc_one(row_correlation), width=0.9, color=colors, legend=legend)
    plot.xaxis.axis_label = 'Candidate ranking'
    plot.yaxis.axis_label = 'Candidate nr.'
    show(plot)


def plot_correlation(corr_mtrx, max_row):
    plot = figure(plot_width=1200, plot_height=800)
    x_values = np.arange(6990)

    for i in range(0, 16):
        y_values = np.absolute(corr_mtrx[i, :])
        color = 'red' if i == max_row else 'blue'

        plot.line(x_values, y_values, color=color, legend='Absolute correlation')

    show(plot)


def attack(nr_of_traces):
    inn = sio.loadmat('in1.mat')['in']
    print(inn.shape)
    traces = sio.loadmat('traces1.mat')['traces'][:nr_of_traces, :]
    print(traces.shape)

    power_mtrx = np.empty((nr_of_traces, 16), dtype=int)

    for i in range(0, nr_of_traces):
        for j in range(0, 16):
            inn_val = inn[i][0]
            power_mtrx[i, j] = hw(s_box(xor(inn_val, j)))

    print(power_mtrx.shape)
    corr_mtrx = np.corrcoef(traces, power_mtrx, rowvar=False)
    corr_mtrx = corr_mtrx[: len(power_mtrx[0]), len(power_mtrx[0]):]

    # corr_mtrx = np.empty((6990, 16), dtype=float)
    # for i in range(0, 6990):
    #     for j in range(0, 16):
    #         temp_corr_mtrx = np.corrcoef(traces[:, i], power_mtrx[:, j], rowvar=False)
    #         corr_mtrx[i, j] = temp_corr_mtrx[0, 1]

    return corr_mtrx


def attack_total():
    corr_mtrx = attack(14900)

    row_correlation = process_row_correlation(corr_mtrx)
    max_row = row_correlation[0]

    plot_correlation(corr_mtrx, max_row)

    return max_row


def attack_nr(nr_of_traces, max_row):
    corr_mtrx = attack(nr_of_traces)

    row_correlation = process_row_correlation(corr_mtrx)
    plot_row_correlation(row_correlation, max_row, nr_of_traces)


max_row = attack_total()

# attack_nr(500, max_row)
# attack_nr(1000, max_row)
# attack_nr(2000, max_row)
# attack_nr(4000, max_row)
# attack_nr(8000, max_row)
# attack_nr(12000, max_row)
# attack_nr(14900, max_row)
