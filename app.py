from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('registro.db')
    conn.row_factory = sqlite3.Row
    return conn
#rutas
@app.route('/')
def index():
    conn = get_db_connection()
    personas = conn.execute('''
    SELECT 
        personas.id,
        personas.nombre,
        personas.dni,
        personas.edad,
        generos.descripcion AS genero_descripcion,
        tiempo_calle.descripcion AS tiempo_calle_nombre,
        ubicaciones.direccion,
        ubicaciones.coordenadas,
        personas.contacto_emergencia,
        personas.observaciones
    FROM personas
    LEFT JOIN generos ON personas.genero_id = generos.id
    LEFT JOIN tiempo_calle ON personas.tiempo_calle_id = tiempo_calle.id
    LEFT JOIN ubicaciones ON personas.ubicacion_id = ubicaciones.id
''').fetchall()
# Consulta de problemáticas asociadas
    problematicas_por_persona = conn.execute("""
        SELECT pp.persona_id, GROUP_CONCAT(pr.descripcion, ', ') as problematicas
        FROM persona_problematica pp
        JOIN problematica pr ON pp.problematica_id = pr.id
        GROUP BY pp.persona_id
    """).fetchall()
# Convertir problemáticas a un diccionario {persona_id: "lista de problematicas"}
    problemas_dict = {row["persona_id"]: row["problematicas"] for row in problematicas_por_persona}
    print("problematicas: ", problemas_dict )
    # Agregar las problemáticas a cada persona
    personas_con_problemas = []
    for persona in personas:
        persona = dict(persona)
        persona["problematicas"] = problemas_dict.get(persona["id"], "Sin especificar")
        personas_con_problemas.append(persona)
    
    print("personas con problematicas: ", personas_con_problemas )
    conn.close()
    return render_template("index.html", personas=personas_con_problemas)

#ruta manual de agregar un nuevo elemento
@app.route('/agregar', methods=('GET', 'POST'))
def agregar():
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        nombre = request.form['nombre']
        dni = request.form['dni']
        edad = request.form['edad']
        genero_id = request.form['genero_id']
        tiempo_calle_id = request.form['tiempo_calle_id']
        estado_civil_id = request.form['estado_civil_id']
        nivel_estudios_id = request.form['nivel_estudios_id']
        mant_economico_id = request.form['mant_economico_id']
        obra_social_id = request.form['obra_social_id']
        grupo_familiar_id = request.form['grupo_familiar_id']
        contacto_emergencia = request.form['contacto_emergencia']
        observaciones = request.form['observaciones']
        direccion = request.form['direccion']
        coordenadas = request.form['coordenadas']
        problematica_ids = request.form.getlist('problematica_ids')

