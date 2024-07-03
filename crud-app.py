import requests
import streamlit as st
import smtplib
import email.message

# STREAMLIT GUI
st.title('Trabalho Avaliativo 05')
st.markdown('Feito no Senac')
st.markdown('Tutor: Antônio')

error = False

def send_email(name, recipient_email, password): 
    email_body = f"""
    <p>Olá, {name}!</p>
    <p>Fico feliz em lhe informar que seu e-mail foi cadastrado com sucesso!</p>
    <p>Atenciosamente,</p>
    <p><i>Gui</i></p>
    """
    
    sender_email = 'guilherme.assis.bittencourt@outlook.com'
    message = email.message.EmailMessage()

    message['Subject'] = 'Usuário Cadastrado'
    message['From'] = sender_email
    message['To'] = recipient_email
    message.add_header('Content-Type', 'text/html')
    
    message.set_payload(email_body)
    
    servidor = smtplib.SMTP('smtp-mail.outlook.com: 587')
    servidor.starttls()
    servidor.login(sender_email, password)
    servidor.sendmail(sender_email, [recipient_email], message.as_string().encode('latin1'))


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
        return error, text_error
    if len(telephone) != 10 and len(telephone) != 11:
        error = True
        text_error = 'O telefone deve conter dez digitos.'
    return error, text_error


def verifyEmail(email):
    error = False
    text_error = ''
    res = 'incorrect'
    if '@' in email:
        if email.find('@') - 1 != -1:
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
    if cpf.isnumeric() == False:
        error = True
        text_error = 'O CPF deve conter apenas números.'
        return error, text_error
    if len(cpf) != 11:
        error = True
        text_error = 'O CPF deve conter apenas onze digitos.'
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

user_email = str(st.text_input(label='E-mail')).strip()
error_email = verifyEmail(user_email)
if user_email and error_email[0] == True:
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

if name and telephone and user_email and cpf and cep and error == False:
    dados = f'''Nome: {name}
telefone: {telephone}
E-mail: {user_email}
CPF: {cpf}
Endereço: Cidade: {address['localidade']} | Bairro {address['bairro']} | Rua: {address['logradouro']}
'''
    with st.form('Login Administrador'):
        password = st.text_input('Senha de Administrador', type='password')
        if st.form_submit_button('Cadastrar Usuário'):
            try:
                send_email(name, user_email, password)
            except:
                st.error('Ocorreu um erro, verifique a senha e tente novamente.')
            else:
                st.success('Usuário Cadastrado!')
            with open('data.txt', 'w') as arquive:
                arquive.write(dados)
