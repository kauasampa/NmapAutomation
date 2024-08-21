from utils import menu
from scanner import NmapScanner

def run_nmap(target):
    while True:
        option=menu.show_menu()
        try:
            if option == 1:
                print("Processando opção 1...\n")
                devices, MACs, MACPresence= NmapScanner.localScan(target)
                menu.show_devices(devices, MACs, MACPresence)
            elif option == 2:
                print("Processando opção 2...\n")
                NmapScanner.run_intrusive_nmap(target)
            elif option == 3:
                print("saindo...")
                break

        except:
            print(f"ocorreu um erro ao executar nmap com a opção: {option}")

run_nmap(NmapScanner.get_default_gateway())