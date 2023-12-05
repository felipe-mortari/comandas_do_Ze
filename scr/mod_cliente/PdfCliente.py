from reportlab.pdfgen import canvas

def gerar_pdf_cliente(nome_arquivo, dados_cliente):
    c = canvas.Canvas(nome_arquivo)
    c.drawString(72, 800, f"Detalhes do Cliente:")
    c.drawString(72, 780, f"Nome: {dados_cliente['nome']}")
    c.drawString(72, 760, f"CPF: {dados_cliente['cpf']}")
    # Adicione mais detalhes conforme necessário
    c.save()

# Exemplo de uso
dados_cliente = {'nome': 'Maria Oliveira', 'cpf': '98765432109', 'telefone': '555-555-5555'}
gerar_pdf_cliente("cliente.pdf", dados_cliente)
