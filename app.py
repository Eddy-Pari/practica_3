from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Lista de seminarios
seminarios = ["Inteligencia Artificial", "Machine Learning", "Simulación con Arena", "Robótica Educativa"]

# Datos inscritos
inscritos = []
current_id = 1

# Página principal con el formulario de registro
@app.route('/', methods=['GET', 'POST'])
def index():
    global current_id
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        fecha = request.form['fecha']
        turno = request.form['turno']
        seminarios_seleccionados = request.form.getlist('seminarios')
        
        nuevo_inscrito = {
            'id': current_id,
            'nombre': nombre,
            'apellido': apellido,
            'fecha': fecha,
            'turno': turno,
            'seminarios': seminarios_seleccionados
        }
        
        inscritos.append(nuevo_inscrito)
        current_id += 1
        
        return redirect(url_for('lista'))

    return render_template('index.html', seminarios=seminarios)

# Lista de inscritos
@app.route('/lista')
def lista():
    return render_template('lista.html', inscritos=inscritos)

# Editar un inscrito
@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    inscrito = next((i for i in inscritos if i['id'] == id), None)
    if not inscrito:
        return redirect(url_for('lista'))
    
    if request.method == 'POST':
        inscrito['nombre'] = request.form['nombre']
        inscrito['apellido'] = request.form['apellido']
        inscrito['fecha'] = request.form['fecha']
        inscrito['turno'] = request.form['turno']
        inscrito['seminarios'] = request.form.getlist('seminarios')
        return redirect(url_for('lista'))

    return render_template('editar.html', inscrito=inscrito, seminarios=seminarios)

# Eliminar un inscrito
@app.route('/eliminar/<int:id>')
def eliminar(id):
    global inscritos
    inscritos = [i for i in inscritos if i['id'] != id]
    return redirect(url_for('lista'))

if __name__ == '_main_':
    app.run(debug=True)