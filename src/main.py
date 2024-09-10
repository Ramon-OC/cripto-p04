import argparse
from cifrador_afin import CifradorAfin

def main():
    # Configurar el parser de argumentos
    parser = argparse.ArgumentParser(description='Descifra archivos usando cifrado afín.')
    parser.add_argument('file', type=str, help='Ruta del archivo cifrado')

    args = parser.parse_args()

    cifrador = CifradorAfin()

    cifrador.descifrar_archivo_completo(args.file)

if __name__ == '__main__':
    main()
