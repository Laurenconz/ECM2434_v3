#!/bin/bash

set -e  # Exit on any error

# Create necessary directories
mkdir -p templates static/js static/css
mkdir -p static/media/profile_pics  # For profile images

# ✅ Write the correct index.html
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
    <script defer="defer" src="/static/js/main.d051e62f.js"></script>
    <link href="/static/css/main.577de2ab.css" rel="stylesheet">
  </head>
  <body>
    <noscript>You need to enable JavaScript to run this app.</noscript>
    <div id="root"></div>
  </body>
</html>
EOF

# ✅ Install backend dependencies
pip install -r requirements.txt

# ✅ Run DB migrations
python manage.py migrate
python manage.py load_bingo_tasks

# ✅ Copy media files (especially profile images) into static before collectstatic
if [ -d "media/profile_pics" ]; then
  cp -r media/profile_pics/* static/media/profile_pics/ 2>/dev/null || true
fi

# ✅ Collect all static files
python manage.py collectstatic --noinput
