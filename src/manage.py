"""
Command line utility for managing the POS system.
"""
import bcrypt
import click
from database.db_config import engine, Session, Base
from models.user import User, UserRole
from models.product import Category, CategoryType

@click.group()
def cli():
    """Talinda POS management CLI."""
    pass

@cli.command()
def init_db():
    """Initialize the database."""
    Base.metadata.create_all(engine)
    click.echo("Database initialized successfully!")

@cli.command()
@click.option('--username', prompt=True, help='Admin username')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='Admin password')
@click.option('--full-name', prompt=True, help='Admin full name')
def create_admin(username, password, full_name):
    """Create an admin user."""
    session = Session()
    
    # Check if user already exists
    if session.query(User).filter_by(username=username).first():
        click.echo("Error: Username already exists!")
        return
    
    # Create password hash
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    # Create admin user
    admin = User(
        username=username,
        password_hash=password_hash,
        role=UserRole.ADMIN,
        full_name=full_name,
        active=1
    )
    
    session.add(admin)
    session.commit()
    click.echo("Admin user created successfully!")

@cli.command()
@click.option('--username', required=True, help='Admin username')
@click.option('--password', required=True, help='Admin password')
@click.option('--full-name', required=True, help='Admin full name')
def create_admin_noninteractive(username, password, full_name):
    """Create an admin user non-interactively (for development/testing)."""
    session = Session()
    if session.query(User).filter_by(username=username).first():
        click.echo("Error: Username already exists!")
        return
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    admin = User(
        username=username,
        password_hash=password_hash,
        role=UserRole.ADMIN,
        full_name=full_name,
        active=1
    )
    session.add(admin)
    session.commit()
    click.echo("Admin user created successfully (non-interactive)!")

@cli.command()
def seed_categories():
    """Seed the database with initial categories."""
    session = Session()
    initial_categories = ["Food", "Beverage", "Dessert", "Other"]
    for cat_name in initial_categories:
        # Check if category already exists
        if not session.query(Category).filter_by(name=cat_name).first():
            category = Category(name=cat_name, description=f"{cat_name} category", tax_rate=14.0)
            session.add(category)
        else:
            # Update existing category to have 14% tax rate
            existing_category = session.query(Category).filter_by(name=cat_name).first()
            if existing_category and (not hasattr(existing_category, 'tax_rate') or existing_category.tax_rate == 0.0):
                existing_category.tax_rate = 14.0
    session.commit()
    click.echo("Categories seeded successfully with 14% tax rate!")

@cli.command()
def create_default_users():
    """Create default users for the system."""
    session = Session()
    
    # Default users
    default_users = [
        {
            'username': 'admin',
            'password': 'admin123',
            'role': UserRole.ADMIN,
            'full_name': 'System Administrator'
        },
        {
            'username': 'cashier',
            'password': 'cashier123',
            'role': UserRole.CASHIER,
            'full_name': 'Cashier User'
        },
        {
            'username': 'manager',
            'password': 'manager123',
            'role': UserRole.MANAGER,
            'full_name': 'Manager User'
        }
    ]
    
    created_count = 0
    for user_data in default_users:
        # Check if user already exists
        if not session.query(User).filter_by(username=user_data['username']).first():
            password_hash = bcrypt.hashpw(user_data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            user = User(
                username=user_data['username'],
                password_hash=password_hash,
                role=user_data['role'],
                full_name=user_data['full_name'],
                active=1
            )
            session.add(user)
            created_count += 1
            click.echo(f"Created user: {user_data['username']} ({user_data['role'].value})")
    
    session.commit()
    click.echo(f"Successfully created {created_count} new users!")

if __name__ == '__main__':
    cli()
