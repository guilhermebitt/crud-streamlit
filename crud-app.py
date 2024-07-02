# Utilizando a biblioteca Streamlit e uma API de CEP, 
# crie um CRUD completo, com informações pessoais de um usuário:
# Nome, Telefone, e-mail e CPF, além do endereço completo a partir do CEP.
# Ao final, implemente um botão que exporte as informações preenchidas
# como um arquivo de texto (.txt) (Não se esqueça das devidas validações).

import requests
import streamlit as st

# STREAMLIT GUI
st.title('Trabalho Avaliativo 05')
st.markdown('Feito no Senac')
st.markdown('Tutor: Antônio')

error = False

def verifyName(name):
    error = False
    text_error = ''
    if name.replace(' ', '').isalpha() == False:
        error = True
        text_error = 'O nome deve conter apenas letras.'
    return error, text_error


def verifyPhone(telephone):
    error = False
    text_error = ''
    if telephone.isnumeric() == False:
        error = True
        text_error = 'O telefone deve conter números.'
    if len(telephone) != 10 and len(telephone) != 11:
        error = True
        text_error = 'O telefone deve conter dez digitos.'
    return error, text_error


def verifyEmail(email):
    error = False
    text_error = ''
    res = 'incorrect'
    if '@' in email:
        pos_at = email.find('@')
        if '.' in email[pos_at+2:] and email[-1] != '.':
            res = 'correct'
    if res != 'correct':
        error = True
        text_error = 'E-mail inválido.'
    return error, text_error


def verifyCpf(cpf):
    error = False
    text_error = ''
    if len(cpf) != 11:
        error = True
        text_error = 'O CPF deve conter apenas onze digitos.'
    if cpf.isnumeric() == False:
        error = True
        text_error = 'O CPF deve conter apenas números.'
    return error, text_error


def lookCep(cep):
    error = False
    try:
        url = f'https://viacep.com.br/ws/{cep}/json/'
        response = requests.get(url)
        dados = response.json()
        if 'erro' in dados:
            text_error = 'CEP inexistente'
            error = True
            return error, text_error
    except:
        text_error = f'CEP inválido. Código de erro: {response.status_code}'
        error = True
        return error, text_error
    else:
        return error, dados # logradouro -> rua / localidade -> cidade


name = str(st.text_input(label='Nome', )).strip()
error_name = verifyName(name)
if name and error_name[0] == True:
    st.error(error_name[1])
    error = True

telephone = str(st.text_input(label='Telefone', placeholder='Apenas números')).replace(' ', '')
error_tel = verifyPhone(telephone)
if telephone and error_tel[0] == True:
    st.error(error_tel[1])
    error = True

email = str(st.text_input(label='E-mail')).strip()
error_email = verifyEmail(email)
if email and error_email[0] == True:
    st.error(error_email[1])
    error = True

cpf = str(st.text_input(label='CPF', placeholder='Apenas números')).strip()
error_cpf = verifyCpf(cpf)
if cpf and error_cpf[0] == True:
    st.error(error_cpf[1])
    error = True

cep = str(st.text_input(label='CEP', placeholder='Apenas números')).strip()
error_cep = lookCep(cep)
if cep and error_cep[0] == True:
    st.error(error_cep[1])
    error = True
else:
    address = lookCep(cep)[1]

if name and telephone and email and cpf and cep and error == False:
    dados = f'''Nome: {name}
telefone: {telephone}
E-mail: {email}
CPF: {cpf}
Endereço: Cidade: {address['localidade']} | Bairro {address['bairro']} | Rua: {address['logradouro']}
'''

    st.download_button('Exportar Informações', str(dados), 'user-info.txt')

