Requires python-requests


git clone ...
git submodule init
git submodule update

Example:

    ./run.py -f <custom subdir (defaults to current)> -b http://<blog's name>.tumblr.com -l <number of pages to get> -u -F -G # -F fetch media, -G generate local html page
