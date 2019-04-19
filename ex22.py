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


def multiply_all(arr):
    result = []

    for i in range(0, len(arr)):
        for j in range(i + 1, len(arr)):
            result.append(arr[i] * arr[j])

    return result


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


def plot_row_correlation(row_correlation, max_row):
    colors = []
    for i in row_correlation:
        colors.append('red' if i == max_row else 'blue')

    inc_one = lambda x: x + 1
    legend = 'Row correlation per candidate power traces attack'

    plot = figure(plot_width=900, plot_height=600)
    plot.vbar(x=np.arange(1, 257), top=inc_one(row_correlation), width=0.9, color=colors, legend=legend)
    plot.xaxis.axis_label = 'Candidate ranking'
    plot.yaxis.axis_label = 'Candidate nr.'
    show(plot)


def plot_correlation(corr_mtrx, max_row):
    plot = figure(plot_width=1200, plot_height=800)
    x_values = np.arange(45)

    for i in range(0, 16):
        y_values = np.absolute(corr_mtrx[i, :])
        color = 'red' if i == max_row else 'blue'

        plot.line(x_values, y_values, color=color, legend='Absolute correlation')

    show(plot)


input = sio.loadmat('input.mat')['input']
leakage_y0_y1 = sio.loadmat('leakage_y0_y1.mat')['L']

proc_mtrx = np.empty((2000, 45), dtype=float)
pred_mtrx = np.empty((2000, 16), dtype=int)

for i in range(0, 2000):
    val = leakage_y0_y1[i]
    proc_mtrx[i] = multiply_all(val)

for i in range(0, 2000):
    for k in range(0, 16):
        val = s_box(xor(i, k))
        pred_mtrx[i][k] = val

corr_mtrx = np.corrcoef(proc_mtrx, pred_mtrx, rowvar=False)
corr_mtrx = corr_mtrx[: len(pred_mtrx[0]), len(pred_mtrx[0]):]

row_correlation = process_row_correlation(corr_mtrx)
max_row = row_correlation[0]
print(max_row)

plot_row_correlation(row_correlation, max_row)
plot_correlation(corr_mtrx, max_row)
