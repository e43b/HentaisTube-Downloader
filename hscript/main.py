import os

print("Bem vindos ao Hentais Tube Downloader")
print("\nEsse script foi criado por e42b, acesse o repositório do projeto em https://github.com/e43b/HentaisTube-Downloader")

print("\nPara baixar vários episódios de uma obra digite 1")
print("Para baixar um episódio específico digite 2")

opcao = input("\nDigite sua opção: ")

if opcao == "1":
    # Executar script para baixar todos os episódios de uma obra
    os.system("python obra.py")
elif opcao == "2":
    # Executar script para baixar um episódio específico
    os.system("python episodio.py")
else:
    print("Opção inválida. Por favor, escolha 1 ou 2.")
