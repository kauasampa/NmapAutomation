
class menu:

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

    def show_devices(devices, MACs, MACPresence):
        #Exibe Nome, IP e MAC do host, caso haja.
        for i in range (len(devices)):
            print(f"Nome da máquina {i}: {devices[i]}")
            if MACPresence==True:
                try:
                    print(f"MAC da máquina {i}: {MACs[i]}\n")
                except:
                    print("Máquina do usuário\n")