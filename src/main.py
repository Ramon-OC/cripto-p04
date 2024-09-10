import sys
from cifrador_afin import CifradorAfin

def main():
    if len(sys.argv) != 2:
        print("Uso: python main.py <ruta_al_archivo>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    cifrador = CifradorAfin()
    cifrador.descifrar_archivo(file_path)

if __name__ == "__main__":
    main()
