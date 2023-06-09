events_branch := "events"
git_committer_name := "Python España"
git_committer_email := "contacto@es.python.org"

clean-future:
    pyevents clean-after -v -l $(date -I)

fetch-upcoming:
    pyevents fetch-upcoming -v -c communities.toml

commit-events:
    git fetch
    # This assumes the branch does not exist yet
    git switch -c {{events_branch}} --track origin/{{events_branch}}
    cp -r _events/* events/
    git add ./events
    git commit --allow-empty -m "Update events $(date -I)"
    git push origin {{events_branch}}
