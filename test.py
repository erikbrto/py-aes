import __main__
import os
import random
from hashlib import md5

from aes import AES


def main():
    nome_arq_img = "wallpaper.jpg"
    img_teste = os.path.join(os.path.dirname(__main__.__file__), nome_arq_img)
    chave = hex(random.getrandbits(128))[2:]
    nonce = hex(random.getrandbits(64))[2:]
    
    print(f"Chave utilizada nos testes [{chave}]")
    print(f"Nonce utilizado nos testes [{nonce}]")

    with open(img_teste, "rb") as f:
        dados_img_original = f.read()
        md5_img_original = md5(dados_img_original).hexdigest()

    for modo in ("ECB", "CTR"):
        for n_rodadas in (1, 5, 9, 13):
            aes = AES(chave, n_rodadas)
            dir_saida = os.path.join(os.path.dirname(__main__.__file__), "tests")
            nome_arq_cifrado = f"wallpaper_cifrado_{modo}_{n_rodadas}-rodadas.jpg"
            nome_arq_decifrado = f"wallpaper_decifrado_{modo}_{n_rodadas}-rodadas.jpg"
            arq_cifrado = os.path.join(dir_saida, nome_arq_cifrado)
            arq_decifrado = os.path.join(dir_saida, nome_arq_decifrado)

            if not os.path.exists(dir_saida):
                os.makedirs(dir_saida)

            print(f"\nTESTE - Modo {modo} - {n_rodadas} Rodadas")
            print(f"MD5 {nome_arq_img}: [{md5_img_original}]")
            
            dados_cifrados = aes.cifrar(dados_img_original, modo, nonce=nonce, v_inicial_ctr=0)
            md5_img_cifrada = md5(dados_cifrados).hexdigest()

            with open(arq_cifrado, "wb") as f:
                f.write(dados_cifrados)
            
            print(f"MD5 {nome_arq_cifrado}: [{md5_img_cifrada}]")
            
            dados_decifrados = aes.decifrar(dados_cifrados, modo, nonce=nonce, v_inicial_ctr=0)
            md5_img_decifrada = md5(dados_decifrados).hexdigest()

            with open(arq_decifrado, "wb") as f:
                f.write(dados_decifrados)
            
            print(f"MD5 {nome_arq_decifrado}: [{md5_img_decifrada}]")
            print("MD5 Imagem Original = MD5 Imagem Decifrada ->", 
                  "OK!" if (md5_img_original == md5_img_decifrada) else "ERRO!")


if __name__ == "__main__":
    main()