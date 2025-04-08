#!/bin/bash

set -e  # Exit on any error

# Create directories
mkdir -p templates static/js static/css

# Write index.html
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
    <script defer="defer" src="/static/js/main.b2233ee6.js"></script>
    <link href="/static/css/main.ebfb8bca.css" rel="stylesheet">
  </head>
  <body>
    <noscript>You need to enable JavaScript to run this app.</noscript>
    <div id="root"></div>
  </body>
</html>
EOF

# Install dependencies
pip install -r requirements.txt

# Static files and database setup
python manage.py collectstatic --noinput
python manage.py migrate
python manage.py load_bingo_tasks
