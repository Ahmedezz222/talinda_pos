# Talinda POS System

A modern, feature-rich Point of Sale system built with Python and PyQt5.

## Features

- Modern and beautiful UI using PyQt5
- Multi-language support (Arabic & English)
- User role management (admin, cashier, etc.)
- Shift management
- Sales and inventory management
- Report generation
- SQLite database integration
- Touch-friendly design

## Requirements

- Python 3.8+
- Dependencies listed in requirements.txt

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```
   python -m venv venv
   ```
3. Activate the virtual environment:
   - Windows:
     ```
     .\venv\Scripts\activate
     ```
   - Linux/Mac:
     ```
     source venv/bin/activate
     ```
4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Running the Application

```
python src/main.py
```

## Development

The project follows a modular architecture:

- `src/ui/`: User interface components
- `src/database/`: Database models and operations
- `src/models/`: Business logic models
- `src/controllers/`: Application controllers
- `src/utils/`: Utility functions
- `src/resources/`: Application resources (images, translations, etc.)

## License

MIT License
