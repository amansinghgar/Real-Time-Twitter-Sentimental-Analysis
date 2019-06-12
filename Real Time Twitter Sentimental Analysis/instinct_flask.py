#Flask file to navigate to varios pages

from flask import Flask, request, render_template #import main Flask class and request object
import get_sentiment
app = Flask(__name__) #create the Flask app

@app.route('/',methods=['get'])
def home():
    return render_template('index.html')

@app.route('/printSentiment',methods = ['POST'])
def result():
	result = request.form
	ans = get_sentiment.getSentiment(result['query'])
	return render_template("printSentiment.html",result = ans)

if __name__ == '__main__':
    app.run(debug=True, port=5000) #run app in debug