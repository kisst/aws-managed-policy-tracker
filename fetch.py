import json
import boto3

iam = boto3.client("iam")

policies = []

paginator = iam.get_paginator("list_policies")
for page in paginator.paginate():
    policies += page["Policies"]

policies = [
    policy for policy in policies if policy["Arn"].startswith("arn:aws:iam::aws:policy")
]
policies.sort(key=lambda x: x["PolicyName"])

def policy_row(policy):
    return (
        f"| {policy['PolicyName']} | {policy['Path']} | "
        f"[{policy['DefaultVersionId']}](./policies/{policy['PolicyName']}.json) |\n"
    )


HEADER = "| Policy Name | Path | Version |\n| --- | --- | --- |\n"

job_function_rows = ""
managed_policy_rows = ""
for policy in policies:
    if policy["Path"] == "/job-function/":
        job_function_rows += policy_row(policy)
    else:
        managed_policy_rows += policy_row(policy)

    policy_version = iam.get_policy_version(
        PolicyArn=policy["Arn"], VersionId=policy["DefaultVersionId"]
    )
    policy_document = policy_version["PolicyVersion"]["Document"]
    with open(f"./policies/{policy['PolicyName']}.json", "w", encoding="utf-8") as f:
        json.dump(policy_document, f, indent=4)

DOC = (
    "# AWS Job Function Policies\n\n" + HEADER + job_function_rows
    + "\n# AWS Managed Policies\n\n" + HEADER + managed_policy_rows
)

with open("readme.md", "w", encoding="utf-8") as f:
    f.write(DOC)
