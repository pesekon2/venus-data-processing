Help()
{
   # Display Help
   echo "*****"
   echo "download-results.sh"
   echo "Download all Venus data from the link the user has been provided."
   echo
   echo "Syntax: download-results.sh [-h] url username"
   echo "options:"
   echo "url         The url the user has obtained from the Venus request"
   echo "username    The username required to obtain the data"
   echo "h           Print this help and exit"
   echo "*****"
}

# check flags
while getopts ":h" option; do
   case "$option" in
      h) # display Help
         Help
         exit;;
     \?) # incorrect option
         echo "ERROR: Invalid option"
         echo
         echo
         echo "See help for the correct syntax:"
         echo
         Help
         exit;;
   esac
done

# parse arguments
url="$1"
username="$2"

# check if arguments provided
if [[ -z "$url" ]]; then
  echo "The first parameter (url) is empty"
  exit 1
fi

if [[ -z "$username" ]]; then
  echo "The second parameter (username) is empty"
  exit 1
fi

# run download
wget -r -np -nH -R index.html* "$url" --user "$username" --ask-password
