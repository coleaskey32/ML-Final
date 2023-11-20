from flask import Flask, render_template, redirect, request, session
import spotipy
import spotipy.util as util

app = Flask(__name__)
app.secret_key = "some_secret_key" # you can generate a random secret key

# these are the credentials you get from registering your app on the Spotify Developer Dashboard
client_id = "your_client_id"
client_secret = "your_client_secret"
redirect_uri = "http://localhost:8000/callback" # this should match the redirect URI you set on the dashboard
scope = "user-top-read" # this is the scope you need for accessing the user's top artists

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    # this will redirect the user to the Spotify authentication page
    auth_url = util.prompt_for_user_token("", scope, client_id, client_secret, redirect_uri)
    return redirect(auth_url)

@app.route("/callback")
def callback():
    # this will receive the authorization code from Spotify and exchange it for an access token
    code = request.args.get("code")
    token_info = util.get_access_token(code, scope, client_id, client_secret, redirect_uri)
    session["token_info"] = token_info # store the token info in the session
    return redirect("/profile")

@app.route("/profile")
def profile():
    # this will use the access token to make requests to the Spotify Web API
    token_info = session.get("token_info", None) # get the token info from the session
    if token_info is None:
        return redirect("/")
    access_token = token_info["access_token"]
    sp = spotipy.Spotify(auth=access_token) # create a Spotify client with the access token
    top_artists = sp.current_user_top_artists() # get the user's top artists
    return render_template("profile.html", top_artists=top_artists)

if __name__ == "__main__":
    app.run(debug=True)
