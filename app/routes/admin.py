import os
from flask import (Blueprint, render_template, request, flash,
                   redirect, url_for, current_app)
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from app.models import Admin, AdmissionRequest, News, Teacher, Lecture, ContactMessage
from app import db

admin_bp = Blueprint('admin', __name__)


def allowed_file(filename):
    return ('.' in filename and
            filename.rsplit('.', 1)[1].lower() in
            current_app.config['ALLOWED_EXTENSIONS'])


def save_file(file):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(path)
        return f'uploads/{filename}'
    return None


# ── Auth ──────────────────────────────────────────────────────────────────────

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        admin = Admin.query.filter_by(username=username).first()
        if admin and admin.check_password(password):
            login_user(admin)
            flash('Welcome back!', 'success')
            return redirect(url_for('admin.dashboard'))
        flash('Invalid username or password.', 'danger')
    return render_template('admin/login.html')


@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('admin.login'))


# ── Dashboard ─────────────────────────────────────────────────────────────────

@admin_bp.route('/')
@admin_bp.route('/dashboard')
@login_required
def dashboard():
    stats = {
        'admissions': AdmissionRequest.query.count(),
        'news': News.query.count(),
        'teachers': Teacher.query.count(),
        'lectures': Lecture.query.count(),
        'messages': ContactMessage.query.filter_by(is_read=False).count(),
    }
    recent_admissions = AdmissionRequest.query.order_by(
        AdmissionRequest.created_at.desc()).limit(5).all()
    return render_template('admin/dashboard.html', stats=stats,
                           recent_admissions=recent_admissions)


# ── Admissions ────────────────────────────────────────────────────────────────

@admin_bp.route('/admissions')
@login_required
def admissions():
    items = AdmissionRequest.query.order_by(AdmissionRequest.created_at.desc()).all()
    return render_template('admin/admissions.html', items=items)


@admin_bp.route('/admissions/delete/<int:item_id>', methods=['POST'])
@login_required
def delete_admission(item_id):
    item = AdmissionRequest.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash('Admission request deleted.', 'success')
    return redirect(url_for('admin.admissions'))


# ── News ──────────────────────────────────────────────────────────────────────

@admin_bp.route('/news')
@login_required
def news_list():
    items = News.query.order_by(News.created_at.desc()).all()
    return render_template('admin/news_list.html', items=items)


@admin_bp.route('/news/add', methods=['GET', 'POST'])
@login_required
def add_news():
    activities = ['E-Igniters', 'NSS', 'Workshops', 'Conferences', 'Sports', 'Cultural']
    if request.method == 'POST':
        # Save multiple images
        images = request.files.getlist('images')
        img_paths = []
        for img in images:
            path = save_file(img)
            if path:
                img_paths.append(path)

        # Save PDF/PPT
        pdf = request.files.get('pdf')
        pdf_path = save_file(pdf) if pdf else None

        news = News(
            title=request.form.get('title'),
            description=request.form.get('description'),
            activity_name=request.form.get('activity_name'),
            img_paths=','.join(img_paths) if img_paths else None,
            pdf_path=pdf_path,
        )
        db.session.add(news)
        db.session.commit()
        flash('News added successfully!', 'success')
        return redirect(url_for('admin.news_list'))
    return render_template('admin/news_form.html', activities=activities, item=None)


@admin_bp.route('/news/edit/<int:item_id>', methods=['GET', 'POST'])
@login_required
def edit_news(item_id):
    item = News.query.get_or_404(item_id)
    activities = ['E-Igniters', 'NSS', 'Workshops', 'Conferences', 'Sports', 'Cultural']
    if request.method == 'POST':
        item.title = request.form.get('title')
        item.description = request.form.get('description')
        item.activity_name = request.form.get('activity_name')

        images = request.files.getlist('images')
        new_paths = [save_file(img) for img in images if img.filename]
        new_paths = [p for p in new_paths if p]
        if new_paths:
            item.img_paths = ','.join(new_paths)

        pdf = request.files.get('pdf')
        if pdf and pdf.filename:
            item.pdf_path = save_file(pdf)

        db.session.commit()
        flash('News updated successfully!', 'success')
        return redirect(url_for('admin.news_list'))
    return render_template('admin/news_form.html', activities=activities, item=item)


@admin_bp.route('/news/delete/<int:item_id>', methods=['POST'])
@login_required
def delete_news(item_id):
    item = News.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash('News deleted.', 'success')
    return redirect(url_for('admin.news_list'))


