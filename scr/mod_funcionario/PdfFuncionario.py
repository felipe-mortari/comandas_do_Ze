from fpdf import FPDF
from datetime import datetime
import requests
from settings import HEADERS_API, ENDPOINT_FUNCIONARIO

class PDF(FPDF):
    def header(self):

        self.set_font('helvetica', 'B', 15)
        self.cell(0, 5, 'Abc Bolinhas', 0, 1, 'C', 0)
        self.ln(5)
   
    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.cell(0, 10, 'Página ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')
    
    def listaTodos(self):
        pdf = PDF(orientation="P", unit="mm", format="A4") 
        pdf.set_author("Joao")
        pdf.set_title('Funcionários')
        pdf.alias_nb_pages() 
        pdf.add_page()
   
        pdf.set_font('helvetica', 'b', 12)
        pdf.cell(190, 5, 'Funcionários', 0, 1, 'C', 0)
        pdf.set_font('helvetica', '', 6)
        pdf.cell(190, 4, "Emitido em: " + str(datetime.now()), 0, 1, 'R')
        pdf.ln(5)
       
        pdf.set_font('helvetica', 'B', 8)
        pdf.cell(20, 5, 'ID', 0, 0, 'L')
        pdf.cell(20, 5, 'Nome', 0, 0, 'L')
        pdf.cell(20, 5, 'Matrícula', 0, 0, 'L')
        pdf.cell(30, 5, 'CPF', 0, 0, 'L')
        pdf.cell(30, 5, 'Telefone', 0, 0, 'L')
        pdf.cell(20, 5, 'Grupo', 0, 0, 'L')
        pdf.cell(20, 5, 'Senha', 0, 1, 'L')

    
        pdf.set_font('helvetica', '', 8)
        try:
            response = requests.get(ENDPOINT_FUNCIONARIO, headers=HEADERS_API)
            result = response.json()
            if (response.status_code != 200):
                raise Exception(result[0])
            for row in result[0]:
                pdf.cell(20, 5, str(row['id_funcionario']), 0, 0, 'L')
                pdf.cell(20, 5, str(row['nome']), 0, 0, 'L')
                pdf.cell(20, 5, str(row['matricula']), 0, 0, 'L')
                pdf.cell(30, 5, str(row['cpf']), 0, 0, 'L')
                pdf.cell(30, 5, str(row['telefone']), 0, 0, 'L')
                pdf.cell(20, 5, str(row['grupo']), 0, 0, 'L')
                pdf.cell(20, 5, str(row['senha']), 0, 1, 'L')


        except Exception as e:
            pdf.multi_cell(190, 5, 'ERRO: ' + str(e.args[0]), 1, 'J', False)
        
        pdf.output("pdfFuncionarios.pdf")