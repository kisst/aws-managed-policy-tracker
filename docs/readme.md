# AWS Managed Policy Tracker

This repo with it's linked CI action implemented in GitHub Actions is designed
to track the content of AWS managed policies under version control.

To replicate the setup:
1) Create a GitHub repo
2) Deploy the GitHub-Actions-role.yaml to your AWS account
3) Fetch the CFN output and save it into GitHub Secrets under the name `ROLE_ARN`
4) Enable GitHub Actions
5) Make sure that you grant Action write permission to the repo