# ── Teachers ──────────────────────────────────────────────────────────────────

@admin_bp.route('/teachers')
@login_required
def teacher_list():
    items = Teacher.query.order_by(Teacher.department).all()
    return render_template('admin/teacher_list.html', items=items)


@admin_bp.route('/teachers/add', methods=['GET', 'POST'])
@login_required
def add_teacher():
    if request.method == 'POST':
        photo = request.files.get('photo')
        photo_path = save_file(photo) if photo and photo.filename else None
        teacher = Teacher(
            name=request.form.get('name'),
            designation=request.form.get('designation'),
            department=request.form.get('department'),
            qualification=request.form.get('qualification'),
            email=request.form.get('email'),
            photo=photo_path,
        )
        db.session.add(teacher)
        db.session.commit()
        flash('Teacher added successfully!', 'success')
        return redirect(url_for('admin.teacher_list'))
    return render_template('admin/teacher_form.html', item=None)


@admin_bp.route('/teachers/edit/<int:item_id>', methods=['GET', 'POST'])
@login_required
def edit_teacher(item_id):
    item = Teacher.query.get_or_404(item_id)
    if request.method == 'POST':
        item.name = request.form.get('name')
        item.designation = request.form.get('designation')
        item.department = request.form.get('department')
        item.qualification = request.form.get('qualification')
        item.email = request.form.get('email')
        photo = request.files.get('photo')
        if photo and photo.filename:
            item.photo = save_file(photo)
        db.session.commit()
        flash('Teacher updated!', 'success')
        return redirect(url_for('admin.teacher_list'))
    return render_template('admin/teacher_form.html', item=item)


@admin_bp.route('/teachers/delete/<int:item_id>', methods=['POST'])
@login_required
def delete_teacher(item_id):
    item = Teacher.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash('Teacher deleted.', 'success')
    return redirect(url_for('admin.teacher_list'))


# ── Lectures ──────────────────────────────────────────────────────────────────

@admin_bp.route('/lectures')
@login_required
def lecture_list():
    items = Lecture.query.order_by(Lecture.created_at.desc()).all()
    return render_template('admin/lecture_list.html', items=items)


@admin_bp.route('/lectures/add', methods=['GET', 'POST'])
@login_required
def add_lecture():
    teachers = Teacher.query.order_by(Teacher.name).all()
    if request.method == 'POST':
        file = request.files.get('file')
        file_path = save_file(file) if file and file.filename else None
        lecture = Lecture(
            title=request.form.get('title'),
            subject=request.form.get('subject'),
            teacher_id=request.form.get('teacher_id') or None,
            file_path=file_path,
        )
        db.session.add(lecture)
        db.session.commit()
        flash('Lecture added!', 'success')
        return redirect(url_for('admin.lecture_list'))
    return render_template('admin/lecture_form.html', teachers=teachers, item=None)


@admin_bp.route('/lectures/delete/<int:item_id>', methods=['POST'])
@login_required
def delete_lecture(item_id):
    item = Lecture.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash('Lecture deleted.', 'success')
    return redirect(url_for('admin.lecture_list'))


# ── Contact Messages ──────────────────────────────────────────────────────────

@admin_bp.route('/messages')
@login_required
def messages():
    items = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
    # Mark all as read
    ContactMessage.query.filter_by(is_read=False).update({'is_read': True})
    db.session.commit()
    return render_template('admin/messages.html', items=items)


@admin_bp.route('/messages/delete/<int:item_id>', methods=['POST'])
@login_required
def delete_message(item_id):
    item = ContactMessage.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash('Message deleted.', 'success')
    return redirect(url_for('admin.messages'))


# ── Change Password ───────────────────────────────────────────────────────────

@admin_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        old_pass = request.form.get('old_password')
        new_pass = request.form.get('new_password')
        confirm = request.form.get('confirm_password')
        if not current_user.check_password(old_pass):
            flash('Current password is incorrect.', 'danger')
        elif new_pass != confirm:
            flash('New passwords do not match.', 'danger')
        elif len(new_pass) < 6:
            flash('Password must be at least 6 characters.', 'danger')
        else:
            current_user.set_password(new_pass)
            db.session.commit()
            flash('Password changed successfully!', 'success')
            return redirect(url_for('admin.dashboard'))
    return render_template('admin/change_password.html')
