import fitz  # PyMuPDF
import pandas as pd

# Function to determine if a line is a question
def is_question(line):
    line = line.strip()
    return len(line) > 1 and line[0].isdigit() and (line[1] == '.' or line[1] == ')')

# Open the PDF file
file_path = 'CuestionarioTDF2021ServiciosFinal.pdf'
doc = fitz.open(file_path)

# Prepare a list to store the questions and options
questions = []
current_question = None
current_options = []
current_page = None

# Iterate through the pages and paragraphs to find questions and options
for page_num in range(len(doc)):
    page = doc.load_page(page_num)
    text = page.get_text("text")
    lines = text.split('\n')
    
    for line in lines:
        if is_question(line):
            if current_question:
                # If already a current question, store the previous question and its options
                questions.append({'Question': current_question, 'Options': current_options, 'Page': current_page})
                current_options = []
            current_question = line.strip()
            current_page = page_num + 1  # Page numbers are 1-based
        elif line.strip():
            current_options.append(line.strip())

# Add the last question and options
if current_question:
    questions.append({'Question': current_question, 'Options': current_options, 'Page': current_page})

# Create a DataFrame
data = []
for q in questions:
    question = q['Question']
    options = q['Options']
    page = q['Page']
    if not options:  # If no options, add a row without options
        data.append({'Question': question, 'Option': '', 'Page': page})
    else:
        for option in options:
            data.append({'Question': question, 'Option': option, 'Page': page})

df = pd.DataFrame(data)

# Save to an Excel file
output_path = 'archivo.xlsx'
df.to_excel(output_path, index=False)

print(f"Archivo Excel generado en: {output_path}")
