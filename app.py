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

        self.essay_output = QTextEdit(self)
        self.essay_output.move(20, 150)
        self.essay_output.resize(1150, 500)

        length_label = QLabel('Select Essay Length:', self)
        length_label.move(327, 40)
        self.length_dropdown = QComboBox(self)
        self.length_dropdown.move(320, 60)
        self.length_dropdown.addItems(["500", "1000", "2000", "3000",
        "4000"])

        generate_button = QPushButton("Generate Essay", self)
        generate_button.move(1050, 100)
        generate_button.clicked.connect(self.generate_essay)

        save_button = QPushButton("Save", self)
        save_button.move(20, 655)
        save_button.clicked.connect(self.save_essay)

    def generate_essay(self):
        topic = self.topic_input.text()

        tokens = int(self.length_dropdown.currentText())

        engine = "gpt-4"

        prompt = f"Write an {tokens/1.5} words essay on the following topic: {topic}\n\n"

        response = client.chat.completions.create(
            model = engine,
            messages = [
                {"role": "user", "content": "You are a professional essay writer. Please be sure to include a concluding statement and a thesis statement, and don't stop in the middle of a sentence."},
                {"role": "assistant", "content":"Sure, I can help you with that. Please provide me with the topic you would like me to write about."},
                {"role": "user", "content": f"{prompt}"}],
                max_tokens = tokens)
        essay = response.choices[0].message.content
        self.essay_output.setText(essay)

    def save_essay(self):
        topic = self.topic_input.text()
        final_text = self.essay_output.toPlainText()
        document = docx.Document()
        document.add_paragraph(final_text)
        document.save(topic + ".docx")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = EssayGenerator()
    ex.show()
    sys.exit(app.exec())
