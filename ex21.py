import numpy as np
import scipy.io as sio
from bokeh.plotting import figure
from bokeh.io import show


def xor(val1, val2):
    return val1 ^ val2


def hw(val):
    return bin(val).count("1")


def hd(val1, val2):
    return hw(xor(val1, val2))


def process_row_correlation(corr_mtrx):
    d = dict()

    for i in range(0, 256):
        row_corr_data = corr_mtrx[i, :]
        correlation = np.max(np.abs(row_corr_data))
        d[correlation] = i

    row_correlation = np.arange(256)
    for i, (key, value) in enumerate(sorted(d.items(), reverse=True)):
        row_correlation[i] = value

    return row_correlation


def plot_row_correlation(row_correlation, max_row):
    colors = []
    for i in row_correlation:
        colors.append('red' if i == max_row else 'blue')

    inc_one = lambda x: x + 1
    legend = 'Row correlation per candidate ' + str(10000) + ' power traces attack'

    plot = figure(plot_width=900, plot_height=600)
    plot.vbar(x=np.arange(1, 257), top=inc_one(row_correlation), width=0.9, color=colors, legend=legend)
    plot.xaxis.axis_label = 'Candidate ranking'
    plot.yaxis.axis_label = 'Candidate nr.'
    show(plot)


def plot_correlation(corr_mtrx, max_row):
    plot = figure(plot_width=1200, plot_height=800)
    x_values = np.arange(2000)

    for i in range(0, 16):
        y_values = np.absolute(corr_mtrx[i, :])
        color = 'red' if i == max_row else 'blue'

        plot.line(x_values, y_values, color=color, legend='Absolute correlation')

    show(plot)


sbox_vals = (
    0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38, 0xBF, 0x40, 0xA3, 0x9E, 0x81, 0xF3, 0xD7, 0xFB,
    0x7C, 0xE3, 0x39, 0x82, 0x9B, 0x2F, 0xFF, 0x87, 0x34, 0x8E, 0x43, 0x44, 0xC4, 0xDE, 0xE9, 0xCB,
    0x54, 0x7B, 0x94, 0x32, 0xA6, 0xC2, 0x23, 0x3D, 0xEE, 0x4C, 0x95, 0x0B, 0x42, 0xFA, 0xC3, 0x4E,
    0x08, 0x2E, 0xA1, 0x66, 0x28, 0xD9, 0x24, 0xB2, 0x76, 0x5B, 0xA2, 0x49, 0x6D, 0x8B, 0xD1, 0x25,
    0x72, 0xF8, 0xF6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xD4, 0xA4, 0x5C, 0xCC, 0x5D, 0x65, 0xB6, 0x92,
    0x6C, 0x70, 0x48, 0x50, 0xFD, 0xED, 0xB9, 0xDA, 0x5E, 0x15, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84,
    0x90, 0xD8, 0xAB, 0x00, 0x8C, 0xBC, 0xD3, 0x0A, 0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x45, 0x06,
    0xD0, 0x2C, 0x1E, 0x8F, 0xCA, 0x3F, 0x0F, 0x02, 0xC1, 0xAF, 0xBD, 0x03, 0x01, 0x13, 0x8A, 0x6B,
    0x3A, 0x91, 0x11, 0x41, 0x4F, 0x67, 0xDC, 0xEA, 0x97, 0xF2, 0xCF, 0xCE, 0xF0, 0xB4, 0xE6, 0x73,
    0x96, 0xAC, 0x74, 0x22, 0xE7, 0xAD, 0x35, 0x85, 0xE2, 0xF9, 0x37, 0xE8, 0x1C, 0x75, 0xDF, 0x6E,
    0x47, 0xF1, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89, 0x6F, 0xB7, 0x62, 0x0E, 0xAA, 0x18, 0xBE, 0x1B,
    0xFC, 0x56, 0x3E, 0x4B, 0xC6, 0xD2, 0x79, 0x20, 0x9A, 0xDB, 0xC0, 0xFE, 0x78, 0xCD, 0x5A, 0xF4,
    0x1F, 0xDD, 0xA8, 0x33, 0x88, 0x07, 0xC7, 0x31, 0xB1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xEC, 0x5F,
    0x60, 0x51, 0x7F, 0xA9, 0x19, 0xB5, 0x4A, 0x0D, 0x2D, 0xE5, 0x7A, 0x9F, 0x93, 0xC9, 0x9C, 0xEF,
    0xA0, 0xE0, 0x3B, 0x4D, 0xAE, 0x2A, 0xF5, 0xB0, 0xC8, 0xEB, 0xBB, 0x3C, 0x83, 0x53, 0x99, 0x61,
    0x17, 0x2B, 0x04, 0x7E, 0xBA, 0x77, 0xD6, 0x26, 0xE1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0C, 0x7D
)

inv_sbox = np.array(sbox_vals)

hardware_traces = sio.loadmat('hardware_traces.mat')['traces']
output_data = sio.loadmat('output_data.mat')['output_data']

power_mtrx = np.empty((10000, 256), dtype=int)

for out in np.arange(0, 10000):
    for key in np.arange(0, 256):
        output = output_data[out][0]
        register_val2 = xor(output, key)
        register_val1 = inv_sbox[register_val2]

        power_mtrx[out, key] = hd(register_val2, register_val1)

corr_mtrx = np.corrcoef(hardware_traces, power_mtrx, rowvar=False)
corr_mtrx = corr_mtrx[: len(power_mtrx[0]), len(power_mtrx[0]):]

row_correlation = process_row_correlation(corr_mtrx)
max_row = row_correlation[0]
print(max_row)

plot_correlation(corr_mtrx, max_row)
plot_row_correlation(row_correlation, max_row)
