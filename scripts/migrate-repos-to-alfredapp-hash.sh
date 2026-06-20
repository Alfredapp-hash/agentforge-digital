#!/usr/bin/env bash
# Migrate WonWayup89 repos → Alfredapp-hash org
# Run AFTER org owner accepts pending GitHub transfer requests (email notification).
set -euo pipefail

ORG="Alfredapp-hash"
SRC="WonWayup89"

echo "=== Repos already on $ORG (no transfer needed) ==="
gh repo list "$ORG" --json name -q '.[].name' | sort

echo ""
echo "=== Check pending transfers (still on $SRC?) ==="
for repo in agentforge-digital thomas-marine-preview tapsafe ark-studio Ark-Cleaner forgedinthefire -arkhe-holdings-site arkhe-market arkhe-assistant Alfred Forcast-Wars; do
  if gh api "repos/$ORG/$repo" &>/dev/null; then
    echo "✅ $ORG/$repo"
  elif gh api "repos/$SRC/$repo" &>/dev/null; then
    echo "⏳ $SRC/$repo (transfer pending or not started)"
  else
    echo "❓ $repo not found"
  fi
done

echo ""
echo "=== Initiate transfers for repos not yet on $ORG ==="
EXISTING=$(gh repo list "$ORG" --json name -q '.[].name')
for repo in $(gh repo list "$SRC" --json name -q '.[].name'); do
  if echo "$EXISTING" | grep -qx "$repo"; then
    continue
  fi
  echo "Transferring $repo..."
  gh api -X POST "repos/$SRC/$repo/transfer" -f new_owner="$ORG" || true
  sleep 1
done

echo ""
echo "=== Update local git remotes (known projects) ==="
declare -A LOCAL_PATHS=(
  ["agentforge-digital"]="$HOME/agentforge_digital"
  ["Alfred"]="$HOME/Desktop/Projects/ArkheApps/Arkhe-AgentOS"
  ["tapsafe"]="$HOME/tapsafe"
  ["Forcast-Wars"]="$HOME/CascadeProjects/Forcast-Wars"
  ["arkhevault-api"]="$HOME/Desktop/The Ark Vault/arkhevault-api"
  ["Clear-Trace"]="$HOME/SentinelScope/cleartrace"
)

for repo in "${!LOCAL_PATHS[@]}"; do
  path="${LOCAL_PATHS[$repo]}"
  if [[ -d "$path/.git" ]]; then
    echo "Updating $path → $ORG/$repo"
    git -C "$path" remote set-url origin "https://github.com/$ORG/$repo.git"
    git -C "$path" remote -v | head -1
  fi
done

echo ""
echo "Done. If transfers show ⏳, accept them as Alfredapp-hash org owner:"
echo "  GitHub → Organization Settings → Requests (or email link)"