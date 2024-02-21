from bs4 import BeautifulSoup
import requests
import os

# Função para procurar pelos links do MediaFire e do Google Drive em uma página de episódio
def encontrar_links(url_episodio):
    response = requests.get(url_episodio)
    soup = BeautifulSoup(response.content, "html.parser")
    mediafire_links = soup.find_all("a", href=lambda href: href and "mediafire.com" in href)
    drive_links = soup.find_all("a", href=lambda href: href and "drive.google.com" in href)
    return mediafire_links, drive_links

# Função para baixar o arquivo de vídeo do link
def baixar_video(link, episode_title, directory):
    if "mediafire.com" in link:
        # Realiza a solicitação HTTP para o URL fornecido
        response = requests.get(link)

        # Verifica se a solicitação foi bem-sucedida
        if response.status_code == 200:
            # Extrai o conteúdo HTML da resposta
            html = response.text

            # Utiliza BeautifulSoup para analisar o HTML
            soup = BeautifulSoup(html, 'html.parser')

            # Encontra o link direto de download
            download_link = soup.find('a', class_='input popsok')['href']

            # Define o nome do arquivo a partir do título do episódio
            file_name = f"{episode_title}.mp4"

            # Define o caminho completo para salvar o arquivo
            file_path = os.path.join(directory, file_name)

            # Cria o diretório de destino se ainda não existir
            if not os.path.exists(directory):
                os.makedirs(directory)

            # Baixa o arquivo
            with open(file_path, 'wb') as file:
                response = requests.get(download_link)
                file.write(response.content)

            print('Arquivo baixado com sucesso:', file_path)
        else:
            print("Falha ao obter o conteúdo da página. Status code:", response.status_code)
    elif "drive.google.com" in link:
        # Se for um link do Google Drive, apenas imprime o link e avisa no console
        print("Link do Google Drive encontrado:", link)
        print("Por favor, baixe o arquivo manualmente.")
    else:
        print("Link não suportado:", link)

# Link do episódio
url_episodio = input("Digite o Link do episódio que deseja baixar: ")

# Extrair parte final do link como o nome do episódio
episode_title = os.path.basename(url_episodio[:-1])  # Remove a barra no final e extrai a parte final do link

# Procurar pelos links do MediaFire e do Google Drive para o episódio atual
mediafire_links, drive_links = encontrar_links(url_episodio)

# Diretório de destino para salvar os arquivos
directory = "downloads"

print("Episódio:", episode_title)
print("Link:", url_episodio)

# Baixar os arquivos do MediaFire
for mediafire_link in mediafire_links:
    baixar_video(mediafire_link['href'], episode_title, directory)

# Salvar os links do Google Drive em um arquivo txt
if drive_links:
    # Cria o diretório de destino se ainda não existir
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Define o caminho completo para salvar o arquivo txt
    txt_file_path = os.path.join(directory, f"{episode_title}_google_drive_links.txt")

    # Escreve os links no arquivo txt
    with open(txt_file_path, 'w') as txt_file:
        for link in drive_links:
            txt_file.write(link['href'] + '\n')

    print(f"Os links do Google Drive para o episódio {episode_title} foram salvos em: {txt_file_path}\n")
else:
    print("Nenhum link do Google Drive encontrado.\n")
