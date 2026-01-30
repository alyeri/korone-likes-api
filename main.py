from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Pekora API URL
PEKORA_API_URL = "https://www.pekora.zip/apisite/games/v1/games/votes"

@app.route('/')
def home():
    return "API is running! Use /get-likes?universeId=ID"

@app.route('/get-likes', methods=['GET'])
def get_likes():
    universe_id = request.args.get('universeId')
    
    if not universe_id:
        return jsonify({"result": "error", "message": "Missing universeId"}), 400

    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        params = {"universeIds": universe_id}
        
        response = requests.get(PEKORA_API_URL, params=params, headers=headers)
        
        if response.status_code != 200:
            return jsonify({"result": "error", "message": "Pekora rejected the connection"}), 500
            
        data = response.json()
        
        if "data" in data and len(data["data"]) > 0:
            vote_data = data["data"][0]
            return jsonify({
                "result": "success",
                "game": {
                    "id": vote_data["id"],
                    "likes": vote_data.get("upVotes", 0),
                    "dislikes": vote_data.get("downVotes", 0)
                }
            })
        else:
            return jsonify({"result": "error", "message": "Game not found"}), 404

    except Exception as e:
        return jsonify({"result": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # Render assigns a dynamic port, this handles it
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)