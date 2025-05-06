# Steps to Run the Flask Application

1. **Set environment variables for Flask**

```bash
export FLASK_APP=snowflake_cp_flask_app.py
export FLASK_ENV=development
export SECRET_KEY=your-secret-key
```

4.**Install required packages if not already done**

```bash
pip install -r requirements.txt
```

5. **Run the Flask application**

```bash
flask run
```

The application should start and be available at `http://127.0.0.1:5000/`

**Common troubleshooting:**
- If you get a port error, you can specify a different port:

  ```bash
  flask run --port=5001
  ```

- To allow external access:

  ```bash
  flask run --host=0.0.0.0
  ```

- To check if the app is running, look for output like:

  ```
  * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
  ```

To stop the application, press `Ctrl+C` in the terminal.// filepath: /Users/yashy/Projects/sf-control-panel/config.ini
[snowflake]
user = your_username
password = your_password
account = your_account_identifier
```

3. **Set environment variables for Flask**
```bash
export FLASK_APP=snowflake_cp_flask_app.py
export FLASK_ENV=development
export SECRET_KEY=your-secret-key
```

4. **Install required packages if not already done**
```bash
pip install -r requirements.txt
```

5. **Run the Flask application**
```bash
flask run
```

The application should start and be available at `http://127.0.0.1:5000/`

**Common troubleshooting:**
- If you get a port error, you can specify a different port:
  ```bash
  flask run --port=5001
  ```
- To allow external access:
  ```bash
  flask run --host=0.0.0.0
  ```
- To check if the app is running, look for output like:
  ```
  * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
  ```

To stop the application, press `Ctrl+C` in the terminal.