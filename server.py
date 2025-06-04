import socket
from time import sleep

def determinar_vencedor(escolha_cliente, escolha_servidor):
    """Determina o vencedor com base nas escolhas."""
    if escolha_cliente == escolha_servidor:
        return "Empate!"
    elif (escolha_cliente == "pedra" and escolha_servidor == "tesoura") or \
         (escolha_cliente == "tesoura" and escolha_servidor == "papel") or \
         (escolha_cliente == "papel" and escolha_servidor == "pedra"):
        return "Jogador 1 (Cliente) Venceu!"
    else:
        return "Jogador 2 (Servidor) Venceu!"

def obter_escolha_valida(jogador_nome):
    """Obtém uma escolha válida (pedra, papel, tesoura) do jogador."""
    opcoes_validas = ["pedra", "papel", "tesoura"]
    while True:
        escolha = input(f"{jogador_nome}, faça sua jogada (pedra, papel, tesoura): ").lower()
        if escolha in opcoes_validas:
            return escolha
        else:
            print("Jogada inválida. Tente novamente.")

def main():
    host = '192.168.0.4'  # localhost
    port = 65432

    # Cria o socket TCP/IP do servidor
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Servidor (Jogador 2) escutando em {host}:{port}")
        print("Aguardando conexão do Jogador 1 (Cliente)...")

        # Aceita a conexão do cliente
        conn, addr = s.accept()
        with conn:
            print(f"Jogador 1 (Cliente) conectado de {addr}")
            print(" =============  BEM-VINDO AO JOGO PEDRA PAPEL TESOURA ============ \n")
            print("O Jogador 2 (Cliente) começa jogando. Aguarde!")

            novo_jogo = False
            while conn:
                if novo_jogo:
                    print("Jogador 1 (Cliente) deseja jogar novamente!\n")
                    print("Aguarde a jogada do Jogador 1")
                # Cliente Joga
                escolha_cliente_bytes = conn.recv(1024)
                if not escolha_cliente_bytes:
                    print("Cliente desconectado inesperadamente antes de enviar a jogada.")
                    return
                escolha_cliente = escolha_cliente_bytes.decode('utf-8')
                #print(f"Jogador 1 (Cliente) escolheu: {escolha_cliente}")

                # Servidor (Jogador 2) faz sua jogada e envia ao cliente
                escolha_servidor = obter_escolha_valida("Servidor (Jogador 2)")
                print("Servidor (Jogador 2) fez sua jogada. Aguardando jogada do Cliente...")
                conn.sendall(escolha_servidor.encode('utf-8'))


                # Determina o resultado
                resultado = determinar_vencedor(escolha_cliente, escolha_servidor)
                print(f"\n--- Resultado ---")
                print(f"Jogador 1 (Cliente): {escolha_cliente.capitalize()}")
                print(f"Jogador 2 (Servidor): {escolha_servidor.capitalize()}")
                print(f"Resultado: {resultado}")

                # Envia o resultado para o cliente
                conn.sendall(resultado.encode('utf-8'))
                print("Resultado enviado ao cliente.")

                cliente_joga_novamente = conn.recv(1024).decode('utf-8')
                if cliente_joga_novamente == 's':
                    novo_jogo = True
                    continue
                else:
                    print("Jogador 1 (Cliente) encerrou o jogo!")
                    sleep(1)
                    break

if __name__ == "__main__":
    main()
