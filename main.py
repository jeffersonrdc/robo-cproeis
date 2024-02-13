from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import base64
import re
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException, NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from anticaptchaofficial.imagecaptcha import *
from identificadores import *
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from tkinter import *
import tkinter as tk
from tkinter import PhotoImage, messagebox
from tkcalendar import *
import pandas as pd
import datetime
from datetime import date
import os

from Service.LoginService import *
from Service.TipoLoginService import *

navegador = None


def acessarSite():
    # # Configuração do Chrome em modo headless
    # chrome_options = Options()
    # chrome_options.add_argument('--headless')  # Executar em modo headless
    #
    # # Configuração do WebDriver
    # navegador = webdriver.Chrome(options=chrome_options)
    navegador = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    # navegador.implicitly_wait(1)
    link = "http://www.proeis.rj.gov.br/"
    navegador.get(link)

    select = Select(navegador.find_element(By.ID, 'ddlTipoAcesso'))
    select.select_by_value('ID')
    navegador.find_element(By.ID, 'ddlTipoAcesso')
    navegador.find_element(By.ID, 'txtLogin').send_keys(login)
    navegador.find_element(By.ID, 'txtSenha').send_keys(senha)
    print(navegador.page_source)

    geraImagemCaptchaLogin(navegador)
    captcha_text = retornaValorCaptcha('imagelogin.png')
    if captcha_text != 0:
        navegador.find_element(By.ID, 'TextCaptcha').send_keys(captcha_text)
        navegador.find_element(By.ID, 'btnEntrar').click()

    # print(navegador.page_source);
    # navegador.find_element(By.ID, 'btnEntrar').click()
    Visible = isVisible(navegador)

    while Visible == 1:
        navegador.find_element(By.ID, 'TextCaptcha').clear()
        geraImagemCaptchaLogin(navegador)
        captcha_text = retornaValorCaptcha('imagelogin.png')
        if captcha_text != 0:
            navegador.find_element(By.ID, 'txtSenha').send_keys(senha)
            navegador.find_element(By.ID, 'TextCaptcha').send_keys(captcha_text)
            navegador.find_element(By.ID, 'btnEntrar').click()
            Visible = isVisible(navegador)

    novaInscricao(navegador)


def novaInscricao(navegador):
    navegador.find_element(By.ID, 'btnEscala').click()
    pesquisarVaga(navegador)


