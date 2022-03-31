#!/bin/bash

#PYTHON=python3
PYTHON=python

myname=$(basename "$0")
mydir=$(cd $(dirname "$0") && pwd)
venv_dir="${mydir}/.saluminatorv4-venv/dev"

usage() {
    printf "Usage: %s (activate|deactivate)\n" "$myname"
}

[ $# -eq 1 ] || { usage >&2; exit 1; }

in_venv() {
    [ -n "$VIRTUAL_ENV" -a "$VIRTUAL_ENV" = "$venv_dir" -a -n "$VIRTUAL_ENV_SHELL_PID" ]
}

case $1 in
    activate)
        # check if already active
        in_venv && {
            printf "Virtual environment already active\n"
            exit 0
        }

        # check if created
        [ -e "$venv_dir" ] || {
            $PYTHON -m venv --clear --prompt "venv: dev" "$venv_dir" || {
                printf "Failed to initialize venv\n" >&2
                exit 1
            }
        }

        # activate
        tmp_file=$(mktemp)
        cat <<EOF >"$tmp_file"
# original bash behavior
if [ -f /etc/bash.bashrc ]; then
    source /etc/bash.bashrc
fi
if [ -f ~/.bashrc ]; then
    source ~/.bashrc
fi

# activating venv
source "${venv_dir}/bin/activate"

# remove deactivate function:
# we don't want to call it by mistake
# and forget we have an additional shell running
unset -f deactivate

# exit venv shell
venv_deactivate() {
    printf "Exitting virtual env shell.\n" >&2
    exit 0
}
trap "venv_deactivate" SIGUSR1

VIRTUAL_ENV_SHELL_PID=$$
export VIRTUAL_ENV_SHELL_PID

# remove ourself, don't let temporary files laying around
rm -f "${tmp_file}"
EOF
        exec "/bin/bash" --rcfile "$tmp_file" -i || {
            printf "Failed to execute virtual environment shell\n" >&2
            exit 1
        }
    ;;
    deactivate)
        # check if active
        in_venv || {
            printf "Virtual environment not found\n" >&2
            exit 1
        }

        # exit venv shell
        kill -SIGUSR1 $VIRTUAL_ENV_SHELL_PID || {
            printf "Failed to kill virtual environment shell\n" >&2
            exit 1
        }
        exit 0
    ;;
    *)
        usage >&2
        exit 1
    ;;
esac