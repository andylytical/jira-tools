# jira-tools
Interface with the Jira API

## Start a docker container from which to run python
Requires docker. Will create a local Docker container running an image of
containing this git repo. (Tested on Ubuntu 22.04.3 LTS.)

1. Build a test server
1. `vim ~/.jira-tools-config.sh`
1. `vim ~/.netrc`
1. `curl -o go_jira-tools.sh "https://raw.githubusercontent.com/andylytical/jira-tools/${BRANCH:-main}/go.sh"`
1. `bash go_jira-tools.sh`
1. ### Inside the running container
  1. ln -s /home/.netrc /root/.netrc
  1. ln -s /home/.jira-tools-config.ini /root/.jira-tools-config.ini
