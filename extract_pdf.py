import re
from pathlib import Path

import pandas as pd
import pdfplumber

from core import logger


def clean_currency_value(value: str) -> float:
    """Converte string de moeda brasileira para float."""
    if not value or value == '':
        return 0.0
    
    cleaned = value.replace('R$', '').strip()
    cleaned = cleaned.replace('.', '')
    cleaned = cleaned.replace(',', '.')
    
    try:
        return float(cleaned)
    except ValueError:
        return 0.0


def parse_line_comprehensive(line: str, page_num: int) -> dict:
    """
    Faz parsing de uma linha do relatório de forma abrangente.
    Retorna None se a linha não for válida.
    """
    # Remove espaços extras
    line = ' '.join(line.split())
    
    # Verifica se começa com data
    if not re.match(r'^\d{2}/\d{2}/\d{4}', line):
        return None
    
    # Ignora linhas de totais e cabeçalhos
    if any(x in line for x in ['Σ', 'Total', 'Reg:', 'Dt. Atendimento', 'Cód.Usuario']):
        return None
    
    try:
        # Extrai a data (primeiro campo)
        data_match = re.match(r'^(\d{2}/\d{2}/\d{4})', line)
        if not data_match:
            return None
        data_atendimento = data_match.group(1)
        resto = line[len(data_atendimento):].strip()
        
        # Extrai o valor (último campo com R$)
        valor_match = re.search(r'R\$\s*([\d.,]+)$', resto)
        if not valor_match:
            return None
        valor_liberado = clean_currency_value(valor_match.group(1))
        resto = resto[:valor_match.start()].strip()
        
        # Extrai quantidade (número antes do valor)
        qtde_match = re.search(r'(\d+)\s*$', resto)
        if not qtde_match:
            return None
        quantidade = int(qtde_match.group(1))
        resto = resto[:qtde_match.start()].strip()
        
        # Tudo que sobrou entre data e quantidade contém:
        # código_usuario, nome_usuario, código_tuss e procedimento
        
        # Separa por espaços
        partes = resto.split()
        
        if len(partes) < 4:
            return None
        
        # Código do usuário é o primeiro (formato: XXXX.XX.XXXXX.XX-X)
        codigo_usuario = partes[0]
        
        # Procura código TUSS (número de 8 dígitos)
        codigo_tuss = None
        tuss_idx = None
        for i, parte in enumerate(partes[1:], 1):
            if re.match(r'^\d{8}$', parte):
                codigo_tuss = parte
                tuss_idx = i
                break
        
        if not codigo_tuss:
            return None
        
        # Nome do usuário está entre código_usuario e código_tuss
        nome_usuario = ' '.join(partes[1:tuss_idx])
        
        # Procedimento está entre código_tuss e quantidade
        procedimento = ' '.join(partes[tuss_idx+1:])
        
        return {
            'data_atendimento': data_atendimento,
            'codigo_usuario': codigo_usuario,
            'nome_usuario': nome_usuario,
            'codigo_tuss': codigo_tuss,
            'procedimento': procedimento,
            'quantidade': quantidade,
            'valor_liberado': valor_liberado,
            'pagina_pdf': page_num
        }
    
    except Exception as e:
        return None


def extract_from_pdf(pdf_path: str) -> pd.DataFrame:
    """
    Extrai todos os dados do PDF.
    """
    all_data = []
    
    with pdfplumber.open(pdf_path) as pdf:
        logger.info(f"Processando PDF com {len(pdf.pages)} páginas...")
        
        for page_num, page in enumerate(pdf.pages, 1):
            logger.debug(f"Processando página {page_num}/{len(pdf.pages)}...")
            
            text = page.extract_text()
            if not text:
                logger.warning(f"Página {page_num}: sem texto")
                continue
            
            lines = text.split('\n')
            records_found = 0
            
            for line in lines:
                data = parse_line_comprehensive(line, page_num)
                if data:
                    all_data.append(data)
                    records_found += 1
            
            logger.info(f"Página {page_num}: {records_found} registros")
    
    if all_data:
        df = pd.DataFrame(all_data)
        logger.success(f"Total de registros extraídos: {len(df)}")
        return df
    else:
        logger.warning("Nenhum dado foi extraído")
        return pd.DataFrame()


