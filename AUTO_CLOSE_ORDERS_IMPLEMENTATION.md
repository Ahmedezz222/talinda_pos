# Auto-Close Orders Implementation

## Overview

This implementation adds automatic order closure functionality to the Talinda POS system. Orders that are older than 24 hours are automatically marked as completed to prevent them from remaining in an active state indefinitely.

## Features

- **Automatic Order Closure**: Orders older than 24 hours are automatically completed
- **Background Processing**: Runs in the background without blocking the UI
- **Configurable Interval**: Check interval can be configured (default: 60 minutes)
- **User Notifications**: Users are notified when orders are auto-closed
- **Error Handling**: Robust error handling with logging
- **Clean Shutdown**: Proper cleanup when the application closes

## Implementation Details

### 1. Background Task Manager (`src/utils/background_tasks.py`)

The `BackgroundTaskManager` class handles all background operations:

- **QTimer-based**: Uses PyQt5's QTimer for periodic checks
- **Signal-based Communication**: Uses PyQt5 signals to communicate with the main application
- **Database Safety**: Uses fresh database sessions for each operation
- **Error Isolation**: Errors in background tasks don't affect the main application

#### Key Methods:
- `start()`: Start the background task manager
- `stop()`: Stop the background task manager
- `check_and_close_old_orders()`: Main method that finds and closes old orders
- `force_check_now()`: Force an immediate check (for testing)

### 2. Integration with Main Application (`src/main.py`)

The background task manager is integrated into the main application:

- **Initialization**: Created during application startup
- **Signal Handling**: Connected to notification handlers
- **Lifecycle Management**: Started after authentication, stopped on application exit
- **Error Reporting**: Errors are logged and optionally shown to users

### 3. Order Status Management

Orders are automatically moved from `ACTIVE` to `COMPLETED` status:

- **Timestamp-based**: Uses `created_at` field to determine order age
- **Non-destructive**: Only changes status, preserves all order data
- **Audit Trail**: `completed_at` timestamp is set when auto-closed

## Configuration

### Check Interval

The check interval can be configured when creating the BackgroundTaskManager:

```python
# Check every 30 minutes
task_manager = BackgroundTaskManager(check_interval_minutes=30)

# Check every 2 hours
task_manager = BackgroundTaskManager(check_interval_minutes=120)
```

### Auto-Close Threshold

The 24-hour threshold is hardcoded in the `check_and_close_old_orders()` method:

```python
cutoff_time = datetime.utcnow() - timedelta(hours=24)
```

To change this, modify the `hours=24` parameter.

## Usage

### Automatic Operation

The auto-close functionality runs automatically when the application starts:

1. Application initializes
2. User logs in
3. Background task manager starts
4. Periodic checks begin (every 60 minutes by default)
5. Old orders are automatically completed

### Manual Testing

Use the test script to verify functionality:

```bash
python test_auto_close_orders.py
```

This script:
- Creates test orders with different ages
- Runs the auto-close check
- Verifies that only orders older than 24 hours are closed
- Cleans up test data

### Manual Trigger

To manually trigger a check (for testing or maintenance):

```python
# In the application
app_manager.background_task_manager.force_check_now()
```

## Logging

The implementation includes comprehensive logging:

- **Info Level**: Normal operations (orders closed, manager started/stopped)
- **Debug Level**: Detailed operation information
- **Error Level**: Error conditions and failures

Log messages include:
- Number of orders auto-closed
- Order numbers and creation times
- Error details with stack traces
- Background task manager status

## Error Handling

### Database Errors
- Fresh sessions are used for each operation
- Errors are caught and logged
- Failed operations don't affect other orders
- Session cleanup is guaranteed

### Application Errors
- Background task errors don't crash the main application
- Error notifications are shown to users
- Detailed error information is logged

## Performance Considerations

### Database Impact
- Queries are optimized to only fetch necessary data
- Sessions are properly closed after each operation
- Batch operations minimize database round trips

### Memory Usage
- Background task manager uses minimal memory
- No data is cached between operations
- Sessions are created and destroyed as needed

### UI Responsiveness
- All operations run in background threads
- UI remains responsive during checks
- No blocking operations on the main thread

## Monitoring

### Status Information

Get the current status of the background task manager:

```python
status = task_manager.get_status()
print(f"Running: {status['is_running']}")
print(f"Next check in: {status['next_check_in']} minutes")
```

### Event Notifications

The system emits signals when operations occur:

- `orders_auto_closed(int)`: Emitted when orders are auto-closed
- `task_error(str)`: Emitted when errors occur

## Future Enhancements

Potential improvements for future versions:

1. **Configurable Thresholds**: Allow users to set custom auto-close times
2. **Order Types**: Different rules for different order types
3. **Notification Preferences**: Allow users to configure notification settings
4. **Statistics**: Track auto-close statistics and trends
5. **Manual Override**: Allow users to prevent auto-closure for specific orders

## Troubleshooting

### Common Issues

1. **Orders Not Being Closed**
   - Check if orders are actually older than 24 hours
   - Verify order status is `ACTIVE`
   - Check application logs for errors

2. **Background Task Not Running**
   - Verify the task manager was started
   - Check for error messages in logs
   - Ensure PyQt5 signals are working

3. **Database Errors**
   - Check database connectivity
   - Verify database permissions
   - Check for database locks

### Debug Mode

Enable debug logging to see detailed operation information:

```python
import logging
logging.getLogger('utils.background_tasks').setLevel(logging.DEBUG)
```

## Security Considerations

- **Database Access**: Uses existing database connection with proper permissions
- **Data Integrity**: Only modifies order status, preserves all other data
- **Audit Trail**: All auto-closures are logged with timestamps
- **User Context**: Operations run in application context, not user context

## Testing

The implementation includes comprehensive testing:

1. **Unit Tests**: Test individual components
2. **Integration Tests**: Test with real database
3. **Manual Tests**: Test script for verification
4. **Error Tests**: Test error conditions and recovery

Run tests with:
```bash
python test_auto_close_orders.py
``` 