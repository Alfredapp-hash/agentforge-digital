#!/bin/bash
# Example cron script for daily autonomous runs
# chmod +x autonomy_cron.sh
# crontab -e
# 0 9 * * * /path/to/agentforge_digital/deployment/autonomy_cron.sh >> /path/to/logs/autonomy.log 2>&1

set -e
cd "$(dirname "$0")/../"   # go to agentforge_digital root

source .venv/bin/activate

export XAI_API_KEY="${XAI_API_KEY:-}"
export GUMROAD_ACCESS_TOKEN="${GUMROAD_ACCESS_TOKEN:-}"

python autonomy_runner.py --cycles 2 --publish

echo "Autonomy cron run completed at $(date)"