import subprocess
import requests
from utils import menu

class NmapScanner:
    '''#Para próxima versão
    def IpInterval(target):#usuário tem que dizer se é /24, /32...
        input("Diga o intervalo de IPs que quer verificar")

    def importMac(MAC):
        #importar api  de macvendors.com
    '''
    def writeIp():
        IpAdress=str(input("Digite o Ip a ser utilizado(utilize ponto a cada 8 bits):"))
        print("\n")
        return IpAdress
    
    #Função utilizada para fazer conexão com MACvendors API
    def import_MacVendor(MAC):
        url= f"https://api.macvendors.com/{MAC}"
        try:
            response=requests.get(url)
            if response.status_code == 200:
                return response.text
            else:
                return "MAC not found"
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

        #Tratamento de informações de cada dispositivo, exibindo nome, IP e MAC de cada dispositivo(como meu disp. não tem MAC, ele não aparece)
        for line in lines:
            #Captura IP e nome do host
            if line.startswith("Nmap scan report for "): 
                cleaned_line=line[len("Nmap scan report for "):]
                devices.append(str(cleaned_line))
            #Captura MAC do host
            if line.startswith("MAC Address"):
                MACPresence=True
                cleaned_line=line[13:30]
                vendor=NmapScanner.import_MacVendor(cleaned_line) #Faz a adição da maquina achada no macvendor
                cleaned_line += f" ({vendor})"
                MACs.append(str(cleaned_line))
        
        return devices, MACs, MACPresence
    
    #Tratar saída "limpa" na próxima versão
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
                    print("Digite o IP do host a ser analisado:")
                    output=subprocess.run(["nmap", "-A", NmapScanner.writeIp()])
                    print(output)
                elif option == 3:
                    print("Voltando para o menu principal...\n")
                    break
            except:
                print("Ocorreu um erro ao executar nmap intrusivo")