# Insertar ubicación y obtener el ID generado
        cursor.execute("""
        INSERT INTO ubicaciones (direccion, coordenadas) VALUES (?, ?)
        """, (direccion, coordenadas))
        ubicacion_id = cursor.lastrowid

        cursor.execute("""
            INSERT INTO personas (
                nombre, dni, edad, genero_id, tiempo_calle_id, ubicacion_id, estado_civil_id,
                nivel_estudios_id, mant_economico_id, obra_social_id,
                grupo_familiar_id, contacto_emergencia, observaciones
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            nombre, dni, edad, genero_id, tiempo_calle_id, ubicacion_id, estado_civil_id,
            nivel_estudios_id, mant_economico_id, obra_social_id,
            grupo_familiar_id, contacto_emergencia, observaciones
        ))

        persona_id = cursor.lastrowid

        for pid in problematica_ids:
            cursor.execute(
                "INSERT INTO persona_problematica (persona_id, problematica_id) VALUES (?, ?)",
                (persona_id, pid)
            )

        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    generos = conn.execute("SELECT * FROM generos").fetchall()
    tiempo_calle = conn.execute("SELECT * FROM tiempo_calle").fetchall()
    estado_civil = conn.execute("SELECT * FROM estado_civil").fetchall()
    ubicaciones = conn.execute("SELECT * FROM ubicaciones").fetchall()
    nivel_estudios = conn.execute("SELECT * FROM nivel_estudios").fetchall()
    mant_economico = conn.execute("SELECT * FROM mant_economico").fetchall()
    obra_social = conn.execute("SELECT * FROM obra_social").fetchall()
    grupo_familiar = conn.execute("SELECT * FROM grupo_familiar").fetchall()
    problematica = conn.execute("SELECT * FROM problematica").fetchall()

    conn.close()

    return render_template(
        'agregar.html',
        generos=generos,
        tiempo_calle=tiempo_calle,
        ubicaciones = ubicaciones,
        estado_civil=estado_civil,
        nivel_estudios=nivel_estudios,
        mant_economico=mant_economico,
        obra_social=obra_social,
        grupo_familiar=grupo_familiar,
        problematica=problematica
    )

@app.route('/eliminar/<int:id>', methods=['POST', 'GET'])
def eliminar(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Eliminar relaciones con problemáticas primero y ubicaciones
    cursor.execute("DELETE FROM persona_problematica WHERE persona_id = ?", (id,))

    # Eliminar la persona
    cursor.execute("DELETE FROM personas WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        nombre = request.form['nombre']
        dni = request.form['dni']
        edad = request.form['edad']
        genero_id = request.form['genero_id']
        tiempo_calle_id = request.form['tiempo_calle_id']
        estado_civil_id = request.form['estado_civil_id']
        nivel_estudios_id = request.form['nivel_estudios_id']
        mant_economico_id = request.form['mant_economico_id']
        obra_social_id = request.form['obra_social_id']
        grupo_familiar_id = request.form['grupo_familiar_id']
        contacto_emergencia = request.form['contacto_emergencia']
        observaciones = request.form['observaciones']
        direccion = request.form['direccion']
        coordenadas = request.form['coordenadas']
        problematica_ids = request.form.getlist('problematica_ids')

        # Actualizar ubicación
        cursor.execute("""
            UPDATE ubicaciones
            SET direccion = ?, coordenadas = ?
            WHERE id = (SELECT ubicacion_id FROM personas WHERE id = ?)
        """, (direccion, coordenadas, id))

        # Actualizar persona
        cursor.execute("""
            UPDATE personas SET
                nombre = ?, dni = ?, edad = ?, genero_id = ?, tiempo_calle_id = ?,
                estado_civil_id = ?, nivel_estudios_id = ?, mant_economico_id = ?,
                obra_social_id = ?, grupo_familiar_id = ?, contacto_emergencia = ?,
                observaciones = ?
            WHERE id = ?
        """, (
            nombre, dni, edad, genero_id, tiempo_calle_id,
            estado_civil_id, nivel_estudios_id, mant_economico_id,
            obra_social_id, grupo_familiar_id, contacto_emergencia,
            observaciones, id
        ))

        # Actualizar problemáticas
        cursor.execute("DELETE FROM persona_problematica WHERE persona_id = ?", (id,))
        for pid in problematica_ids:
            cursor.execute(
                "INSERT INTO persona_problematica (persona_id, problematica_id) VALUES (?, ?)",
                (id, pid)
            )

        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    # Obtener datos para el formulario
    persona = conn.execute("SELECT * FROM personas WHERE id = ?", (id,)).fetchone()
    ubicacion = conn.execute("SELECT * FROM ubicaciones WHERE id = ?", (persona['ubicacion_id'],)).fetchone()

    persona = dict(persona)
    persona['direccion'] = ubicacion['direccion']
    persona['coordenadas'] = ubicacion['coordenadas']

    # problemáticas asociadas
    problematica_ids = [row['problematica_id'] for row in conn.execute(
        "SELECT problematica_id FROM persona_problematica WHERE persona_id = ?", (id,)
    ).fetchall()]
    persona['problematica_ids'] = problematica_ids

    generos = conn.execute("SELECT * FROM generos").fetchall()
    tiempo_calle = conn.execute("SELECT * FROM tiempo_calle").fetchall()
    estado_civil = conn.execute("SELECT * FROM estado_civil").fetchall()
    nivel_estudios = conn.execute("SELECT * FROM nivel_estudios").fetchall()
    mant_economico = conn.execute("SELECT * FROM mant_economico").fetchall()
    obra_social = conn.execute("SELECT * FROM obra_social").fetchall()
    grupo_familiar = conn.execute("SELECT * FROM grupo_familiar").fetchall()
    problematica = conn.execute("SELECT * FROM problematica").fetchall()

    conn.close()

    return render_template('editar.html', persona=persona,
                           generos=generos,
                           tiempo_calle=tiempo_calle,
                           estado_civil=estado_civil,
                           nivel_estudios=nivel_estudios,
                           mant_economico=mant_economico,
                           obra_social=obra_social,
                           grupo_familiar=grupo_familiar,
                           problematica=problematica)

if __name__ == '__main__':
    app.run(debug=True)
