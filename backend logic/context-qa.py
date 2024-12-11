import transformers
from transformers import AutoTokenizer, AutoModelForQuestionAnswering
transformers.logging.set_verbosity_error()
import torch
from newspaper import Article
import PyPDF2
import speech_recognition as sr

# Load tokenizer and model
model_name = "bert-large-uncased-whole-word-masking-finetuned-squad"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForQuestionAnswering.from_pretrained(model_name)

def transcribe_audio(audio_path):
    # Initialize the recognizer
    recognizer = sr.Recognizer()

    try:
        # Load the audio file
        with sr.AudioFile(audio_path) as source:
            print("Processing audio...")
            audio_data = recognizer.record(source)  # Read the entire audio file

        # Transcribe audio to text
        text = recognizer.recognize_google(audio_data)
        return text

    except Exception as e:
        return f"An error occurred: {e}"

def extract_text_from_pdf(pdf_path):
    try:
        # Open the PDF file in read-binary mode
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""

            # Iterate through all the pages
            for page in reader.pages:
                text += page.extract_text()

            return text

    except Exception as e:
        return f"An error occurred: {e}"

def extract_main_text(url):
    try:
        # Download and parse the article
        article = Article(url)
        article.download()
        article.parse()

        # Extract the main content
        return article.text

    except Exception as e:
        return f"An error occurred: {e}"

# Function to get the answer
def get_answer(context, question):
    inputs = tokenizer.encode_plus(question, context, return_tensors="pt")
    input_ids = inputs["input_ids"].tolist()[0]

    # Get the model's output
    outputs = model(**inputs)
    start_scores = outputs.start_logits
    end_scores = outputs.end_logits

    # Find the start and end of the answer
    answer_start = torch.argmax(start_scores)
    answer_end = torch.argmax(end_scores) + 1

    # Convert tokens to string
    answer = tokenizer.convert_tokens_to_string(
        tokenizer.convert_ids_to_tokens(input_ids[answer_start:answer_end])
    )
    return answer

# Example paragraph and question
# context = """
# The Amazon rainforest, also known as Amazonia, is a vast tropical rainforest in South America. 
# It covers approximately 5.5 million square kilometers and is home to millions of species, many of which are not found anywhere else on Earth. 
# The Amazon is often referred to as the "lungs of the planet" due to its role in absorbing carbon dioxide and producing oxygen.
# """
# question = "How much area does amazon raiforest cover?"

# Get and print the answer
# context = extract_main_text("https://en.wikipedia.org/wiki/Artos_(drink)")

context = extract_text_from_pdf(r"backend logic\testpdf.pdf")

# context = transcribe_audio(r"backend logic\testaudio.wav")

question = "What is Artos?"

answer = get_answer(context, question)
print(f"Answer: {answer}")
