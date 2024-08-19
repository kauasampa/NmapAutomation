import subprocess

def writeIp():
    IpAdress=str(input("Digite o Ip a ser utilizado(utilize ponto a cada 8 bits):"))
    print("\n")
    return IpAdress

'''#Para próxima versão
def IpInterval(target):#usuário tem que dizer se é /24, /32...
    input("Diga o intervalo de IPs que quer verificar")

def importMac(MAC):
    #importar api  de macvendors.com
'''
#incluir try except na próxima versão, impedindo ip inválido.
def localScan(targetIP):
    IpInterval=str(targetIP) + "/24"
    result=subprocess.run(["nmap", "-sn", IpInterval], capture_output=True, text=True)
    output=result.stdout
    lines=output.splitlines()
    devices=[]
    MACs=[]
    MACPresence=0 

    #Tratamento de informações de cada dispositivo, exibindo nome, IP e MAC de cada dispositivo(como meu disp. não tem MAC, ele não aparece)
    for line in lines:
        #Captura IP e nome do host
        if line.startswith("Nmap scan report for "): 
            cleaned_line=line[len("Nmap scan report for "):]
            devices.append(str(cleaned_line))
        #Captura MAC do host
        if line.startswith("MAC Address"):
            MACPresence=1
            cleaned_line=line[13:30]
            MACs.append(str(cleaned_line))
    
    return devices, MACs, MACPresence

def show_devices(devices, MACs, MACPresence):
    #Exibe Nome, IP e MAC do host, caso haja.
    for i in range (len(devices)):
        print(f"Nome da máquina {i}: {devices[i]}")
        if MACPresence==1:
            try:
                print(f"MAC da máquina {i}: {MACs[i]}\n")
            except:
                print("Máquina do usuário\n")
    


def show_menu():
    while True:    
        print("Escolha uma varredura Nmap (número de 1 a 3):")
        print("1. Scan comum de dispositivos na rede local")
        print("2. Scan intrusivo de hosts locais")
        print("3. Sair")
        choice=input()
        if choice in ["1", "2", "3"]:
            return int(choice)
        else:
            print("Opção inválida! Por favor, escolha 1, 2 ou 3.\n")

def show_second_menu():
    while True:
        print("1. Fazer varredura geral de todos os IPs conectados")
        print("2. Fazer varredura geral de 1 IP especifico")
        print("3. Voltar para o menu principal")
        choice=input()
        if choice in ["1", "2", "3"]:
            return int(choice)
        else:
            print("Opção inválida! Por favor, escolha 1, 2 ou 3.\n")


#Tratar saída "limpa" na próxima versão
def run_intrusive_nmap(target):
    while True:
        option=show_second_menu()
        try:
            if option == 1:
                print("Processando opção 1 (Essa operação pode demorar bastante)...\n")
                devices, MACs, MACPresence=localScan(target)
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
                output=subprocess.run(["nmap", "-A", writeIp()])
                print(output)
            elif option == 3:
                print("Voltando para o menu principal...\n")
                break
        except:
            print("Ocorreu um erro ao executar nmap intrusivo")
    

def run_nmap(target):
    while True:
        option=show_menu()
        try:
            if option == 1:
                print("Processando opção 1...\n")
                devices, MACs, MACPresence= localScan(target)
                show_devices(devices, MACs, MACPresence)
            elif option == 2:
                print("Processando opção 2...\n")
                run_intrusive_nmap(target)
            elif option == 3:
                print("saindo...")
                break

        except:
            print(f"ocorreu um erro ao executar nmap com a opção: {option}")


run_nmap(writeIp())
