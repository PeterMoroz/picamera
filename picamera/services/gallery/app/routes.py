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
    for root,dirs,files in os.walk(photos_dir):
        for file in files:
            if file.endswith('jpg'):
                fullpath = os.path.join(root, file)
                shoot_time = time.ctime(os.path.getctime(fullpath))
                image = {
                    'filename': file,
                    'shoot_time': shoot_time
                }
                # print("-- DEBUG: file = %s\n" % file)
                images.append(image)
                
    return render_template('index.html', images=images)

@main.route('/photos')
def photos():
    images = []
    photos_dir = current_app.config['PHOTOS_DIRECTORY']
    for root,dirs,files in os.walk(photos_dir):
        for file in files:
            if file.endswith('jpg'):
                fullpath = os.path.join(root, file)
                shoot_time = time.ctime(os.path.getctime(fullpath))
                image = {
                    'filename': file,
                    'shoot_time': shoot_time
                }
                # print("-- DEBUG: file = %s\n" % file)
                images.append(image)
                
    return render_template('photos.html', images=images)

@main.route('/videos')
def videos():
    videos = []
    videos_dir = current_app.config['VIDEOS_DIRECTORY']
    for root,dirs,files in os.walk(videos_dir):
        for file in files:
            if file.endswith('mp4'):
                fullpath = os.path.join(root, file)
                shoot_time = time.ctime(os.path.getctime(fullpath))
                video = {
                    'filename': file,
                    'shoot_time': shoot_time
                }
                # print("-- DEBUG: file = %s\n" % file)
                videos.append(video)
                
    return render_template('videos.html', videos=videos)


@main.route("/image/<filename>")
def send_image(filename):
    return send_from_directory(current_app.config['PHOTOS_DIRECTORY'], filename)

@main.route("/video/<filename>")
def send_video(filename):
    return send_from_directory(current_app.config['VIDEOS_DIRECTORY'], filename)

@main.route("/image/delete/<filename>", methods=['POST'])
def delete_image(filename):
    photos_dir = current_app.config['PHOTOS_DIRECTORY']
    os.remove(os.path.join(photos_dir, filename))
    flash('image has been deleted!', 'success')
    return redirect(url_for('main.home'))

@main.route("/video/delete/<filename>", methods=['POST'])
def delete_video(filename):
    videos_dir = current_app.config['VIDEOS_DIRECTORY']
    os.remove(os.path.join(videos_dir, filename))
    flash('video has been deleted!', 'success')
    return redirect(url_for('main.videos'))

@main.route("/image/rename/<filename>", methods=['GET', 'POST'])
def rename_image(filename):
    if request.method == 'POST':
        file_name = secure_filename(request.form['filename'])
        # print("-- DEBUG: secure filename '%s'" % (file_name,))
        if file_name != '':
            file_ext = os.path.splitext(file_name)[1]
            if file_ext != '.jpg':
                flash('invalid file extension!', 'danger')
            else:
                # print("-- DEBUG: rename filename '%s' into '%s' " % (filename, file_name,))
                photos_dir = current_app.config['PHOTOS_DIRECTORY']
                new_path = os.path.join(photos_dir, file_name)
                if os.path.exists(new_path):                    
                    flash('such name already exists!', 'danger')
                else:
                    os.rename(os.path.join(photos_dir, filename), new_path)
                    flash('image has been renamed!', 'success')
        return redirect(url_for('main.home'))        
    return render_template('rename.html', title='Rename Image')

@main.route("/videos/rename/<filename>", methods=['GET', 'POST'])
def rename_video(filename):
    if request.method == 'POST':
        file_name = secure_filename(request.form['filename'])
        # print("-- DEBUG: secure filename '%s'" % (file_name,))
        if file_name != '':
            file_ext = os.path.splitext(file_name)[1]
            if file_ext != '.mp4':
                flash('invalid file extension!', 'danger')
            else:
                # print("-- DEBUG: rename filename '%s' into '%s' " % (filename, file_name,))
                videos_dir = current_app.config['VIDEOS_DIRECTORY']
                new_path = os.path.join(videos_dir, file_name)
                if os.path.exists(new_path):                    
                    flash('such name already exists!', 'danger')
                else:
                    os.rename(os.path.join(videos_dir, filename), new_path)
                    flash('video has been renamed!', 'success')
        return redirect(url_for('main.videos'))
    return render_template('rename.html', title='Rename Video')

@main.route("/image/download/<filename>")
def download_image(filename):
    return send_from_directory(current_app.config['PHOTOS_DIRECTORY'], filename, as_attachment=True)

@main.route("/video/download/<filename>")
def download_video(filename):
    return send_from_directory(current_app.config['VIDEOS_DIRECTORY'], filename, as_attachment=True)
