from flask import Flask, redirect, request, session
import spotipy
import spotipy.util as util

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Spotify credentials
client_id = "8f070f252f2c498d90dc3c5c09b30baf"
client_secret = "9b0b2f7f198b4c198e2a59db2628dd88"
redirect_uri =  "http://127.0.0.1:5000/callback"  # Match this with your Spotify app settings
scope = "user-read-private user-read-email"  # Define the required scope for accessing user data

@app.route("/")
def index():
    # Display a login button to initiate the Spotify authentication
    return render_template("index.html")

@app.route("/login")
def login():
    # Redirect the user to Spotify's authentication page
    auth_url = util.prompt_for_user_token("", scope, client_id, client_secret, redirect_uri)
    return redirect(auth_url)

@app.route("/callback")
def callback():
    # Handle the callback from Spotify after user authorization
    code = request.args.get("code")
    token_info = util.get_access_token(code, scope, client_id, client_secret, redirect_uri)
    session["token_info"] = token_info  # Store the token info in session
    return redirect("/profile")

@app.route("/profile")
def profile():
    # Extract user data using the access token
    token_info = session.get("token_info", None)
    if token_info is None:
        return "Authentication required"

    access_token = token_info["access_token"]
    sp = spotipy.Spotify(auth=access_token)
    user_data = sp.current_user()
    return f"Hello, {user_data['display_name']}! Your email is {user_data['email']}"

if __name__ == "__main__":
    app.run(debug=True)