from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3



app = Flask(__name__)
CORS(app)

def create_table():
    conn = sqlite3.connect('events.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS events
                 (day TEXT, repeat_type TEXT, start_time TEXT, end_time TEXT, duration TEXT, color TEXT, title TEXT)''')
    conn.commit()
    conn.close()

@app.route('/add_event', methods=['POST'])
def add_event():
    event_data = request.json
    day = event_data['day']
    repeat_type = event_data['repeatType']
    start_time = event_data['startTime']
    end_time = event_data['endTime']
    duration = event_data['duration']
    color = event_data['color']
    title = event_data['title']
    
    conn = sqlite3.connect('events.db')
    c = conn.cursor()
    c.execute("INSERT INTO events VALUES (?, ?, ?, ?, ?, ?, ?)", (day, repeat_type, start_time, end_time, duration, color, title))
    conn.commit()
    conn.close()
    
    return 'Event added successfully'

@app.route('/get_events', methods=['GET'])
def get_events():
    # Conectar ao banco de dados SQLite
    conn = sqlite3.connect('events.db')
    c = conn.cursor()

    # Consultar o banco de dados para buscar os eventos
    c.execute("SELECT * FROM events")
    events = c.fetchall()

    # Fechar a conexão com o banco de dados
    conn.close()

    # Formatar os eventos como lista de dicionários
    formatted_events = [{'day': event[0], 'start_time': event[2] ,'color': event[5], 'title': event[6]} for event in events]
    print(formatted_events)
    # Retornar os eventos como JSON
    return jsonify(formatted_events)

if __name__ == '__main__':
    create_table()
    app.run(host='0.0.0.0', port=6060)