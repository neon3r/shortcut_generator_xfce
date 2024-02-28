#!/bin/bash

# This file is part of Fanlight.
# See the file "LICENSE" for the full license governing this code.
# @Author: Dmitry Grushin (dim)

# Required parameters are passed via environment variables.

# USER
# USER_ID
# USER_GROUP
# USER_GID
# XGROUPS

# Home dir is /home/$USER

echo "Setting local user..."

# Debug info
id
set
set -x

# User info
[[ `id -u` == 0 ]] || { echo "This script must be run by root"; exit 1; }

[[ -v USER ]] || { echo "Missing env var: USER"; exit 1; }

# XGROUPS format = 'group:id group:id group:id'
[[ -v XGROUPS ]] || echo "No additional groups set: XGROUPS"

[[ -v USER_ID ]] || echo "No user id set: USER_ID"
[[ -v USER_GROUP ]] || echo "No user group set: USER_GROUP"
[[ -v USER_GID ]] || echo "No user group id set: USER_GID"

USERADD_ARGS="-m"

echo "Creating local user..."

if [[ -n $USER_GROUP ]]
then
  # Create group first
  groupadd -f -g $USER_GID $USER_GROUP
  # Set group args
  USERADD_ARGS="$USERADD_ARGS -g $USER_GROUP"
fi

if [[ -n $USER_ID ]]
then
  USERADD_ARGS="$USERADD_ARGS -u $USER_ID"
fi

# Create user if not exist
id $USER || useradd $USERADD_ARGS -s /bin/bash $USER

export USER_GROUP=`id -gn $USER`

echo "Setup user groups"

for i in $XGROUPS
do
  groupadd -f -g $(echo $i | cut -d':' -f2) $(echo $i | cut -d':' -f1)
  gpasswd -a $USER $(echo $i | cut -d':' -f1)
done

# Docker creates user dir if it does not exist. In this case chown it.
if [[ `stat -c "%u" /home/$USER` == 0 ]]
then
  chown $USER:$USER_GROUP /home/$USER
fi

# Otherwise dir already exists and may be mounted incorrectly. Exit with error.
if [[ `stat -c "%u" /home/$USER` != $USER_ID ]] || [[ `stat -c "%g" /home/$USER` != $USER_GID ]]
then
  echo "Invalid user home directory ownership: $(stat -c "%U(%u) %G(%g)" /home/$USER)"
  exit 1
fi
