#!/bin/bash

set -e  # Exit on any error

# Create target dirs
mkdir -p templates static/js static/css

# Capture hashed filenames from React build
JS_FILE=$(ls build/static/js/main.*.js | xargs -n 1 basename)
CSS_FILE=$(ls build/static/css/main.*.css | xargs -n 1 basename)

# Write index.html dynamically with real filenames
cat <<EOF > templates/index.html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8"/>
    <link rel="icon" href="/static/sustainability-bingo-logo.ico"/>
    <meta name="viewport" content="width=device-width,initial-scale=1"/>
    <meta name="theme-color" content="#000000"/>
    <meta name="description" content="Sustainability Bingo App"/>
    <link rel="apple-touch-icon" href="/static/sustainability bingo logo.jpeg"/>
    <link rel="manifest" href="/static/manifest.json"/>
    <title>Sustainability Bingo</title>
    <script defer="defer" src="/static/js/$JS_FILE"></script>
    <link href="/static/css/$CSS_FILE" rel="stylesheet">
  </head>
  <body>
    <noscript>You need to enable JavaScript to run this app.</noscript>
    <div id="root"></div>
  </body>
</html>
EOF

# Install dependencies and setup
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate
python manage.py load_bingo_tasks