def pesquisarVaga(navegador):
    navegador.find_element(By.ID, 'btnNovaInscricao').click()
    select_cpa = None

    for informacao in informacoes_array:

        # SELECIONA A VAGA PELO CONVÊNIO
        if informacao['tipo_filtro'] == 1:
            select_convenio = None
            while not select_convenio:
                try:
                    select_convenio = Select(WebDriverWait(navegador, 10).until(EC.presence_of_element_located(
                        (By.ID, 'ddlConvenios'))))  # METODO QUE AGUARDA ATÉ X SEGUNDOS O ID SER CARREGADO NA PÁGINA
                    select_convenio.select_by_visible_text(informacao['local_servico'])  # CARREGA PELA DESCRIÇÃO
                except StaleElementReferenceException as e:
                    select_convenio = None
                    print(f"Erro ao selecionar convênio. {e}. Será feita nova tentativa.")

        # SELECIONA A VAGA PELO CPA
        else:
            while not select_cpa:
                try:
                    select_cpa = Select(WebDriverWait(navegador, 10).until(EC.presence_of_element_located(
                        (By.ID, 'ddlCPAS'))))  # METODO QUE AGUARDA ATÉ X SEGUNDOS O ID SER CARREGADO NA PÁGINA
                    select_cpa.select_by_visible_text(informacao['local_servico'])  # CARREGA PELA DESCRIÇÃO
                except StaleElementReferenceException as e:
                    select_cpa = None
                    print(f"Erro ao selecionar CPA. {e}. Será feita nova tentativa.")
        # ________________________________________________________________________________________________________________________________________________________________#

        # SELECIONA A DATA
        select_data_evento = None
        while not select_data_evento:
            try:
                select_data_evento = Select(WebDriverWait(navegador, 10).until(EC.presence_of_element_located(
                    (By.ID, 'ddlDataEvento'))))  # METODO QUE AGUARDA ATÉ X SEGUNDOS O ID SER CARREGADO NA PÁGINA
                select_data_evento.select_by_visible_text(informacao['data_servico'])
            except StaleElementReferenceException as e:
                select_data_evento = None
                print(f"Erro ao selecionar Data do evento. {e}. Será feita nova tentativa.")

        #________________________________________________________________________________________________________________________________________________________________#

        # CLICA NO LINK PARA EXIBIR O CAPTCHA
        abriCaptcha = None
        abriCaptchaClick = None
        while not abriCaptcha and not abriCaptchaClick:
            try:
                abriCaptcha = WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.ID, 'lnkNewCaptcha')))
                abriCaptchaClick = navegador.find_element(By.ID, 'lnkNewCaptcha')
                if abriCaptchaClick != None:
                    abriCaptchaClick.click()

            except ElementClickInterceptedException as e:
                abriCaptchaClick = None
                print(f"Erro ao clicar para exibir imagem do captcha. {e}. Será feita nova tentativa.")
            except StaleElementReferenceException as f:
                abriCaptchaClick = None
                print(f"Erro ao localizar elemento para clicar e exibir imagem do captcha. {f}. Será feita nova tentativa.")

        #________________________________________________________________________________________________________________________________________________________________#

        # FAZ CONSULTA A API, DIGITA O CAPTCHA E CLICA PARA CONSULTAR VAGAS
        consultaVaga = None
        while not consultaVaga:
            try:
                consultaVaga = WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.ID, 'btnConsultar')))
            except ElementClickInterceptedException as e:
                print(f"Erro ao clicar para consultar vaga. {e}. Será feita nova tentativa.")

        geraImagemCaptchaVaga(navegador)
        captcha_text = retornaValorCaptcha('imagevaga.png')
        if captcha_text != 0:
            navegador.find_element(By.ID, 'TextCaptcha').send_keys(captcha_text)
            navegador.find_element(By.ID, 'btnConsultar').click()
        alert = isAlert(navegador)

        while alert == 1:
            navegador.find_element(By.ID, 'TextCaptcha').clear()
            geraImagemCaptchaVaga(navegador)
            captcha_text = retornaValorCaptcha('imagevaga.png')
            if captcha_text != 0:
                navegador.find_element(By.ID, 'TextCaptcha').send_keys(captcha_text)
                navegador.find_element(By.ID, 'btnConsultar').click()
                alert = isAlert(navegador)

        # ________________________________________________________________________________________________________________________________________________________________#

        # SE O FILTRO FOI FEITO POR CPA, É CLICADO NO CONVÊNIO ESCOLHIDO DISPONIVEL NAQUELE CPA PARA EXIBIR AS VAGAS
        if select_cpa != None:
            convenioXcpa = None
            while not convenioXcpa:
                try:
                    convenioXcpa = WebDriverWait(navegador, 10).until(EC.presence_of_element_located(
                        (By.LINK_TEXT,
                         'MUNICIPIO DE NITEROI')))  # METODO QUE AGUARDA ATÉ X SEGUNDOS O ID SER CARREGADO NA PÁGINA
                except StaleElementReferenceException as e:
                    print(e)
            navegador.execute_script("arguments[0].click();", convenioXcpa)

            # XPath para encontrar a tag 'a' correspondente ao evento desejado
            xpath_evento = f"//td[text()='{informacao['setor_servico']}' and following-sibling::td[text()='{informacao['hora_servico']}']]/following-sibling::td[@class='btnCollumn']/a"

            # Encontrar elementos correspondentes ao XPath
            elementos_evento = navegador.find_elements(By.XPATH, xpath_evento)

            # Verificar se a lista de elementos não está vazia antes de clicar
            if elementos_evento:
                # Se houver elementos, clique no primeiro
                elementos_evento[0].click()
            else:
                print("Elemento não encontrado.")

            # Clique no elemento encontrado
            # navegador.find_element(By.XPATH, xpath_evento).click()
            isAlert(navegador)
            # WebDriverWait(navegador, 10).until(EC.alert_is_present())
            # navegador.switch_to.alert.accept()

        # ________________________________________________________________________________________________________________________________________________________________#

        time.sleep(300)
    # FECHA O NAVEGADOR AO TERMINAR DE INSERIR AS VAGAS
    navegador.quit()


def geraImagemCaptchaLogin(navegador):
    div = navegador.find_element(By.XPATH, '//*[@id="captcha"]/div')
    bg_url = div.value_of_css_property('background')
    bg_url = re.split('[()]', bg_url)[3]
    bg_url = bg_url[23:]

    with open("imagelogin.png", "wb") as fh:
        fh.write(base64.urlsafe_b64decode(bg_url))