def generate_summary(df: pd.DataFrame):
    """Gera resumo estatístico."""
    logger.info("=" * 70)
    logger.info("RESUMO DOS DADOS EXTRAÍDOS")
    logger.info("=" * 70)

    logger.info(f"Total de registros: {len(df)}")

    if len(df) > 0:
        logger.info("Estatísticas Financeiras:")
        logger.info(f"   Valor total liberado: R$ {df['valor_liberado'].sum():,.2f}")
        logger.info(f"   Valor médio por atendimento: R$ {df['valor_liberado'].mean():,.2f}")
        logger.info(f"   Valor mínimo: R$ {df['valor_liberado'].min():,.2f}")
        logger.info(f"   Valor máximo: R$ {df['valor_liberado'].max():,.2f}")

        logger.info("Período:")
        if not df['data_atendimento'].empty:
            datas = pd.to_datetime(df['data_atendimento'], format='%d/%m/%Y', errors='coerce')
            if not datas.isna().all():
                logger.info(f"   Primeira data: {datas.min().strftime('%d/%m/%Y')}")
                logger.info(f"   Última data: {datas.max().strftime('%d/%m/%Y')}")

        logger.info("Pacientes:")
        logger.info(f"   Total de pacientes únicos: {df['nome_usuario'].nunique()}")

        logger.info("Procedimentos:")
        logger.info(f"   Total de tipos de procedimentos: {df['procedimento'].nunique()}")
        logger.info(f"   Total de procedimentos realizados: {df['quantidade'].sum()}")

        logger.info("Top 10 Procedimentos mais realizados:")
        top_procedures = df.groupby('procedimento').agg({
            'quantidade': 'sum',
            'valor_liberado': 'sum'
        }).sort_values('quantidade', ascending=False).head(10)

        for i, (proc, row) in enumerate(top_procedures.iterrows(), 1):
            proc_short = proc[:60] + '...' if len(proc) > 60 else proc
            logger.info(f"   {i:2d}. {proc_short:<63} | {int(row['quantidade']):3d}x | R$ {row['valor_liberado']:>10,.2f}")

        logger.info("Top 10 Procedimentos por valor total:")
        top_values = df.groupby('procedimento').agg({
            'quantidade': 'sum',
            'valor_liberado': 'sum'
        }).sort_values('valor_liberado', ascending=False).head(10)

        for i, (proc, row) in enumerate(top_values.iterrows(), 1):
            proc_short = proc[:60] + '...' if len(proc) > 60 else proc
            logger.info(f"   {i:2d}. {proc_short:<63} | {int(row['quantidade']):3d}x | R$ {row['valor_liberado']:>10,.2f}")

        logger.info("Top 10 Pacientes por valor de atendimento:")
        top_patients = df.groupby('nome_usuario')['valor_liberado'].sum().sort_values(ascending=False).head(10)
        for i, (patient, value) in enumerate(top_patients.items(), 1):
            patient_short = patient[:50] + '...' if len(patient) > 50 else patient
            logger.info(f"   {i:2d}. {patient_short:<53} | R$ {value:>10,.2f}")


def save_to_excel(df: pd.DataFrame, output_path: str):
    """Salva em Excel com formatação."""
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Atendimentos')
        
        worksheet = writer.sheets['Atendimentos']
        
        # Ajusta larguras
        column_widths = {
            'A': 18,  # data_atendimento
            'B': 22,  # codigo_usuario
            'C': 40,  # nome_usuario
            'D': 12,  # codigo_tuss
            'E': 70,  # procedimento
            'F': 12,  # quantidade
            'G': 15,  # valor_liberado
            'H': 12,  # pagina_pdf
        }
        
        for col, width in column_widths.items():
            worksheet.column_dimensions[col].width = width
    
    logger.success(f"Arquivo Excel salvo: {output_path}")


def save_to_csv(df: pd.DataFrame, output_path: str):
    """Salva em CSV."""
    df.to_csv(output_path, index=False, encoding='utf-8-sig', sep=';')
    logger.success(f"Arquivo CSV salvo: {output_path}")


def main():
    """Função principal."""
    pdf_path = "./data/98663RELATORIO_ATENDIMENTO_01_2026.pdf"
    output_dir = Path("./data")
    
    logger.info("=" * 70)
    logger.info("EXTRAÇÃO DE DADOS - RELATÓRIO DE ATENDIMENTOS PDF")
    logger.info("=" * 70)
    
    # Extrai dados
    df = extract_from_pdf(pdf_path)
    
    if not df.empty:
        # Gera resumo
        generate_summary(df)
        
        # Salva arquivos
        logger.info("=" * 70)
        logger.info("SALVANDO ARQUIVOS")
        logger.info("=" * 70)
        
        excel_path = output_dir / "relatorio_atendimentos_extraido.xlsx"
        csv_path = output_dir / "relatorio_atendimentos_extraido.csv"
        
        save_to_excel(df, str(excel_path))
        save_to_csv(df, str(csv_path))
        
        # Estatísticas finais
        logger.info("Estatísticas Gerais:")
        logger.info(f"   {len(df)} registros em {df['pagina_pdf'].nunique()} páginas")
        logger.info(f"   {df['nome_usuario'].nunique()} pacientes únicos")
        logger.info(f"   {df['procedimento'].nunique()} tipos de procedimentos")
        logger.info(f"   R$ {df['valor_liberado'].sum():,.2f} em valores liberados")

        logger.info("=" * 70)
        logger.success("EXTRAÇÃO CONCLUÍDA COM SUCESSO!")
        logger.info("=" * 70)
    else:
        logger.error("Não foi possível extrair dados do PDF.")


if __name__ == "__main__":
    main()