# add-ticket-hook
Add ticket number to your git commit message. This works well with Atlassian JIRA, but is tool agnostic so you can use any tool you prefer as long it uses somewhat parseable format.

This is made to work with https://pre-commit.com/ purely so you need to setup that in your environment.

# Setup

1. Install pre-commit `pip install pre-commit`
2. Create your .pre-commit-config.yaml file
3. Install this hook `pre-commit install --hook-type=prepare-commit-msg`


# Configure
Your `.pre-commit-config.yaml` could look like this:

```yaml
- repo: https://github.com/hanshoi/add-ticket-hook
    hooks:
      - id: add-ticket
        args: ["--tags='TAG,ANOTHERTAG'"]
```
