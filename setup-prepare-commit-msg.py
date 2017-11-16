#!/usr/bin/env python

import argparse
import fnmatch
import os
import stat

parser = argparse.ArgumentParser(
    description='Setup git precommit message formatting')
parser.add_argument('-w', '--workspace-path', metavar='<path-to-workspace-dir>',
                    help='Path to your workspace directory', required=True,
                    dest="workspace_path")
args = parser.parse_args()

workspace_path = args.workspace_path

prepare_commit_msg_file_content = """#!/bin/bash

# This way you can customize which branches should be skipped when
# prepending commit message. 
if [ -z "$BRANCHES_TO_SKIP" ]; then
  BRANCHES_TO_SKIP=(master)
fi

BRANCH_NAME=$(git symbolic-ref --short HEAD)
BRANCH_NAME="${BRANCH_NAME##*/}"

BRANCH_EXCLUDED=$(printf "%s\n" "${BRANCHES_TO_SKIP[@]}" | grep -c "^$BRANCH_NAME$")
BRANCH_IN_COMMIT=$(grep -c "\[$BRANCH_NAME\]" $1)

if [ -n "$BRANCH_NAME" ] && ! [[ $BRANCH_EXCLUDED -eq 1 ]] && ! [[ $BRANCH_IN_COMMIT -ge 1 ]]; then 
  sed -i.bak -e "1s/^/[$BRANCH_NAME] /" $1
fi
"""

print "Start searching for local git repositories at [{}]".format(
    workspace_path)
git_repositories_count = 0
failed_git_repositories_count = 0
for root, directory_names, file_names in os.walk(workspace_path):
  for git_directory_name in fnmatch.filter(directory_names, '*.git'):
    git_directory_path = os.path.join(root, git_directory_name)
    prepare_commit_msg_file_path = os.path.join(git_directory_path,
                                                'hooks/prepare-commit-msg')

    print "Git repository found at [{}], writing file [{}]".format(
        git_directory_path, prepare_commit_msg_file_path)
    try:
      prepare_commit_msg_file = open(prepare_commit_msg_file_path, 'w')
      prepare_commit_msg_file.write(prepare_commit_msg_file_content)

      print "Fix file permissions [{}]".format(prepare_commit_msg_file_path)
      prepare_commit_msg_file_stat = os.stat(prepare_commit_msg_file_path)
      os.chmod(prepare_commit_msg_file_path,
               prepare_commit_msg_file_stat.st_mode | stat.S_IEXEC)
    except Exception, e:
      failed_git_repositories_count += 1
      print "Processing file [{}] completed failed, proceeding...\n{}".format(
          prepare_commit_msg_file_path, e)
    print "Processing file [{}] completed successfully".format(
        prepare_commit_msg_file_path)
    git_repositories_count += 1

print "Git repositories found and processed [{}], with [{}] failed".format(
    git_repositories_count, failed_git_repositories_count)
