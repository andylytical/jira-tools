DEBUG=1
REGISTRY=ghcr.io
OWNER=andylytical
REPO=jira-tools


function is_windows {
  rv=1
  [[ -n "$USERPROFILE" ]] && rv=0
  return $rv
}


[[ "$DEBUG" -eq 1 ]] && set -x

tag=latest

action=''
src_home="$HOME"
if is_windows ; then
  action=winpty
  src_home="$USERPROFILE"
fi

$action docker run -it --pull always \
--mount type=bind,src="${src_home}",dst=/home \
--env JIRA_TOOLS_CONFIG="/home/.config/jira-tools/config.ini" \
$REGISTRY/$OWNER/$REPO:$tag

