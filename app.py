from flask import Flask, request, jsonify, render_template
from rule_parser import parse_rule
from database import init_db, save_rule, get_rules
import json

app = Flask(__name__)

# Initialize database
init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/create_rule', methods=['POST'])
def create_rule():
    data = request.json
    rule_string = data.get('rule', None)
    
    if not rule_string:
        return jsonify({"error": "No rule string provided"}), 400
    
    try:
        ast = parse_rule(rule_string)
        # For simplicity, just return the AST without saving it to the DB
        return jsonify({"ast": ast.to_dict()}), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": "Internal server error: " + str(e)}), 500



@app.route('/api/combine_rules', methods=['POST'])
def combine_rules():
    rule_ids = request.json.get('rule_ids')
    try:
        rules = get_rules(rule_ids)
        combined_ast = combine_ast([json.loads(rule['ast']) for rule in rules])
        return jsonify({"combined_ast": combined_ast}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/evaluate_rule', methods=['POST'])
def evaluate_rule():
    ast = request.json.get('ast')
    data = request.json.get('data')
    try:
        result = eval_ast(ast, data)
        return jsonify({"result": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=False)
