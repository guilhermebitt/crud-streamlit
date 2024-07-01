# Utilizando a biblioteca Streamlit e uma API de CEP, 
# crie um CRUD completo, com informações pessoais de um usuário:
# Nome, Telefone, e-mail e CPF, além do endereço completo a partir do CEP.
# Ao final, implemente um botão que exporte as informações preenchidas
# como um arquivo de texto (.txt) (Não se esqueça das devidas validações).

import requests
import streamlit as st

def verifyName(name):
    error = False
    text_error = ''
    if name.strip().isalpha() == False or name.count(' ') >= 1:
        error = True
        text_error = 'O nome deve conter apenas letras.'
    return error, text_error


def verifyPhone(telephone):
    error = False
    text_error = ''
    if telephone.isnumeric() == False:
        error = True
        text_error = 'O telefone deve conter apenas números.'
    if len(telephone) != 10:
        error = True
        text_error = 'O telefone deve conter apenas dez digitos.'
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
    try:
        url = f'https://viacep.com.br/ws/{cep}/json/'
        response = requests.get(url)
        dados = response.json()
    except:
        error = f'CEP inválido ou inexistente. Código de erro: {response.status_code}'
        return error
    else:
        return dados # logradouro -> rua / localidade -> cidade


name = str(input('Nome: ')).strip()
telephone = str(input('Telephone: ')).replace(' ', '')
email = str(input('E-mail: ')).strip()
cpf = str(input('CPF: ')).strip()
cep = str(input('CEP: ')).strip()

test = []
test.append(verifyName(name))
test.append(verifyPhone(telephone))
test.append(verifyEmail(email))
test.append(verifyCpf(cpf))
test.append(lookCep(cep))

# STREAMLIT GUI
st.title('Trabalho Avaliativo 05')
st.markdown('Feito no Senac')
st.markdown('Tutor: Antônio')
st.write(test)