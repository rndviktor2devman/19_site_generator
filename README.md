# 19_site_generator

Script converts markdown files set with provided site structure into 
static site. You could check out the results of the script [here](https://rndviktor2devman.github.io/19_site_generator)


####config.json
 file with a site structure(topics/titles nodes are quite descriptive)
 __file structure must correspond directory 'articles' structure__


####Run Script
pip3 install -r requirements.txt

python3 site_generator.py config.json

####Pre-Commit Hook
Copy file 'pre-commit' into '.git/hooks/' folder to make site auto-build

