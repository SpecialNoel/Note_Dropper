import os
from flask import Flask, flash, render_template, request, redirect, url_for
from markupsafe import escape
from werkzeug.utils import secure_filename

# ** Run the Application
# To activate the .venv environment: . .venv/bin/activate
# To run this application: flask --app MinimalApp run
# Shortcut: if the file is named app.py or wsgi.py, don't have to use --app.

# ** --host Option
# The server is only accessible from this computer because it is in debugging mode.
# If trust other users on your network, use option: --host=0.0.0.0
#   to tell your OS to listen on all public IPs.

# ** --debug Option
# Enabling debug mode allows the server to reload automatically if code changes.
# To enable debug mode, use option: --debug
# Warning: do not run the development server or debugger in a production environment.

# ** HTML Escaping
# Need to escape HTML to protect from injection attacks.
# Escaping renders things like <script>alert("bad")</script> as text, rather than running an actual script.
# Jinja will do this automatically on HTML templates.
# Use escape() from markupsafe to do this manually.

# ** Routing
# Use route() decorator to bind a function to a URL
# Can also add variable sections to a URL with <variable_name>
# Can use a converter to specify the type of the argument for <variable_name>

# ** Unique URLs vs. Redirection
# URLs like '/projects/' act like a folder.
# URLs like '/about' act like an unique URL, or the pathname of a file.

# ** URL building
# Use url_for() to build a URL to a specific function.
# The generated paths are always absolute.

# ** HTTP Methods
# Use methods=[] argument of app.route() to handle different HTTP methods.
# Or, use shortcut app.get(URL), app.post(URL), etc..

# ** Static Files
# CSS and JS files should be stored in a folder named 'static'.

# ** Rendering Templates
# Use Jinja2 template to generate HTML (or other type of text files) within Python.
# Use render_template() to render a template.
# Flask will look for templates in the 'templates' folder.

# ** Accessing Request Data
# Use the global 'request' object to access data a client sends to the server.

# ** Context Locals:
# The reason why the 'request' object is global, and that Flask manages to still
#   be threadsafe even it contains that global object.
# A request comes in and web server decides to spawn a new thread.
# When Flask starts its internal request handling, it figures out that 
#   the current thread is the active context, and binds the current application
#   and the WSGI environment to that context (thread).
# It does that in a way that one app can invoke another app without breaking.
# This is particularly useful for unit testing.
# Use app.test_request_context(URL, method='') for unit testing.

# ** The 'request' Object
# Use the 'form' attribute to access form data.
# Use request.args.get(parameter, '') to access parameters submitted in the URL such as (?key=value).
# Read the API for 'request' for more.

# ** File Uploads
# Set enctype="multipart/form-data" on HTML <form> tag to enable file uploading.
# Use 'request.files[]' to access uploaded files.

UPLOAD_FOLDER = './uploadedFiles'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg'} # prevent XSS problems

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Check if the extension of the filename uploaded by the user is valid
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Transmit the file uploaded by the user to UPLOAD_FOLDER
@app.route('/upload', methods=['GET', 'POST']) 
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        f = request.files['file']
        if f.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if f and allowed_file(f.filename):
            filename = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('download_file', name=filename))
        
    return render_template('download_file.html', name=filename)

def validate_login(username, password):
    # Validate user inputted username and password.
    # If valid, return True; return False otherwise.
    pass

def log_user_in(username):
    # Log the user in with username
    pass

@app.route('/login', methods=['POST', 'GET'])
def index():
    print('This is the main page. /nYou can login here with your username and password.')
    error = None
    if request.method == 'POST':
        if validate_login(request.form['username'], request.form['password']):
            return log_user_in(request.form['username'])
        else:
            error = 'Invalid username/password'
    return render_template('login.html', error=error)

@app.route('/hello/')
@app.route('/hello/<name>')
def say_hi(name=None):
    # Automatic escaping is enabled with render_template()
    # This meas that person will be escaped if it contains HTML contents
    return render_template('hello.html', person=name)

# <username> is a variable name that client can input to get to this page
# e.g.: http://127.0.0.1:5000/u will have 'Hello, u' on the page
@app.route('/user/<username>')
def welcome_user(username):
    return f'Hello, {username}. This is your user page'

# test_request_context() makes Flask to execute things inside this function
with app.test_request_context():
    print()
    print('URL for the index/main page:', url_for('index'))
    print('URL for style.css:', url_for('static', filename='style.css'))
    print()
    