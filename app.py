import sys
import os

# ⚠️ Fix for flask_sqlalchemy
sys.path.append(r"C:\Users\KIIT0001\AppData\Roaming\Python\Python311\site-packages")

from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = "supersecretkey"

# ================= DATABASE CONFIG =================
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projects.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# ================= UPLOAD CONFIG =================
app.config['UPLOAD_FOLDER'] = 'static/images/certificates'
app.config['RESUME_FOLDER'] = 'static/resume'

# ================= MAIL CONFIG =================
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True

# YOUR GMAIL
app.config['MAIL_USERNAME'] = 'sambhavsahoo109@gmail.com'

# YOUR APP PASSWORD
app.config['MAIL_PASSWORD'] = 'yaja wddq njkk ewoy'

db = SQLAlchemy(app)
mail = Mail(app)

# ================= PROJECT MODEL =================
class Project(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(
        db.String(100),
        nullable=False,
        unique=True
    )

    description = db.Column(
        db.String(300),
        nullable=False
    )

    github = db.Column(
        db.String(200),
        nullable=False
    )

# ================= CERTIFICATE MODEL =================
class Certificate(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(
        db.String(150),
        nullable=False
    )

    subtitle = db.Column(
        db.String(200),
        nullable=False
    )

    image = db.Column(
        db.String(300),
        nullable=False
    )

# ================= CONTACT MODEL =================
class Contact(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(150),
        nullable=False
    )

    message = db.Column(
        db.Text,
        nullable=False
    )

# ================= HOME =================
@app.route('/')
def home():

    return render_template('index.html')

# ================= PROJECTS =================
@app.route('/projects')
def projects():

    all_projects = Project.query.order_by(
        Project.id.desc()
    ).all()

    return render_template(
        'projects.html',
        projects=all_projects
    )

# ================= CERTIFICATES =================
@app.route('/certificates')
def certificates():

    all_certificates = Certificate.query.order_by(
        Certificate.id.desc()
    ).all()

    return render_template(
        'certificates.html',
        certificates=all_certificates
    )

# ================= RESUME =================
@app.route('/resume')
def resume():

    return redirect(
        url_for(
            'static',
            filename='resume/resume.pdf'
        )
    )

# ================= LOGIN =================
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        password = request.form.get('password')

        if password == "admin123":

            session['admin'] = True

            flash(
                "Login Successful!",
                "success"
            )

            return redirect(url_for('admin'))

        else:

            flash(
                "Wrong Password!",
                "error"
            )

            return redirect(url_for('login'))

    return render_template('login.html')

# ================= ADMIN PANEL =================
@app.route('/admin', methods=['GET', 'POST'])
def admin():

    if not session.get('admin'):
        return redirect(url_for('login'))

    if request.method == 'POST':

        form_type = request.form.get('form_type')

        # ================= ADD PROJECT =================
        if form_type == "project":

            title = request.form.get('title')
            desc = request.form.get('description')
            github = request.form.get('github')

            if title and desc and github:

                try:

                    new_project = Project(
                        title=title.strip(),
                        description=desc.strip(),
                        github=github.strip()
                    )

                    db.session.add(new_project)
                    db.session.commit()

                    flash(
                        "Project Added Successfully!",
                        "success"
                    )

                except Exception:

                    db.session.rollback()

                    flash(
                        "Project already exists!",
                        "error"
                    )

        # ================= ADD CERTIFICATE =================
        elif form_type == "certificate":

            title = request.form.get('cert_title')
            subtitle = request.form.get('cert_subtitle')

            image = request.files.get('cert_image')

            if title and subtitle and image:

                filename = secure_filename(image.filename)

                image_path = os.path.join(
                    app.config['UPLOAD_FOLDER'],
                    filename
                )

                image.save(image_path)

                new_certificate = Certificate(
                    title=title.strip(),
                    subtitle=subtitle.strip(),
                    image=filename
                )

                db.session.add(new_certificate)
                db.session.commit()

                flash(
                    "Certificate Added Successfully!",
                    "success"
                )

            else:

                flash(
                    "All certificate fields required!",
                    "error"
                )

        return redirect(url_for('admin'))

    projects = Project.query.order_by(
        Project.id.desc()
    ).all()

    certificates = Certificate.query.order_by(
        Certificate.id.desc()
    ).all()

    contacts = Contact.query.order_by(
        Contact.id.desc()
    ).all()

    return render_template(
        'admin.html',
        projects=projects,
        certificates=certificates,
        contacts=contacts
    )

# ================= UPLOAD RESUME =================
@app.route('/upload_resume', methods=['POST'])
def upload_resume():

    if not session.get('admin'):
        return redirect(url_for('login'))

    file = request.files.get('resume_file')

    if file and file.filename != "":

        # ALWAYS SAVE AS resume.pdf
        save_path = os.path.join(
            app.config['RESUME_FOLDER'],
            'resume.pdf'
        )

        file.save(save_path)

        flash(
            "Resume Uploaded Successfully!",
            "success"
        )

    else:

        flash(
            "Please Select Resume PDF!",
            "error"
        )

    return redirect(url_for('admin'))

# ================= DELETE PROJECT =================
@app.route('/delete-project/<int:id>')
def delete_project(id):

    if not session.get('admin'):
        return redirect(url_for('login'))

    project = Project.query.get_or_404(id)

    db.session.delete(project)
    db.session.commit()

    flash(
        "Project Deleted!",
        "success"
    )

    return redirect(url_for('admin'))

# ================= DELETE CERTIFICATE =================
@app.route('/delete-certificate/<int:id>')
def delete_certificate(id):

    if not session.get('admin'):
        return redirect(url_for('login'))

    certificate = Certificate.query.get_or_404(id)

    image_path = os.path.join(
        app.config['UPLOAD_FOLDER'],
        certificate.image
    )

    if os.path.exists(image_path):
        os.remove(image_path)

    db.session.delete(certificate)
    db.session.commit()

    flash(
        "Certificate Deleted!",
        "success"
    )

    return redirect(url_for('admin'))

# ================= DELETE MESSAGE =================
@app.route('/delete-message/<int:id>')
def delete_message(id):

    if not session.get('admin'):
        return redirect(url_for('login'))

    message = Contact.query.get_or_404(id)

    db.session.delete(message)
    db.session.commit()

    flash(
        "Message Deleted!",
        "success"
    )

    return redirect(url_for('admin'))

# ================= CONTACT =================
@app.route('/contact', methods=['GET', 'POST'])
def contact():

    if request.method == 'POST':

        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        new_message = Contact(
            name=name,
            email=email,
            message=message
        )

        db.session.add(new_message)
        db.session.commit()

        try:

            msg = Message(
                subject=f"Portfolio Contact From {name}",
                sender='sambhavsahoo109@gmail.com',
                recipients=['sambhavsahoo109@gmail.com']
            )

            msg.body = f"""
New Portfolio Message

Name: {name}

Email: {email}

Message:
{message}
"""

            mail.send(msg)

            flash(
                "Message Sent Successfully!",
                "success"
            )

        except Exception:

            flash(
                "Message Saved But Email Failed!",
                "error"
            )

        return redirect(url_for('contact'))

    return render_template('contact.html')

# ================= LOGOUT =================
@app.route('/logout')
def logout():

    session.pop('admin', None)

    flash(
        "Logged out successfully",
        "success"
    )

    return redirect(url_for('home'))

# ================= RUN =================
if __name__ == "__main__":

    # CREATE FOLDERS IF NOT EXIST
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['RESUME_FOLDER'], exist_ok=True)

    with app.app_context():
        db.create_all()

    app.run(debug=True)