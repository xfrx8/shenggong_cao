from flask import Flask, request, jsonify, render_template
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
from scipy.stats import linregress
from flask_cors import CORS
import pandas as pd

app = Flask(__name__, template_folder='templates')
CORS(app)

@app.route('/')
def index():
    # 返回 index.html 页面（位于 templates 文件夹中）
    return render_template('index.html')

@app.route('/fit_curve', methods=['POST'])
def fit_curve():
    try:
        data = request.get_json(force=True)
        concentrations = np.array(data['concentration'], dtype=float)
        voltages = np.array(data['voltage'], dtype=float)
    except Exception as e:
        return jsonify({'error': 'Invalid input data', 'message': str(e)}), 400

    slope, intercept, r_value, _, _ = linregress(concentrations, voltages)

    plt.figure()
    plt.scatter(concentrations, voltages, label="Data points")
    plt.plot(concentrations, slope * concentrations + intercept, color='red',
             label=f'Fit: y = {slope:.3f}x + {intercept:.3f}')
    plt.xlabel("Concentration (mM)")
    plt.ylabel("Voltage (V)")
    plt.title("Standard Curve")
    plt.legend()

    img_io = io.BytesIO()
    plt.savefig(img_io, format='png', bbox_inches='tight')
    plt.close()
    img_io.seek(0)
    plot_url = base64.b64encode(img_io.getvalue()).decode('ascii')

    return jsonify({
        'a': slope,
        'b': intercept,
        'r_squared': r_value ** 2,
        'plot_url': plot_url
    })

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json(force=True)
        voltage = float(data['voltage'])
        a = float(data['a'])
        b = float(data['b'])
    except Exception as e:
        return jsonify({'error': 'Invalid input data', 'message': str(e)}), 400

    try:
        concentration = (voltage - b) / a
    except ZeroDivisionError:
        return jsonify({'error': 'Division by zero in calculation'}), 400
    except Exception as e:
        return jsonify({'error': 'Calculation error', 'message': str(e)}), 400

    return jsonify({'concentration': concentration})

@app.route('/upload_csv', methods=['POST'])
def upload_csv():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        df = pd.read_csv(file)
        if 'concentration' not in df.columns or 'voltage' not in df.columns:
            return jsonify({'error': 'CSV must contain columns: concentration, voltage'}), 400

        concentrations = df['concentration'].values.astype(float)
        voltages = df['voltage'].values.astype(float)
    except Exception as e:
        return jsonify({'error': 'Error reading CSV', 'message': str(e)}), 400

    slope, intercept, r_value, _, _ = linregress(concentrations, voltages)

    plt.figure()
    plt.scatter(concentrations, voltages, label="Data points")
    plt.plot(concentrations, slope * concentrations + intercept, color='red',
             label=f'Fit: y = {slope:.3f}x + {intercept:.3f}')
    plt.xlabel("Concentration (mM)")
    plt.ylabel("Voltage (V)")
    plt.title("Standard Curve (CSV)")
    plt.legend()

    img_io = io.BytesIO()
    plt.savefig(img_io, format='png', bbox_inches='tight')
    plt.close()
    img_io.seek(0)
    plot_url = base64.b64encode(img_io.getvalue()).decode('ascii')

    return jsonify({
        'a': slope,
        'b': intercept,
        'r_squared': r_value ** 2,
        'plot_url': plot_url
    })

if __name__ == '__main__':
    app.run(debug=True)
