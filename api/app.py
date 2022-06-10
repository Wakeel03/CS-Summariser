import re
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
import json
from extract_pdf import extract_pdf
from summariser import summariser
from joblib import load

app = Flask(__name__)
CORS(app)
api = Api(app)

model = load('LogisticRegression.joblib')

class Summariser(Resource):
    def post(self):
        files = request.files.getlist('file')
        
        number_of_sentences = int(request.form['numberOfSentences'])
        
        summaries = []

        for file in files:

            #extract source text from file
            source_text = extract_pdf(file)

            # summarise text using model
            generated_summaries = summariser(source_text, [model], number_of_sentences)

            for gs in generated_summaries:
                text = gs[0].lower()
                
                # Format words and remove unwanted characters
                text = re.sub('[^0-9a-zA-Z\.]+', '', text)

                if len(text) < len(gs[0]) * 0.7:
                    summaries.append({
                        'summary': 'Error processing this PDF file. Please try another file.',
                        'filename': file.filename.split('.')[0],
                        'processingError': True
                    })

                else:
                    summaries.append({
                        "summary": gs,
                        "filename": file.filename.split('.')[0]
                    }) 

        return {'summaries': json.dumps(summaries)}, 200  # return data with 200 OK
    
#localhost:5000
api.add_resource(Summariser, '/')  # '/users' is our entry point for Users

if __name__ == '__main__':
    app.run()  # run our Flask ap