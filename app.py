from flask import Flask, render_template, request,jsonify
import sqlite3
import pickle

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/contact', methods = ['GET', 'POST'])
def contactus():
    if request.method == 'POST':
        fname = request.form.get('name')
        pno = request.form.get('phone')
        email = request.form.get('email')
        addr = request.form.get('address')
        msg = request.form.get('message')
        conn = sqlite3.connect('crop.db')
        cur = conn.cursor()
        cur.execute(f'''
                    INSERT INTO CONTACT VALUES("{fname}", "{pno}","{email}", "{addr}", "{msg}")
                ''')
        conn.commit()
        return render_template('message.html')
    else:
        return render_template('contactus.html')
    
@app.route('/analysis')
def analysis():
    return render_template('analysis.html')

# Dictionary to map encoded values to crop names


@app.route('/prediction', methods=['GET', 'POST'])
def prediction():
    if request.method == 'POST':
        nitrogen = request.form.get("nitrogen")
        phos = request.form.get("phosphorous")
        pot = request.form.get("potassium")
        ph = request.form.get("ph")
        soil = request.form.get("soil-color")
        rain = request.form.get("rainfall")
        temp = request.form.get("temperature")
        print(temp)

        # Load the model and make prediction
        with open("model.pickle", 'rb') as mod:
            model = pickle.load(mod)
        pred = model.predict([[float(nitrogen), float(phos), float(pot), float(ph), float(soil), float(rain), float(temp)]])
        print(pred)
        
        # Create a dictionary to match prediction result to crop
        crops = {
            0: 'Cotton',
            1: 'Ginger',
            2: 'Gram',
            3: 'Grapes',
            4: 'Groundnut',
            5: 'Jowar',
            6: 'Maize',
            7: 'Masoor',
            8: 'Moong',
            9: 'Rice',
            10: 'Soybean',
            11: 'Sugarcane',
            12: 'Tur',
            13: 'Turmeric',
            14: 'Urad',
            15: 'Wheat'
        }
        
        crop = crops.get(int(round(pred[0])), 'Unknown')
        return render_template('result.html', pred=crop)
    else:
        return render_template('prediction.html')


# Create a dictionary to store the results
results = {
    "Logistic Regression": {
        "Training Accuracy": 0.7620,
        "Test Accuracy": 0.7719,
        "Training Loss": 0.6661,
        "Test Loss": 0.6685
    },
    "K-Nearest Neighbors": {
        "Training Accuracy": 0.9917,
        "Test Accuracy": 0.9546,
        "Training Loss": 0.0452,
        "Test Loss": 0.4048
    },
    "Random Forest": {
        "Training Accuracy": 1.0000,
        "Test Accuracy": 0.9967,
        "Training Loss": 0.0188,
        "Test Loss": 0.0506
    },
    "Gradient Boosting": {
        "Training Accuracy": 1.0000,
        "Test Accuracy": 0.9967,
        "Training Loss": 0.0165,
        "Test Loss": 0.0228
    },
    "XGBoost": {
        "Training Accuracy": 1.0000,
        "Test Accuracy": 0.9989,
        "Training Loss": 0.0060,
        "Test Loss": 0.0109
    },
    "Support Vector Machine": {
        "Training Accuracy": 0.9150,
        "Test Accuracy": 0.9147,
        "Training Loss": 0.2942,
        "Test Loss": 0.3243
    },
    "Naive Bayes": {
        "Training Accuracy": 0.7884,
        "Test Accuracy": 0.7841,
        "Training Loss": 0.6678,
        "Test Loss": 0.6601
    }
}

# You can now access the results dictionary for any model

@app.route('/results')
def get_results():
    return jsonify(results)

@app.route('/output')
def output():
    return render_template('output.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)