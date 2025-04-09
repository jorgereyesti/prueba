import sqlite3

conn = sqlite3.connect('registro.db')
cursor = conn.cursor()

# Crear tablas normalizadas
cursor.execute("CREATE TABLE IF NOT EXISTS generos (id INTEGER PRIMARY KEY, descripcion TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS tiempo_calle (id INTEGER PRIMARY KEY, descripcion TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS ubicaciones (id INTEGER PRIMARY KEY, direccion TEXT, coordenadas TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS problematica (id INTEGER PRIMARY KEY, descripcion TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS estado_civil (id INTEGER PRIMARY KEY, descripcion TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS mant_economico (id INTEGER PRIMARY KEY, descripcion TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS obra_social (id INTEGER PRIMARY KEY, descripcion TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS nivel_estudios (id INTEGER PRIMARY KEY, descripcion TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS grupo_familiar (id INTEGER PRIMARY KEY, descripcion TEXT)")

# Crear tabla personas
cursor.execute("""
CREATE TABLE IF NOT EXISTS personas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT,
    dni TEXT,
    edad INTEGER,
    genero_id INTEGER,
    tiempo_calle_id INTEGER,
    ubicacion_id INTEGER,
    estado_civil_id INTEGER,
    nivel_estudios_id INTEGER,
    mant_economico_id INTEGER,
    obra_social_id INTEGER,
    grupo_familiar_id INTEGER,
    contacto_emergencia TEXT,
    observaciones TEXT,
    FOREIGN KEY (genero_id) REFERENCES generos(id),
    FOREIGN KEY (tiempo_calle_id) REFERENCES tiempo_calle(id),
    FOREIGN KEY (ubicacion_id) REFERENCES ubicaciones(id),
    FOREIGN KEY (estado_civil_id) REFERENCES estado_civil(id),
    FOREIGN KEY (nivel_estudios_id) REFERENCES nivel_estudios(id),
    FOREIGN KEY (mant_economico_id) REFERENCES mant_economico(id),
    FOREIGN KEY (obra_social_id) REFERENCES obra_social(id),
    FOREIGN KEY (grupo_familiar_id) REFERENCES grupo_familiar(id)
)
""")
# Crear tabla persona_problematica (una persona puede tener problematicas)
cursor.execute("""
CREATE TABLE persona_problematica (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    persona_id INTEGER NOT NULL,
    problematica_id INTEGER NOT NULL,
    FOREIGN KEY (persona_id) REFERENCES personas(id),
    FOREIGN KEY (problematica_id) REFERENCES problematica(id)
)
""")

# Insertar valores fijos
cursor.executemany("INSERT INTO generos (descripcion) VALUES (?)", [
    ("Masculino",), ("Femenino",), ("X",)
])
cursor.executemany("INSERT INTO tiempo_calle (descripcion) VALUES (?)", [
    ("1 a 11 meses",), ("1 a 5 años",), ("5 a 10 años",), ("más de 10 años",), ("no especifica",)
])
cursor.executemany("INSERT INTO problematica (descripcion) VALUES (?)", [
    ("Elección propia",), ("Alcohol",), ("Droga",), ("Violencia de género",),
    ("Tabaco",), ("Discapacidad",), ("Abandono",)
])
cursor.executemany("INSERT INTO estado_civil (descripcion) VALUES (?)", [
    ("Soltero",), ("Casado",), ("Divorciado",), ("Viudo",), ("Otro",)
])
cursor.executemany("INSERT INTO mant_economico (descripcion) VALUES (?)", [
    ("AUH",), ("Cartonero",), ("Pensión Alimenticia",), ("Pensión Discapacidad",),
    ("Cuida auto",), ("Jubilado",), ("Empleado",), ("Ninguno",)
])
cursor.executemany("INSERT INTO obra_social (descripcion) VALUES (?)", [
    ("PAMI",), ("IPSST",), ("Otro",), ("No posee",)
])
cursor.executemany("INSERT INTO nivel_estudios (descripcion) VALUES (?)", [
    ("Ninguno",), ("Primario completo",), ("Primario incompleto",),
    ("Secundario completo",), ("Secundario incompleto",),
    ("Terciario completo",), ("Terciario incompleto",),
    ("Universitario completo",), ("Universitario incompleto",)
])
cursor.executemany("INSERT INTO grupo_familiar (descripcion) VALUES (?)", [
    ("Unipersonal",), ("Hijos",), ("Padre",), ("Madre",), ("No declara",)
])

conn.commit()
conn.close()
print("Base de datos creada correctamente.")
