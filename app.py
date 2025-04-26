from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)
SOLR_COLLECTION = "abd"  # replace with your collection name
SOLR_URL = f"http://localhost:8983/solr/{SOLR_COLLECTION}/select"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    query = request.args.get('q', '*:*')
    category_filter = request.args.get('category', '')

    params = {
        'q': f'title:{query}*' if query != '*:*' else '*:*',
        'wt': 'json',
        'rows': 10
    }

    if category_filter:
        params['fq'] = f'category:{category_filter}'

    solr_response = requests.get(SOLR_URL, params=params).json()
    results = solr_response.get('response', {}).get('docs', [])

    formatted_results = []
    for doc in results:
        formatted_results.append({
            'id': doc.get('id', ''),
            'title': doc.get('title', [''])[0],
            'author': doc.get('author', [''])[0],
            'category': doc.get('category', [''])[0],
            'published': doc.get('published', [False])[0]
        })
    print(formatted_results)
    return formatted_results


if __name__ == '__main__':
    app.run(debug=True)
