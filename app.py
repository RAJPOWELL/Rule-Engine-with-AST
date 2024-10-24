# app.py
from flask import Flask, request, jsonify, render_template
import sqlite3
import json
from ast_parser import create_rule, combine_rules, evaluate_rule
import os

app = Flask(__name__)

def init_db():
    # Delete the existing database file if it exists
    if os.path.exists('rules.db'):
        os.remove('rules.db')
    
    conn = sqlite3.connect('rules.db')
    c = conn.cursor()
    # Updated schema with correct column names
    c.execute('''
        CREATE TABLE IF NOT EXISTS rules
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
         rule_name TEXT NOT NULL,
         rule_string TEXT NOT NULL,
         ast_json TEXT NOT NULL)
    ''')
    conn.commit()
    conn.close()

# Initialize the database when the application starts
with app.app_context():
    init_db()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/rules', methods=['POST'])
def create_new_rule():
    data = request.json
    rule_string = data['rule_string']
    rule_name = data['name']
    
    try:
        # Create AST and convert to JSON
        ast = create_rule(rule_string)
        ast_json = json.dumps(ast)
        
        conn = sqlite3.connect('rules.db')
        c = conn.cursor()
        c.execute('INSERT INTO rules (rule_name, rule_string, ast_json) VALUES (?, ?, ?)',
                 (rule_name, rule_string, ast_json))
        conn.commit()
        rule_id = c.lastrowid
        conn.close()
        
        return jsonify({'id': rule_id, 'message': 'Rule created successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/rules', methods=['GET'])
def get_rules():
    conn = sqlite3.connect('rules.db')
    c = conn.cursor()
    c.execute('SELECT id, rule_name, rule_string FROM rules')
    rules = [{'id': r[0], 'name': r[1], 'rule_string': r[2]} 
             for r in c.fetchall()]
    conn.close()
    return jsonify(rules)

@app.route('/api/evaluate', methods=['POST'])
def evaluate():
    data = request.json
    user_data = data['user_data']
    rule_ids = data['rule_ids']
    
    conn = sqlite3.connect('rules.db')
    c = conn.cursor()
    placeholder = ','.join('?' * len(rule_ids))
    c.execute(f'SELECT ast_json FROM rules WHERE id IN ({placeholder})', rule_ids)
    rules = [json.loads(r[0]) for r in c.fetchall()]
    conn.close()
    
    if not rules:
        return jsonify({'error': 'No rules found'}), 404
    
    combined_ast = combine_rules(rules)
    result = evaluate_rule(combined_ast, user_data)
    
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=False)