# Order Management System

This document describes the new order management features added to the Talinda POS system.

## Features Implemented

### 1. Tabbed Interface for POS
- **Active Orders Tab**: Shows all currently active orders
- **Completed Orders Tab**: Shows all completed orders
- **Cancelled Orders Tab**: Shows all cancelled orders

### 2. Name Tags for Orders
- Each order can have an optional customer name
- Customer names are displayed prominently on order cards
- Names can be added when creating orders or edited later

### 3. Order History Management
- **Active Orders**: Orders that are currently being processed
- **Completed Orders**: Orders that have been finished and delivered
- **Cancelled Orders**: Orders that were cancelled with reasons

### 4. Order Status Tracking
- **Active**: Order is being prepared
- **Completed**: Order has been finished
- **Cancelled**: Order was cancelled
- **Pending**: Order is waiting (future use)

## How to Use

### Creating Orders
1. Add items to your cart in the POS interface
2. Click the "Create Order" button in the cart
3. Enter an optional customer name and notes
4. Click "Create Order" to save

### Managing Orders
1. Navigate to the "Order Management" tab
2. View orders by status (Active, Completed, Cancelled)
3. For active orders, you can:
   - **Edit**: Change customer name and notes
   - **Complete**: Mark order as finished
   - **Cancel**: Cancel the order with optional reason

### Order Cards Display
Each order card shows:
- Order number
- Customer name (if provided)
- Status badge
- List of items with quantities and prices
- Total amount
- Creation time
- Notes (if any)
- Action buttons (for active orders)

## Database Schema

### Orders Table
```sql
CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    order_number VARCHAR(20) UNIQUE NOT NULL,
    customer_name VARCHAR(100),
    status VARCHAR(20) NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    completed_at DATETIME,
    cancelled_at DATETIME,
    cancelled_by INTEGER,
    cancelled_reason TEXT,
    user_id INTEGER NOT NULL,
    subtotal FLOAT NOT NULL,
    discount_amount FLOAT NOT NULL,
    tax_amount FLOAT NOT NULL,
    total_amount FLOAT NOT NULL,
    notes TEXT
);
```

### Order Products Table
```sql
CREATE TABLE order_products (
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    price_at_order FLOAT NOT NULL,
    notes TEXT,
    PRIMARY KEY (order_id, product_id)
);
```

## Technical Implementation

### New Files Created
1. `src/models/order.py` - Order model and status enum
2. `src/controllers/order_controller.py` - Order management logic
3. `src/ui/components/order_widget.py` - Order display and management UI
4. `src/ui/components/new_order_dialog.py` - Order creation dialog
5. `src/migrate_add_orders.py` - Database migration script

### Modified Files
1. `src/ui/main_window.py` - Added order management tab
2. `src/ui/components/enhanced_cart_widget.py` - Added "Create Order" button

### Key Features
- **Auto-refresh**: Order management interface refreshes every 30 seconds
- **Real-time updates**: Order status changes are reflected immediately
- **User-friendly interface**: Clean, modern design with status badges
- **Flexible order creation**: Can create orders from cart items
- **Comprehensive tracking**: Full history of all order states

## Usage Examples

### Creating an Order
```
1. Add "Coffee" x2 and "Sandwich" x1 to cart
2. Click "Create Order"
3. Enter customer name: "John Smith"
4. Add notes: "Extra hot coffee"
5. Click "Create Order"
Result: Order #ORD-20250726063835-51edaa24 created
```

### Managing Orders
```
1. Go to Order Management tab
2. See active order for "John Smith"
3. Click "Complete" to finish the order
4. Order moves to Completed tab
```

### Cancelling Orders
```
1. Select an active order
2. Click "Cancel"
3. Enter reason: "Customer cancelled"
4. Order moves to Cancelled tab with reason
```

## Benefits

1. **Better Customer Service**: Track orders by customer name
2. **Improved Efficiency**: Clear status tracking for all orders
3. **Order History**: Complete audit trail of all orders
4. **Flexible Workflow**: Support for different order states
5. **User-Friendly**: Intuitive interface for order management

## Future Enhancements

- Order printing functionality
- Email/SMS notifications
- Order timing and SLA tracking
- Advanced filtering and search
- Order templates and favorites
- Integration with kitchen display systems 