def geraImagemCaptchaVaga(navegador):
    div = None
    bg_url = None
    while not div:
        try:
            div = navegador.find_element(By.XPATH, '//*[@id="captcha"]/div')
            bg_url = div.value_of_css_property('background')
            bg_url = re.split('[()]', bg_url)[3]
            bg_url = bg_url[23:]

        except NoSuchElementException:
            ""

    with open("imagevaga.png", "wb") as fh:
        fh.write(base64.urlsafe_b64decode(bg_url))


def retornaValorCaptcha(image):
    solver = imagecaptcha()
    solver.set_verbose(1)
    solver.set_key(chave_api)

    captcha_text = solver.solve_and_return_solution(image)
    if captcha_text != 0:
        return captcha_text
    else:
        print(f"task finished with error {solver.error_code}")
        return 0


def isAlert(navegador):
    try:
        alert = WebDriverWait(navegador, 0).until(EC.alert_is_present())
        if alert is not None:
            alert.accept()
            return 1
    except Exception as err:
        print(f"retrying after {type(err)}: {err}")

    return 0


def isVisible(navegador):
    try:
        erro_captcha = WebDriverWait(navegador, 0).until(EC.presence_of_element_located(
            (By.ID, 'lblLogin')))
        if erro_captcha.is_displayed():
            return 1
        else:
            return 0
    except TimeoutException:
        return 0


def validaInformacoes(tipoFiltro, localServico, data_servico, hora_servico, setor_servico):
    # Faça algo com as informações recebidas
    print(f"Tipo Filtro: {tipoFiltro}")
    print(f"Local Serviço: {localServico}")
    print(f"Data Serviço: {data_servico}")
    print(f"Hora Serviço: {hora_servico}")
    print(f"Setor Serviço: {setor_servico}")
    return


