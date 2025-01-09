from flask import  redirect, render_template, current_app

@current_app.route('/')  # URL '/' to be handled by main() route handler
def main():
    return redirect("resume")

@current_app.route('/resume')
def resume():
    return render_template('resume.html', title="Резюме")

@current_app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404
