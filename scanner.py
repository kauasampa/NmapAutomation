import subprocess
import requests
import time#usado para que API não exceda limite de requests/second
from utils import menu

class NmapScanner:
    '''#Para próxima versão
    def IpInterval(target):#usuário tem que dizer se é /24, /32...
        input("Diga o intervalo de IPs que quer verificar")

    def importMac(MAC):
        #importar api  de macvendors.com
    '''
    def writeIp():
        IpAdress=str(input("Digite manualmente o Ip a ser utilizado (utilize ponto a cada 8 bits):"))
        print("\n")
        return IpAdress
    
    def get_default_gateway():
        try:
            # Executa o comando 'ip route' para obter as rotas da rede
            result = subprocess.run(['ip', 'route'], capture_output=True, text=True)
            output = result.stdout
            
            # Processa a saída para encontrar o gateway padrão
            for line in output.splitlines():
                if line.startswith('default'):
                    # Extrai o endereço IP do gateway padrão
                    gateway_ip = line.split()[2]
                    print(f"Seu gateway padrão é: {gateway_ip}")
                    return gateway_ip
        except Exception as e:
            print(f"Erro ao obter o gateway padrão: {e}")
            gateway_ip=NmapScanner.writeIp()
            return gateway_ip
    
    #Função utilizada para fazer conexão com MACvendors API
    def import_MacVendor(MAC):
        url= f"https://api.macvendors.com/{MAC}"
        try:
            response=requests.get(url)
            print(f"resposta para o endereço {MAC}: {response.status_code}")
            if response.status_code == 200: #Codigo de status 429 indica tempo limite excedido
                return response.text
            else:
                return response.text
        except requests.exceptions.RequestException:
            return "Erro ao acessar a API"

    
    #incluir try except na próxima versão, impedindo ip inválido.
    def localScan(targetIP):
        IpInterval=str(targetIP) + "/24"
        result=subprocess.run(["nmap", "-sn", IpInterval], capture_output=True, text=True)
        output=result.stdout
        lines=output.splitlines()
        devices=[]
        MACs=[]
        MACPresence=False 
        TimePause=0

        #Tratamento de informações de cada dispositivo, exibindo nome, IP e MAC de cada dispositivo(como meu disp. não tem MAC, ele não aparece)
        for line in lines:
            #Captura IP e nome do host
            if line.startswith("Nmap scan report for "): 
                cleaned_line=line[len("Nmap scan report for "):]
                devices.append(str(cleaned_line))
            #Captura MAC do host
            if line.startswith("MAC Address"):
                #TimePause é utilizado para que a API demore 2 segundos após 2 requests, pois o plano é limitado.
                if TimePause >=2:
                    print("Pause for API")
                    time.sleep(2)
                    TimePause=0

                MACPresence=True
                cleaned_line=line[13:30]
                vendor=NmapScanner.import_MacVendor(cleaned_line) #Faz a adição da maquina achada no macvendor
                cleaned_line += f" ({vendor})"
                MACs.append(str(cleaned_line))
                
                TimePause+=1
        
        return devices, MACs, MACPresence
    
    #Tratar saída "limpa" na próxima versão
    #Usuário não precisa digitar IP alvo completo, a lista de IPs conectados irá aparecer direto
    def run_intrusive_nmap(target):
        while True:
            option=menu.show_second_menu()
            try:
                if option == 1:
                    print("Processando opção 1 (Essa operação pode demorar bastante)...\n")
                    devices, MACs, MACPresence=NmapScanner.localScan(target)
                    for device in devices:
                        print(f"\nEscaneando {device}...\n")
                        result=subprocess.run(["nmap", "-A", device], capture_output=True, text=True)
                        output=result.stdout
                        lines=output.splitlines()
                        for line in lines:
                            print(line)
                        print("\n")
                    print("Scan finalizado\n")    
                elif option == 2:
                    print("Processando opção 2...\n")
                    output=subprocess.run(["nmap", "-A", NmapScanner.writeIp()])
                    print(output)
                elif option == 3:
                    print("Voltando para o menu principal...\n")
                    break
            except:
                print("Ocorreu um erro ao executar nmap intrusivo")