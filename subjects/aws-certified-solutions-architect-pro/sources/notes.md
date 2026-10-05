Role assumption: borrowing another role’s identity

 An application starts with credentials for its current role. Assuming another role means obtaining
 temporary credentials for that role—not adding its permissions to the current role.

 ### The flow

 1. Caller permission: The current role’s identity policy must allow sts:AssumeRole on the target
    role’s ARN.
 2. Target trust: The target role’s trust policy must allow that caller to assume it. Trust answers
    “Who can become this role?”, not “Which S3 objects can it read?”
 3. Request credentials: The application calls AWS Security Token Service (STS) AssumeRole,
    authenticated with its current credentials.
 4. Receive credentials: If authorized, STS returns a temporary access key ID, secret access key
    and session token, with an expiration time.
 5. Use the new identity: The application signs subsequent AWS requests with those temporary
    credentials. Those requests act as an assumed-role session, governed by the target role’s
    permissions and applicable controls—not the original role’s permissions.

 The target role’s ordinary permissions policy answers “What can this role do?” For example,
 allowing assumption does not itself grant S3 access.

 When the credentials expire, the application must obtain new ones; AWS SDK credential providers
 can manage this refresh.
