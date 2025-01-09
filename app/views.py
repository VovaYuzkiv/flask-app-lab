from flask import  redirect, render_template
from . import app

@app.route('/')  # URL '/' to be handled by main() route handler
def main():
    return redirect("resume")

@app.route('/resume')
def resume():
    return render_template('resume.html', title="Резюме")

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404
