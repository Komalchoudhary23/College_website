from flask import Blueprint, render_template, request, flash, redirect, url_for
from app.models import News, Teacher, AdmissionRequest, ContactMessage
from app import db

public_bp = Blueprint('public', __name__)


@public_bp.route('/')
def index():
    latest_news = News.query.order_by(News.created_at.desc()).limit(3).all()
    return render_template('public/index.html', latest_news=latest_news)


@public_bp.route('/about')
def about():
    return render_template('public/about.html')


@public_bp.route('/mba')
def mba():
    return render_template('public/mba.html')


@public_bp.route('/mca')
def mca():
    return render_template('public/mca.html')


@public_bp.route('/phd')
def phd():
    return render_template('public/phd.html')


@public_bp.route('/faculty')
def faculty():
    teachers = Teacher.query.order_by(Teacher.department).all()
    return render_template('public/faculty.html', teachers=teachers)


@public_bp.route('/news')
def news():
    activity = request.args.get('activity', '')
    page = request.args.get('page', 1, type=int)
    query = News.query.order_by(News.created_at.desc())
    if activity:
        query = query.filter_by(activity_name=activity)
    news_items = query.paginate(page=page, per_page=9)
    activities = ['E-Igniters', 'NSS', 'Workshops', 'Conferences', 'Sports', 'Cultural']
    return render_template('public/news.html', news_items=news_items,
                           activities=activities, current_activity=activity)


@public_bp.route('/news/<int:news_id>')
def news_detail(news_id):
    item = News.query.get_or_404(news_id)
    return render_template('public/news_detail.html', item=item)


@public_bp.route('/admission', methods=['GET', 'POST'])
def admission():
    if request.method == 'POST':
        req = AdmissionRequest(
            name=request.form.get('name'),
            address=request.form.get('address'),
            email=request.form.get('email'),
            qualification=request.form.get('qualification'),
            contact=request.form.get('contact'),
            course=request.form.get('course'),
            message=request.form.get('message'),
        )
        db.session.add(req)
        db.session.commit()
        flash('Your admission request has been submitted successfully! We will contact you soon.', 'success')
        return redirect(url_for('public.admission'))
    return render_template('public/admission.html')


@public_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        msg = ContactMessage(
            name=request.form.get('name'),
            email=request.form.get('email'),
            phone=request.form.get('phone'),
            subject=request.form.get('subject'),
            message=request.form.get('message'),
        )
        db.session.add(msg)
        db.session.commit()
        flash('Thank you! Your message has been sent.', 'success')
        return redirect(url_for('public.contact'))
    return render_template('public/contact.html')


@public_bp.route('/placement')
def placement():
    return render_template('public/placement.html')


@public_bp.route('/vision-mission')
def vision_mission():
    return render_template('public/vision_mission.html')
