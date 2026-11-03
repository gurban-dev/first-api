# Git and GitHub Basics

Git is a version control system. It is designed to track changes in source code during software development. A version control system tracks changes made in a filesystem over time. It allows a previous version of the code to be cloned in case a newer version breaks it.

GitHub is a cloud-based hosting service built on top of Git where developers store their projects.

A repository is a project directory managed by a version control system.

## Common Git Commands

### Cloning a Repository
`git clone` downloads an existing repository from GitHub. It creates the project folder, downloads all of the project's files, and initializes Git inside the folder for you.

```bash
git clone <https_link_for_github_repo>
```

**Example:**
```bash
git clone https://github.com/gurban-dev/first-api.git
```

### Stashing and Pulling Changes

Temporarily save uncommitted local changes to clear the working directory:
```bash
git stash
```

Fetch updates from the remote GitHub repository and merge them into the current branch:
```bash
git pull
```

Restore the saved local changes and remove them from the stash list:
```bash
git stash pop
```