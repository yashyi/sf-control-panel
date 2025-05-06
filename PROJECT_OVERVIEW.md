# Snowflake Control Panel

## Overview
A Flask-based web application that provides a centralized management interface for Snowflake operations. The control panel enables secure access management, query execution, resource allocation, and policy enforcement for Snowflake data warehouse operations.

## Features
- **User Authentication**: Secure login system with role-based access control
- **Query Management**: Web interface for SQL query execution with policy enforcement
- **Resource Control**: Warehouse size selection and automatic resource allocation
- **Policy Enforcement**: Built-in security policies for different user roles
- **Connection Pooling**: Efficient connection management to Snowflake
- **Logging**: Comprehensive logging for auditing and monitoring

## Technical Stack
- **Backend Framework**: Flask (Python)
- **Database**: Snowflake
- **Frontend**: Bootstrap 5.3
- **Forms**: Flask-WTF
- **Template Engine**: Jinja2

## Project Structure
````text
sf-control-panel/
├── templates/
│   ├── base.html          # Base template with navigation and layout
│   ├── index.html         # Dashboard template
│   ├── login.html         # Login page
│   └── query.html         # Query execution interface
├── [config.ini](http://_vscodecontentref_/1)             # Snowflake configuration
├── [control_plane.log](http://_vscodecontentref_/2)      # Application logs
├── [snowflake_cp_flask_app.py](http://_vscodecontentref_/3)  # Main application file
└── [requirements.txt](http://_vscodecontentref_/4)       # Python dependencies
`````

## Key Components

### Role-Based Access
- **Admin**: Full access to all operations
- **Data Scientist**: Access to DS_WH warehouse
- **Analyst**: Limited to read operations on ANALYST_WH

### Resource Limits
- Query timeout: 300 seconds
- Maximum rows returned: 10,000
- Warehouse mapping based on user roles

### Security Features
- Session-based authentication
- Query validation and sanitization
- Role-specific warehouse allocation
- Operation restrictions based on user roles

## Configuration

### Environment Variables
- `SECRET_KEY`: Flask application secret key

### Snowflake Configuration (config.ini)
```ini
[snowflake]
user=your_username
password=your_password
account=your_account
```

### Warehouse Mapping
```python
WAREHOUSE_MAPPING = {
    'analyst': 'ANALYST_WH',
    'data_scientist': 'DS_WH',
    'admin': 'ADMIN_WH'
}
```

## Setup Instructions
1. Clone the repository
2. Create and activate a virtual environment
3. Install dependencies: `pip install -r requirements.txt`
4. Configure Snowflake credentials in `config.ini`
5. Set environment variables
6. Run the application: `python snowflake_cp_flask_app.py`

## Development Guidelines
- Use logging for all critical operations
- Implement proper error handling
- Follow Flask best practices
- Maintain separation of concerns
- Document code changes
- Test thoroughly before deployment

## Security Considerations
- Keep `SECRET_KEY` secure and unique per environment
- Never commit sensitive credentials
- Regularly rotate Snowflake credentials
- Monitor query execution logs
- Implement rate limiting for queries
- Regular security audits