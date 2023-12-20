import csv
import datetime
import os
import sys
from tab4_theory import Ui_Form

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import qdarkstyle
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTableWidget, QHBoxLayout, QLabel, QAbstractItemView, \
    QMessageBox, QAction, QTabWidget, QVBoxLayout, QFormLayout, QTableWidgetItem, QFileDialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import data
from broser import WebBroser

NOW = datetime.datetime.now()
ABOUT_TEXT = (
        """
Graphical User Interface for In-plane Permeability Calculator
Copyright %d

Developped by Bin Yang,

Email: bin.yang@polymtl.ca

Blog: https://www.binyang.fun/
"""
        % NOW.year
)


class MyTable(QTableWidget):
    def __init__(self, r, c):
        """
        Table constructor.

        Parameters
        ----------
        r : int
            Number of rows
        c : int
            Number of columns
        """
        super().__init__(r, c)
        self.check_change = True
        # allow user to paste data
        self.setEditTriggers(QAbstractItemView.AllEditTriggers)
        # allow user to select multiple rows
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setColumnWidth(0, 90)
        self.setColumnWidth(1, 130)
        self.init_ui()

    def init_ui(self):
        self.cellChanged.connect(self.c_current)
        # self.show()

    def c_current(self):
        if self.check_change:
            row = self.currentRow()
            col = self.currentColumn()
            value = self.item(row, col)
            value = value.text()
            # print("The current cell is ", row, ", ", col)
            # print("In this cell we have: ", value)

    def open_sheet(self, c, skip=0):
        """
        Open a spreadsheet, and populate the table with the data from the spreadsheet.

        Parameters
        ----------
        c : int
            Number of columns
        """
        self.check_change = False
        path = QFileDialog.getOpenFileName(self, 'Open CSV', os.getenv('HOME'), 'CSV(*.csv)')
        if path[0] != '':
            with open(path[0], newline='') as csv_file:
                self.setRowCount(0)
                self.setColumnCount(c)
                my_file = csv.reader(csv_file, delimiter=',', quotechar='|')
                for i in range(skip):
                    next(my_file, None)
                for row_data in my_file:
                    row = self.rowCount()
                    self.insertRow(row)
                    if len(row_data) > c:
                        self.setColumnCount(len(row_data - skip))
                    for column, stuff in enumerate(row_data):
                        item = QTableWidgetItem(stuff)
                        self.setItem(row, column, item)

            self.check_change = True


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.visco = None
        self.pressure = None
        self.porosity = None

        self.window_width, self.window_height = 1024, 768
        self.setMinimumSize(self.window_width, self.window_height)

        self.resize(1280, 800)
        self.dark_mode = False

        self.setWindowTitle("My App")

        self.make_menu()

        self.tabs = QTabWidget()
        self.tabs.setTabPosition(
            QTabWidget.West)  # QTabWidget.North, QTabWidget.South, QTabWidget.East, QTabWidget.West

        self.tab1 = QWidget()

        """ tab2 Experiment data processing """
        self.tab2 = QWidget()
        """ tab2 left-hand side: Data table """
        # Add a table widget, and set it as the central widget of the window
        self.table_header = QLabel("Experimental Data")
        self.table_header.sizePolicy().setHorizontalStretch(1)
        self.table_header.setFont(QFont("Times", 18, QFont.Bold))
        self.table_header.setAlignment(QtCore.Qt.AlignCenter)

        self.table = MyTable(20, 2)
        self.table.setHorizontalHeaderLabels(["Time (s)", "Flow Front (m)"])
        self.table.resize(self.table.sizeHint())

        self.widget = QWidget()
        # self.widget.setGeometry(QtCore.QRect(32, 562, 244, 74))
        self.widget.setObjectName("widget")

        self.formLayout = QFormLayout()
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")

        self.line_pressure = QtWidgets.QLineEdit(self.widget)
        self.line_pressure.setObjectName("line_pressure")
        self.formLayout.addRow("Pressure (Pa)", self.line_pressure)

        self.line_visco = QtWidgets.QLineEdit(self.widget)
        self.line_visco.setObjectName("line_visco")
        self.formLayout.addRow("Viscosity (Pa·s)", self.line_visco)

        self.line_porosity = QtWidgets.QLineEdit(self.widget)
        self.line_porosity.setObjectName("line_porosity")
        self.formLayout.addRow("Porosity", self.line_porosity)

        self.button_more = QtWidgets.QPushButton(self.widget)
        self.button_more.setObjectName("button_more")
        self.button_more.setText("More Information")
        # error message box when the user clicks the button
        self.button_more.clicked.connect(lambda: self._error_dialog("Not implemented yet", "More Information"))
        self.layout_table = QVBoxLayout()
        self.layout_table.addWidget(self.table_header)
        self.layout_table.addWidget(self.table)
        self.layout_table.addLayout(self.formLayout)
        self.layout_table.addWidget(self.button_more)

        self.button_calculate = QtWidgets.QPushButton(self.widget)
        self.button_calculate.setObjectName("button_calculate")
        self.button_calculate.setText("Calculate")
        self.button_calculate.clicked.connect(self.physical_property)
        self.layout_table.addWidget(self.button_calculate)

        """ tab2 right-hand side: Plotting and Calculation """
        self.label = QLabel("Plotting and Calculation")
        self.label.setFont(QFont("Times", 20, QFont.Bold))
        self.label.sizePolicy().setHorizontalStretch(1)
        self.label.setAlignment(QtCore.Qt.AlignCenter)

        self._plot_holder()  # create self.canvas, self.ax1, self.ax1_twin, and self.ax2

        self.layout_plot = QVBoxLayout()
        self.layout_plot.addWidget(self.label)
        self.layout_plot.addWidget(self.canvas)

        self.layout = QHBoxLayout()
        self.layout.addLayout(self.layout_table)
        self.layout.addLayout(self.layout_plot)
        self.tab2.setLayout(self.layout)

        """ tab3: Transverse permeability calculation """
        self.tab3 = QWidget()
        # TODO : add a text browser to display the theory:
        #  offline but add a link to the online documentation
        #  [Creating a simple browser using PyQt5]
        #  (https://www.geeksforgeeks.org/creating-a-simple-browser-using-pyqt5/)
        
        """ tab4: Theory for permeability calculation """
        self.tab4 = QWidget()
        self.tab4.ui = Ui_Form()
        self.tab4.ui.setupUi(self.tab4)

        # connect the buttons to the web browser with the corresponding url
        self.tab4.ui.pushButton_2.clicked.connect(lambda: self._show_web_browser("https://www.binyang.fun/"))
        self.tab4.ui.pushButton_4.clicked.connect(lambda: self._show_web_browser("https://www.binyang.fun/"))
        self.tab4.ui.pushButton_6.clicked.connect(lambda: self._show_web_browser("https://www.binyang.fun/"))

        """ Add tabs to main window """
        self.tabs.addTab(self.tab1, "Acquisition")
        self.tabs.addTab(self.tab2, "In-plane")
        self.tabs.addTab(self.tab3, "Transverse")
        self.tabs.addTab(self.tab4, "Theory")
        self.tabs.setCurrentIndex(1)  # default tab

        self.setCentralWidget(self.tabs)

    def make_menu(self):
        """Generates menus"""
        self.menu = self.menuBar()  # PyQt5.QtWidgets.QMenuBar
        self.menu.setNativeMenuBar(True)  # PyQt5.QtWidgets.QMenuBar.setNativeMenuBar

        # main menu
        self.file_menu = self._build_file_menu()
        self.view_menu = self._build_view_menu()
        self.help_menu = self._build_help_menu()

    def _build_file_menu(self):
        """
        Creates file menu and adds items.

        Returns
        -------
        menu : PyQt5.QtWidgets.QMenu
            File menu object with items added. This is stored in self.file_menu
        """
        menu = self.menu.addMenu("File")

        self.add_menu_item(menu, "Load", self.load, shortcut="Ctrl+O")
        self.add_menu_item(menu, "Save", self.save, shortcut="Ctrl+S")
        self.add_menu_item(menu, "Clear", self.clear, shortcut="Ctrl+Shift+C")
        # self.add_menu_item(menu, "Save Screenshot", self.plotter.screenshot, shortcut="Alt+S")
        # self.add_menu_item(menu, "Clear Scene", self.plotter.clear, shortcut="Ctrl+Shift+C")
        self.add_menu_item(menu, "Close", self.close, shortcut="Ctrl+Q")

        return menu

    def add_menu_item(self, menu, text, func, addsep=False, enabled=True, shortcut=None):
        """
        Clean way of adding menu items

        Parameters
        ----------
        menu : PyQt5.QtWidgets.QMenu
            Menu to add item to
        text : str
            Text to display
        func : function
            A function to call when item is clicked
        addsep : bool, optional
            Add a separator before the item
        enabled : bool, optional
            Enable the item
        shortcut : str, optional
            Shortcut to add to the item
        """
        item = QAction(text, self)
        if func:
            item.triggered.connect(func)

        if addsep:
            menu.insertSeparator(menu.addAction(item))
        else:
            menu.addAction(item)

        if enabled:
            item.setEnabled(True)
        else:
            item.setEnabled(False)

        if shortcut is not None:
            item.setShortcut(shortcut)

        return item

    def _build_view_menu(self):
        """Creates view menu"""
        menu = self.menu.addMenu("View")
        self.add_menu_item(menu, "Dark Mode", self.dark_mode_on_off)

        return menu

    def load(self):
        """Loads a mesh from file using a file dialog"""
        # Check the current tab
        current_tab = self.tabs.currentIndex()
        print(current_tab)
        if current_tab == 0:  # Acquisition
            self.table.open_sheet(2)
        elif current_tab == 1: # In-plane permeability 
            self.table.open_sheet(2)
        elif current_tab == 2:  # Transverse permeability
            self.table.open_sheet(2)
        elif current_tab == 3:  # Theory
            # disable the load button
            self._error_dialog("No data is required for this tab, thanks.", "No data required")

    def save(self):
        """Saves a mesh to file using a file dialog"""
        self._error_dialog("Not implemented yet", "Save mesh")

    def clear(self):
        """ Clear all the data in the table"""
        self.table.clearContents()
        self.message_box = QMessageBox(self)
        self.message_box.setWindowTitle("Clear")
        self.message_box.setIcon(QMessageBox.Information)
        self.message_box.setText("All the data in the table has been cleared.")
        self.message_box.show()

        # clear the plot
        self.canvas.ax1.clear()
        self.canvas.ax1_twin.clear()
        self.canvas.ax2.clear()
        self.canvas.draw()

        # clear the line edit
        self.line_visco.clear()
        self.line_pressure.clear()
        self.line_porosity.clear()

    def _plot_holder(self):
        font = {'family': 'Times New Roman',
                'weight': 'normal',
                'size': 10,
                }
        plt.rc('font', **font)
        matplotlib.rcParams['mathtext.fontset'] = 'stix'

        # define figure size according to the screen size
        self.canvas = FigureCanvas(Figure(figsize=(5.5, 6.5), dpi=150))
        self.canvas.ax1 = self.canvas.figure.add_subplot(211)
        self.canvas.ax1.set_title("Time (s) (m) VS Flow Front Position")
        self.canvas.ax1.tick_params(axis='both', which='both', direction='in')

        self.canvas.ax1_twin = self.canvas.ax1.twinx()
        self.canvas.ax1_twin.tick_params(axis='both', which='both', direction='in')

        self.canvas.ax2 = self.canvas.figure.add_subplot(212)
        self.canvas.ax2.set_title("Time (s) VS Permeability (m$^2$)")
        self.canvas.ax2.tick_params(axis='both', which='both', direction='in')

        self.canvas.figure.subplots_adjust(left=0.10, bottom=0.1, right=0.90, top=0.95, wspace=0.2, hspace=0.4)

    def _show_web_browser(self, url="https://www.binyang.fun/"):
        self.browser = WebBroser(url)
        self.browser.show()

    def _build_help_menu(self):
        """Creates help menu"""
        menu = self.menu.addMenu("Help")
        self.add_menu_item(menu, "About", self.about)
        self.add_menu_item(menu, "Online Resources", self.online_docs)
        return menu

    def about(self):
        """About the software and the developer"""
        QMessageBox.about(self, "About", ABOUT_TEXT)

    def online_docs(self):
        """Open online documentation at www.binyang.fun/polykriging/"""
        import webbrowser
        webbrowser.open("https://www.binyang.fun/")

    def dark_mode_on_off(self):
        if self.dark_mode is False:
            """Turns on dark mode"""
            self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
            self.dark_mode = True

        else:
            """Turns off dark mode"""
            self.setStyleSheet("")
            self.dark_mode = False

    def readTableData(self):
        rowCounts = self.table.rowCount()
        columnCounts = self.table.columnCount()

        data = []
        for i in range(rowCounts):
            temp = []
            for j in range(columnCounts):
                if self.table.item(i, j) is not None and self.table.item(i, j).text() != "":
                    temp.append(self.table.item(i, j).text())
                else:
                    temp.append(0)

            data.append(temp)

        data = np.array(data, dtype=float)

        return data

    def physical_property(self):
        # check if the data is numeric
        if data.check_numeric(self.line_visco.text()):
            self.visco = float(self.line_visco.text())
        else:
            # error message box when the user clicks the button
            self._error_dialog("Viscosity must be a number", "Viscosity Error")

        if data.check_numeric(self.line_pressure.text()):
            self.pressure = float(self.line_pressure.text())
        else:
            self._error_dialog("Pressure must be a number", "Pressure Error")

        if data.check_numeric(self.line_porosity.text()):
            self.porosity = float(self.line_porosity.text())
        else:
            self._error_dialog("Porosity must be a number between 0 and 1", "Porosity Error")

        return self.visco, self.pressure, self.porosity

    def _error_dialog(self, txt, textinfo=None):
        """
        Creates error dialogue

        Parameters
        ----------
        txt : str
            Error message
        textinfo : str, optional
            Additional text to display
        """
        self.err_message_box = QMessageBox(self)
        self.err_message_box.setWindowTitle("Error")
        self.err_message_box.setIcon(QMessageBox.Critical)
        self.err_message_box.setText(txt)

        if textinfo:
            # Need when we want to add more information to the error message
            self.err_message_box.setInformativeText(textinfo)

        self.err_message_box.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = MainWindow()
    demo.show()
    sys.exit(app.exec_())
