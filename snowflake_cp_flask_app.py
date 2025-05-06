"""
Snowflake Control Plane - Flask Implementation

This Flask application serves as a control plane interface for Snowflake,
providing centralized management of:
- User access and authentication 
- Query execution and monitoring
- Resource allocation
- Policy enforcement
"""

from flask import Flask, session, redirect, url_for, render_template, flash
import snowflake.connector
#import pandas as pd
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired
import os
import logging
#import plotly
#import json
import configparser
#from datetime import datetime
import time

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-for-testing')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler("control_plane.log"), logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Load configuration
config = configparser.ConfigParser()
config.read('config.ini')

# Snowflake connection pool
connection_pool = {}

# Resource limits configuration
QUERY_TIMEOUT = 300  # seconds
MAX_ROWS_RETURN = 10000
WAREHOUSE_MAPPING = {
    'analyst': 'ANALYST_WH',
    'data_scientist': 'DS_WH',
    'admin': 'ADMIN_WH'
}

# Forms
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class QueryForm(FlaskForm):
    query = TextAreaField('SQL Query', validators=[DataRequired()])
    warehouse = SelectField('Warehouse', choices=[
        ('xs', 'X-Small'),
        ('s', 'Small'),
        ('m', 'Medium'),
        ('l', 'Large')
    ])
    submit = SubmitField('Execute Query')

# Helper functions
def get_snowflake_connection(user_role):
    """Create or retrieve a Snowflake connection for the user role"""
    if user_role in connection_pool and connection_pool[user_role]['valid']:
        return connection_pool[user_role]['conn']
    
    try:
        conn = snowflake.connector.connect(
            user=config['snowflake']['user'],
            password=config['snowflake']['password'],
            account=config['snowflake']['account'],
            warehouse=WAREHOUSE_MAPPING.get(user_role, 'SMALL_WH'),
            role=user_role.upper()
        )
        connection_pool[user_role] = {'conn': conn, 'valid': True, 'last_used': time.time()}
        return conn
    except Exception as e:
        logger.error(f"Failed to connect to Snowflake: {str(e)}")
        raise

def execute_query_with_policy(query, user_role):
    """Execute query with policy enforcement"""
    if "DROP " in query.upper() and user_role != 'admin':
        raise PermissionError("DROP operations restricted to admin role")
    
    if "UPDATE " in query.upper() and user_role == 'analyst':
        raise PermissionError("UPDATE operations not permitted for analysts")
    
    conn = get_snowflake_connection(user_role)
    
    try:
        cursor = conn.cursor()
        cursor.execute(f"ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = {QUERY_TIMEOUT}")
        cursor.execute(query)
        
        results = cursor.fetchmany(MAX_ROWS_RETURN)
        column_names = [desc[0] for desc in cursor.description] if cursor.description else []
        
        logger.info(f"User {session.get('username')} executed query: {query[:100]}...")
        
        return column_names, results
    except Exception as e:
        logger.error(f"Query execution error: {str(e)}")
        raise

@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Add your login logic here
        session['username'] = form.username.data
        return redirect(url_for('index'))
    return render_template('login.html', form=form)

@app.route('/query', methods=['GET', 'POST'])
def query():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    form = QueryForm()
    if form.validate_on_submit():
        try:
            columns, results = execute_query_with_policy(form.query.data, session.get('role', 'analyst'))
            return render_template('query.html', form=form, results=results, columns=columns)
        except Exception as e:
            flash(str(e), 'error')
    
    return render_template('query.html', form=form)

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)