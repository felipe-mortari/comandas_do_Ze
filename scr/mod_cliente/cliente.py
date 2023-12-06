import requests
from settings import HEADERS_API, ENDPOINT_CLIENTE
from flask import send_file
from mod_cliente.PdfCliente import PDF
from funcoes import Funcoes
from flask import Blueprint, render_template ,request, redirect, url_for, jsonify
bp_cliente = Blueprint('cliente', __name__, url_prefix="/cliente", template_folder='templates')

''' rotas dos formulários '''
@bp_cliente.route('/',methods=['GET', 'POST'])

def formListaCliente():
    try:
        response = requests.get(ENDPOINT_CLIENTE, headers=HEADERS_API)
        result = response.json()

        if (response.status_code != 200):
            raise Exception(result[0])

        return render_template('formListaCliente.html', result=result[0])
    except Exception as e:
        return render_template('formListaCliente.html', msgErro=e.args[0])

@bp_cliente.route('/form-cliente/', methods=['GET'])

def formCliente():
  return render_template('formCliente.html')

@bp_cliente.route('/insert', methods=['POST'])

def insert():
    try: 
        # dados enviados via FORM
        id_cliente = request.form['id']
        nome = request.form['nome']
        cpf = request.form['cpf']
        telefone = request.form['telefone']
        compra_fiado = request.form['compra_fiado']
        dia_fiado = request.form['dia_fiado']
        senha = Funcoes.cifraSenha(request.form['senha'])
        
        ##monta o JSON para envio a API
        payload = {'id_cliente': id_cliente, 'nome': nome, 'cpf': cpf, 'telefone': telefone,'compra_fiado': compra_fiado,'dia_fiado': dia_fiado, 'senha': senha}
        # executa o verbo POST da API e armazena seu retorno
        response = requests.post(ENDPOINT_CLIENTE, headers=HEADERS_API, json=payload)
        result = response.json()

        print(result[0])
        print(result) # [{'msg': 'Cadastrado com sucesso!', 'id': 13}, 200]
        print(response.status_code) # 200

        if (response.status_code != 200 or result[1] != 200):
            raise Exception(result[0])

        #return render_template('formListaCliente.html', msg=result[0])
        return redirect(url_for('cliente.formListaCliente', msg=result[0]))

    except Exception as e:
       
        return render_template('formListaCliente.html', msgErro=e.args[0])

@bp_cliente.route("/form-edit-cliente", methods=['POST'])

def formEditCliente():
    try:
        # ID enviado via FORM
        id_cliente = request.form['id']
        # executa o verbo GET da API buscando somente o cliente selecionado,
        
        # obtendo o JSON do retorno
        response = requests.get(ENDPOINT_CLIENTE + id_cliente, headers=HEADERS_API)
        result = response.json()
         
        if (response.status_code != 200):
          raise Exception(result[0])
       
        # renderiza o form passando os dados retornados
        return render_template('formCliente.html', result=result[0])
    
    except Exception as e:
      print(e.args[0])
      return render_template('formListaCliente.html', msgErro=e.args[0])

@bp_cliente.route('/edit', methods=['POST'])

def edit():
    try:
        # dados enviados via FORM
        id_cliente = request.form['id']
        nome = request.form['nome']
        cpf = request.form['cpf']
        telefone = request.form['telefone']
        compra_fiado = request.form['compra_fiado']
        dia_fiado = request.form['dia_fiado']
        senha = Funcoes.cifraSenha(request.form['senha'])
        
        #monta o JSON para envio a API
        payload = {'id': id_cliente, 'nome': nome, 'cpf': cpf, 'telefone': telefone,'compra_fiado': compra_fiado,'dia_fiado': dia_fiado, 'senha': senha}

        # executa o verbo PUT da API e armazena seu retorno
        response = requests.put(ENDPOINT_CLIENTE + id_cliente, headers=HEADERS_API, json=payload)
        result = response.json()
      
        if (response.status_code != 200 or result[1] != 200):
            raise Exception(result[0])
      
        return redirect(url_for('cliente.formListaCliente', msg=result[0]))
    
    except Exception as e:
      return render_template('formListaCliente.html', msgErro=e.args[0])

@bp_cliente.route('/delete', methods=['POST'])

def delete():
    try:
      # dados enviados via FORM
      id_cliente = request.form['id_cliente']
      
      # executa o verbo DELETE da API e armazena seu retorno
      response = requests.delete(ENDPOINT_CLIENTE + id_cliente, headers=HEADERS_API)
      result = response.json()
      
      print(result)
      
      if (response.status_code != 200 or result[1] != 201):
        raise Exception(result[0])
      
      # return redirect(url_for('funcionario.formListaFuncionario', msg=result[0]))
      return jsonify(erro=False, msg=result[0])
    except Exception as e:
      # return render_template('formListaFuncionario.html', msgErro=e.args[0])
      return jsonify(erro=True, msgErro=e.args[0])
    
@bp_cliente.route('/pdfTodos', methods=['GET', 'POST'])

def pdfTodos():
      geraPdf = PDF()
      geraPdf.listaTodos()
      return send_file('../pdfClientes.pdf')