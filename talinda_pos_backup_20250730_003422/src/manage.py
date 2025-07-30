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
    click.echo("Categories seeded successfully!")

@cli.command()
@click.option('--type', 'reset_type', 
              type=click.Choice(['all', 'active', 'completed', 'cancelled', 'old']),
              default='all', help='Type of reset to perform')
@click.option('--username', prompt=True, help='Admin username for logging')
@click.option('--password', prompt=True, hide_input=True, help='Admin password')
def reset_orders(reset_type, username, password):
    """Reset the order management system."""
    # Verify admin credentials
    session = Session()
    user = session.query(User).filter_by(username=username, active=1).first()
    
    if not user:
        click.echo("Error: User not found or inactive!")
        return
    
    if user.role != UserRole.ADMIN:
        click.echo("Error: Only admin users can reset orders!")
        return
    
    # Verify password
    import bcrypt
    if not bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
        click.echo("Error: Invalid password!")
        return
    
    # Perform reset
    from controllers.order_controller import OrderController
    order_controller = OrderController()
    
    click.echo(f"Resetting order manager (type: {reset_type})...")
    results = order_controller.reset_order_manager(reset_type, user)
    
    if results["success"]:
        total_cleared = (results["active_cleared"] + results["completed_cleared"] + 
                        results["cancelled_cleared"] + results["old_cleared"])
        
        click.echo(f"✅ Order manager reset completed successfully!")
        click.echo(f"Orders cleared:")
        click.echo(f"  • Active: {results['active_cleared']}")
        click.echo(f"  • Completed: {results['completed_cleared']}")
        click.echo(f"  • Cancelled: {results['cancelled_cleared']}")
        click.echo(f"  • Old: {results['old_cleared']}")
        click.echo(f"  • Total: {total_cleared}")
        
        if results["errors"]:
            click.echo(f"⚠️  Warnings: {len(results['errors'])} errors occurred during reset.")
            for error in results["errors"]:
                click.echo(f"    • {error}")
    else:
        click.echo("❌ Failed to reset order manager:")
        for error in results["errors"]:
            click.echo(f"  • {error}")

@cli.command()
def show_order_stats():
    """Show current order management statistics."""
    from controllers.order_controller import OrderController
    order_controller = OrderController()
    
    stats = order_controller.get_order_manager_stats()
    
    click.echo("📊 Order Management Statistics:")
    click.echo(f"  • Active Orders: {stats['active_orders']}")
    click.echo(f"  • Completed Orders: {stats['completed_orders']}")
    click.echo(f"  • Cancelled Orders: {stats['cancelled_orders']}")
    click.echo(f"  • Today's Orders: {stats['today_orders']}")
    click.echo(f"  • Total Orders: {stats['total_orders']}")

@cli.command()
@click.option('--type', 'reset_type', 
              type=click.Choice(['all', 'products', 'categories']),
              default='all', help='Type of reset to perform')
@click.option('--username', prompt=True, help='Admin username for logging')
@click.option('--password', prompt=True, hide_input=True, help='Admin password')
def reset_products(reset_type, username, password):
    """Reset the product management system."""
    # Verify admin credentials
    session = Session()
    user = session.query(User).filter_by(username=username, active=1).first()
    
    if not user:
        click.echo("Error: User not found or inactive!")
        return
    
    if user.role != UserRole.ADMIN:
        click.echo("Error: Only admin users can reset products!")
        return
    
    # Verify password
    import bcrypt
    if not bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
        click.echo("Error: Invalid password!")
        return
    
    # Perform reset
    from controllers.product_controller import ProductController
    product_controller = ProductController()
    
    click.echo(f"Resetting product manager (type: {reset_type})...")
    results = product_controller.reset_product_manager(reset_type, user)
    
    if results["success"]:
        total_cleared = results["products_cleared"] + results["categories_cleared"]
        
        click.echo(f"✅ Product manager reset completed successfully!")
        click.echo(f"Items cleared:")
        click.echo(f"  • Products: {results['products_cleared']}")
        click.echo(f"  • Categories: {results['categories_cleared']}")
        click.echo(f"  • Total: {total_cleared}")
        
        if results["errors"]:
            click.echo(f"⚠️  Warnings: {len(results['errors'])} errors occurred during reset.")
            for error in results["errors"]:
                click.echo(f"    • {error}")
    else:
        click.echo("❌ Failed to reset product manager:")
        for error in results["errors"]:
            click.echo(f"  • {error}")