# Criar uma lista vazia para armazenar as informações
informacoes_array = []
def abrirJanela():
    janela = Tk()
    janela.title('Bot PROEIS')
    # janela.geometry('600x600')


    list_of_date = pd.date_range(date.today(), periods=8)
    data = [
        "Selecione a data",
        list_of_date.date[0],
        list_of_date.date[1],
        list_of_date.date[2],
        list_of_date.date[3],
        list_of_date.date[4],
        list_of_date.date[5],
        list_of_date.date[6],
        list_of_date.date[7]
    ]
    i = 1
    row = 0
    column = 0

    convenio_vars = []
    cpa_vars = []
    checkbuttons_convenio = []
    checkbuttons_cpa = []
    selectConvenio = []
    selectcpa = []
    selectlocaiscpa = []
    # Função de callback para checkboxes de Convênio e CPA
    def on_checkbox_click(i, is_convenio):
        if is_convenio:
            if convenio_vars[i].get() == 1:
                cpa_vars[i].set(0)  # Desativa a checkbox de CPA
                checkbuttons_cpa[i].config(state='disabled')
                selectcpa[i].config(state='disabled')
                selectlocaiscpa[i].config(state='disabled')
                variable_cpa[i].set(OPTIONS_CPA[0])  # Reseta o OptionMenu de CPA
            else:
                checkbuttons_cpa[i].config(state='normal')  # Ativa a checkbox de CPA
                selectcpa[i].config(state='normal')
        else:
            if cpa_vars[i].get() == 1:
                convenio_vars[i].set(0)  # Desativa a checkbox de Convênio
                checkbuttons_convenio[i].config(state='disabled')
                selectConvenio[i].config(state='disabled')
                selectlocaiscpa[i].config(state='normal')
                variable_convenio[i].set(OPTIONS_CONVENIO[0])  # Reseta o OptionMenu de Convênio
            else:
                checkbuttons_convenio[i].config(state='normal')  # Ativa a checkbox de Convênio
                selectConvenio[i].config(state='normal')
                selectlocaiscpa[i].config(state='disabled')

    def btn_abrir_site_click():
        for i in range(7):
            if convenio_vars[i].get():
                # Adicionar as informações à lista
                informacoes_array.append({
                    'local_servico': variable_convenio[i].get(),
                    'tipo_filtro': 1,
                    'data_servico': variable_data[i].get(),
                    'hora_servico': variable_horario[i].get(),
                    'setor_servico': variable_vaga[i].get()
                })
            elif cpa_vars[i].get():
                # Adicionar as informações à lista
                informacoes_array.append({
                    'local_servico': variable_cpa[i].get(),
                    'tipo_filtro': 2,
                    'data_servico': variable_data[i].get(),
                    'hora_servico': variable_horario[i].get(),
                    'setor_servico': variable_vaga[i].get()
                })

        # validaInformacoes(tipoFiltro, localServico, data_servico, hora_servico, setor_servico)
        acessarSite()

    def update_locais(texto, i):
        # selected_cpa = variable_cpa[index].get()
        index = OPTIONS_CPA.index(texto)
        locais_options = OPTIONS_LOCAISXCPA.get(texto, [])
        w_locaiscpa[0].set(locais_options[0] if locais_options else "Selecione um local")
        w_locaiscpa[0]['menu'].delete(0, 'end')
        for local in locais_options:
            w_locaiscpa[0]['menu'].add_command(label=local, command=lambda l=local: variable_locaisxcpa[index].set(l))

    convenio_vars = []
    cpa_vars = []
    variable_convenio = []
    variable_cpa = []
    variable_locaisxcpa = []
    variable_data = []
    variable_vaga = []
    variable_horario = []
    w_locaiscpa = []

    for i in range(7):
        convenio_vars.append(IntVar())
        convenio_check = Checkbutton(janela, text='Convênio:', onvalue=1, offvalue=0, variable=convenio_vars[i])
        convenio_check.grid(column=column, row=row, padx=5, pady=5)
        checkbuttons_convenio.append(convenio_check)
        convenio_check.config(command=lambda index=i: on_checkbox_click(index, True))
        column += 1

        variable_convenio.append(StringVar(janela))
        variable_convenio[i].set(OPTIONS_CONVENIO[0])
        w_convenio = OptionMenu(janela, variable_convenio[i], *OPTIONS_CONVENIO)
        w_convenio.grid(column=column, row=row, padx=5, pady=5)
        selectConvenio.append(w_convenio)
        column += 1

        cpa_vars.append(IntVar())
        cpa_check = Checkbutton(janela, text='CPA: ', onvalue=1, offvalue=0, variable=cpa_vars[i])
        cpa_check.grid(column=column, row=row, padx=5, pady=5)
        checkbuttons_cpa.append(cpa_check)
        cpa_check.config(command=lambda index=i: on_checkbox_click(index, False))
        column += 1

        variable_cpa.append(StringVar(janela))
        variable_cpa[i].set(OPTIONS_CPA[0])
        w_cpa = OptionMenu(janela, variable_cpa[i], *OPTIONS_CPA, command=lambda idx=i: update_locais(idx, i))
        w_cpa.grid(column=column, row=row, padx=5, pady=5)
        selectcpa.append(w_cpa)
        column += 1

        variable_locaisxcpa.append(StringVar(janela))
        variable_locaisxcpa[i].set(OPTIONS_CPA[0])
        w_locaiscpa = OptionMenu(janela, variable_locaisxcpa[i], "")
        w_locaiscpa.config(state='disabled')
        w_locaiscpa.grid(column=column, row=row, padx=5, pady=5)
        selectlocaiscpa.append(w_locaiscpa)
        column += 1

        variable_data.append(StringVar(janela))
        variable_data[i].set(data[0])
        w_data = OptionMenu(janela, variable_data[i], *data)
        w_data.grid(column=column, row=row, padx=5, pady=5)
        column += 1

        variable_vaga.append(StringVar(janela))
        variable_vaga[i].set(OPTIONS_VAGA[0])
        w_vaga = OptionMenu(janela, variable_vaga[i], *OPTIONS_VAGA)
        w_vaga.grid(column=column, row=row, padx=5, pady=5)
        column += 1

        variable_horario.append(StringVar(janela))
        variable_horario[i].set(OPTIONS_HORARIO[0])
        w_horario = OptionMenu(janela, variable_horario[i], *OPTIONS_HORARIO)
        w_horario.grid(column=column, row=row, padx=5, pady=5)

        row += 1
        i += 1
        column = 0

    btn_abrir_siste = Button(janela, text='Abrir Site', command=btn_abrir_site_click)
    btn_abrir_siste.grid(column=0, row=row, padx=10, pady=10)
    janela.mainloop()

def on_button_click(button_name):
    if button_name == "Login":
        create_login_window()
