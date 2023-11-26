from flask import Flask, redirect, request, session, render_template
import spotipy
import spotipy.oauth2 as oauth2  # Use the spotipy.oauth2 module instead of spotipy.util

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Spotify credentials
client_id = "8f070f252f2c498d90dc3c5c09b30baf"
client_secret = "9b0b2f7f198b4c198e2a59db2628dd88"
redirect_uri =  "http://127.0.0.1:5000/callback"  # Match this with your Spotify app settings
scope = "user-read-private user-read-email"  # Define the required scope for accessing user data

# Create an instance of SpotifyOAuth with your credentials and scope
sp_oauth = oauth2.SpotifyOAuth(client_id, client_secret, redirect_uri, scope=scope)  

@app.route("/")
def index():
    # Display a login button to initiate the Spotify authentication
    return render_template("index.html")

@app.route("/login")
def login():
    # Redirect the user to Spotify's authentication page
    auth_url = sp_oauth.get_authorize_url()  # Use the SpotifyOAuth instance to get the authorization URL
    return redirect(auth_url)

@app.route("/callback")
def callback():
    # Handle the callback from Spotify after user authorization
    code = request.args.get("code")
    token_info = sp_oauth.get_access_token(code)  # Use the SpotifyOAuth instance to exchange the code for a token    session["token_info"] = token_info  # Store the token info in session
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
    
    playlists = sp.user_playlists(user_data['id'])
    
    for playlist in playlists['items']:
        print(playlist['name'], playlist['images'], playlist['tracks'], '\n')

    return render_template("profile.html", playlists = playlists)

if __name__ == "__main__":
    app.run(debug=True)