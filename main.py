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
from tkcalendar import *
import pandas as pd
import datetime
from datetime import date

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
    print(navegador.page_source);

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
    # Função de callback para checkboxes de Convênio e CPA
    def on_checkbox_click(i, is_convenio):
        if is_convenio:
            if convenio_vars[i].get() == 1:
                cpa_vars[i].set(0)  # Desativa a checkbox de CPA
                checkbuttons_cpa[i].config(state='disabled')
                variable_cpa[i].set(OPTIONS_CPA[0])  # Reseta o OptionMenu de CPA
            else:
                checkbuttons_cpa[i].config(state='normal')  # Ativa a checkbox de CPA
        else:
            if cpa_vars[i].get() == 1:
                convenio_vars[i].set(0)  # Desativa a checkbox de Convênio
                checkbuttons_convenio[i].config(state='disabled')
                variable_convenio[i].set(OPTIONS_CONVENIO[0])  # Reseta o OptionMenu de Convênio
            else:
                checkbuttons_convenio[i].config(state='normal')  # Ativa a checkbox de Convênio

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

    convenio_vars = []
    cpa_vars = []
    variable_convenio = []
    variable_cpa = []
    variable_data = []
    variable_vaga = []
    variable_horario = []

    for i in range(7):
        convenio_vars.append(IntVar())
        convenio_check = Checkbutton(janela, text='Convênio:', onvalue=1, offvalue=0, variable=convenio_vars[i])
        convenio_check.grid(column=column, row=row, padx=5, pady=5)
        checkbuttons_convenio.append(convenio_check)
        convenio_check.config(command=lambda i=i: on_checkbox_click(i, True))
        column += 1

        variable_convenio.append(StringVar(janela))
        variable_convenio[i].set(OPTIONS_CONVENIO[0])
        w_convenio = OptionMenu(janela, variable_convenio[i], *OPTIONS_CONVENIO)
        w_convenio.grid(column=column, row=row, padx=5, pady=5)
        column += 1

        cpa_vars.append(IntVar())
        cpa_check = Checkbutton(janela, text='CPA: ', onvalue=1, offvalue=0, variable=cpa_vars[i])
        cpa_check.grid(column=column, row=row, padx=5, pady=5)
        checkbuttons_cpa.append(cpa_check)
        cpa_check.config(command=lambda i=i: on_checkbox_click(i, False))
        column += 1

        variable_cpa.append(StringVar(janela))
        variable_cpa[i].set(OPTIONS_CPA[0])
        w_cpa = OptionMenu(janela, variable_cpa[i], *OPTIONS_CPA)
        w_cpa.grid(column=column, row=row, padx=5, pady=5)
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

if __name__ == "__main__":
    # acessarSite()
    abrirJanela()

