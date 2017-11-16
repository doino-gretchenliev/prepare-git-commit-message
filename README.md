Description
-----------
The [setup-prepare-commit-msg](setup-prepare-commit-msg.py) scans user workspace directory and configures every local git repository with prepare-commit-msg hook.
The hook is configured with [prepare-commit-msg.sh](https://gist.github.com/bartoszmajsak/1396344#file-prepare-commit-msg-sh) script.

Requirments
-----------
Python 2 or up

Installtion
-----------
* As is, no installation required
* As cron job
    1. Enter cron editing mode: 
    `crontab -e`
    2. Add the following line:
    `0 8 * * * <path_to_setup-prepare-commit-msg.py> -w <path_to_workspace_directory>`

Usage
-----
Check `setup-prepare-commit-msg.py --help`