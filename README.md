# add-ticket-hook
Add ticket number to your git commit message. This works well with Atlassian JIRA and GitHub,
but is tool agnostic so you can use any tool you prefer as long it uses somewhat parseable format.

Logic:

1. use ticket number from commit if one exists
2. take ticket number from branch name if one exists
3. either break or move along (depending on `strict` option)

This is made to work with https://pre-commit.com/ purely so you need to setup that in your environment.

# Setup

1. Install pre-commit `pip install pre-commit`
2. Create your .pre-commit-config.yaml file
3. Install this hook `pre-commit install --hook-type=prepare-commit-msg`


# Configure
Your `.pre-commit-config.yaml` could look like this:

For JIRA:

```yaml
- repo: https://github.com/bagerard/add-ticket-hook
  rev: v0.1.2
  hooks:
    - id: add-ticket
      args: ["--prefixes='TICKETNAME-,ANOTHERONE-'"]
```

For GitHub:

```yaml
- repo: https://github.com/bagerard/add-ticket-hook
  rev: v0.1.2
  hooks:
    - id: add-ticket
      args: ["--prefixes=#"]
```


## Possible Args

* `-s` `--strict`: Will fail if there is no ticket name and number present (default: False)
* `-p` `--prefixes`: prefixes that would correspond to ticket name