@cli.command()
def show_product_stats():
    """Show current product management statistics."""
    from controllers.product_controller import ProductController
    product_controller = ProductController()
    
    stats = product_controller.get_product_manager_stats()
    
    click.echo("📦 Product Management Statistics:")
    click.echo(f"  • Total Products: {stats['total_products']}")
    click.echo(f"  • Total Categories: {stats['total_categories']}")
    click.echo(f"  • Products with Barcodes: {stats['products_with_barcodes']}")
    click.echo(f"  • Products with Images: {stats['products_with_images']}")
    click.echo(f"  • Categories with Products: {stats['categories_with_products']}")

@cli.command()
def seed_default_categories():
    """Seed the database with default categories."""
    from controllers.product_controller import ProductController
    product_controller = ProductController()
    
    click.echo("🌱 Seeding default categories...")
    if product_controller.seed_default_categories():
        click.echo("✅ Default categories seeded successfully!")
    else:
        click.echo("❌ Failed to seed default categories!")

@cli.command()
@click.option('--username', prompt=True, help='Admin username for logging')
@click.option('--password', prompt=True, hide_input=True, help='Admin password')
@click.option('--confirm', is_flag=True, help='Skip confirmation prompt')
def reset_system(username, password, confirm):
    """Reset the entire system (orders, products, categories)."""
    # Verify admin credentials
    session = Session()
    user = session.query(User).filter_by(username=username, active=1).first()
    
    if not user:
        click.echo("Error: User not found or inactive!")
        return
    
    if user.role != UserRole.ADMIN:
        click.echo("Error: Only admin users can reset the system!")
        return
    
    # Verify password
    import bcrypt
    if not bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
        click.echo("Error: Invalid password!")
        return
    
    # Show warning and confirmation
    if not confirm:
        click.echo("⚠️  WARNING: This will reset the ENTIRE system!")
        click.echo("This action will delete:")
        click.echo("  • ALL orders (active, completed, cancelled)")
        click.echo("  • ALL products")
        click.echo("  • ALL categories")
        click.echo("  • ALL sales data")
        click.echo("")
        click.echo("This action cannot be undone!")
        
        if not click.confirm("Are you absolutely sure you want to continue?"):
            click.echo("System reset cancelled.")
            return
    
    click.echo("🔄 Starting system reset...")
    
    # Reset orders
    from controllers.order_controller import OrderController
    order_controller = OrderController()
    click.echo("  • Resetting orders...")
    order_results = order_controller.reset_order_manager("all", user)
    
    # Reset products and categories
    from controllers.product_controller import ProductController
    product_controller = ProductController()
    click.echo("  • Resetting products and categories...")
    product_results = product_controller.reset_product_manager("all", user)
    
    # Show results
    click.echo("")
    click.echo("📋 System Reset Results:")
    
    if order_results["success"]:
        order_total = (order_results["active_cleared"] + order_results["completed_cleared"] + 
                      order_results["cancelled_cleared"] + order_results["old_cleared"])
        click.echo(f"  ✅ Orders: {order_total} cleared")
    else:
        click.echo(f"  ❌ Orders: Failed to reset")
    
    if product_results["success"]:
        product_total = product_results["products_cleared"] + product_results["categories_cleared"]
        click.echo(f"  ✅ Products/Categories: {product_total} cleared")
    else:
        click.echo(f"  ❌ Products/Categories: Failed to reset")
    
    # Seed default categories
    click.echo("  • Seeding default categories...")
    if product_controller.seed_default_categories():
        click.echo("  ✅ Default categories seeded successfully")
    else:
        click.echo("  ❌ Failed to seed default categories")
    
    click.echo("")
    click.echo("🎉 System reset completed!")
    click.echo("The system has been reset to a clean state with default categories.")

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
