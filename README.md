# Ebook Library Example

This repository contains a minimal Flask application that demonstrates how to
organize ebook files stored in Google Drive. Users authenticate with Google and
specify a Drive folder where their books are stored. The app lists files from
that folder and allows downloading them.

## Setup

1. Create a Google Cloud project and configure OAuth credentials.
2. Download the `client_secrets.json` file and place it in the repository root.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the application:

```bash
python app.py
```

After signing in with Google, you will be prompted to provide a Drive folder ID.
All files in that folder will appear in the library view.

