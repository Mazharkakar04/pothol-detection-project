from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
from werkzeug.utils import secure_filename
from db_config import get_db_connection
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
# from werkzeug.security import generate_password_hash, check_password_hash # Hashing is removed as per your request

app = Flask(__name__)
app.secret_key = "your_strong_secret_key_here"
app.config['UPLOAD_FOLDER'] = "static/uploads"
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5 MB

# Load the DL model
try:
    model = load_model('pothole_model/pothole_model.h5')
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

# Allowed file types
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# --- Route Protection with Session Management ---
@app.before_request
def require_login():
    allowed_routes = ['home', 'login', 'login_post', 'static']
    if request.endpoint in allowed_routes or 'user_id' in session:
        return
    return redirect(url_for('login'))

# --- ROUTES ---

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    role = request.form.get('role')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if role == 'user':
        email = request.form.get('user-email')
        password = request.form.get('user-password')
        cursor.execute("SELECT * FROM users WHERE email = %s AND role = 'user'", (email,))
        user = cursor.fetchone()

        if user and user['password'] == password:
            session['user_id'] = user['id']
            flash('Login successful!', 'success')
            return redirect(url_for('user_dashboard'))
        else:
            flash('Invalid user credentials', 'danger')
            return redirect(url_for('login'))

    elif role == 'admin':
        admin_id = request.form.get('admin-id')
        password = request.form.get('admin-password')
        cursor.execute("SELECT * FROM users WHERE name = %s AND role = 'admin'", (admin_id,))
        admin = cursor.fetchone()

        if admin and admin['password'] == password:
            session['user_id'] = admin['id']
            flash('Admin login successful!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid admin credentials', 'danger')
            return redirect(url_for('login'))

    cursor.close()
    conn.close()
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash("You have been logged out.", "success")
    return redirect(url_for('home'))

@app.route('/user_dashboard')
def user_dashboard():
    user_id = session.get('user_id')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM complaints WHERE user_id = %s", (user_id,))
    complaints = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('user_dashboard.html', complaints=complaints)

@app.route('/admin_dashboard')
def admin_dashboard():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM complaints")
    complaints = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('admin_dashboard.html', complaints=complaints)

@app.route('/submit_complaint', methods=['POST'])
def submit_complaint():
    user_id = session.get('user_id')
    location = request.form.get('pothole-location')
    description = request.form.get('pothole-description')
    file = request.files.get('pothole-image')

    if not file or not allowed_file(file.filename):
        flash("Invalid file format!", "danger")
        return redirect(url_for('user_dashboard'))

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    if model:
        try:
            img = image.load_img(filepath, target_size=(224, 224))
            img_array = image.img_to_array(img) / 255.0
            img_array = np.expand_dims(img_array, axis=0)
            
            # Predict the class (pothole or not)
            prediction = model.predict(img_array)
            predicted_class = np.argmax(prediction, axis=1)[0]
            
            # Check if the image is a pothole based on a class index
            # NOTE: This assumes your model's class indices are mapped as follows:
            # Class 0: Not a Pothole
            # Class 1: White severity pothole
            # Class 2: Yellow severity pothole
            # Class 3: Red severity pothole
            
            if predicted_class == 0:
                flash("The uploaded image is not a pothole. Please upload a valid image.", "warning")
                return redirect(url_for('user_dashboard'))
            
            # Map model output to severity color
            severity_map = {1: "White", 2: "Yellow", 3: "Red"}
            severity_color = severity_map.get(predicted_class, "White")
            
        except Exception as e:
            print(f"Error during model prediction: {e}")
            flash("An error occurred during image processing. Please try again.", "danger")
            return redirect(url_for('user_dashboard'))
    else:
        flash("Image processing model is not available.", "danger")
        return redirect(url_for('user_dashboard'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO complaints (user_id, location, description, image, status, severity) VALUES (%s, %s, %s, %s, %s, %s)",
                   (user_id, location, description, filename, 'Pending', severity_color))
    conn.commit()
    cursor.close()
    conn.close()

    flash(f"Complaint submitted successfully! Severity is: {severity_color}", "success")
    return redirect(url_for('user_dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
