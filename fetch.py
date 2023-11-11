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

TABLE = "| Policy Name | Path | Version |\n| --- | --- | --- |\n"
for policy in policies:
    TABLE += f"| {policy['PolicyName']} | {policy['Path']} | [{policy['DefaultVersionId']}](./policies/{policy['PolicyName']}.json) |\n"
    policy_version = iam.get_policy_version(
        PolicyArn=policy["Arn"], VersionId=policy["DefaultVersionId"]
    )
    policy_document = policy_version["PolicyVersion"]["Document"]
    with open(f"./policies/{policy['PolicyName']}.json", "w", encoding="utf-8") as f:
        json.dump(policy_document, f, indent=4)

with open("readme.md", "w", encoding="utf-8") as f:
    f.write(TABLE)
