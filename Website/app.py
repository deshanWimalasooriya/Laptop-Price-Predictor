from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)

def prediction(features):
    filename = 'model/predictor.pickle'
    with open(filename, 'rb') as file:
        model = pickle.load(file)
        
    pred_value = model.predict([features])
    return pred_value


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        
        pred = 0
        ram = request.form['ram']
        weight = request.form['weight']
        company = request.form['company']
        typename = request.form['typename']
        opsys = request.form['opsys']
        gpu = request.form['gpuname']
        cpu = request.form['cpuname']
        touchscreen = request.form.getlist('touchscreen')
        ips = request.form.getlist('ips')
        
        feature_list = []
        feature_list.append(int(ram))
        feature_list.append(float(weight))
        feature_list.append(len(touchscreen))
        feature_list.append(len(ips))
        
        company_list = ['apple', 'asus', 'dell', 'hp', 'lenovo', 'msi', 'acer', 'toshiba', 'other']
        typename_list = ['2in1convertible', 'gaming', 'notebook', 'netbook', 'ultrabook', 'workstation']
        opsys_list = ['windows', 'mac', 'linux', 'other']
        cpu_list = ['intelcorei7', 'intelcorei5', 'intelcorei3', 'other', 'amd']
        gpu_list = ['nvidia', 'intel', 'amd']
        
        def traverse(item_list, value):
            for item in item_list:
                if item == value:
                    feature_list.append(1)
                else:
                    feature_list.append(0)
        
        traverse(company_list, company)
        traverse(typename_list, typename)
        traverse(opsys_list, opsys)
        traverse(cpu_list, cpu)
        traverse(gpu_list, gpu)
        
        pred = prediction(feature_list)
        pred = np.round(pred[0])

    return render_template('index.html', pred = pred)

if __name__ == '__main__':
    app.run(debug=True)