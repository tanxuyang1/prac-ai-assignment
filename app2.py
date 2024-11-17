# Using Swagger to run API
from flask import Flask, request, jsonify, render_template
from analyze import read_image
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__, template_folder='templates')

SWAGGER_URL = '/api/docs'  
API_URL = '/static/swagger.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Test application"
    },
    # oauth_config={  # OAuth config. See https://github.com/swagger-api/swagger-ui#oauth2-configuration .
    #    'clientId': "your-client-id",
    #    'clientSecret': "your-client-secret-if-required",
    #    'realm': "your-realms",
    #    'appName': "your-app-name",
    #    'scopeSeparator': " ",
    #    'additionalQueryStringParams': {'test': "hello"}
    # }
)

app.register_blueprint(swaggerui_blueprint)

@app.route("/")
def home():
    return render_template('index.html')


# API at /api/v1/analysis/ 
@app.route("/api/v1/analysis/", methods=['GET'])
def analysis():
    # Try to get the URI from the JSON
    image_uri = request.args.get('uri')
    
    # If 'uri' is missing, return a 400 error
    if not image_uri:
        return jsonify({'error': 'Missing URI in query parameters'}), 400
    
    # Try to get the text from the image
    try:
        res = read_image(image_uri)
        
        response_data = {
            "text": res
        }
    
        return jsonify(response_data), 200
    except:
        return jsonify({'error': 'Error in processing'}), 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)