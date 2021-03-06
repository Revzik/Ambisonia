from PyQt5 import QtCore, QtWidgets
from src.engine import track, mixer
from src.gui.bar import Bar
from src.gui.slider import LabeledSlider


VOL_MIN = -60
VOL_MAX = 12
VOL_YELLOW = -12
VOL_RED = 0

TRACKS_NO = 4


class Ui_MainWindow(object):
    def __init__(self):
        self.centralwidget = None
        self.gridLayout = None
        self.main_layout = None

        self.track_controls = None

        self.button_bar = None
        self.buttons = {}

        self.mixer = mixer.Mixer(TRACKS_NO)
        self.mixer_widget = None
        self.master = {}
        self.tracks = []
        self.selected_track = -1

        self.ambisonic_control = None
        
        self.space_control = {}
        self.space_display = {}

        self.menubar = None
        self.statusbar = None

        self.initialized = False

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(900, 500)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        
        self.main_layout = QtWidgets.QHBoxLayout()
        self.main_layout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.main_layout.setObjectName("main_layout")
        
        self.create_track_controls()
        
        spacerItem1 = QtWidgets.QSpacerItem(40, 0, QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Minimum)
        self.main_layout.addItem(spacerItem1)
        
        self.create_ambisonic_control()
        
        self.gridLayout.addLayout(self.main_layout, 0, 0, 1, 1)
        
        MainWindow.setCentralWidget(self.centralwidget)
        
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setEnabled(True)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 900, 21))
        self.menubar.setNativeMenuBar(True)
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setSizeGripEnabled(False)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        MainWindow.setWindowTitle("Ambisonia")

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.initialized = True
        
    def create_track_controls(self):
        self.track_controls = QtWidgets.QVBoxLayout()
        self.track_controls.setObjectName("track_controls")
        
        self.create_button_bar()
        
        self.mixer_widget = QtWidgets.QHBoxLayout()
        self.mixer_widget.setObjectName("mixer_widget")
        
        self.create_master_track()

        for i in range(TRACKS_NO):
            self.tracks.append(self.create_track(stereo=False))
        
        self.track_controls.addLayout(self.mixer_widget)
        
        self.main_layout.addLayout(self.track_controls)
        
    def create_button_bar(self):
        self.button_bar = QtWidgets.QHBoxLayout()
        self.button_bar.setContentsMargins(-1, -1, -1, -1)
        self.button_bar.setSpacing(0)
        self.button_bar.setObjectName("button_bar")
        
        self.buttons['play'] = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttons['play'].sizePolicy().hasHeightForWidth())
        self.buttons['play'].setSizePolicy(sizePolicy)
        self.buttons['play'].setMinimumSize(QtCore.QSize(60, 60))
        self.buttons['play'].setObjectName("play_pause")
        self.buttons['play'].setText("Play")
        self.buttons['play'].clicked.connect(self.mixer.play)
        self.button_bar.addWidget(self.buttons['play'])
        
        self.buttons['stop'] = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttons['stop'].sizePolicy().hasHeightForWidth())
        self.buttons['stop'].setSizePolicy(sizePolicy)
        self.buttons['stop'].setMinimumSize(QtCore.QSize(60, 60))
        self.buttons['stop'].setObjectName("stop")
        self.buttons['stop'].setText("Stop")
        self.buttons['stop'].clicked.connect(self.mixer.stop)
        self.button_bar.addWidget(self.buttons['stop'])

        self.buttons['export'] = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttons['export'].sizePolicy().hasHeightForWidth())
        self.buttons['export'].setSizePolicy(sizePolicy)
        self.buttons['export'].setMinimumSize(QtCore.QSize(60, 60))
        self.buttons['export'].setObjectName("export")
        self.buttons['export'].setText("Export")
        self.buttons['export'].clicked.connect(self.export)
        self.button_bar.addWidget(self.buttons['export'])
        
        spacerItem = QtWidgets.QSpacerItem(0, 20, QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Minimum)
        self.button_bar.addItem(spacerItem)

        self.track_controls.addLayout(self.button_bar)
        
    def create_master_track(self):
        self.master['widget'] = QtWidgets.QVBoxLayout()
        self.master['widget'].setObjectName("master")

        self.master['label'] = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.master['label'].sizePolicy().hasHeightForWidth())
        self.master['label'].setSizePolicy(sizePolicy)
        self.master['label'].setMinimumSize(QtCore.QSize(100, 0))
        self.master['label'].setMaximumSize(QtCore.QSize(100, 25))
        self.master['label'].setObjectName("master_label")
        self.master['label'].setText("Master")
        self.master['label'].setCheckable(True)
        self.master['label'].clicked.connect(lambda: self.update_ambisonic_control(-1))
        self.master['widget'].addWidget(self.master['label'])

        self.master['mode'] = QtWidgets.QComboBox(self.centralwidget)
        self.master['mode'].setObjectName("master_mode")
        self.master['mode'].addItem("Simple stereo")
        self.master['mode'].addItem("UHJ Stereo")
        self.master['mode'].addItem("Binaural")
        self.master['mode'].currentIndexChanged.connect(self.update_master_format)
        self.master['widget'].addWidget(self.master['mode'])
        
        self.master['volume'] = QtWidgets.QHBoxLayout()
        self.master['volume'].setObjectName("master_volume")
        
        self.master['v_control'] = LabeledSlider(VOL_MIN, VOL_MAX, interval=6, orientation=QtCore.Qt.Vertical,
                                                 parent=self.centralwidget, side='right')
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.master['v_control'].sizePolicy().hasHeightForWidth())
        self.master['v_control'].setSizePolicy(sizePolicy)
        self.master['v_control'].setMinimumSize(QtCore.QSize(0, 250))
        self.master['v_control'].sl.setProperty("value", 0)
        self.master['v_control'].setObjectName("master_volume_control")
        self.master['v_control'].sl.valueChanged.connect(lambda: self.read_gain(-1))
        self.master['volume'].addWidget(self.master['v_control'])

        # self.master['v_display_l'] = Bar(VOL_MIN, VOL_MAX, VOL_YELLOW, VOL_RED)
        # self.master['volume'].addWidget(self.master['v_display_l'])
        #
        # self.master['v_display_r'] = Bar(VOL_MIN, VOL_MAX, VOL_YELLOW, VOL_RED)
        # self.master['volume'].addWidget(self.master['v_display_r'])
        
        self.master['widget'].addLayout(self.master['volume'])

        self.mixer_widget.addLayout(self.master['widget'])
        
    def create_track(self, stereo=False):
        track_no = len(self.tracks)

        t = {'widget': QtWidgets.QVBoxLayout()}
        t['widget'].setObjectName("track{}".format(track_no))

        t['label'] = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(t['label'].sizePolicy().hasHeightForWidth())
        t['label'].setSizePolicy(sizePolicy)
        t['label'].setMinimumSize(QtCore.QSize(100, 0))
        t['label'].setMaximumSize(QtCore.QSize(100, 25))
        t['label'].setObjectName("tack{}_label".format(track_no))
        t['label'].setText("Track {}".format(track_no + 1))
        t['label'].setProperty('track_id', track_no)
        t['label'].setCheckable(True)
        t['label'].clicked.connect(lambda: self.update_ambisonic_control(track_no))
        t['widget'].addWidget(t['label'])

        t['load'] = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(t['load'].sizePolicy().hasHeightForWidth())
        t['load'].setSizePolicy(sizePolicy)
        t['load'].setMinimumSize(QtCore.QSize(0, 0))
        t['load'].setMaximumSize(QtCore.QSize(16777215, 25))
        t['load'].setObjectName("tack{}_load".format(track_no))
        t['load'].setText("Load")
        t['load'].clicked.connect(lambda: self.load_track(track_no))
        t['widget'].addWidget(t['load'])

        t['volume'] = QtWidgets.QHBoxLayout()
        t['volume'].setObjectName("track{}_volume".format(track_no))

        t['v_control'] = LabeledSlider(VOL_MIN, VOL_MAX, interval=6, orientation=QtCore.Qt.Vertical,
                                       parent=self.centralwidget, side='right')
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(t['v_control'].sizePolicy().hasHeightForWidth())
        t['v_control'].setSizePolicy(sizePolicy)
        t['v_control'].setMinimumSize(QtCore.QSize(0, 250))
        t['v_control'].sl.setProperty("value", 0)
        t['v_control'].setObjectName("track{}_volume_control".format(track_no))
        t['v_control'].sl.valueChanged.connect(lambda: self.read_gain(track_no))
        t['volume'].addWidget(t['v_control'])

        # if stereo:
        #     t['v_bar_l'] = Bar(VOL_MIN, VOL_MAX, VOL_YELLOW, VOL_RED)
        #     t['volume'].addWidget(t['v_bar_l'])
        #
        #     t['v_bar_r'] = Bar(VOL_MIN, VOL_MAX, VOL_YELLOW, VOL_RED)
        #     t['volume'].addWidget(t['v_bar_r'])
        # else:
        #     t['v_bar'] = Bar(VOL_MIN, VOL_MAX, VOL_YELLOW, VOL_RED)
        #     t['volume'].addWidget(t['v_bar'])

        t['widget'].addLayout(t['volume'])

        self.mixer_widget.addLayout(t['widget'])

        return t

    def create_ambisonic_control(self):
        self.ambisonic_control = QtWidgets.QVBoxLayout()
        self.ambisonic_control.setObjectName("ambisonic_control")

        spacerItem2 = QtWidgets.QSpacerItem(360, 0, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.ambisonic_control.addItem(spacerItem2)

        self.create_space_control()

        # self.create_space_display()

        self.main_layout.addLayout(self.ambisonic_control)

    def create_space_control(self):
        self.space_control['widget'] = QtWidgets.QHBoxLayout()
        self.space_control['widget'].setObjectName("space_control")

        # stereo spacing
        self.space_control['stereo'] = QtWidgets.QVBoxLayout(self.centralwidget)
        self.space_control['stereo'].setObjectName("stereo_separation")

        self.space_control['stereo_label'] = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.space_control['stereo_label'].sizePolicy().hasHeightForWidth())
        self.space_control['stereo_label'].setSizePolicy(sizePolicy)
        self.space_control['stereo_label'].setMinimumSize(QtCore.QSize(60, 0))
        self.space_control['stereo_label'].setMaximumSize(QtCore.QSize(60, 16777215))
        self.space_control['stereo_label'].setAlignment(QtCore.Qt.AlignCenter)
        self.space_control['stereo_label'].setObjectName("stereo_label")
        self.space_control['stereo_label'].setText("Stereo sep.")
        self.space_control['stereo'].addWidget(self.space_control['stereo_label'])

        self.space_control['stereo_control'] = LabeledSlider(0, 90, interval=15, orientation=QtCore.Qt.Vertical,
                                                             parent=self.centralwidget, side='right')
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.space_control['stereo_control'].sizePolicy().hasHeightForWidth())
        self.space_control['stereo_control'].setSizePolicy(sizePolicy)
        self.space_control['stereo_control'].setMinimumSize(QtCore.QSize(0, 250))
        self.space_control['stereo_control'].sl.setProperty("value", 0)
        self.space_control['stereo_control'].setObjectName("stereo_separation_control")
        self.space_control['stereo_control'].sl.setEnabled(False)
        self.space_control['stereo_control'].sl.valueChanged.connect(self.read_stereo_separation)
        self.space_control['stereo'].addWidget(self.space_control['stereo_control'])

        self.space_control['widget'].addLayout(self.space_control['stereo'])

        # horizontal position
        self.space_control['horizontal'] = QtWidgets.QVBoxLayout(self.centralwidget)
        self.space_control['horizontal'].setObjectName("horizontal_space")

        self.space_control['horizontal_label'] = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.space_control['horizontal_label'].sizePolicy().hasHeightForWidth())
        self.space_control['horizontal_label'].setSizePolicy(sizePolicy)
        self.space_control['horizontal_label'].setMinimumSize(QtCore.QSize(0, 20))
        self.space_control['horizontal_label'].setMaximumSize(QtCore.QSize(16777215, 20))
        self.space_control['horizontal_label'].setAlignment(QtCore.Qt.AlignCenter)
        self.space_control['horizontal_label'].setObjectName("horizontal_space_label")
        self.space_control['horizontal_label'].setText("Horizontal")
        self.space_control['horizontal'].addWidget(self.space_control['horizontal_label'])

        self.space_control['horizontal_control'] = QtWidgets.QDial(self.centralwidget)
        self.space_control['horizontal_control'].setMinimum(-180)
        self.space_control['horizontal_control'].setMaximum(180)
        self.space_control['horizontal_control'].setWrapping(True)
        self.space_control['horizontal_control'].setNotchTarget(5.7)
        self.space_control['horizontal_control'].setNotchesVisible(True)
        self.space_control['horizontal_control'].setObjectName("horizontal_space_control")
        self.space_control['horizontal_control'].setEnabled(False)
        self.space_control['horizontal_control'].valueChanged.connect(self.read_rotation)
        self.space_control['horizontal'].addWidget(self.space_control['horizontal_control'])

        self.space_control['widget'].addLayout(self.space_control['horizontal'])

        # horizontal position
        self.space_control['vertical'] = QtWidgets.QVBoxLayout(self.centralwidget)
        self.space_control['vertical'].setObjectName("vertical_space")

        self.space_control['vertical_label'] = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.space_control['vertical_label'].sizePolicy().hasHeightForWidth())
        self.space_control['vertical_label'].setSizePolicy(sizePolicy)
        self.space_control['vertical_label'].setMinimumSize(QtCore.QSize(60, 0))
        self.space_control['vertical_label'].setMaximumSize(QtCore.QSize(60, 16777215))
        self.space_control['vertical_label'].setAlignment(QtCore.Qt.AlignCenter)
        self.space_control['vertical_label'].setObjectName("vertical_space_label")
        self.space_control['vertical_label'].setText("Vertical")
        self.space_control['vertical'].addWidget(self.space_control['vertical_label'])

        self.space_control['vertical_control'] = LabeledSlider(-90, 90, interval=30, orientation=QtCore.Qt.Vertical,
                                                               parent=self.centralwidget, side='left')
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.space_control['vertical_control'].sizePolicy().hasHeightForWidth())
        self.space_control['vertical_control'].setSizePolicy(sizePolicy)
        self.space_control['vertical_control'].setMinimumSize(QtCore.QSize(0, 250))
        self.space_control['vertical_control'].sl.setProperty("value", 0)
        self.space_control['vertical_control'].setObjectName("vertical_control")
        self.space_control['vertical_control'].sl.setEnabled(False)
        self.space_control['vertical_control'].sl.valueChanged.connect(self.read_elevation)
        self.space_control['vertical'].addWidget(self.space_control['vertical_control'])

        self.space_control['widget'].addLayout(self.space_control['vertical'])

        self.ambisonic_control.addLayout(self.space_control['widget'])

    def create_space_display(self):
        self.space_display['widget'] = QtWidgets.QHBoxLayout()
        self.space_display['widget'].setObjectName("space_display")

        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.space_display['widget'].addItem(spacerItem3)

        self.space_display['omni'] = {}
        self.space_display['omni']['widget'] = QtWidgets.QVBoxLayout()
        self.space_display['omni']['widget'].setObjectName("omni_display")
        self.space_display['omni']['label'] = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.space_display['omni']['label'].sizePolicy().hasHeightForWidth())
        self.space_display['omni']['label'].setSizePolicy(sizePolicy)
        self.space_display['omni']['label'].setMinimumSize(QtCore.QSize(20, 0))
        self.space_display['omni']['label'].setAlignment(QtCore.Qt.AlignCenter)
        self.space_display['omni']['label'].setObjectName("omni_label")
        self.space_display['omni']['label'].setText("W")
        self.space_display['omni']['widget'].addWidget(self.space_display['omni']['label'])
        self.space_display['omni']['bar'] = Bar(VOL_MIN, VOL_MAX, VOL_YELLOW, VOL_RED)
        self.space_display['omni']['widget'].addWidget(self.space_display['omni']['bar'])
        self.space_display['widget'].addLayout(self.space_display['omni']['widget'])

        self.space_display['x'] = {}
        self.space_display['x']['widget'] = QtWidgets.QVBoxLayout()
        self.space_display['x']['widget'].setObjectName("x_display")
        self.space_display['x']['label'] = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.space_display['x']['label'].sizePolicy().hasHeightForWidth())
        self.space_display['x']['label'].setSizePolicy(sizePolicy)
        self.space_display['x']['label'].setMinimumSize(QtCore.QSize(20, 0))
        self.space_display['x']['label'].setAlignment(QtCore.Qt.AlignCenter)
        self.space_display['x']['label'].setObjectName("x_label")
        self.space_display['x']['label'].setText("X")
        self.space_display['x']['widget'].addWidget(self.space_display['x']['label'])
        self.space_display['x']['bar'] = Bar(VOL_MIN, VOL_MAX, VOL_YELLOW, VOL_RED)
        self.space_display['x']['widget'].addWidget(self.space_display['x']['bar'])
        self.space_display['widget'].addLayout(self.space_display['x']['widget'])

        self.space_display['y'] = {}
        self.space_display['y']['widget'] = QtWidgets.QVBoxLayout()
        self.space_display['y']['widget'].setObjectName("y_display")
        self.space_display['y']['label'] = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.space_display['y']['label'].sizePolicy().hasHeightForWidth())
        self.space_display['y']['label'].setSizePolicy(sizePolicy)
        self.space_display['y']['label'].setMinimumSize(QtCore.QSize(20, 0))
        self.space_display['y']['label'].setAlignment(QtCore.Qt.AlignCenter)
        self.space_display['y']['label'].setObjectName("y_label")
        self.space_display['y']['label'].setText("Y")
        self.space_display['y']['widget'].addWidget(self.space_display['y']['label'])
        self.space_display['y']['bar'] = Bar(VOL_MIN, VOL_MAX, VOL_YELLOW, VOL_RED)
        self.space_display['y']['widget'].addWidget(self.space_display['y']['bar'])
        self.space_display['widget'].addLayout(self.space_display['y']['widget'])

        self.space_display['z'] = {}
        self.space_display['z']['widget'] = QtWidgets.QVBoxLayout()
        self.space_display['z']['widget'].setObjectName("z_display")
        self.space_display['z']['label'] = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.space_display['z']['label'].sizePolicy().hasHeightForWidth())
        self.space_display['z']['label'].setSizePolicy(sizePolicy)
        self.space_display['z']['label'].setMinimumSize(QtCore.QSize(20, 0))
        self.space_display['z']['label'].setAlignment(QtCore.Qt.AlignCenter)
        self.space_display['z']['label'].setObjectName("z_label")
        self.space_display['z']['label'].setText("Z")
        self.space_display['z']['widget'].addWidget(self.space_display['z']['label'])
        self.space_display['z']['bar'] = Bar(VOL_MIN, VOL_MAX, VOL_YELLOW, VOL_RED)
        self.space_display['z']['widget'].addWidget(self.space_display['z']['bar'])
        self.space_display['widget'].addLayout(self.space_display['z']['widget'])

        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.space_display['widget'].addItem(spacerItem4)
        self.ambisonic_control.addLayout(self.space_display['widget'])

    def update_ambisonic_control(self, index):
        self.selected_track = index

        stereo_toggle = False
        stereo = 0
        horizontal_toggle = True
        vertical_toggle = True

        if index == -1:
            horizontal_toggle = False
            phi = 0
            vertical_toggle = False
            theta = 0
            if self.mixer.master.type == track.SIMPLE_STEREO:
                stereo = self.mixer.master.stereo_angle
                stereo_toggle = True
        else:
            phi = self.mixer.tracks[index].phi
            theta = self.mixer.tracks[index].theta
            if self.mixer.tracks[index].type == track.SIMPLE_STEREO:
                stereo = self.mixer.tracks[index].stereo_angle
                stereo_toggle = True

        print('Selected track {}, phi: {}, theta: {}, stereo toggled: {}, vertica toggled: {}, stereo angle: {}'.
              format(index, phi, theta, stereo_toggle, vertical_toggle, stereo))

        self.space_control['stereo_control'].sl.setProperty('value', stereo)
        self.space_control['stereo_control'].sl.setEnabled(stereo_toggle)
        self.space_control['horizontal_control'].setProperty('value', -phi)
        self.space_control['horizontal_control'].setEnabled(horizontal_toggle)
        self.space_control['vertical_control'].sl.setProperty('value', theta)
        self.space_control['vertical_control'].sl.setEnabled(vertical_toggle)

        for i, t in enumerate(self.tracks):
            t['label'].setChecked(i == index)
        self.master['label'].setChecked(index == -1)

    def load_track(self, index):
        try:
            previous_type = self.mixer.tracks[index].type

            dialog = QtWidgets.QFileDialog()
            dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)
            dialog.setAcceptMode(QtWidgets.QFileDialog.AcceptOpen)
            dialog.setNameFilter("Wave files (*.wav)")
            if dialog.exec_():
                path = dialog.selectedFiles()
                self.mixer.tracks[index].load(path[0])

                current_type = self.mixer.tracks[index].type
                # if not current_type == previous_type:
                #     self.update_track_bars(index, previous_type, current_type)

                print('Successfully loaded track from {} as Track {}'.format(path[0], index + 1))
        except Exception as e:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText('Could not load the file!')
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msg.setWindowTitle("Error")
            msg.exec_()

    def update_track_bars(self, index, old_type, new_type):
        if old_type == track.MONO:
            self.tracks[index]['volume'].removeWidget(self.tracks[index]['v_bar'])
            self.tracks[index]['v_bar'].deleteLater()
            del self.tracks[index]['v_bar']
        elif old_type == track.SIMPLE_STEREO:
            self.tracks[index]['volume'].removeWidget(self.tracks[index]['v_bar_l'])
            self.tracks[index]['v_bar_l'].deleteLater()
            del self.tracks[index]['v_bar_l']
            self.tracks[index]['volume'].removeWidget(self.tracks[index]['v_bar_r'])
            self.tracks[index]['v_bar_r'].deleteLater()
            del self.tracks[index]['v_bar_r']

        if new_type == track.MONO:
            self.tracks[index]['v_bar'] = Bar(VOL_MIN, VOL_MAX, VOL_YELLOW, VOL_RED)
            self.tracks[index]['volume'].addWidget(self.tracks[index]['v_bar'])
        elif new_type == track.SIMPLE_STEREO:
            self.tracks[index]['v_bar_l'] = Bar(VOL_MIN, VOL_MAX, VOL_YELLOW, VOL_RED)
            self.tracks[index]['volume'].addWidget(self.tracks[index]['v_bar_l'])

            self.tracks[index]['v_bar_r'] = Bar(VOL_MIN, VOL_MAX, VOL_YELLOW, VOL_RED)
            self.tracks[index]['volume'].addWidget(self.tracks[index]['v_bar_r'])

        self.update_ambisonic_control(index)

        print('Changed track {} type to {}'.format(index, new_type))

    def read_stereo_separation(self):
        value = self.space_control['stereo_control'].sl.value()
        if self.selected_track == -1:
            self.mixer.master.stereo_angle = value
        else:
            self.mixer.tracks[self.selected_track].stereo_angle = value

    def update_master_format(self, index):
        if index == 0:
            self.mixer.master.type = track.SIMPLE_STEREO
            self.mixer.master.stereo_angle = 30
        elif index == 1:
            self.mixer.master.type = track.UHJ_STEREO
        elif index == 2:
            self.mixer.master.type = track.BINAURAL
        self.update_ambisonic_control(-1)

    def read_rotation(self):
        value = self.space_control['horizontal_control'].value()
        if self.selected_track == -1:
            self.mixer.master.phi = -value
        else:
            self.mixer.tracks[self.selected_track].phi = -value

    def read_elevation(self):
        value = self.space_control['vertical_control'].sl.value()
        if self.selected_track == -1:
            self.mixer.master.theta = value
        else:
            self.mixer.tracks[self.selected_track].theta = value

    def read_gain(self, index):
        if index == -1:
            self.mixer.master.gain = self.master['v_control'].sl.value()
        else:
            self.mixer.tracks[index].gain = self.tracks[index]['v_control'].sl.value()

    def export(self):
        try:
            dialog = QtWidgets.QFileDialog()
            dialog.setFileMode(QtWidgets.QFileDialog.AnyFile)
            dialog.setAcceptMode(QtWidgets.QFileDialog.AcceptSave)
            path = dialog.getSaveFileName(caption="Save file", filter="Wave files (*.wav)")
            if path[0].endswith('.wav'):
                self.mixer.export(path[0])
            else:
                self.mixer.export(path[0] + '.wav')
            print('File successfully saved to {}'.format(path[0]))
        except Exception as e:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText('Could not save the file!')
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msg.setWindowTitle("Error")
            msg.exec_()
