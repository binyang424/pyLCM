import data
import sys

import numpy as np
from PyQt5.QtWidgets import QApplication

from gui import MainWindow
from permeability import perm_1d
from PyQt5.QtWebEngineWidgets import *
import qdarkstyle


class InPlanePermeability(MainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TexPermeability (Bin Yang, bin.yang@polymtl.ca)")

        self.button_calculate.clicked.connect(self.update_graph)

    def update_graph(self):
        plot_data = self.readTableData()
        mask = plot_data[:, 0] == 0
        mask[0] = False
        plot_data = plot_data[~mask, :]  # if a row is 0, then the data is not valid
        self.physical_property()

        perm_t = [perm_1d(plot_data[:i, 1], plot_data[:i, 0], 1 - self.porosity,
                          self.pressure, self.visco, plot=False) for i in range(2, len(plot_data[:, 1]))]
        # skip the first two data points for successful fitting

        self.canvas.ax1.clear()
        # remove the twin axis
        if hasattr(self.canvas, 'ax1_twin'):
            self.canvas.ax1_twin.remove()

        self.canvas.ax1.plot(plot_data[:, 0], plot_data[:, 1])
        self.canvas.ax1.set_title("Time (s) VS Flow Front Position $x_f$ (m)")
        self.canvas.ax1.tick_params(axis='both', which='both', direction='in')

        self.canvas.ax1_twin = self.canvas.ax1.twinx()
        self.canvas.ax1_twin.scatter(plot_data[:, 0], np.square(plot_data[:, 1]), color='r', marker='x', s=8)

        fit_coefficients = np.polyfit(plot_data[:, 0], np.square(plot_data[:, 1]), 1)
        # r-square
        r_sq = np.corrcoef(plot_data[:, 0], np.square(plot_data[:, 1]))[0, 1] ** 2
        equation = np.poly1d(fit_coefficients)  # retrieve the equation
        self.canvas.ax1_twin.text(np.mean(plot_data[:, 0]) * 1.5, np.mean(np.square(plot_data[:, 1])) * 0.5,
                                  'y={} \n\n $R^2$={}'.format(str(equation)[2:], round(r_sq, 3)), color='r',
                                  fontsize=10)
        self.canvas.ax1_twin.plot(plot_data[:, 0], np.polyval(fit_coefficients, plot_data[:, 0]), color='r',
                                  label="$x_f^2$ (right axis)")
        self.canvas.ax1.legend(loc="upper left", fontsize=8, frameon=False)
        self.canvas.ax1_twin.legend(loc="lower right", fontsize=8, frameon=False)
        self.canvas.ax1_twin.tick_params(axis='y', which='both', direction='in')
        # y tick labels of the twin axis in red
        for label in self.canvas.ax1_twin.get_yticklabels():
            label.set_color("r")

        self.canvas.ax2.clear()
        self.canvas.ax2.plot(plot_data[2:, 0], perm_t)
        self.canvas.ax2.scatter(plot_data[-1, 0], perm_t[-1], color='r', marker='x', s=12)
        self.canvas.ax2.text(plot_data[-1, 0] * 0.8, perm_t[-1] * 0.65,
                             data.as_si(perm_t[-1], 2) + " m$^2$", color='r', fontsize=10)
        self.canvas.ax2.annotate("", xy=(plot_data[-1, 0], perm_t[-1] * 0.9),
                                 xytext=(plot_data[-1, 0] * 0.9, perm_t[-1] * 0.73),
                                 arrowprops=dict(arrowstyle="->", color='r'))

        self.canvas.ax2.set_title("Time (s) VS Permeability (m$^2$)")
        self.canvas.ax2.tick_params(axis='both', which='both', direction='in')

        self.canvas.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = InPlanePermeability()
    demo.show()
    sys.exit(app.exec_())
