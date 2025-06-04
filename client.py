import socket
from time import sleep

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
    host = '192.168.243.26'  # localhost
    port = 65432

    # Cria o socket TCP/IP do cliente
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((host, port))
            print("Conectado ao servidor.\n")
            print(" =============  BEM-VINDO AO JOGO PEDRA PAPEL TESOURA ============ \n")
            print("Você (Cliente) começa jogando!")

            novo_jogo = False
            while True:
                if novo_jogo:
                    print("MAIS UMA RODADA!!!")
                    print("")
                # Cliente (Jogador 1) faz sua jogada ANTES de enviar ao servidor
                escolha_cliente = obter_escolha_valida("Você (Jogador 1)")
                print(f"Você escolheu: {escolha_cliente.capitalize()}. Aguardando o Servidor (Jogador 2) fazer a jogada...")
                # envia ao servidor a escolha do cliente
                s.sendall(escolha_cliente.encode('utf-8'))

                # cliente recebe jogada do servidor
                resposta_servidor = s.recv(1024).decode('utf-8')

                # Recebe o resultado do jogo
                resultado_bytes = s.recv(1024)
                if not resultado_bytes:
                    print("Servidor desconectado inesperadamente antes de enviar o resultado.")
                    return
                resultado = resultado_bytes.decode('utf-8')

                print(f"\n--- Resultado Recebido ---")
                print(f"Sua jogada: {escolha_cliente.capitalize()}")
                print(f"Jogada do Jogador 2 (Servidor): {resposta_servidor}")
                print(f"Resultado do jogo ... \n")
                sleep(0.5)
                print(resultado)

                while True:
                    continuar_jogando = input("DESEJA CONTINUAR JOGANDO? (S) para sim (N) para nao: ").lower().strip()
                    s.sendall(continuar_jogando.encode('utf-8'))
                    if continuar_jogando == 's':
                        novo_jogo = True
                        break
                    elif continuar_jogando == 'n':
                        print("JOGO FINALIZADO. VOLTE SEMPRE ... :)")
                        sleep(1)
                        return
                    else:
                        print("RESPOSTA INVÁLIDA. DIGITE NOVAMENTE")

                else:
                    print(f"Sinal inesperado do servidor: {sinal_servidor}")
                
                if novo_jogo:
                    continue

        except ConnectionRefusedError:
            print(f"Não foi possível conectar ao servidor em {host}:{port}. Verifique se o servidor está rodando.")
        except Exception as e:
            print(f"Ocorreu um erro: {e}")

if __name__ == "__main__":
    main()
