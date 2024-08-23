import ipaddress

def validar_ip(ip):
    try:
        ip_valido = ipaddress.ip_address(ip)
        return ip_valido
    except ValueError:
        return None

def validar_mascara(mascara):
    try:
        mask = ipaddress.ip_network(f'0.0.0.0/{mascara}').netmask
        mask_str = str(mask)
        
        return mask_str == mascara
    except ValueError:
        return False

def calcular_rede(ip, mascara):
    try:
        ip_obj = ipaddress.ip_address(ip)
        mascara_obj = ipaddress.ip_network(f'0.0.0.0/{mascara}', strict=False).netmask
        
        ip_int = int(ip_obj)
        mascara_int = int(mascara_obj)
        
        # BITWISE
        rede_int = ip_int & mascara_int
        
        rede = ipaddress.ip_address(rede_int)
        return str(rede)
    except ValueError:
        return None

def calcular_broadcast(ip, mascara):
    try:
        ip_obj = ipaddress.ip_address(ip)
        mascara_obj = ipaddress.ip_network(f'0.0.0.0/{mascara}', strict=False).netmask
        
        ip_int = int(ip_obj)
        mascara_int = int(mascara_obj)
        
        rede_int = ip_int & mascara_int
        complemento_mascara_int = ~mascara_int & 0xFFFFFFFF
        
        # OR BITWISE
        broadcast_int = rede_int | complemento_mascara_int
        
        broadcast = ipaddress.ip_address(broadcast_int)
        return str(broadcast)
    except ValueError:
        return None

def numero_de_hosts(mascara):
    try:
        ip_network = ipaddress.ip_network(f'0.0.0.0/{mascara}', strict=False)
        total_enderecos = ip_network.num_addresses
    
        numero_hosts = total_enderecos - 2
        return numero_hosts
    except ValueError:
        return None

def listar_ips_rede(ip, mascara):
    try:
        rede = ipaddress.ip_network(f'{ip}/{mascara}', strict=False)
        
        endereco_rede = rede.network_address
        endereco_broadcast = rede.broadcast_address
        
        ips_validos = [str(ip) for ip in rede.hosts() if ip != endereco_rede and ip != endereco_broadcast]
        
        return ips_validos
    except ValueError:
        return None

def faixa_de_uso(ip, mascara):
    try:
        rede = ipaddress.ip_network(f'{ip}/{mascara}', strict=False)
        
        endereco_rede = rede.network_address
        endereco_broadcast = rede.broadcast_address
        
        primeiro_ip = endereco_rede + 1
        ultimo_ip = endereco_broadcast - 1
        
        return str(primeiro_ip), str(ultimo_ip)
    except ValueError:
        return None, None

def main():
    ip = input("Endereço IP: ")
    mascara = input("Máscara de Sub-Rede: ")

    # 1. Validação do IP
    ip_validado = validar_ip(ip)
    if ip_validado:
        print(f"Endereço IP {ip} é válido.")
    else:
        print("Endereço IP inválido.")
    
    # 2. Validação da Máscara de Sub-Rede
    mascara_validada = validar_mascara(mascara)
    if mascara_validada:
        print(f"Máscara de Sub-Rede {mascara} é válida.")
    else:
        print("Máscara de Sub-Rede inválida.")

    if ip_validado == False or mascara_validada == False:
        print("Informe um IP ou Máscara de Sub-Rede válida para continuar")
        exit()

    # 3. Cálculo do Endereço de Rede
    rede = calcular_rede(ip, mascara)
    if rede:
        print(f"Endereço de Rede: {rede}")
    else:    
        print("Não foi possível calcular o endereço de rede.")

    # 4. Cálculo do Endereço de Broadcast
    broadcast = calcular_broadcast(ip, mascara)
    if broadcast:
        print(f"Endereço de Broadcast: {broadcast}")
    else:
        print("Não foi possível calcular o endereço de broadcast.")

    # 5. Número de Hosts na Sub-rede
    hosts = numero_de_hosts(mascara)
    if hosts is not None:
        print(f"Número de Hosts Utilizáveis: {hosts}")
    else:
        print("Não foi possível calcular o número de hosts.")
    
    # 6. Listagem de IPs Disponíveis:
    ips = listar_ips_rede(ip, mascara)
    if ips is not None:
        print(f"IPs Disponíveis na Sub-rede:")
        for ip in ips:
            print(ip)
    else:
        print("Não foi possível listar os IPs.")

    # 7. Faixa de Uso
    primeiro_ip, ultimo_ip = faixa_de_uso(ip, mascara)
    if primeiro_ip and ultimo_ip:
        print(f"Faixa de IPs Utilizáveis: {primeiro_ip} - {ultimo_ip}")
    else:
        print("Não foi possível calcular a faixa de IPs utilizáveis.")
        
if __name__ == '__main__':
    main()
