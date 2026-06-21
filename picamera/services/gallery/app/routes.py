from flask import Blueprint, current_app, flash, redirect, render_template, request, send_from_directory, url_for
from werkzeug.utils import secure_filename

import os
import time

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():
    images = []
    photos_dir = current_app.config['PHOTOS_DIRECTORY']
    for item in os.listdir(photos_dir):
        (name, extension) = os.path.splitext(item)
        if not name.endswith('_small'):
            fullpath = os.path.join(photos_dir, item)
            shoot_time = time.ctime(os.path.getctime(fullpath))
            image = {
                'name': name,
                'shoot_time': shoot_time
            }
            images.append(image)

    return render_template('index.html', images=images)

@main.route('/photos')
def photos():
    images = []
    photos_dir = current_app.config['PHOTOS_DIRECTORY']
    for item in os.listdir(photos_dir):
        (name, extension) = os.path.splitext(item)
        if not name.endswith('_small'):
            fullpath = os.path.join(photos_dir, item)
            shoot_time = time.ctime(os.path.getctime(fullpath))
            image = {
                'name': name,
                'shoot_time': shoot_time
            }
            images.append(image)

    return render_template('index.html', images=images)

@main.route('/videos')
def videos():
    videos = []
    videos_dir = current_app.config['VIDEOS_DIRECTORY']
    for item in os.listdir(videos_dir):
        (name, extension) = os.path.splitext(item)
        fullpath = os.path.join(videos_dir, item)
        shoot_time = time.ctime(os.path.getctime(fullpath))
        video = {
            'name': name,
            'shoot_time': shoot_time
        }
        videos.append(video)

    return render_template('videos.html', videos=videos)


@main.route("/image/<name>")
def send_image(name):
    filename = name + '_small.jpg'
    return send_from_directory(current_app.config['PHOTOS_DIRECTORY'], filename)

@main.route("/video/<name>")
def send_video(name):
    filename = name + '.mp4'
    return send_from_directory(current_app.config['VIDEOS_DIRECTORY'], filename, conditional=True, mimetype='video/mp4')

@main.route("/image/delete/<name>", methods=['POST'])
def delete_image(name):
    photos_dir = current_app.config['PHOTOS_DIRECTORY']
    os.remove(os.path.join(photos_dir, name + '.jpg'))
    os.remove(os.path.join(photos_dir, name + '_small.jpg'))
    flash('image has been deleted!', 'success')
    return redirect(url_for('main.home'))

@main.route("/video/delete/<name>", methods=['POST'])
def delete_video(name):
    videos_dir = current_app.config['VIDEOS_DIRECTORY']
    os.remove(os.path.join(videos_dir, name + '.mp4'))
    flash('video has been deleted!', 'success')
    return redirect(url_for('main.videos'))

@main.route("/image/rename/<name>", methods=['GET', 'POST'])
def rename_image(name):
    if request.method == 'POST':
        file_name = secure_filename(request.form['filename'])
        if file_name != '':
            (filename, extension) = os.path.splitext(file_name)
            if extension != '.jpg':
                flash('invalid file extension!', 'danger')
            else:
                photos_dir = current_app.config['PHOTOS_DIRECTORY']
                new_path = os.path.join(photos_dir, file_name)
                if os.path.exists(new_path):
                    flash('such name already exists!', 'danger')
                else:
                    new_path_small = os.path.join(photos_dir, filename + '_small.jpg')
                    os.rename(os.path.join(photos_dir, name + '.jpg'), new_path)
                    os.rename(os.path.join(photos_dir, name + '_small.jpg'), new_path_small)
                    flash('image has been renamed!', 'success')
        return redirect(url_for('main.home'))
    return render_template('rename.html', title='Rename Image')

@main.route("/videos/rename/<name>", methods=['GET', 'POST'])
def rename_video(name):
    if request.method == 'POST':
        file_name = secure_filename(request.form['filename'])
        if file_name != '':
            (filename, extension) = os.path.splitext(file_name)
            if extension != '.mp4':
                flash('invalid file extension!', 'danger')
            else:
                videos_dir = current_app.config['VIDEOS_DIRECTORY']
                new_path = os.path.join(videos_dir, file_name)
                if os.path.exists(new_path):
                    flash('such name already exists!', 'danger')
                else:
                    os.rename(os.path.join(videos_dir, name + '.mp4'), new_path)
                    flash('video has been renamed!', 'success')
        return redirect(url_for('main.videos'))
    return render_template('rename.html', title='Rename Video')

@main.route("/image/download/<name>")
def download_image(name):
    filename = name + '.jpg'
    return send_from_directory(current_app.config['PHOTOS_DIRECTORY'], filename, as_attachment=True)

@main.route("/video/download/<name>")
def download_video(name):
    filename = name + '.mp4'
    return send_from_directory(current_app.config['VIDEOS_DIRECTORY'], filename, as_attachment=True)
