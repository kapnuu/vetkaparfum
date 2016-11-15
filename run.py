import os
from vetka import app

port = int(os.environ.get('PORT', 5000))
app.run(debug=app.config['DEBUG'], host='0.0.0.0', port=port)
