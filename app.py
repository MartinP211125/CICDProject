from flask import Flask, request, render_template, redirect
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
mongo = PyMongo(app)
db = mongo.db


@app.route('/courses', methods=['POST', 'GET'])
@app.route('/kiii/courses', methods=['POST', 'GET'])
def courses():
    if request.method == 'POST':
        data = request.form
        new_course = {'name': data['name']}
        db.courses.insert_one(new_course)
        return redirect('/courses')
    courses = db.courses.find()
    return render_template('courses.html', courses=courses)


@app.route('/courses/<string:course_id>', methods=['GET', 'POST'])
@app.route('/kiii/courses/<string:course_id>', methods=['GET', 'POST'])
def update_course(course_id):
    course = db.courses.find_one_or_404({'_id': ObjectId(course_id)})

    if request.method == 'POST':
        db.courses.update_one({'_id': ObjectId(course_id)}, {'$set': {'name': request.form['name']}})
        return redirect('/courses')

    return render_template('update_course.html', course=course)


@app.route('/courses/<string:course_id>/delete', methods=['POST'])
@app.route('/kiii/courses/<string:course_id>/delete', methods=['POST'])
def delete_course(course_id):
    db.courses.delete_one({'_id': ObjectId(course_id)})
    return redirect('/courses')


# Professors section
@app.route('/professors', methods=['POST', 'GET'])
@app.route('/kiii/professors', methods=['POST', 'GET'])
def professors():
    if request.method == 'POST':
        data = request.form
        course_ids = [ObjectId(course_id) for course_id in request.form.getlist('course_ids')]
        new_professor = {'name': data['name'], 'course_ids': course_ids}
        db.professors.insert_one(new_professor)
        return redirect('/professors')

    professors = list(db.professors.find())
    courses = list(db.courses.find())

    # Create a mapping of course IDs to course names
    course_mapping = {str(course['_id']): course['name'] for course in courses}

    # Add course names to each professor
    for professor in professors:
        professor['course_names'] = [course_mapping.get(str(course_id), "Unknown") for course_id in
                                     professor['course_ids']]

    return render_template('professors.html', professors=professors, courses=courses)


@app.route('/professors/<string:professor_id>', methods=['GET', 'POST'])
@app.route('/kiii/professors/<string:professor_id>', methods=['GET', 'POST'])
def update_professor(professor_id):
    professor = db.professors.find_one_or_404({'_id': ObjectId(professor_id)})
    courses = db.courses.find()

    if request.method == 'POST':
        # Update multiple course IDs
        course_ids = [ObjectId(course_id) for course_id in request.form.getlist('course_ids')]
        db.professors.update_one(
            {'_id': ObjectId(professor_id)},
            {'$set': {'name': request.form['name'], 'course_ids': course_ids}}
        )
        return redirect('/professors')

    return render_template('update_professor.html', professor=professor, courses=courses)


@app.route('/professors/<string:professor_id>/delete', methods=['POST'])
@app.route('/kiii/professors/<string:professor_id>/delete', methods=['POST'])
def delete_professor(professor_id):
    db.professors.delete_one({'_id': ObjectId(professor_id)})
    return redirect('/professors')


if __name__ == '__main__':
    app.run()
