Help()
{
  # Display Help
  echo "*****"
  echo "unzip-archives.sh"
  echo "Unzip all downloaded archives and save them to the same directory."
  echo
  echo "Syntax: unzip-archives.sh [-h] data_dir"
  echo "options:"
  echo "data_dir    Path to the directory containing the archives"
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
data_dir="$1"

# check if arguments provided
if [[ -z "$data_dir" ]]; then
  echo "The first parameter (data_dir) is empty"
  exit 1
fi

# run the unzipping process
for i in "$data_dir"/*ZIP; do
  if [[ -z "$i" ]]; then
    # break if no file
    echo "No *ZIP files in data_dir"
    break
  fi
  unzip -x "$i" -d "$data_dir"
  rm "$i"
done
