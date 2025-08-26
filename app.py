from flask import Flask, render_template, request, redirect, url_for, flash
import os
from werkzeug.utils import secure_filename
from db_config import get_db_connection
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np

app = Flask(__name__)
app.secret_key = "supersecretkey"
app.config['UPLOAD_FOLDER'] = "static/uploads"
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5 MB

# Load the DL model
model = load_model('pothole_model/pothole_model.h5')

# Allowed file types
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# --- ROUTES ---

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/user_dashboard')
def user_dashboard():
    # Here you can fetch user complaints from MySQL
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM complaints WHERE user_id = 1")  # Example user_id
    complaints = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('user_dashboard.html', complaints=complaints)

@app.route('/admin_dashboard')
def admin_dashboard():
    # Fetch all complaints for admin
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM complaints")
    complaints = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('admin_dashboard.html', complaints=complaints)

@app.route('/submit_complaint', methods=['POST'])
def submit_complaint():
    location = request.form['pothole-location']
    description = request.form['pothole-description']
    file = request.files['pothole-image']

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # --- DL Model Prediction ---
        img = image.load_img(filepath, target_size=(224,224))
        img_array = image.img_to_array(img)/255.0
        img_array = np.expand_dims(img_array, axis=0)
        severity_pred = model.predict(img_array)
        severity = np.argmax(severity_pred, axis=1)[0]  # example

        # Map model output to severity color
        severity_map = {0: "White", 1: "Yellow", 2: "Red"}
        severity_color = severity_map.get(severity, "White")

        # Save to DB
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO complaints (user_id, location, description, image, status, severity) VALUES (%s,%s,%s,%s,%s,%s)",
                       (1, location, description, filename, 'Pending', severity_color))
        conn.commit()
        cursor.close()
        conn.close()

        flash("Complaint submitted successfully!", "success")
        return redirect(url_for('user_dashboard'))
    else:
        flash("Invalid file format!", "danger")
        return redirect(url_for('user_dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
