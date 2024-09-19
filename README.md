# jira-tools
Interface with the Jira API

## Start the docker container from which to run python scripts
Will create a local Docker container running an image of
containing this git repo. (Tested on Ubuntu 22.04)

1. `mkdir -p ~/.config/jira-tools`
1. `curl -o ~/.config/jira-tools/config.ini https://raw.githubusercontent.com/andylytical/jira-tools/main/config.ini.sample`
1. `vim ~/.config/jira-tools/config.ini`
1. `vim ~/.netrc`
1. `curl -o go_jira-tools.sh "https://raw.githubusercontent.com/andylytical/jira-tools/${BRANCH:-main}/go.sh"`
1. `bash go_jira-tools.sh`
1. #### Inside the running container
   1. `cp /home/.netrc /root/.netrc`
   1. `python xyz.py`
