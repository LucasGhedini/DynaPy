import sys
import numpy as np
from DynaPy import *
from GUI.stepbystepGUI import Ui_MainWindow
from GUI.textBrowserGUI import Ui_MainWindow as textBrowserGUI
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib import pyplot as plt

class TextBrowser(QMainWindow, textBrowserGUI):

    def __init__(self, parent=None, inputData=None, outputData=None):
        super(TextBrowser, self).__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QIcon('img/icon_64.ico'))
        self.inputData = inputData
        self.outputData = outputData
        self.show()

class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None, inputData=None, outputData=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QIcon('img/icon_64.ico'))
        self.inputData = inputData
        self.outputData = outputData
        self.setup_inputs()
        self.setup_equation()
        self.setup_outputs()
        self.showMaximized()


    def setup_inputs(self):
        # Structure Canvas
        # self.splitter.setSizes([400, 400])
        self.SBSstructureWidget.structureCanvas = StructureCanvas(self.SBSstructureWidget)
        self.SBSstructureWidget.grid = QGridLayout()
        self.SBSstructureWidget.grid.addWidget(self.SBSstructureWidget.structureCanvas, 1, 1)
        self.SBSstructureWidget.setLayout(self.SBSstructureWidget.grid)

        # TLCD Canvas
        self.SBSTLCDWidget.tlcdCanvas = TLCDCanvas(self.SBSTLCDWidget)
        self.SBSTLCDWidget.grid = QGridLayout()
        self.SBSTLCDWidget.grid.addWidget(self.SBSTLCDWidget.tlcdCanvas, 1, 1)
        self.SBSTLCDWidget.setLayout(self.SBSTLCDWidget.grid)

        # Excitation Canvas
        self.SBSexcitationWidget
        self.SBSexcitationWidget.excitationCanvas = PltCanvas()
        self.SBSexcitationWidget.mpl_toolbar = NavigationToolbar(self.SBSexcitationWidget.excitationCanvas, self)
        self.SBSexcitationWidget.gridLabel = QLabel('Show Grid', self)
        self.SBSexcitationWidget.gridChkBox = QCheckBox(self)
        self.SBSexcitationWidget.gridChkBox.stateChanged.connect(self.excitation_grid_toggle)

        self.SBSexcitationWidget.gridLayout = QGridLayout()
        self.SBSexcitationWidget.gridLayout.addWidget(self.SBSexcitationWidget.excitationCanvas, 1, 1, 1, 3)
        self.SBSexcitationWidget.gridLayout.addWidget(self.SBSexcitationWidget.gridLabel, 2, 1)
        self.SBSexcitationWidget.gridLayout.addWidget(self.SBSexcitationWidget.gridChkBox, 2, 2)
        self.SBSexcitationWidget.gridLayout.addWidget(self.SBSexcitationWidget.mpl_toolbar, 2, 3)

        self.SBSexcitationWidget.setLayout(self.SBSexcitationWidget.gridLayout)

        # Connect Buttons
        self.refreshbtn.clicked.connect(self.refresh)
        self.StructDetailBtn.clicked.connect(self.structure_input_details)
        self.TLCDdetailBtn.clicked.connect(self.tlcd_input_details)

    def setup_equation(self):
        # Equation Graphics add figure
        pixmap = QPixmap(r'./img/equations.png')
        self.equationFigureLabel.setGeometry(400, 400, 0, 0)
        self.equationFigureLabel.setPixmap(pixmap)

        # Equation Canvas
        self.equationWidget.equationCanvas = PltCanvas()
        self.equationWidget.gridLayout = QGridLayout()
        self.equationWidget.gridLayout.addWidget(self.equationWidget.equationCanvas, 1, 1)
        self.equationWidget.setLayout(self.equationWidget.gridLayout)
        self.equationWidget.equationCanvas.fig.clf()

        # Connection
        self.equationLineComboBox.currentIndexChanged.connect(self.plot_equation)
        self.equationTypeComboBox.currentIndexChanged.connect(self.plot_equation)

        # Get number of DOFs and TLCD
        lines = len(self.inputData.stories)
        hasTLCD = self.inputData.tlcd is not None
        if hasTLCD:
            lines += 1

        # Add lines to combobox
        for i in range(lines):
            self.equationLineComboBox.addItem(f'{i+1}')

        # First plot
        self.plot_equation()

    def plot_equation(self):
        ids = self.inputData.stories
        idf = self.inputData.tlcd
        lines = len(self.inputData.stories)
        type = get_text(self.equationTypeComboBox)
        hasTLCD = self.inputData.tlcd is not None
        if hasTLCD:
            lines += 1
        t = ''
        n = int(get_text(self.equationLineComboBox))
        
        if type == "Symbolic":
            if n == 1:
                t += f'$m_{{s{n}}}\ddot{{x}}_{{s{n}}}'
                t += f'+c_{{s{n}}}\dot{{x}}_{{s{n}}}'
                t += f'+(k_{{s{n}}}+k_{{s{n+1}}})x_{{s{n}}}'
                t += f'-k_{{s{n+1}}}x_{{s{n+1}}}'
                t += f'=F_{{q{n}}}(t)$'
            elif (hasTLCD and n < lines-1) or ((not hasTLCD) and n < lines):
                t += f'$m_{{s{n}}}\ddot{{x}}_{{s{n}}}'
                t += f'+c_{{s{n}}}\dot{{x}}_{{s{n}}}'
                t += f'-k_{{s{n}}}x_{{s{n-1}}}'
                t += f'+(k_{{s{n}}}+k_{{s{n+1}}})x_{{s{n}}}'
                t += f'-k_{{s{n+1}}}x_{{s{n+1}}}'
                t += f'=F_{{q{n}}}(t)$'
            elif hasTLCD and n == lines-1:
                t += f'$(m_{{s{n}}}+m_{{f}})\ddot{{x}}_{{s{n}}} + \\frac{{b}}{{L}}m_{{f}}\ddot{{x}}_{{f}}'
                t += f'+c_{{s{n}}}\dot{{x}}_{{s{n}}}'
                t += f'-k_{{s{n}}}x_{{s{n-1}}}'
                t += f'+k_{{s{n}}}x_{{s{n}}}'
                t += f'=F_{{q{n}}}(t)$'
            elif hasTLCD and n == lines:
                t += f'$\\frac{{b}}{{L}}m_{{f}}\ddot{{x}}_{{s{n-1}}} + m_{{f}}\ddot{{x}}_{{f}}'
                t += f'+c_{{f}}\dot{{x}}_{{f}}'
                t += f'+k_{{f}}x_{{f}}'
                t += f'=\\frac{{b}}{{L}}F_{{qf}}(t)$'
            elif (not hasTLCD) and n == lines:
                t += f'$m_{{s{n}}}\ddot{{x}}_{{s{n}}}'
                t += f'+c_{{s{n}}}\dot{{x}}_{{s{n}}}'
                t += f'-k_{{s{n}}}x_{{s{n-1}}}'
                t += f'+k_{{s{n}}}x_{{s{n}}}'
                t += f'=F_{{q{n}}}(t)$'
        if type == "Numeric":
            if n == 1:
                t += f'$({ids[n].mass:1.2E})\ddot{{x}}_{{s{n}}}'
                t += f'+({ids[n].dampingCoefficient:1.2E})\dot{{x}}_{{s{n}}}'
                t += f'+({ids[n].stiffness + ids[n+1].stiffness:1.2E})x_{{s{n}}}'
                t += f'-({ids[n].stiffness:1.2E})x_{{s{n+1}}}'
                t += f'=-({ids[n].mass:1.2E})\ddot{{x}}_{{q}}(t)$'
            elif (hasTLCD and n < lines-1) or ((not hasTLCD) and n < lines):
                t += f'$({ids[n].mass:1.2E})\ddot{{x}}_{{s{n}}}'
                t += f'+({ids[n].dampingCoefficient:1.2E})\dot{{x}}_{{s{n}}}'
                t += f'-({ids[n].stiffness:1.2E})x_{{s{n-1}}}'
                t += f'+({ids[n].stiffness + ids[n+1].stiffness:1.2E})x_{{s{n}}}'
                t += f'-({ids[n+1].stiffness:1.2E})x_{{s{n+1}}}'
                t += f'=-({ids[n].mass:1.2E})\ddot{{x}}_{{q}}(t)$'
            elif hasTLCD and n == lines-1:
                t += f'$({ids[n].mass + idf.mass:1.2E})\ddot{{x}}_{{s{n}}} + ({idf.width/idf.length*idf.mass:1.2E})\ddot{{x}}_{{f}}'
                t += f'+({ids[n].dampingCoefficient:1.2E})\dot{{x}}_{{s{n}}}'
                t += f'-({ids[n].stiffness:1.2E})x_{{s{n-1}}}'
                t += f'+({ids[n].stiffness:1.2E})x_{{s{n}}}'
                t += f'=-({ids[n].mass + idf.mass:1.2E})\ddot{{x}}_{{q}}(t)$'
            elif hasTLCD and n == lines:
                t += f'$({idf.width/idf.length*idf.mass:1.2E})\ddot{{x}}_{{s{n-1}}} + ({idf.mass:1.2E})\ddot{{x}}_{{f}}'
                t += f'+c_{{f}}(t)\dot{{x}}_{{f}}'
                t += f'+({idf.stiffness:1.2E})x_{{f}}'
                t += f'=({idf.width/idf.length*idf.mass:1.2E})\ddot{{x}}_{{q}}(t)$'
            elif (not hasTLCD) and n == lines:
                t += f'$({ids[n].mass:1.2E})\ddot{{x}}_{{s{n}}}'
                t += f'+({ids[n].dampingCoefficient:1.2E})\dot{{x}}_{{s{n}}}'
                t += f'-({ids[n].stiffness:1.2E})x_{{s{n-1}}}'
                t += f'+({ids[n].stiffness:1.2E})x_{{s{n}}}'
                t += f'=-({ids[n].mass:1.2E})\ddot{{x}}_{{q}}(t)$'

        # Draw equation
        eqCanvas = self.equationWidget.equationCanvas
        eqCanvas.fig.clf()
        eqCanvas.axes = eqCanvas.axes = eqCanvas.fig.add_subplot(111)
        eqCanvas.axes.set_axis_off()
        eqCanvas.axes.text(0.5, 0.5, t, wrap=False, ha='center', va='center', fontsize=14)
        eqCanvas.draw()

    def setup_outputs(self):
        # Dynamic Response Canvas
        self.outputPlt1.dynRespCanvas = PltCanvas()
        self.outputPlt1.mpl_toolbar = NavigationToolbar(self.outputPlt1.dynRespCanvas, self)
        # self.outputPlt1.exportBtn = QPushButton('Export CSV', self)
        self.outputPlt1.gridLabel = QLabel('Show Grid', self)
        self.outputPlt1.gridChkBox = QCheckBox(self)
        self.outputPlt1.gridChkBox.stateChanged.connect(self.dynamic_response_grid_toggle)
        # self.outputPlt1.exportBtn.clicked.connect(self.dynamic_response_export_csv)

        self.outputPlt1.gridLayout = QGridLayout()
        self.outputPlt1.gridLayout.addWidget(self.outputPlt1.dynRespCanvas, 1, 1, 1, 4)
        self.outputPlt1.gridLayout.addWidget(self.outputPlt1.gridLabel, 2, 1)
        self.outputPlt1.gridLayout.addWidget(self.outputPlt1.gridChkBox, 2, 2)
        self.outputPlt1.gridLayout.addWidget(self.outputPlt1.mpl_toolbar, 2, 3)
        # self.outputPlt1.gridLayout.addWidget(self.outputPlt1.exportBtn, 2, 4)

        self.outputPlt1.setLayout(self.outputPlt1.gridLayout)

        # ComboBox update
        DOFs = [f"Story {i+1}" for i in range(len(self.inputData.stories))] + ["TLCD"]
        self.outputsDOF1.addItems(DOFs)
        self.outputsDOF2.addItems(DOFs)
        self.outputsDOF3.addItems(DOFs)

        # Connections
        self.plotButton.clicked.connect(self.plot_dynamic_respose)


    def plot_dynamic_respose(self):
        n = 1
        if get_text(self.outputsDOF2) != "None":
            n += 1
        if get_text(self.outputsDOF3) != "None":
            n += 1
        
        DOFs = [i.currentIndex() - 1 for i in [self.outputsDOF1, self.outputsDOF2, self.outputsDOF3]]
        DOFs[0] += 1
        x = get_text(self.outputsXaxis1)
        y = [get_text(i) for i in [self.outputsYaxis1, self.outputsYaxis2, self.outputsYaxis3]]

        labels = [None]
        xaxis = [None for i in DOFs]
        for i in range(len(xaxis)):
            if DOFs[i] != -1:
                if x == "Time":
                    xaxis[i] = self.outputData.dynamicResponse.t
                    labels[0] = 't (s)'
                elif x == "Displacement":
                    xaxis[i] = self.outputData.dynamicResponse.x[DOFs[i], :].A1
                    labels[0] = 'x (m)'
                elif x == "Velocity":
                    xaxis[i] = self.outputData.dynamicResponse.v[DOFs[i], :].A1
                    labels[0] = 'v (m/s)'
                elif x == "Acceleration":
                    xaxis[i] = self.outputData.dynamicResponse.a[DOFs[i], :].A1
                    labels[0] = r'a (m/$s^2$)'
                elif x == "Force":
                    xaxis[i] = self.outputData.dynamicResponse.F[DOFs[i], :].A1
                    labels[0] = 'F (N)'
                elif x == "Excitation Acceleration":
                    xaxis[i] = self.outputData.dynamicResponse.F[0, :].A1 / self.inputData.stories[1].mass
                    labels[0] = r'a (m/$s^2$)'

        yaxis = [None for i in DOFs]
        for i in range(len(yaxis)):
            if DOFs[i] != -1:
                if y[i] == "Time":
                    yaxis[i] = self.outputData.dynamicResponse.t
                    labels.append('t (s)')
                elif y[i] == "Displacement":
                    yaxis[i] = self.outputData.dynamicResponse.x[DOFs[i], :].A1
                    labels.append('x (m)')
                elif y[i] == "Velocity":
                    yaxis[i] = self.outputData.dynamicResponse.v[DOFs[i], :].A1
                    labels.append('v (m/s)')
                elif y[i] == "Acceleration":
                    yaxis[i] = self.outputData.dynamicResponse.a[DOFs[i], :].A1
                    labels.append(r'a (m/$s^2$)')
                elif y[i] == "Force":
                    yaxis[i] = self.outputData.dynamicResponse.F[DOFs[i], :].A1
                    labels.append('F (N)')
                elif y[i] == "Excitation Acceleration":
                    yaxis[i] = self.outputData.dynamicResponse.F[0, :].A1 / self.inputData.stories[1].mass
                    labels.append(r'a (m/$s^2$)')
                


        # self.textBrowser.setText(str(DOFs) + str(x) + str(y))
        self.textBrowser.setText(str(n))
        # self.outputData.dynamicResponse.x
        
        self.outputPlt1.dynRespCanvas.stepbystep_subplots(n, xaxis, yaxis, labels)


    def dynamic_response_grid_toggle(self):
        """ Toggles plot grid on and off

        :return: None
        """
        self.outputPlt1.dynRespCanvas.axes.grid(self.outputPlt1.gridChkBox.isChecked())
        self.outputPlt1.dynRespCanvas.draw()
        

    def structure_input_details(self):
        self.structureDetailWindow = TextBrowser(self, self.inputData, self.outputData)
        s =  f"""STRUCTURE DETAILS
--------------------------
"""
        for i in range(1, len(self.inputData.stories)+1):
            s += f"""Story {i}:
Mass = {self.inputData.stories[i].mass/1e3} t
Height = {self.inputData.stories[i].height} m
Column Width = {self.inputData.stories[i].width*100} cm
Column Depth = {self.inputData.stories[i].depth*100} cm
Column Elasticity Module = {self.inputData.stories[i].E/1e9} GPa

"""
        s += f"Damping Ratio = {self.inputData.configurations.dampingRatio}"
        self.structureDetailWindow.textBrowser.setText(s)

    def tlcd_input_details(self):
        self.tlcdDetailWindow = TextBrowser(self, self.inputData, self.outputData)
        s = f"""TLCD DETAILS
---------------------
"""
# TO DO: ADD UNITS
        s += f"""TLCD Type = {self.inputData.tlcd.type}
Diameter = {self.inputData.tlcd.diameter}
Width = {self.inputData.tlcd.width}
Water Height = {self.inputData.tlcd.waterHeight}
Length = {self.inputData.tlcd.length}
Mass = {self.inputData.tlcd.mass}
Stiffness = {self.inputData.tlcd.stiffness}
Natural Frequency = {self.inputData.tlcd.naturalFrequency}
"""
#         if self.inputData.tlcd.type == 'Basic TLCD':
#             s += f"""Gas Height = {self.inputData.tlcd.gasHeight}
# Gas Pressure = {self.inputData.tlcd.gasPressure}
# """
        if self.inputData.tlcd.type == 'Pressurized TLCD':
            s += f"""Gas Height = {self.inputData.tlcd.gasHeight}
Gas Pressure = {self.inputData.tlcd.gasPressure}
"""
        
        s += f"Specific Mass = {self.inputData.configurations.liquidSpecificMass} kg/m^3"
        s += f"Kinetic Viscosity = {self.inputData.configurations.kineticViscosity} m^2/s"
        s += f"Gravity Acceleration = {self.inputData.configurations.gravity} m/s^2 "
        s += f"Pipe Roughness = {self.inputData.configurations.pipeRoughness}"
        self.tlcdDetailWindow.textBrowser.setText(s)

    def refresh(self):
        self.SBSstructureWidget.structureCanvas.painter(self.inputData.stories)
        self.SBSTLCDWidget.tlcdCanvas.painter(self.inputData.tlcd)
        if self.inputData.excitation.type == 'Sine Wave':
            tAnly = np.arange(0, self.inputData.excitation.anlyDuration + self.inputData.configurations.timeStep,
                              self.inputData.configurations.timeStep)
            tExct = np.arange(0, self.inputData.excitation.exctDuration + self.inputData.configurations.timeStep,
                              self.inputData.configurations.timeStep)
            a = self.inputData.excitation.amplitude * np.sin(self.inputData.excitation.frequency * tExct)
            a = np.hstack((a, np.array([0 for i in range(len(tAnly) - len(tExct))])))
            self.SBSexcitationWidget.excitationCanvas.plot_excitation(tAnly, a)
        elif self.inputData.excitation.type == 'General Excitation':
            self.SBSexcitationWidget.excitationCanvas.plot_excitation(self.inputData.excitation.t_input, self.inputData.excitation.a_input)

    def excitation_grid_toggle(self):
        """ Toggles plot grid on and off

        :return: None
        """
        self.SBSexcitationWidget.excitationCanvas.axes.grid(self.SBSexcitationWidget.gridChkBox.isChecked())
        self.SBSexcitationWidget.excitationCanvas.draw()

    def closeEvent(self, event):
        quit_msg = "Are you sure you want to exit the program?"
        reply = QMessageBox.question(self, 'Confirm Exit',
                                     quit_msg, QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    # Menu Methods
    



if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = MainWindow()
    gui.show()
    sys.exit(app.exec_())
    # comment
