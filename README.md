# Git Repo Backup
The goal of this script is to loop through a config file
and clone all the repositories locally. Then a tool like **rsync**
could sync the cloned repositores to a safe location.

For now, this is hardcoded to work only with bitbucket, but plans to
make more generic for other vendors exist.

## Config.ini
The file shall have each section named after the bitbucket workspace. Each
section has 2 keys:

- repos: the list of repos to clone; use ',' as a delimiter
- ssh_key: the location of the ssh key to use for workspace

The ssh_key should be in the keys directory where the script is located.

### Config Example
```
[example-workspace]
repos        = repo1,repo2
ssh_key = bb_auto

[another-workspace]
repos        = test-repo
ssh_key = another_key
```

## Usage
Ensure that the keys required are in the keys directory. Create config.ini within
script directory.

Use podman to build the container
> podman build . -t bbauto

Use podman to run the script in container
> podman run -v /backup:/backup:Z bbauto -b /backup/bitbucket
