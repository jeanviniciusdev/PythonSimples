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
escola_cursos = 'https://escola.inss.gov.br/report/customsql/view.php?id=60'
escola_ofertas = 'https://escola.inss.gov.br/report/customsql/view.php?id=61'
escola_capacitados = "https://escola.inss.gov.br/report/customsql/view.php?id=59"
escola_certificados = "https://escola.inss.gov.br/report/customsql/view.php?id=58"
grafico_wordpress = 'https://universidade.inss.gov.br/wp-admin/post.php?post=4941&action=elementor'

# Credenciais
usuario_escola = '3446511'
senha_escola = '24033110'
usuario_wp = 'daniel.simoes'
senha_wp = 'Daniel@123'

def substituir_dado():
    pyautogui.click(x=213, y=429)
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.5)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1)

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
        print(f"✅ Login realizado com sucesso na Escola INSS: {url}")
    except Exception as e:
        print(f"❌ Erro ao fazer login na Escola INSS: {e}")

def somar_capacitados():
    valores = driver.find_elements(By.XPATH, "//table//tr/td[1]")
    return sum(int(valor.text) for valor in valores if valor.text.isdigit())

def somar_certificados():
    valores = driver.find_elements(By.XPATH, "//table//tr/td[1]")
    return sum(int(valor.text) for valor in valores if valor.text.isdigit())

def rows_ofertas():
    driver.get(escola_ofertas)  # Corrigido
    time.sleep(3)
    linhas = driver.find_elements(By.XPATH, "//table//tr")
    return len(linhas) - 1

def rows_cursos():
    driver.get(escola_cursos)  # Corrigido
    time.sleep(3)
    linhas = driver.find_elements(By.XPATH, "//table//tr")
    return len(linhas) - 1

def copiar_para_area_transferencia(valor, porcentagem=False):
    pyperclip.copy(f"{valor:.2f}" if porcentagem else str(valor))

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

def atualizar_graficos(soma_capacitados, porcentagem_capacitados, soma_certificados, soma_ofertas, soma_cursos):
    try:
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        if iframes:
            driver.switch_to.frame(iframes[0])

        widgets = {
            "b8a2cae": soma_capacitados,
            "2eff370": soma_certificados,  
            "2637c45": soma_ofertas,  
            "0c87f49": porcentagem_capacitados,  
            "dfb3600": soma_cursos,
        }


        for data_id, valor in widgets.items():
            try:
                copiar_para_area_transferencia(valor, porcentagem=(data_id == "0c87f49"))

                widget_xpath = f'//div[@data-id="{data_id}"]'
                widget = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, widget_xpath))
                )
                widget.click()
                print(f"✅ Widget {data_id} clicado com sucesso!")
                time.sleep(2)

                if data_id == "0c87f49":
                    pyautogui.click(x=221, y=519)
                    pyautogui.hotkey('ctrl', 'a')
                    pyautogui.hotkey('ctrl', 'v')
                    time.sleep(1)
                    pyautogui.hotkey('ctrl', 'left')
                    time.sleep(0.5)
                    for _ in range (5):
                        pyautogui.press('right')
                        time.sleep(0.5)
                    for _ in range (10):
                        pyautogui.press('delete')
                
                else:
                    substituir_dado()

                print(f"✅ Valor atualizado para {valor} no widget {data_id}!")

            except Exception as e:
                print(f"❌ Erro ao atualizar o widget {data_id}: {e}")

    except Exception as e:
        print(f"❌ Erro ao localizar ou entrar no iframe: {e}")

# Coleta os dados da Escola antes de logar no WordPress
login_escola_inss(escola_capacitados)
soma_capacitados = somar_capacitados()
print(f"✅ Soma dos Capacitados: {soma_capacitados}")

login_escola_inss(escola_certificados)
soma_certificados = somar_certificados()
print(f"✅ Soma dos Certificados: {soma_certificados}")

login_escola_inss(escola_ofertas)
soma_ofertas = rows_ofertas()
print(f"✅ Soma das Ofertas: {soma_ofertas}")

login_escola_inss(escola_cursos)
soma_cursos = rows_cursos()
print(f"✅ Soma dos Cursos: {soma_cursos}")

# Calcula a porcentagem de capacitados
meta = 5000
porcentagem_capacitados = (soma_capacitados / meta) * 100
print(f"✅ Porcentagem dos Capacitados: {porcentagem_capacitados:.2f}%")

# Realiza login no WordPress e atualiza os gráficos
login_wordpress()
atualizar_graficos(soma_capacitados, porcentagem_capacitados, soma_certificados, soma_ofertas, soma_cursos)

pyautogui.click(x=1344, y=176)

# Espera o usuário pressionar Enter para continuar
input("🔒 Pressione Enter para continuar e fechar o navegador...")

# Fecha o navegador após pressionar Enter
driver.quit()
