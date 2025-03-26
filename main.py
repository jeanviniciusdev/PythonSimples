from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pyperclip
import pyautogui

# Configuração do WebDriver
driver = webdriver.Chrome()
driver.maximize_window()

# Relatórios e suas URLs respectivas do TablePress
relatorios = [
    {"relatorio": "https://escola.inss.gov.br/report/customsql/view.php?id=60", "tablepress": "https://universidade.inss.gov.br/wp-admin/admin.php?page=tablepress&action=edit&table_id=1"},  # TOTAL
    {"relatorio": "https://escola.inss.gov.br/report/customsql/view.php?id=75", "tablepress": "https://universidade.inss.gov.br/wp-admin/admin.php?page=tablepress&action=edit&table_id=SRSEI"},  # SRSEI
    {"relatorio": "https://escola.inss.gov.br/report/customsql/view.php?id=80", "tablepress": "https://universidade.inss.gov.br/wp-admin/admin.php?page=tablepress&action=edit&table_id=SRSEII"},  # SRSEII
    {"relatorio": "https://escola.inss.gov.br/report/customsql/view.php?id=85", "tablepress": "https://universidade.inss.gov.br/wp-admin/admin.php?page=tablepress&action=edit&table_id=SRSEIII"},  # SRSEIII
    {"relatorio": "https://escola.inss.gov.br/report/customsql/view.php?id=65", "tablepress": "https://universidade.inss.gov.br/wp-admin/admin.php?page=tablepress&action=edit&table_id=SRNE"},  # SRNE
    {"relatorio": "https://escola.inss.gov.br/report/customsql/view.php?id=70", "tablepress": "https://universidade.inss.gov.br/wp-admin/admin.php?page=tablepress&action=edit&table_id=SRNCO"},  # SRNCO
    {"relatorio": "https://escola.inss.gov.br/report/customsql/view.php?id=90", "tablepress": "https://universidade.inss.gov.br/wp-admin/admin.php?page=tablepress&action=edit&table_id=SRSUL"}  # SRSUL
]

# Credenciais
usuario_escola = 'xxxxxx'
senha_escola = 'xxxxxxx'
usuario_wp = 'xxxxxxxx'
senha_wp = 'xxxxxxxx'

# Função para fazer login na Escola INSS
def login_escola():
    print("🔄 Realizando login na Escola INSS...")
    driver.get('https://escola.inss.gov.br/login/index.php')
    time.sleep(2)
    try:
        driver.find_element(By.ID, 'username').send_keys(usuario_escola)
        driver.find_element(By.ID, 'password').send_keys(senha_escola)
        driver.find_element(By.ID, 'password').send_keys(Keys.RETURN)
        time.sleep(3)
        print("✅ Login na Escola INSS realizado com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao fazer login na Escola INSS: {e}")

# Função para coletar dados de cada relatório da SRSEI
def coletar_dados_srsei(relatorio_url):
    print("🔄 Coletando dados da SRSEI...")
    driver.get(relatorio_url)
    time.sleep(3)

    # Capturar os números de capacitados e os nomes dos cursos
    capacitados = driver.find_elements(By.XPATH, "//td[contains(@class, 'c0')]")
    cursos = driver.find_elements(By.XPATH, "//td[contains(@class, 'c1 lastcol')]")

    # Criar a lista formatada com cabeçalho
    dados_formatados = ["CAPACITADOS\tCURSOS"]  # Adiciona o cabeçalho separado por tabulação (\t)
    dados_formatados += [f"{cap.text}\t{curso.text}" for cap, curso in zip(capacitados, cursos)]

    # Copiar os dados filtrados para a área de transferência
    pyperclip.copy("\n".join(dados_formatados))

    print("✅ Dados coletados e copiados para a área de transferência!")
    print("\n".join(dados_formatados))

# Função para fazer login no WordPress
def login_wordpress(tablepress_url):
    print("🔄 Realizando login no WordPress...")
    driver.get(tablepress_url)
    time.sleep(2)
    try:
        driver.find_element(By.ID, 'user_login').send_keys(usuario_wp)
        driver.find_element(By.ID, 'user_pass').send_keys(senha_wp)
        driver.find_element(By.ID, 'user_pass').send_keys(Keys.RETURN)
        time.sleep(3)
        print("✅ Login no WordPress realizado com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao fazer login no WordPress: {e}")

# Função para atualizar o TablePress com os dados coletados
def atualizar_tablepress():
    print('🔄 Atualizando dados do TablePress...')
    pyautogui.click(x=1343, y=393)  # Clica na célula que será editada
    time.sleep(0.5)
    pyautogui.scroll(-900)  # Rola a página
    time.sleep(0.5)
    pyautogui.click(x=325, y=252)  # Clica na célula de entrada
    pyautogui.hotkey('ctrl', 'a')  # Seleciona todo o conteúdo
    time.sleep(0.5)
    pyautogui.hotkey('ctrl', 'v')  # Cola os dados copiados
    time.sleep(1)
    pyautogui.scroll(-20000)  # Rola a página para baixo
    time.sleep(1)
    pyautogui.click(x=331, y=651)  # Confirma a atualização
    print('✅ Dados Atualizados')

# Executar a sequência para cada relatório
def processar_relatorios():
    login_escola()  # Realiza o login na Escola INSS
    for relatorio in relatorios:
        coletar_dados_srsei(relatorio['relatorio'])  # Coleta os dados do relatório
        login_wordpress(relatorio['tablepress'])  # Realiza o login no TablePress
        atualizar_tablepress()  # Atualiza os dados no TablePress

# Executar o fluxo
processar_relatorios()
