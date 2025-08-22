# Active Order Checkout Guide

## Overview
The active order checkout functionality allows you to load active orders into the cart and complete them as sales. This feature is essential for managing table orders, reservations, and pending transactions.

## How It Works

### 1. Loading Active Orders
- Go to the **Order Management** tab
- Find orders with **"Active"** status
- Click on an active order to load it into the cart
- The cart will display the order items and customer information

### 2. Cart Interface
When an active order is loaded:
- **Cart Header**: Shows "Order [number] - [customer] (Active)"
- **Button Text**: Changes to "Checkout"
- **Items**: All order items appear in the cart
- **Totals**: Calculated based on current cart contents

### 3. Checkout Process
Click the **"Checkout"** button to see two options:

#### Option A: Update Order
- Modify items, quantities, or customer details
- Save changes to the existing order
- Order remains active for future modifications

#### Option B: Checkout Order
- Complete the sale and process payment
- Mark order as "Completed"
- Create a sale record
- Clear the cart

## Step-by-Step Instructions

### Step 1: Create or Find an Active Order
```
1. Open the POS system
2. Go to Order Management tab
3. Look for orders with "Active" status
4. Note the order number and customer name
```

### Step 2: Load Order into Cart
```
1. Click on the active order card
2. Wait for confirmation message
3. Verify items appear in cart
4. Check cart header shows order information
```

### Step 3: Process Checkout
```
1. Click "Checkout" button
2. Choose action from dialog:
   - "Yes" = Update Order
   - "No" = Checkout Order
   - "Cancel" = Do nothing
3. If choosing checkout:
   - Confirm the action
   - Wait for completion message
   - Verify order status changes to "Completed"
```

## Troubleshooting

### Issue: Order Not Loading into Cart
**Symptoms:**
- Clicking order doesn't load items
- Cart remains empty
- No confirmation message

**Solutions:**
1. Check order status is "Active"
2. Verify order has items
3. Ensure you're using enhanced cart widget
4. Check console for error messages

### Issue: Checkout Button Not Working
**Symptoms:**
- Button doesn't respond to clicks
- No dialog appears
- No error messages

**Solutions:**
1. Verify cart has items
2. Check user permissions
3. Ensure database connection
4. Restart the application

### Issue: Order Not Completing
**Symptoms:**
- Checkout process fails
- Order remains active
- Error messages appear

**Solutions:**
1. Check database connectivity
2. Verify user has proper permissions
3. Ensure all required fields are filled
4. Check for duplicate sales

## Technical Details

### Cart Widget Methods
- `load_order(order)`: Loads order into cart
- `create_order()`: Handles checkout button click
- `checkout_active_order()`: Processes active order checkout
- `checkout()`: Processes regular checkout

### Order Status Flow
```
Active → Loaded into Cart → Checkout → Completed
```

### Database Operations
1. **Load Order**: Copies items to cart, sets loaded_order reference
2. **Update Order**: Modifies existing order items and details
3. **Checkout Order**: Completes order and creates sale record

## Best Practices

### For Cashiers
1. Always verify order details before checkout
2. Check customer information is correct
3. Confirm payment method with customer
4. Review totals before completing sale

### For Managers
1. Monitor active orders regularly
2. Clean up old active orders
3. Train staff on proper checkout procedures
4. Review completed orders for accuracy

## Common Scenarios

### Scenario 1: Table Order Completion
```
1. Customer finishes meal
2. Load their active order into cart
3. Verify all items are correct
4. Process payment
5. Mark order as completed
```

### Scenario 2: Order Modification
```
1. Customer wants to add/remove items
2. Load active order into cart
3. Modify items as needed
4. Update order (don't checkout)
5. Order remains active for future changes
```

### Scenario 3: Split Payment
```
1. Load active order into cart
2. Process partial payment
3. Create new order for remaining items
4. Continue with new active order
```

## Error Messages and Solutions

| Error Message | Cause | Solution |
|---------------|-------|----------|
| "No order loaded to checkout" | No active order in cart | Load an active order first |
| "Cart is empty" | No items in cart | Add items or load order |
| "Failed to complete sale" | Database error | Check connectivity and permissions |
| "Order not found" | Order was deleted | Refresh order list |

## Testing the Functionality

### Manual Test
1. Create a test order with items
2. Load it into cart
3. Try both update and checkout options
4. Verify order status changes correctly

### Automated Test
Run the test script:
```bash
python test_active_order_checkout.py
```

## Support

If you continue to experience issues:
1. Check the application logs
2. Verify database integrity
3. Test with a fresh order
4. Contact system administrator

## Recent Updates

### Version 2.0.0
- Enhanced cart widget with better UI
- Improved error handling
- Added confirmation dialogs
- Better status tracking

### Known Issues
- Arabic translation file has formatting issues (non-critical)
- Session management in debug scripts (fixed)

## Conclusion

The active order checkout functionality is working correctly. If you're experiencing issues, follow the troubleshooting steps above. The system is designed to handle both order updates and completions seamlessly. 