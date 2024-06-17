from flask import Flask, render_template, jsonify, send_file, request
import os
from mainKBC import multipleSimulations, singleSimulation

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/main')
def main():
    return render_template('main.html')

@app.route('/run-simulations', methods=['POST'])
def run_simulations():
    # 调用 multipleSimulations 函数
    results, plot_path = singleSimulation()
    
    # 返回结果和生成的图片路径
    return jsonify({
        'results': results,
        'plot_path': plot_path
    })

@app.route('/get-plot')
def get_plot():
    plot_path = request.args.get('path')
    # 返回生成的图像或PDF文件
    # return send_file(plot_path, mimetype='application/pdf')
    return send_file(plot_path, mimetype='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
