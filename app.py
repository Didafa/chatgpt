from flask import Flask, redirect, url_for, session, render_template, request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
import os

app = Flask(__name__)
app.secret_key = 'REPLACE_ME'
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

CLIENT_SECRETS_FILE = 'client_secrets.json'

@app.route('/')
def index():
    if 'credentials' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('library'))

@app.route('/login')
def login():
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=url_for('oauth2callback', _external=True))
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true')
    session['state'] = state
    return redirect(authorization_url)

@app.route('/oauth2callback')
def oauth2callback():
    state = session['state']
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        state=state,
        redirect_uri=url_for('oauth2callback', _external=True))
    flow.fetch_token(authorization_response=request.url)
    credentials = flow.credentials
    session['credentials'] = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }
    return redirect(url_for('library'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/library')
def library():
    if 'credentials' not in session:
        return redirect('login')
    folder_id = session.get('folder_id')
    if not folder_id:
        return render_template('set_folder.html')
    creds = Credentials(**session['credentials'])
    service = build('drive', 'v3', credentials=creds)
    query = f"'{folder_id}' in parents and trashed=false"
    results = service.files().list(q=query, fields="files(id, name, mimeType, thumbnailLink)").execute()
    files = results.get('files', [])
    return render_template('library.html', files=files)

@app.route('/set_folder', methods=['POST'])
def set_folder():
    folder_id = request.form.get('folder_id')
    session['folder_id'] = folder_id
    return redirect(url_for('library'))

if __name__ == '__main__':
    app.run(debug=True)
