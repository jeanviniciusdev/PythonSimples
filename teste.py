import pyautogui
import time
import pyperclip
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configuração do WebDriver
driver = webdriver.Chrome()
driver.maximize_window()

# URLs
escola_capacitados = "https://escola.inss.gov.br/report/customsql/view.php?id=59"
grafico_wordpress = 'https://universidade.inss.gov.br/wp-admin/post.php?post=4941&action=elementor'

# Credenciais
usuario_escola = 'xxxxxx'
senha_escola = 'xxxxxx'
usuario_wp = 'xxxxxxxx'
senha_wp = 'xxxxxxx'

def login_escola_inss(url):
    driver.get(url)
    time.sleep(3)
    try:
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'username'))
        )
        driver.find_element(By.ID, 'username').send_keys(usuario_escola)
        driver.find_element(By.ID, 'password').send_keys(senha_escola)
        driver.find_element(By.ID, 'password').send_keys(Keys.RETURN)
        time.sleep(3)
        print("✅ Login realizado com sucesso na Escola INSS!")
    except Exception as e:
        print(f"❌ Erro ao fazer login na Escola INSS: {e}")

def copiar_para_area_transferencia(valor):
    pyperclip.copy(valor)  # Copia o valor para a área de transferência

def colar_dado():
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.hotkey('ctrl', 'v')  # Cola o conteúdo da área de transferência no WordPress
    time.sleep(1)

def clicar_com_scroll(xpath, driver):
    try:
        # Aguarda o elemento estar presente no DOM
        elemento = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )

        # Rola até o elemento aparecer na tela
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", elemento)

        # Aguarda até que o elemento esteja visível e clicável
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )

        # Usando JavaScript para clicar, caso o clique normal não funcione
        driver.execute_script("arguments[0].click();", elemento)
        print(f"✅ Botão {xpath} clicado com sucesso!")

    except Exception as e:
        print(f"❌ Erro ao clicar no botão {xpath}: {e}")


def colar_no_wordpress(driver):
    # Clicar no Widget Principal
    clicar_com_scroll('//div[@data-id="b42f855"]', driver)

    # Lista de botões
    botoes = [
        '//div[@data-collapse_id="iq_pie_section_1"]',
        # '//div[@data-setting="element1"]',
        # '//input[@data-setting="value1"]',
        # '//div[@data-setting="element2"]',
        # '//input[@data-setting="value2"]',
        # '//div[@data-setting="element3"]',
        # '//input[@data-setting="value3"]',
        # '//div[@data-setting="element4"]',
        # '//input[@data-setting="value4"]',
        # '//div[@data-setting="element5"]',
        # '//input[@data-setting="value5"]',
        # '//div[@data-setting="element6"]',
        # '//input[@data-setting="value6"]',
        # '//div[@data-setting="element7"]',
        # '//input[@data-setting="value7"]'
    ]

    for xpath in botoes:
        clicar_com_scroll(xpath, driver)

    print("✅ Todos os botões foram clicados com sucesso!")


def login_wordpress():
    print("🔄 Realizando login no WordPress...")
    driver.get(grafico_wordpress)
    time.sleep(2)
    try:
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'user_login'))
        )
        driver.find_element(By.ID, 'user_login').send_keys(usuario_wp)
        driver.find_element(By.ID, 'user_pass').send_keys(senha_wp)
        driver.find_element(By.ID, 'user_pass').send_keys(Keys.RETURN)
        time.sleep(15)
        print("✅ Login no WordPress realizado com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao fazer login no WordPress: {e}")

def pegar_valores_tabela():
    try:
        # Localiza todas as linhas da tabela
        linhas_tabela = driver.find_elements(By.XPATH, "//table//tr")
        for linha in linhas_tabela[1:]:  # Ignora o cabeçalho (primeira linha)
            colunas = linha.find_elements(By.TAG_NAME, "td")
            if len(colunas) > 1:
                valor = colunas[0].text.strip()  # Número (primeira coluna)
                descricao = colunas[1].text.strip()  # Descrição (segunda coluna)

                print(f"✅ Valor: {valor} - Descrição: {descricao}")

                # Copia o valor para a área de transferência
                copiar_para_area_transferencia(valor)

                # Agora vamos colar o valor no WordPress
                login_wordpress()
                colar_no_wordpress(driver)  # Passando o driver aqui

                # Espera um pouco antes de pegar o próximo valor
                time.sleep(2)
    except Exception as e:
        print(f"❌ Erro ao pegar os valores da tabela: {e}")


# Realiza login na Escola INSS e pega os valores da tabela
login_escola_inss(escola_capacitados)
pegar_valores_tabela()

# Espera o usuário pressionar Enter para continuar
input("🔒 Pressione Enter para continuar e fechar o navegador...")

# Fecha o navegador após pressionar Enter
driver.quit()
