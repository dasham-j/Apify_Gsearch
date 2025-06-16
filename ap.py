from flask import Flask, request, jsonify
from apify_client import ApifyClient

app = Flask(__name__)

@app.route('/search', methods=['GET'])
def search_apify():
    query = request.args.get('query')
    api_key = request.args.get('apiKey')

    if not query or not api_key:
        return jsonify({"error": "Missing 'query' or 'apiKey' parameter"}), 400

    try:
        # Initialize ApifyClient
        client = ApifyClient(api_key)

        # Prepare Actor input
        run_input = {
            "queries": query,
            "resultsPerPage": 100,
            "maxPagesPerQuery": 1,
            "focusOnPaidAds": False,
            "searchLanguage": "",
            "languageCode": "",
            "forceExactMatch": False,
            "wordsInTitle": [],
            "wordsInText": [],
            "wordsInUrl": [],
            "mobileResults": False,
            "includeUnfilteredResults": False,
            "saveHtml": False,
            "saveHtmlToKeyValueStore": True,
            "includeIcons": False,
        }

        # Run the actor
        run = client.actor("nFJndFXA5zjCTuudP").call(run_input=run_input)

        # Fetch dataset results
        results = [item for item in client.dataset(run["defaultDatasetId"]).iterate_items()]

        return jsonify({"query": query, "results": results})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
