#%%
import pdfplumber
import re

#%%
pdf_path = "./data/98663RELATORIO_ATENDIMENTO_01_2026.pdf"

base_service = "./data/202601_atendimentos_sao_lucas.csv"

#%%
with pdfplumber.open(pdf_path) as pdf:
    for page_num, page in enumerate(pdf.pages, 1):
        if page_num == 1:
            text = page.extract_text()
            
            if not text:
                continue

            lines = text.split('\n')
        

# %%
for line in lines:
    if re.match(r'^\d{2}/\d{2}/\d{4}', line):
        print(line)

# %%
def extrat_service_date(line: str) -> str:
    match = re.match(r'^(\d{2}/\d{2}/\d{4})', line)
    return match.group(1) if match else None

def extract_user_code(line: str) -> str:
    match = re.search(r'(\d{4}.\d{2}.\d{5}.\d{2}-\d{1})', line)
    return match.group(1) if match else None