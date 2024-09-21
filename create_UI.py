import sys
from run_script import run_script  # Import your existing function
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QLineEdit, QFileDialog, QVBoxLayout, QHBoxLayout, QMessageBox, QSlider
)
from PyQt5.QtCore import Qt  # Import Qt for slider orientation and other constants
import json
import os

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.load_input_values()  # Load saved input values from config.json

    def initUI(self):
        """
        Initializes the user interface (UI) of the application with sliders and better input validation.
        """

        # Image file input
        self.image_label = QLabel('Image File:')
        self.image_path = QLineEdit(self)
        self.browse_button = QPushButton('Browse', self)
        self.browse_button.clicked.connect(self.browse_image)

        # True Time: Integer between 30 and 240 with a slider and text box
        self.true_time_label = QLabel('Desired Video time in seconds (30-240):')
        self.true_time_slider = QSlider(Qt.Horizontal, self)
        self.true_time_slider.setRange(30, 240)
        self.true_time_slider.setValue(60)  # Default value
        self.true_time_slider.valueChanged.connect(self.update_true_time_from_slider)

        self.true_time_text = QLineEdit(self)
        self.true_time_text.setText('60')  # Set initial value
        self.true_time_text.editingFinished.connect(self.update_true_time_from_text)

        # Threshold: Float between 0 and 1 (using a slider with 0-100) and a text box
        self.threshold_label = QLabel('Thresholding value for Horizon (0.0 - 1.0):')
        self.threshold_slider = QSlider(Qt.Horizontal, self)
        self.threshold_slider.setRange(0, 100)  # 0-100 to represent 0.0-1.0
        self.threshold_slider.setValue(50)  # Default value
        self.threshold_slider.valueChanged.connect(self.update_threshold_from_slider)

        self.threshold_text = QLineEdit(self)
        self.threshold_text.setText('0.5')  # Set initial value
        self.threshold_text.editingFinished.connect(self.update_threshold_from_text)

        # Instrument Array: Shows example input and valid instrument names
        self.instrument_array_label = QLabel('Instrument Array (e.g., viola, piano_small):')
        self.instrument_array_input = QLineEdit(self)
        self.instrument_array_input.setPlaceholderText("Example: viola, piano_small")
        self.valid_instruments_label = QLabel('Valid instruments: violin_common, viola_common, cello_common, bass_common, piano_common, violin_full, viola_full, cello_full, bass_full, piano_full')

        # Delay Vector: Shows example input
        self.delay_vector_label = QLabel('Delay Vector (comma-separated integers):')
        self.delay_vector_input = QLineEdit(self)
        self.delay_vector_input.setPlaceholderText("Example: 0, 10, 15")

        # Cross Percentage: Float between 0 and 1 (using a slider with 0-100) and a text box
        self.cross_percentage_label = QLabel('Cross-fade Percentage between notes (0.0 - 1.0):')
        self.cross_percentage_slider = QSlider(Qt.Horizontal, self)
        self.cross_percentage_slider.setRange(0, 100)  # 0-100 to represent 0.0-1.0
        self.cross_percentage_slider.setValue(75)  # Default value
        self.cross_percentage_slider.valueChanged.connect(self.update_cross_percentage_from_slider)

        self.cross_percentage_text = QLineEdit(self)
        self.cross_percentage_text.setText('0.75')  # Set initial value
        self.cross_percentage_text.editingFinished.connect(self.update_cross_percentage_from_text)

        # Scaling Factor: Float between 0 and 1 (using a slider with 0-100) and a text box
        self.scaling_factor_label = QLabel('How much to scale image size (0.0 - 1.0):')
        self.scaling_factor_slider = QSlider(Qt.Horizontal, self)
        self.scaling_factor_slider.setRange(0, 100)  # 0-100 to represent 0.0-1.0
        self.scaling_factor_slider.setValue(20)  # Default value
        self.scaling_factor_slider.valueChanged.connect(self.update_scaling_factor_from_slider)

        self.scaling_factor_text = QLineEdit(self)
        self.scaling_factor_text.setText('0.20')  # Set initial value
        self.scaling_factor_text.editingFinished.connect(self.update_scaling_factor_from_text)

        # Start button
        self.start_button = QPushButton('Start', self)
        self.start_button.clicked.connect(self.run_function)

        # Layouts
        vbox = QVBoxLayout()

        # Image file layout
        hbox_image = QHBoxLayout()
        hbox_image.addWidget(self.image_label)
        hbox_image.addWidget(self.image_path)
        hbox_image.addWidget(self.browse_button)
        vbox.addLayout(hbox_image)

        # Add True Time slider and text box to layout
        hbox_true_time = QHBoxLayout()
        hbox_true_time.addWidget(self.true_time_label)
        hbox_true_time.addWidget(self.true_time_slider)
        hbox_true_time.addWidget(self.true_time_text)
        vbox.addLayout(hbox_true_time)

        # Add Threshold slider and text box to layout
        hbox_threshold = QHBoxLayout()
        hbox_threshold.addWidget(self.threshold_label)
        hbox_threshold.addWidget(self.threshold_slider)
        hbox_threshold.addWidget(self.threshold_text)
        vbox.addLayout(hbox_threshold)

        # Instrument array layout
        vbox.addWidget(self.instrument_array_label)
        vbox.addWidget(self.instrument_array_input)
        vbox.addWidget(self.valid_instruments_label)

        # Delay vector layout
        vbox.addWidget(self.delay_vector_label)
        vbox.addWidget(self.delay_vector_input)

        # Add Cross Percentage slider and text box to layout
        hbox_cross_percentage = QHBoxLayout()
        hbox_cross_percentage.addWidget(self.cross_percentage_label)
        hbox_cross_percentage.addWidget(self.cross_percentage_slider)
        hbox_cross_percentage.addWidget(self.cross_percentage_text)
        vbox.addLayout(hbox_cross_percentage)

        # Add Scaling Factor slider and text box to layout
        hbox_scaling_factor = QHBoxLayout()
        hbox_scaling_factor.addWidget(self.scaling_factor_label)
        hbox_scaling_factor.addWidget(self.scaling_factor_slider)
        hbox_scaling_factor.addWidget(self.scaling_factor_text)
        vbox.addLayout(hbox_scaling_factor)

        # Add start button
        vbox.addWidget(self.start_button)

        self.setLayout(vbox)
        self.setWindowTitle('Enhanced Function Input UI')
        self.setGeometry(300, 300, 500, 400)

    def browse_image(self):
        """
        Opens a file dialog to select an image file and populates the image_path field with the selected path.
        """
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open Image File')
        if file_name:
            self.image_path.setText(file_name)

    # Sync functions for True Time (integer slider)
    def update_true_time_from_slider(self, value):
        self.true_time_text.setText(str(value))

    def update_true_time_from_text(self):
        try:
            value = int(self.true_time_text.text())
            if 30 <= value <= 240:
                self.true_time_slider.setValue(value)
            else:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter a valid integer between 30 and 240.")

    # Sync functions for Threshold (float slider, 0-1)
    def update_threshold_from_slider(self, value):
        self.threshold_text.setText(f"{value / 100:.2f}")

    def update_threshold_from_text(self):
        try:
            value = float(self.threshold_text.text())
            if 0.0 <= value <= 1.0:
                self.threshold_slider.setValue(int(value * 100))
            else:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter a valid float between 0.0 and 1.0.")

    # Sync functions for Cross Percentage (float slider, 0-1)
    def update_cross_percentage_from_slider(self, value):
        self.cross_percentage_text.setText(f"{value / 100:.2f}")

    def update_cross_percentage_from_text(self):
        try:
            value = float(self.cross_percentage_text.text())
            if 0.0 <= value <= 1.0:
                self.cross_percentage_slider.setValue(int(value * 100))
            else:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter a valid float between 0.0 and 1.0.")

    # Sync functions for Scaling Factor (float slider, 0-1)
    def update_scaling_factor_from_slider(self, value):
        self.scaling_factor_text.setText(f"{value / 100:.2f}")

    def update_scaling_factor_from_text(self):
        try:
            value = float(self.scaling_factor_text.text())
            if 0.0 <= value <= 1.0:
                self.scaling_factor_slider.setValue(int(value * 100))
            else:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter a valid float between 0.0 and 1.0.")

    def save_input_values(self):
        """
        Saves the current input values to a config file for future runs.
        """
        config = {
            'image_file': self.image_path.text(),
            'true_time': self.true_time_slider.value(),
            'threshold': self.threshold_slider.value() / 100.0,
            'instrument_array': self.instrument_array_input.text(),
            'delay_vector': self.delay_vector_input.text(),
            'cross_percentage': self.cross_percentage_slider.value() / 100.0,
            'scaling_factor': self.scaling_factor_slider.value() / 100.0
        }

        with open('config.json', 'w') as config_file:
            json.dump(config, config_file)

    import os

    def load_input_values(self):
        """
        Loads saved input values from the config file if it exists.
        """
        if os.path.exists('config.json'):
            with open('config.json', 'r') as config_file:
                config = json.load(config_file)

                # Set the input fields based on loaded values
                self.image_path.setText(config.get('image_file', ''))
                self.true_time_slider.setValue(config.get('true_time', 30))
                self.threshold_slider.setValue(int(config.get('threshold', 0.5) * 100))
                self.instrument_array_input.setText(config.get('instrument_array', ''))
                self.delay_vector_input.setText(config.get('delay_vector', ''))
                self.cross_percentage_slider.setValue(int(config.get('cross_percentage', 0.5) * 100))
                self.scaling_factor_slider.setValue(int(config.get('scaling_factor', 0.5) * 100))
        else:
            # No config file, use default values
            self.true_time_slider.setValue(60)
            self.threshold_slider.setValue(50)
            self.cross_percentage_slider.setValue(75)
            self.scaling_factor_slider.setValue(20)


    def run_function(self):
        """
        This method retrieves input parameters from the UI and calls the existing function.
        """
        try:
            # Fetch input values from the UI
            image_file = self.image_path.text()
            true_time = self.true_time_slider.value()  # Get value from slider
            threshold = self.threshold_slider.value() / 100.0  # Convert to float between 0 and 1
            instrument_array = [item.strip() for item in self.instrument_array_input.text().split(',')]
            delay_vector = self.delay_vector_input.text().strip('[]')
            delay_vector = list(map(int, delay_vector.split(',')))  # Convert to list of ints
            cross_percentage = self.cross_percentage_slider.value() / 100.0  # Convert to float
            scaling_factor = self.scaling_factor_slider.value() / 100.0  # Convert to float

            # Save input values to config.json
            self.save_input_values()

            # Ensure instrument_array and delay_vector are the same size
            if len(instrument_array) != len(delay_vector):
                raise ValueError("Instrument Array and Delay Vector must have the same size.")

            # Call the existing function with parameters and provide the UI's continuation prompt
            run_script(
                image_name=image_file, true_time=true_time, instrument_array=instrument_array, delay_vector=delay_vector, continuation_prompt=self.prompt_user_to_continue, threshold=threshold, cross_percentage=cross_percentage, scaling_factor=scaling_factor
            )

            self.close()
        except ValueError as e:
            # If any conversion fails, show an error message
            QMessageBox.critical(self, 'Input Error', str(e))

    def prompt_user_to_continue(self):
        """
        Displays a dialog box that asks the user if they want to continue.
        This replaces the input() call in the existing function.
        """
        reply = QMessageBox.question(self, 'Continue?', 'Do you want to continue?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        return reply == QMessageBox.Yes


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    sys.exit(app.exec_())