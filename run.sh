#!/bin/bash


################################################################################
# Info
################################################################################

# Start the triplet chance calculator by executing:
#
#   ./run.sh

################################################################################
# Generic
################################################################################

# Bash safe mode + errtrace (-E)
# From: http://redsymbol.net/articles/unofficial-bash-strict-mode/
set -eEuo pipefail
IFS=$'\n\t'
# Disable -e temporarily if sub-scripts caouse problems, or returning non-zero is
# intended behaviour.
# Disable -u temporarily when sourcing a script that causes problems

# echo for stderr
function errcho()
{
  set +e; # Avoid recursively reporting errors of errcho() itself
  >&2 echo "${@}";
  set -e;
  return 0;
}

# Catch-all error handling that displays abnoxious warning to screen
# when something bad happens (requires set -e).
function report_error()
{
  if [ "$1" != "0" ]; then
    # error handling goes here
    errcho "[ERROR] $0 {$(pwd)}: Exit status [$1] occurred on line ($2)";
  fi
}
trap 'report_error $? $LINENO' ERR EXIT INT ABRT KILL TERM HUP;

# Move to parent directory for behaviour independent of script location
readonly parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path";
echo "[LOG] Beginning of script [$0] <-- [$@] @ [$parent_path]";

################################################################################
# TODO Add commands here
################################################################################

command_names=("default");
declare -A commands;
function add_command()
{
  command_names+=("$1");
  return 0;
}

# Default command (when no arguments are given)
function command_default()
{
  echo "Starting p.py...";
  python3 p.py;
}

add_command debug;
function command_debug()
{
  bash -vx "$0" "${@}";
  return "$?";
}

# Print list available commands (rudimentary help)
add_command print_commands;
function command_print_commands()
{
  # Long version
#  echo "$0 commands: ${commands[@]}";
  if [ "$#" -eq 0 ]; then
    echo "$0 commands:";
    echo " ${commands[@]}" | sed -e 's/\<command_//g';
  else
    "./$0" "print_commands" | sed -e 's/ /\n/g' | grep --color=auto -Fe "$1";
  fi
  return 0;
}

################################################################################
# Command dispatcher
################################################################################

# Create command dictionary
for com in "${command_names[@]}"; do
  commands["$com"]="command_${com}";
done

# Call command from args
if [ $# -ge 1 ]; then
  ${commands["$1"]} "${@:2}"; # Pass rest of the arguments to subcommand
else
  ${commands[default]};
fi

exit "$?";
