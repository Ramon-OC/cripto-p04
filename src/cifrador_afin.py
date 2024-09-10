class CifradorAfin:
    def __init__(self):
        """
        Inicializa la clase CifradorAfin con un diccionario de firmas de archivos comunes y sus tipos.
        """
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
        """
        Calcula el inverso multiplicativo de 'a' bajo el módulo 'm'.

        Args:
            a (int): El número para el cual se desea encontrar el inverso multiplicativo.
            m (int): El módulo.

        Returns:
            int: El inverso multiplicativo de 'a' bajo el módulo 'm', o None si no existe.
        """
        for x in range(1, m):
            if (a * x) % m == 1:
                return x
        return None

    def cifrar_afin_bytes(self, datos, a, b):
        """
        Cifra los datos usando el cifrado afín con las claves 'a' y 'b'.

        Args:
            datos (bytes): Los datos a cifrar.
            a (int): La clave de multiplicación.
            b (int): La clave de desplazamiento.

        Returns:
            bytes: Los datos cifrados.
        """
        resultado = bytearray()
        for byte in datos:
            cifrado = (a * byte + b) % self.N
            resultado.append(cifrado)
        return bytes(resultado)

    def descifrar_afin_bytes(self, datos, a, b):
        """
        Descifra los datos cifrados usando el cifrado afín con las claves 'a' y 'b'.

        Args:
            datos (bytes): Los datos cifrados.
            a (int): La clave de multiplicación.
            b (int): La clave de desplazamiento.

        Returns:
            bytes: Los datos descifrados.

        Raises:
            ValueError: Si no existe el inverso multiplicativo para 'a' y el módulo.
        """
        resultado = bytearray()
        a_inv = self.mod_inverse(a, self.N)
        if a_inv is None:
            raise ValueError(f"No existe el inverso multiplicativo para 'a={a}' y módulo {self.N}")
        for byte in datos:
            descifrado = (a_inv * (byte - b)) % self.N
            resultado.append(descifrado)
        return bytes(resultado)

    def encontrar_a_b(self, x1, c1, x2, c2):
        """
        Encuentra las claves 'a' y 'b' usando dos pares de valores originales y cifrados.

        Args:
            x1 (int): Primer valor original.
            c1 (int): Primer valor cifrado.
            x2 (int): Segundo valor original.
            c2 (int): Segundo valor cifrado.

        Returns:
            tuple: Una tupla con las claves 'a' y 'b'.

        Raises:
            ValueError: Si no existe el inverso multiplicativo para delta_x y el módulo.
        """
        delta_x = (x1 - x2) % self.N
        delta_c = (c1 - c2) % self.N
        delta_x_inv = self.mod_inverse(delta_x, self.N)
        if delta_x_inv is None:
            raise ValueError(f"No existe el inverso multiplicativo para delta_x={delta_x} y módulo {self.N}")
        a = (delta_c * delta_x_inv) % self.N
        b = (c1 - a * x1) % self.N
        return a, b

    def probar_firmas(self, datos_cifrados):
        """
        Prueba las firmas conocidas en los primeros bytes de los datos cifrados para identificar el tipo de archivo.

        Args:
            datos_cifrados (bytes): Los datos cifrados.

        Returns:
            tuple: Una tupla con las claves 'a', 'b' y el tipo de archivo identificado, o (None, None, "Desconocido") si no se identifica.
        """
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
        """
        Descifra un archivo completo dado su ruta, identificando el tipo de archivo y las claves 'a' y 'b'.

        Args:
            file_path (str): La ruta del archivo cifrado.

        Returns:
            None
        """
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