def abrirJanela2():


    # Criar janela principal
    root = tk.Tk()
    root.title("Proeis")

    # Configurar ícone da janela
    script_directory = os.path.dirname(os.path.realpath(__file__))
    icon_path = os.path.join(script_directory, "imagens", "icones", "logo_CPROEIS_PMERJ.ico")  # Substitua "subpasta" e "icone.ico" conforme necessário
    root.iconbitmap(default=icon_path)



    # Função para criar botões com imagem e nome
    def create_button(image_path, button_name):
        image = PhotoImage(file=image_path).subsample(2, 2)  # Ajuste a escala conforme necessário
        button = tk.Button(root, image=image, text=button_name, compound=tk.TOP, font=('Arial', 12),
                           command=lambda: on_button_click(button_name))
        button.image = image
        return button

    # Obtém o diretório atual do script
    script_directory = os.path.dirname(os.path.realpath(__file__))
    # Lista de imagens e nomes
    button_data = [
        {"image_path": os.path.join(script_directory, "imagens", "login.png"), "name": "Login"},
        {"image_path": os.path.join(script_directory, "imagens", "convenio.png"), "name": "Convênio"},
        {"image_path": os.path.join(script_directory, "imagens", "marcacao.png"), "name": "Marcação"},
        {"image_path": os.path.join(script_directory, "imagens", "setor_servico.png"), "name": "Setor de Serviço"},
        {"image_path": os.path.join(script_directory, "imagens", "unidade.png"), "name": "Unidade"},
        {"image_path": os.path.join(script_directory, "imagens", "unidade_convenio.png"), "name": "Unidade Convênio"}
    ]

    # Criar e posicionar os botões
    row = 0
    col = 0
    for data in button_data:
        button = create_button(data["image_path"], data["name"])
        button.grid(row=row, column=col, padx=10, pady=10)
        col += 1
        if col > 2:
            col = 0
            row += 1

    # Configurar o crescimento das colunas e linhas para preencher uniformemente o espaço
    for i in range(3):  # Número de colunas
        root.grid_columnconfigure(i, weight=1)

    for i in range(2):  # Número de linhas
        root.grid_rowconfigure(i, weight=1)

    root.state('zoomed')  # Inicia a tela maximinada

    # # Obter informações sobre as dimensões da tela
    # monitors = get_monitors()
    # screen_width = monitors[0].width
    # screen_height = monitors[0].height
    #
    # # Configurar janela para abrir em tela cheia
    # root.geometry(f"{screen_width}x{screen_height}+0+0")  # Ajustar a geometria da janela para ocupar toda a tela

    # Iniciar o loop da interface gráfica
    root.mainloop()

