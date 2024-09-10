class CifradorAfin:
    def __init__(self):
        self.firmas = {
            b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A': 'PNG',
            b'%PDF': 'PDF',
            b'\xFF\xFB': 'MP3',
            b'\xFF\xF3': 'MP3',
            b'\x49\x44\x33': 'MP3',
            b'\xFF\xF2': 'MP3',
            b'\x00\x00\x00\x20\x66\x74\x79\x70': 'MP4',
        }
        self.N = 256  # Tamaño del espacio de bytes (0-255)

    def mod_inverse(self, a, m):
        for x in range(1, m):
            if (a * x) % m == 1:
                return x
        return None

    def cifrar_afin_bytes(self, datos, a, b):
        resultado = bytearray()
        for byte in datos:
            cifrado = (a * byte + b) % self.N
            resultado.append(cifrado)
        return bytes(resultado)

    def descifrar_afin_bytes(self, datos, a, b):
        resultado = bytearray()
        a_inv = self.mod_inverse(a, self.N)
        if a_inv is None:
            raise ValueError(f"No existe el inverso multiplicativo para 'a={a}' y módulo {self.N}")
        for byte in datos:
            descifrado = (a_inv * (byte - b)) % self.N
            resultado.append(descifrado)
        return bytes(resultado)

    def encontrar_a_b(self, x1, c1, x2, c2):
        delta_x = (x1 - x2) % self.N
        delta_c = (c1 - c2) % self.N
        delta_x_inv = self.mod_inverse(delta_x, self.N)
        if delta_x_inv is None:
            raise ValueError(f"No existe el inverso multiplicativo para delta_x={delta_x} y módulo {self.N}")
        a = (delta_c * delta_x_inv) % self.N
        b = (c1 - a * x1) % self.N
        return a, b

    def probar_firmas(self, datos_cifrados):
        primeros_bytes_cifrados = datos_cifrados[:8]
        for firma_real, tipo_archivo in self.firmas.items():
            longitud_firma = len(firma_real)
            for i in range(longitud_firma):
                for j in range(i + 1, longitud_firma):
                    try:
                        a, b = self.encontrar_a_b(firma_real[i], primeros_bytes_cifrados[i], firma_real[j], primeros_bytes_cifrados[j])
                        primeros_bytes_descifrados = self.descifrar_afin_bytes(primeros_bytes_cifrados, a, b)
                        if primeros_bytes_descifrados[:longitud_firma] == firma_real:
                            print(f"Archivo identificado como {tipo_archivo}")
                            print(f"Valores de a: {a}, b: {b}")
                            return a, b, tipo_archivo
                    except ValueError:
                        continue
        return None, None, "Desconocido"

    def descifrar_archivo_completo(self, file_path):
        with open(file_path, 'rb') as f:
            datos_cifrados = f.read()
        a, b, tipo_archivo = self.probar_firmas(datos_cifrados)
        if a is not None and b is not None:
            datos_descifrados = self.descifrar_afin_bytes(datos_cifrados, a, b)
            output_file = f'archivo_descifrado.{tipo_archivo.lower()}'
            with open(output_file, 'wb') as f:
                f.write(datos_descifrados)
            print(f"Archivo descifrado guardado como: {output_file}")
        else:
            print("No se pudo identificar el archivo o descifrar los encabezados.")
