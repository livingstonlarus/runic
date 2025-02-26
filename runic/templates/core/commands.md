# Commands

## Memory Commands
`$mem update`: Update all memory files
`$mem update track=<name>`: Update track-specific memory
`$mem next`: Determine and execute next steps

## Track Commands
`$track status`: Display all track statuses
`$track init <name>`: Initialize new track and create its first branch
`$track <name>`: Focus on specific track

## Branch Commands
`$branch create <name>`: Create a new Git branch
`$branch delete <name>`: Delete a Git branch
`$branch merge <name>`: Merge a Git branch into main
`$branch list`: List all Git branches
`$branch update`: Update feature branch with latest changes from main
`$branch ready <name>`: Signal that a branch is ready to be merged
