#!flask/bin/python
#import app
from app import create_app
app = create_app()
app.run(debug=False, host='0.0.0.0', port=5000)
