class UsuarioSingleton:

    _instance = None

    def __new__(cls,nombre: str):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._nombre = nombre
        return cls._instance
    
    def obtenerNombre(self):
        return self._nombre


# Prueba del singleton
s1 = UsuarioSingleton("Santiago")

s2 = UsuarioSingleton("Juan")

print(s1.obtenerNombre())
print(s2.obtenerNombre())