def create_login_window():
    root2 = tk.Tk()
    root2.title("Cadastra login")

    # Obtém os tipos de login do banco de dados
    login_types = [(0, "SELECIONE UMA OPÇÃO")] + retornaTipoLogin()

    # Use uma lista de rótulos para preencher o OptionMenu
    login_type_options = [label for _, label in login_types]


    # Adicione elementos à nova janela
    tk.Label(root2, text="Tipo de Login:").grid(row=0, column=0, padx=10, pady=10)
    login_type_var = tk.StringVar(root2)
    login_type_var.set(login_type_options[0])  # Defina o valor padrão
    login_type_menu = tk.OptionMenu(root2, login_type_var, *login_type_options)
    login_type_menu.grid(row=0, column=1, padx=10, pady=10)

    # Associa a função atualizar_max_length ao evento de modificação do OptionMenu
    login_type_var.trace_add('write', lambda *args: atualizar_max_length())

    tk.Label(root2, text="Usuário:").grid(row=1, column=0, padx=10, pady=10)
    username_entry = tk.Entry(root2)
    username_entry.grid(row=1, column=1, padx=10, pady=10)

    tk.Label(root2, text="Senha:").grid(row=2, column=0, padx=10, pady=10)
    password_entry = tk.Entry(root2, show="*")
    password_entry.grid(row=2, column=1, padx=10, pady=10)

    save_button = tk.Button(root2, text="Salvar", command=lambda: validar_formulario())
    save_button.grid(row=3, column=1, padx=10, pady=10)

    cancel_button = tk.Button(root2, text="Cancelar", command=root2.destroy)
    cancel_button.grid(row=3, column=0, padx=10, pady=10)

    username_entry.config(state='disabled')
    password_entry.config(state='disabled')

    def on_save_click():
        # Obter o ID associado usando o rótulo selecionado
        ID_TipoLogin = next(id for id, label in login_types if label == login_type_var.get())

        loginService = LoginService()
        result = loginService.salvarLogin(ID_TipoLogin, username_entry.get().strip(), password_entry.get().strip())
        if (result > 0):
            # messagebox.showinfo("Sucesso", "Login salvo com sucesso!")
            # Exibir uma mensagem de alerta ao salvar com sucesso
            alert_window = tk.Toplevel(root2)
            alert_window.title("Sucesso")
            tk.Label(alert_window, text="Os dados foram salvos com sucesso!").pack(padx=10, pady=10)

            # Adiciona um botão "OK" para fechar a janela de alerta
            ok_button = tk.Button(alert_window, text="OK", command=lambda: on_ok_button_click(alert_window))
            ok_button.pack(pady=10)

            # Limpa os campos de entrada
            password_entry.delete(0, 'end')
            username_entry.delete(0, 'end')

    def validar_formulario():
        tipo_login_selecionado = login_type_var.get()
        username = username_entry.get()
        password = password_entry.get()
        msgErro = None



        if tipo_login_selecionado == "SELECIONE UMA OPÇÃO":
            msgErro = "Selecione um tipo de login"
        elif not username:
            msgErro = "Usuário não informado!"
        elif not password:
            msgErro = "Senha não informada!"
        elif tipo_login_selecionado == "CPF" and len(username_entry.get()) < 11:
            msgErro = "CPF incompleto, verifique!"
        elif tipo_login_selecionado == "ID FUNCIONAL" and len(username_entry.get()) < 8:
            msgErro = "ID FUNCIONAL incompleta, verifique!"

        if msgErro:
            alert_window = tk.Toplevel(root2)
            alert_window.title("Erro")
            tk.Label(alert_window, text=f"{msgErro}").pack(padx=10, pady=10)
            # Adiciona um botão "OK" para fechar a janela de alerta
            ok_button = tk.Button(alert_window, text="OK", command=lambda: on_ok_button_click(alert_window))
            ok_button.pack(pady=10)
        else:
            on_save_click()



    def validar_entrada(caracter, entry_type):
        #return char != ' '  # Bloqueia o caractere de espaço
        if entry_type == 'username':
            # Se for password_entry, permita letras e números
            return caracter.isdigit()
        elif entry_type == 'password':
            return caracter != ' '  # Bloqueia o caractere de espaço

    def on_entry_change(event, entry_type):
        entry_widget = event.widget
        novo_texto = entry_widget.get()
        novo_texto_sem_espacos = ''.join(filter(lambda c: validar_entrada(c, entry_type), novo_texto))
        entry_widget.delete(0, 'end')
        entry_widget.insert(0, novo_texto_sem_espacos)

    def atualizar_max_length(*args):
        # Obtém o tipo de login selecionado no OptionMenu
        tipo_login_selecionado = login_type_var.get()

        # Define o comprimento máximo com base no tipo de login selecionado
        max_length = 0  # Defina o valor padrão ou ajuste conforme necessário
        if tipo_login_selecionado == "CPF":
            max_length = 11
            username_entry.config(state='normal')
            password_entry.config(state='normal')
        elif tipo_login_selecionado == "ID FUNCIONAL":
            max_length = 8
            username_entry.config(state='normal')
            password_entry.config(state='normal')
        else:
            username_entry.delete(0, 'end')
            password_entry.delete(0, 'end')
            username_entry.config(state='disabled')
            password_entry.config(state='disabled')


        username_entry.delete(0, 'end')
        # Adapte conforme necessário para outros tipos de login


        # Define o comprimento máximo no Entry correspondente
        username_entry.config(validate='key',
                              validatecommand=(username_entry.register(lambda P: len(P) <= max_length), '%P'))

    # Associa a função on_entry_change ao evento de modificação do Entry
    username_entry.bind('<KeyRelease>', lambda event: on_entry_change(event, 'username'))
    password_entry.bind('<KeyRelease>', lambda event: on_entry_change(event, 'password'))

    # Iniciar o loop da interface gráfica
    root2.mainloop()



def on_ok_button_click(alert_window):
    # Destroi a janela de alerta
    alert_window.destroy()

if __name__ == "__main__":
    # acessarSite()
    #abrirJanela()
    abrirJanela2()
