from flask import Flask, request, jsonify, render_template
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch

# Initialize Flask app
app = Flask(__name__)

# Load the original CodeT5 model
codeT5_path = "D:/codeT5"
codeT5_model = AutoModelForSeq2SeqLM.from_pretrained(codeT5_path)
codeT5_tokenizer = AutoTokenizer.from_pretrained(codeT5_path)

# Load the CodeT5 fine-tuned on CodeAlpaca
codeAlpaca_path = "D:/CodeAlpaca"
alpaca_model = AutoModelForSeq2SeqLM.from_pretrained(codeAlpaca_path)
alpaca_tokenizer = AutoTokenizer.from_pretrained(codeAlpaca_path)

@app.route('/generate-code', methods=['POST'])
def generate_code():
    try:
        data = request.json
        prompt = data.get('prompt', '')
        selected_model = data.get('model', 'codeT5')  # default to codeT5

        if selected_model == 'codeT5':
            model = codeT5_model
            tokenizer = codeT5_tokenizer
        elif selected_model == 'BART':
            model = alpaca_model
            tokenizer = alpaca_tokenizer
        else:
            return jsonify({"error": "Invalid model selected"}), 400

        input_text = "generate code: " + prompt
        inputs = tokenizer.encode(input_text, return_tensors="pt", max_length=512, truncation=True)

        outputs = model.generate(inputs, max_length=512, num_return_sequences=1)
        generated_code = tokenizer.decode(outputs[0], skip_special_tokens=True)

        return jsonify({"generated_code": generated_code})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
