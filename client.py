import socket

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
    host = '127.0.0.1'  # localhost
    port = 65432

    # Cliente (Jogador 1) faz sua jogada ANTES de enviar ao servidor
    escolha_cliente = obter_escolha_valida("Você (Jogador 1)")
    print(f"Você escolheu: {escolha_cliente.capitalize()}. Aguardando o Servidor (Jogador 2) fazer a jogada...")

    # Cria o socket TCP/IP do cliente
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((host, port))
            print("Conectado ao servidor.")

            # Aguarda o sinal do servidor indicando que ele já jogou
            sinal_servidor = s.recv(1024).decode('utf-8')

            if sinal_servidor == "SERVIDOR_PRONTO":
                print("Servidor pronto. Enviando sua jogada...")
                # Envia a jogada do cliente para o servidor
                s.sendall(escolha_cliente.encode('utf-8'))

                # Recebe o resultado do jogo
                resultado_bytes = s.recv(1024)
                if not resultado_bytes:
                    print("Servidor desconectado inesperadamente antes de enviar o resultado.")
                    return
                resultado = resultado_bytes.decode('utf-8')

                print(f"\n--- Resultado Recebido ---")
                print(f"Sua jogada: {escolha_cliente.capitalize()}")
                print(f"Resultado do jogo: {resultado}")
            else:
                print(f"Sinal inesperado do servidor: {sinal_servidor}")

        except ConnectionRefusedError:
            print(f"Não foi possível conectar ao servidor em {host}:{port}. Verifique se o servidor está rodando.")
        except Exception as e:
            print(f"Ocorreu um erro: {e}")

if __name__ == "__main__":
    main()
