# EducBot - Assistente de IA com Interface Gráfica

## Sobre o Projeto

O **EducBot** é um assistente de IA desenvolvido para auxiliar em temas de **educação, meio ambiente e sustentabilidade**. Ele utiliza reconhecimento de voz para receber perguntas do usuário, processa as respostas utilizando o modelo **Gemini AI** e fala a resposta de volta para o usuário. Tudo isso é feito dentro de uma interface gráfica amigável usando **PyQt5**.

### Funcionalidades
- Reconhece perguntas via **comando de voz**
- Exibe a transcrição do que foi dito na interface
- Gera respostas utilizando a API do **Google Gemini AI**
- Exibe a resposta na interface
- Lê a resposta em voz alta utilizando **pyttsx3**

---
## Instalação e Configuração

### **1. Requisitos**

Certifique-se de ter instalado:
- Python 3.8 ou superior
- Pip atualizado (`python -m pip install --upgrade pip`)

### **2. Clonando o Repositório**

```bash
git clone https://github.com/Batinga017/EducBot.git
cd educbot
```

### **3. Criando um Ambiente Virtual**

Para evitar conflitos de dependências, é recomendado usar um ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

### **4. Instalando Dependências**

Instale todas as bibliotecas necessárias:

```bash
pip install -r requirements.txt
```

Se não houver um `requirements.txt`, instale manualmente:

```bash
pip install google-generativeai speechrecognition whisper openai pydub pyttsx3 pyqt5
```

### **5. Configurando a API do Gemini**

Crie um arquivo `.env` na raiz do projeto e adicione sua chave de API:

```bash
GEMINI_API_KEY=SUACHAVEAQUI
```

Se preferir, edite diretamente no código, alterando esta linha em `pepper.py`:

```python
genai.configure(api_key="SUA_CHAVE_AQUI")
```

### **6. Executando o Projeto**

Agora, rode o seguinte comando para iniciar o EducBot:

```bash
python pepper.py
```

---
## Uso do EducBot

### **Fluxo de Interação**

1. **Clique no botão "Escutar"** para capturar sua pergunta via microfone.
2. O texto reconhecido aparecerá no campo "Sua pergunta!".
3. O EducBot processa sua pergunta e gera uma resposta.
4. A resposta é exibida no campo "Resposta:".
5. **Clique no botão "Falar"** para ouvir a resposta em voz alta.

### **Atenção aos Temas**
O EducBot foca nos seguintes temas:
- **Educação**
- **Meio Ambiente**
- **Sustentabilidade**

Perguntas fora desses temas podem não ser respondidas corretamente.

---
## Problemas Conhecidos e Soluções

### 1. **Erro ao capturar áudio**
- Verifique se o microfone está funcionando e reconhecido pelo sistema.
- Teste com:
  ```bash
  python -m speech_recognition
  ```

### 2. **Erro na execução da API do Gemini**
- Confirme que sua chave de API está correta.
- Tente rodar:
  ```python
  import google.generativeai as genai
  genai.configure(api_key="SUA_CHAVE_AQUI")
  print(genai.GenerativeModel("gemini-1.5-flash").generate_content("Teste").text)
  ```

### 3. **Respostas lidas de forma errada**
- Ajuste a velocidade da voz no `pepper.py`:
  ```python
  engine.setProperty('rate', 150)  # Diminua se estiver muito rápido
  ```

---
## Contribuição
Se quiser contribuir com melhorias, faça um **fork** do projeto e envie um **pull request**.

---
