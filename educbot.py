import google.generativeai as genai
import speech_recognition as sr
import whisper
import pyttsx3
import os
from pydub import AudioSegment
import warnings
import re
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from inteface import Ui_inteface

# Ignorando avisos do Whisper FP16
warnings.filterwarnings("ignore", category=UserWarning, message="FP16 is not supported on CPU")

# Configurando a API do Gemini
genai.configure(api_key="AIzaSyBzUqaF7-rT778ih4Mm0NAkIVTt2Ks5Ojk")
model = genai.GenerativeModel("gemini-1.5-flash")

# Inicializando bibliotecas
recognizer = sr.Recognizer()
engine = pyttsx3.init()
whisper_model = whisper.load_model("base")

# Configuração do pyttsx3
engine.setProperty('rate', 150)  
engine.setProperty('volume', 1.0)

# Temas permitidos
temas_permitidos = ["educação", "meio ambiente", "sustentabilidade"]
contexto_conversa = []

class Inteface(QMainWindow):  
    def __init__(self):
        super(Inteface, self).__init__()
        self.ui = Ui_inteface()
        self.ui.setupUi(self)

        # Conectando botões às funções
        self.ui.pushButton.clicked.connect(self.captura_audio)  # Botão "Escutar"
        self.ui.pushButton_2.clicked.connect(self.falar_resposta)  # Botão "Falar"

        # Variável para armazenar a última resposta do bot
        self.ultima_resposta = ""

    def verifica_tema(self, texto):
        texto = texto.lower()
        return any(tema in texto for tema in temas_permitidos)

    def chat_with_gpt(self, prompt):
        if not self.verifica_tema(prompt) and not contexto_conversa:
            return "Esse é um robô educacional focado em Educação, Meio Ambiente e Sustentabilidade. Você gostaria de saber como esses temas impactam o nosso futuro?"
        
        try:
            contexto_conversa.append(f"Usuário: {prompt}")
            prompt_completo = "\n".join(contexto_conversa) + "\nProfessor:"
            response = model.generate_content(prompt_completo)
            clean_response = re.sub(r'[*\\/]', '', response.text)
            contexto_conversa.append(f"Professor: {clean_response.strip()}")
            return clean_response.strip()
        except Exception as e:
            return f"Ocorreu um erro: {str(e)}"

    def speak(self, text):
        engine.say(text)
        engine.runAndWait()

    def captura_audio(self):
        """ Captura áudio do microfone e transcreve usando Whisper """
        with sr.Microphone() as source:
            self.ui.plainTextEdit.setPlainText("Ajustando o microfone para o ambiente...")
            recognizer.adjust_for_ambient_noise(source)
            self.ui.plainTextEdit.setPlainText("Escutando... Diga algo.")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
            audio_file = "captured_audio.wav"
            with open(audio_file, "wb") as f:
                f.write(audio.get_wav_data())

        # Converte para 16kHz para melhorar a transcrição
        converted_audio_file = self.convert_to_16kHz(audio_file)
        transcription = self.transcribe_audio(converted_audio_file if converted_audio_file else audio_file)

        if transcription:
            self.ui.textEdit.setText(transcription)  # Exibir no campo "Sua pergunta!"
            resposta = self.chat_with_gpt(transcription + "De forma resumida")
            self.ui.plainTextEdit.setPlainText(resposta)  # Exibir resposta
            self.ultima_resposta = resposta  # Guardar a última resposta

    def convert_to_16kHz(self, audio_file):
        """ Converte o áudio para 16kHz, mono e 16 bits PCM """
        try:
            audio = AudioSegment.from_file(audio_file)
            audio = audio.set_frame_rate(16000).set_channels(1).set_sample_width(2)
            converted_file = "temp_audio_16kHz.wav"
            audio.export(converted_file, format="wav")
            return converted_file
        except Exception as e:
            print(f"Erro ao converter áudio: {str(e)}")
            return None

    def transcribe_audio(self, audio_file):
        """ Transcreve áudio para texto com Whisper """
        try:
            if not os.path.exists(audio_file):
                return None
            result = whisper_model.transcribe(audio_file)
            return result['text']
        except Exception as e:
            print(f"Erro ao transcrever áudio: {str(e)}")
            return None

    def falar_resposta(self):
        """ Fala a última resposta do bot """
        if self.ultima_resposta:
            self.speak(self.ultima_resposta)

# Criando a aplicação
app = QApplication(sys.argv)
window = Inteface()
window.show()
sys.exit(app.exec_())
