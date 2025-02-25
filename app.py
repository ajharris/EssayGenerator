import sys

from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QTextEdit, QComboBox
import openai
import docx
import config

client = openai.OpenAI(api_key=config.API_KEY)

class EssayGenerator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.setWindowTitle("Essay Generator")
        self.setGeometry (300, 300, 1200, 800)

        topic_label = QLabel('Enter the topic: ', self)
        topic_label.move(20, 40)

        self.topic_input = QLineEdit(self)
        self.topic_input.move(20, 100)
        self.topic_input.resize(1000, 30)

        generate_button = QPushButton("Generate Essay", self)
        generate_button.move(1050, 100)
        generate_button.clicked.connect(self.generate_essay)

        save_button = QPushButton("Save", self)
        save_button.move(20, 655)
        save_button.clicked.connect(self.save_essay)

    def generate_essay(self):
        topic = self.topic_input.text()
        tokens = 500

        engine = "gpt-4"

        prompt = f"Write an {tokens/1.5} words essay on the following topic: {topic}\n\n"

        response = client.completions.create(
            model = engine,
            messages = [
                {"role": "user", "content": "You are a professional essay writer."},
                {"role": "assistant", "content":"OK"},
                {"role": "user", "content": f"{prompt}"}]
        )

    def save_essay(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = EssayGenerator()
    ex.show()
    sys.exit(app.exec())
