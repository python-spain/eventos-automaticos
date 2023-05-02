events_branch := "events"
git_committer_name := "Python España"
git_committer_email := "contacto@es.python.org"

commit-events:
    git switch {{events_branch}}
    cp -r _events/* events/
    git add ./events
    git commit --allow-empty -m "Commit new events $(date -I)"
