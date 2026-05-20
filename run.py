import os
import click
from app import create_app, db
from app.models import Admin

app = create_app(os.environ.get('FLASK_ENV', 'development'))


@app.cli.command('seed')
def seed_db():
    """Create initial admin user. Run: flask seed"""
    existing = Admin.query.filter_by(username='admin').first()
    if existing:
        click.echo('Admin user already exists.')
        return
    admin = Admin(username='admin')
    admin.set_password('admin123')
    db.session.add(admin)
    db.session.commit()
    click.echo('Admin user created: username=admin, password=admin123')
    click.echo('IMPORTANT: Change this password immediately after first login!')


@app.cli.command('create-tables')
def create_tables():
    """Create all database tables."""
    db.create_all()
    click.echo('All tables created successfully.')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
