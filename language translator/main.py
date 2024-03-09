import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QComboBox, QLabel, QPushButton, QLineEdit
from PyQt5.QtGui import QPixmap
from googletrans import LANGUAGES, Translator


class LanguageTranslatorApp(QWidget):
    def __init__(self):
        super().__init__()

        self.from_country = None
        self.to_country = None

        self.init_ui()

    def init_ui(self):
        x = 110
        self.setGeometry(300, 100, 500, 800)
        self.setWindowTitle("Language Translator")
        self.setStyleSheet("background-color: #484558; border-radius: 15px;")

        labelcl = QLabel('CHOOSE LANGUAGE', self)
        labelcl.setStyleSheet('color: white; font-size: 30px;')
        labelcl.move(x, 70)

        self.combo_box = QComboBox(self)
        self.combo_box.addItem("Search From Country")
        self.combo_box.setStyleSheet('font-size: 18px; border: 2px solid white; border-radius: 15px; padding: 5px; background-color: #484558; color: white;')
        self.combo_box.setGeometry(x, 150, 300, 40)
        
        for lang_code, lang_name in sorted(LANGUAGES.items()):
            self.combo_box.addItem(lang_name, lang_code)

        self.combo_box.activated[str].connect(self.on_language_selected)

        labelfrom = QLabel('From ', self)
        labelfrom.setStyleSheet('color: white; font-size: 25px;')
        labelfrom.move(x, 250)

        self.from_country = None
        self.text_fieldFrom = QLabel(self.from_country, self)
        self.text_fieldFrom.setGeometry(x, 300, 300, 40)
        self.text_fieldFrom.setStyleSheet('font-size: 25px; border-radius: 15px; background-color: #636272; ')

        arrow_label = QLabel(self)
        arrow_label.setPixmap(QPixmap("arrow.png"))
        arrow_label.setGeometry(x + 90, 360, 100, 122)

        labelTo = QLabel('To ', self)
        labelTo.setStyleSheet('color: white; font-size: 25px;')
        labelTo.move(x, 480)

        self.to_country = None
        self.text_fieldTo = QLabel(self.to_country, self)
        self.text_fieldTo.setGeometry(x, 520, 300, 40)
        self.text_fieldTo.setStyleSheet('font-size: 25px; border-radius: 15px; background-color: #636272; ')

        ButonStart = QPushButton('Start', self)
        ButonStart.setGeometry(x + 140, 600, 140, 40)
        ButonStart.setStyleSheet('font-size: 25px; border-radius: 15px; background-color: #E6533F; font-weight: bold;')
        ButonStart.clicked.connect(self.open_translation_window)

        ButtonReset = QPushButton('Reset', self)
        ButtonReset.setGeometry(x , 600, 140, 40)
        ButtonReset.setStyleSheet('font-size: 25px; border-radius: 15px; background-color: #E6533F; font-weight: bold;')
        ButtonReset.clicked.connect(self.reset_countries)

        self.show()

    def on_language_selected(self, text):
        if text == "Search From Country":
            return

        if self.from_country is None:
            self.from_country = text
            self.text_fieldFrom.setText(f"{self.from_country}")
            #self.combo_box.clear()
            self.combo_box.addItem(f"Select To Country ({self.from_country})")

        elif self.to_country is None:
            self.to_country = text
            self.text_fieldTo.setText(f"{self.to_country}")
            # Add your code to perform actions based on the selected countries
    def reset_countries(self):
        self.from_country = None
        self.to_country = None
        self.text_fieldFrom.setText(f"{self.from_country}")
        self.text_fieldTo.setText(f"{self.to_country}")
    def open_translation_window(self):
        if self.from_country is not None and self.to_country is not None:
            if hasattr(self, 'translation_window') and self.translation_window:
                self.translation_window.close() 
            self.translation_window = TranslationWindow(self, self.from_country, self.to_country)
            self.translation_window.setWindowFlags(Qt.Window)
            self.translation_window.show()


class TranslationWindow(QWidget):
    def __init__(self, parent=None, from_country_code=None, to_country_code = None):
        super(TranslationWindow, self).__init__(parent)
        self.from_country_code = from_country_code
        self.to_country_code = to_country_code
        self.setWindowTitle('Translation Window')
        self.setGeometry(300, 100, 500, 800)
        self.setStyleSheet("background-color: #484558; border-radius: 15px;")

        LabelEnterText = QLabel("Enter text", self)
        LabelEnterText.setStyleSheet('color: white; font-size: 30px;')
        LabelEnterText.move(110, 70)

        self.textFieldEnterText = QLineEdit(self)
        self.textFieldEnterText.setGeometry(50, 120, 400, 200)
        self.textFieldEnterText.setStyleSheet('font-size: 25px; border-radius: 15px; background-color: white; ')

        ButonSubmit = QPushButton('Submit', self)
        ButonSubmit.setGeometry(180, 350, 140, 40)
        ButonSubmit.setStyleSheet('font-size: 25px; border-radius: 15px; background-color: #E6533F; font-weight: bold;')
        ButonSubmit.clicked.connect(self.translate_text)

        LabelTranslation = QLabel("Translated text", self)
        LabelTranslation.setStyleSheet('color: white; font-size: 30px;')  
        LabelTranslation.move(110, 410)

        self.textFieldTranslation = QLineEdit(self)
        self.textFieldTranslation.setGeometry(50, 450, 400, 250)
        self.textFieldTranslation.setStyleSheet('font-size: 25px; border-radius: 15px; background-color: white; ')
    def translate_text(self):
        text_to_translate = self.textFieldEnterText.text()
        
        # Replace 'en' and 'fr' with the source and target language codes as needed
        translator = Translator()
        translated_text = translator.translate(text_to_translate, src=self.from_country_code, dest=self.to_country_code).text

        self.textFieldTranslation.setText(translated_text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LanguageTranslatorApp()
    sys.exit(app.exec_())
