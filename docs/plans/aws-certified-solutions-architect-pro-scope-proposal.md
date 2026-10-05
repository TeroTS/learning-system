# AWS SAP-C02 Scope Proposal

Status: approved and applied on 2026-10-05 following the learner's explicit request to implement this proposal.
The accepted subject scope is stored in `subjects/aws-certified-solutions-architect-pro/map.md`.

## Applied amendment

Added the checklists and targets below to `subjects/aws-certified-solutions-architect-pro/map.md` after explicit
approval. Preserved all 22 existing topic lines, names, order, dependencies, sticking points and `todo` statuses.
Do not change the goal, sources, mistakes, cards or historical sessions. No topics or dependencies are added.

The goal is deeper architectural understanding before existing practice questions, not certification, a target
score, a timed test or mastery of every AWS service. The checklists are finite; additional concepts require a
separate approved amendment. Passing a topic means completing its accepted local target, not passing SAP-C02.

## Source snapshot and grading basis

All source references below are local files under `subjects/aws-certified-solutions-architect-pro/sources/`.
The following shorthand links identify source files, not new sources or online references:

- [D1](../../subjects/aws-certified-solutions-architect-pro/sources/solutions-architect-professional-02-domain1.md): organizational complexity, Tasks 1.1–1.5.
- [D2](../../subjects/aws-certified-solutions-architect-pro/sources/solutions-architect-professional-02-domain2.md): new solutions, Tasks 2.1–2.6.
- [D3](../../subjects/aws-certified-solutions-architect-pro/sources/solutions-architect-professional-02-domain3.md): existing solutions, Tasks 3.1–3.5.
- [D4](../../subjects/aws-certified-solutions-architect-pro/sources/solutions-architect-professional-02-domain4.md): migration/modernization, Tasks 4.1–4.4.
- [Guide](../../subjects/aws-certified-solutions-architect-pro/sources/solutions-architect-professional-02.md): goal context, response formats and content boundaries.
- [Concepts](../../subjects/aws-certified-solutions-architect-pro/sources/sap-technologies-concepts.md) and [services](../../subjects/aws-certified-solutions-architect-pro/sources/sap-02-in-scope-services.md): supporting scope categories, not mandatory service checklists.
- [Out-of-scope services](../../subjects/aws-certified-solutions-architect-pro/sources/sap-02-out-of-scope-services.md) and [service names](../../subjects/aws-certified-solutions-architect-pro/sources/sap-service-mentions.md): exclusions and terminology, not additional learning requirements.

The stored guide is the scope snapshot; its online currency has not been checked. These outlines support topic
selection, but generally do not explain detailed service behavior or provide answer rubrics. References beside
criteria establish topical grounding, not verification of every technical statement or future answer.

- The AWS exam guide informs scope; the accepted map fixes requirements and passing targets. Answers are always
  graded by agent judgement under Contract 9, not a source-first/fallback split. Generate fresh questions within
  the accepted checklist without a documentation or answer-file prerequisite.
- Additional technical documentation is optional context, not a grading authority. Genuine grading uncertainty
  stays `unverified`, not a learner mistake or failure. Do not claim agent-judgement grades are official AWS validation.
- Historical judgement-based successes remain attributed to agent judgement, not retroactively source-verified.
- No learner-supplied practice-question collection is stored here. Do not assume access to one or a grading key.
- Local exams use fresh applications of these criteria, not solved learning tasks or renamed copies. Their form
  can be architectural explanations and justified choices; existing multiple-choice/multiple-response practice
  remains the later goal activity. No AWS scaled-score threshold is imported into topic targets.

## Proposed scope sections

Each passing target requires all criteria in its section to be demonstrated unaided. Grading is always by agent
judgement and has normal effects, including mistakes, confirmed cards and local topic passes. The named constraints are supplied with the task, not unstated requirements. Genuine grading uncertainty
is not evidence that the learner failed. Scenarios and reasoning tasks must be fresh relative to available history.

### Requirements: iam-and-cross-account-access
- iam-cross-account-s3: Write or explain identity and bucket policies for an existing role to read objects only within a specified prefix in another account; identify which policy belongs in each account. Sources: D1 Task 1.2; D2 Task 2.3.
- iam-role-credentials: Trace a cross-account role-assumption flow, distinguishing role trust, caller permissions, assumed-role permissions and temporary credentials. Sources: D1 Task 1.2; supporting IAM/STS service list and existing map.
- iam-federation: Select a workforce federation approach using IAM Identity Center or an external identity provider, and explain the identity-to-role access flow without long-lived application credentials. Source: D1 Task 1.2.
- iam-least-privilege: Audit a supplied IAM access design for excess permissions and propose action/resource restrictions that retain the required access. Sources: D2 Task 2.3; D3 Task 3.2.
Passing target: Solve fresh cross-account and workforce-access scenarios, producing the required policy boundaries, credential flow and least-privilege justification for all four criteria.

### Requirements: multi-account-governance
- governance-account-structure: Design account and organizational-unit boundaries for supplied isolation, ownership and centralized-management requirements; identify appropriate shared/security/logging accounts. Source: D1 Task 1.4.
- governance-policy-controls: Evaluate the effect of an organizational guardrail alongside existing IAM permissions, distinguishing a permission ceiling from a grant and identifying an allowed versus blocked action. Source: D1 Task 1.4; existing map SCP sticking point.
- governance-landing-zone: Choose how Organizations and Control Tower support a proposed account-governance model and explain responsibilities for provisioning, guardrails and ongoing governance. Sources: D1 Task 1.4; D4 Task 4.2.
- governance-resource-sharing: Select an AWS RAM resource-sharing arrangement and distinguish resource sharing from the permissions required to use that resource. Source: D1 Task 1.4; supporting AWS RAM service list.
Passing target: Produce and justify a fresh multi-account layout and governance model covering all four criteria, including a guardrail decision and shared-resource access boundaries; detailed telemetry pipelines belong to observability.

### Requirements: advanced-vpc-networking
- vpc-address-plan: Produce a non-overlapping VPC/subnet address plan for supplied capacity, segmentation and future-connectivity requirements. Source: D1 Task 1.1.
- vpc-route-flow: Trace public/private subnet traffic using the relevant route tables and gateways, identifying why a proposed path succeeds or fails rather than treating routing as a VPC-wide property. Sources: D1 Task 1.1; existing map.
- vpc-network-controls: Evaluate inbound and outbound flows under supplied security-group and network-ACL rules and propose the minimum necessary changes. Sources: D1 Task 1.2; D2 Task 2.3.
- vpc-failure-domains: Evaluate an AZ failure in a supplied network design and propose subnet/egress placement and routing changes that preserve required connectivity. Sources: D1 Task 1.1; D2 Task 2.4.
Passing target: Produce an address plan and trace normal, blocked and AZ-failure traffic in fresh designs, satisfying all four criteria without assuming unspecified routes or permissions.

### Requirements: private-service-connectivity
- private-endpoint-selection: Select gateway versus interface endpoints or a PrivateLink-based service connection for stated consumer/provider and traffic requirements; justify rejecting an unsuitable alternative. Sources: D1 Task 1.1; D2 Task 2.3; existing map.
- private-path-controls: Trace the chosen private service path and identify relevant route/DNS, endpoint-policy and network-control checks for a failed connection. Sources: D1 Task 1.1; D2 Task 2.3.
- private-connectivity-authorization: Separate private connectivity from IAM/resource authorization in a cross-account service-access scenario and identify which layer a proposed fix changes. Sources: D1 Tasks 1.1–1.2; D2 Task 2.3.
Passing target: Design and troubleshoot fresh private service connections across all three criteria, distinguishing transport/path failures from authorization failures rather than equating PrivateLink with access permission.

### Requirements: hybrid-and-transit-networking
- hybrid-vpc-topology: Select VPC peering or Transit Gateway for supplied connectivity, segmentation and transitive-routing requirements and trace an allowed and disallowed path. Source: D1 Task 1.1.
- hybrid-on-premises-links: Compare Direct Connect and site-to-site VPN for bandwidth, resilience and connectivity requirements and propose a justified primary/backup arrangement. Sources: D1 Task 1.1; D4 Task 4.2.
- hybrid-dns: Design on-premises/cloud name-resolution flows using Route 53 Resolver and identify the direction and purpose of required forwarding paths. Source: D1 Task 1.1.
- hybrid-flow-troubleshooting: Use supplied route, connectivity and traffic-monitoring evidence to locate a failed hybrid path and propose a targeted correction. Source: D1 Task 1.1.
Passing target: Design and troubleshoot a fresh hybrid network covering all four criteria, including segmentation, redundant connectivity and DNS; justify the architecture against supplied requirements.

### Requirements: encryption-and-secrets
- encryption-at-rest-access: Design encrypted data access, distinguishing IAM/resource access from KMS key authorization, including cross-account decryption where required. Sources: D1 Task 1.2; D2 Task 2.3; existing map.
- encryption-in-transit: Place encryption-in-transit and certificate-management controls at the relevant communication boundaries for a supplied architecture. Sources: D1 Task 1.2; D2 Task 2.3.
- encryption-secret-lifecycle: Select a secure secret/credential storage and rotation approach and explain how dependent applications obtain and refresh credentials without exposing them. Source: D3 Task 3.2.
- encryption-data-obligations: Translate stated data sensitivity, retention and regulatory requirements into access, encryption and key/secret-management controls. Source: D3 Task 3.2.
Passing target: Produce and justify fresh at-rest, in-transit and secret-management designs meeting all four criteria, without treating encryption alone as proof of authorized access or compliance.

### Requirements: security-detection-and-compliance
- security-signal-selection: Choose audit, configuration, threat/vulnerability or access-analysis evidence using CloudTrail, Config, GuardDuty, Security Hub, Inspector or IAM Access Analyzer, distinguishing their roles in a supplied security investigation. Sources: D1 Task 1.2; D3 Task 3.2; supporting security service list.
- security-central-audit: Design centralized security-event collection, notifications and user/service traceability across accounts. Sources: D1 Task 1.2; D3 Task 3.2.
- security-web-defense: Select application/request and DDoS mitigation controls for a stated threat model, distinguishing WAF and Shield responsibilities. Source: D2 Task 2.3.
- security-response-priority: Prioritize identified vulnerabilities/compliance findings and propose automated detection-to-response controls with a bounded remediation action. Sources: D3 Tasks 3.1–3.2.
Passing target: Investigate and improve a fresh layered security design across all four criteria, explaining detection evidence, mitigation boundaries and response priorities; secret lifecycle and patch execution have separate primary topics.

### Requirements: compute-and-container-selection
- compute-platform: Select EC2, a container platform or Lambda for supplied workload, operational and managed-service requirements; justify trade-offs rather than naming a preferred service universally. Sources: D2 Tasks 2.1, 2.5; D4 Tasks 4.3–4.4.
- compute-container-hosting: Compare ECS and EKS hosting approaches and managed/server-based capacity choices such as Fargate for supplied deployment and operating constraints. Source: D4 Task 4.3; supporting container service list.
- compute-instance-fit: Select an instance family or compute configuration for a supplied resource/access profile and explain why an alternative is unsuitable. Source: D2 Task 2.5.
- compute-capacity-limits: Identify how stated service quotas or capacity constraints affect a compute proposal and identify a safe capacity-planning action. Source: D2 Task 2.4.
Passing target: Choose and justify fresh compute/container designs satisfying all four criteria, including operating burden, resource fit and explicit capacity limits; fleet scaling behavior belongs to high availability.

### Requirements: storage-design
- storage-access-fit: Select S3, EBS, EFS or FSx for stated object/block/file access, sharing and durability requirements and justify the choice against an alternative. Sources: D2 Task 2.5; D4 Task 4.3.
- storage-lifecycle-retention: Design tiering/lifecycle and retention/deletion controls for supplied access-frequency, recovery-access and data-retention requirements. Sources: D2 Task 2.6; D3 Task 3.2.
- storage-replication: Select and explain a storage replication arrangement for supplied location and availability requirements, identifying what replication does and does not protect. Sources: D2 Tasks 2.2, 2.4.
- storage-hybrid-access: Select a Storage Gateway integration for stated on-premises/cloud access patterns and distinguish ongoing storage access from a one-time migration. Source: D4 Task 4.3; supporting Storage Gateway service list.
Passing target: Produce and justify a fresh storage design across all four criteria, covering access semantics, retention and replication constraints; backup/recovery orchestration belongs to disaster recovery.

### Requirements: database-design
- database-access-fit: Choose among RDS/Aurora, DynamoDB and OpenSearch for supplied relational, key-value/document or search access requirements and reject a mismatched alternative. Sources: D2 Task 2.5; D4 Tasks 4.3–4.4.
- database-availability-reads: Distinguish availability/failover from read-scaling needs and select the appropriate deployment or replication arrangement. Sources: D2 Tasks 2.2, 2.4; existing map Multi-AZ/read-replica sticking point.
- database-consistency-partitioning: Evaluate how stated consistency, partition-key and access-pattern requirements affect a proposed DynamoDB design and identify a problematic hotspot or access mismatch. Source: D2 Task 2.5; existing map.
- database-cache-fit: Decide whether and how an ElastiCache-based cache improves a stated database workload, including the required handling of freshness and misses. Sources: D2 Task 2.5; D4 Task 4.4.
Passing target: Select and explain a fresh database design satisfying all four criteria, separating availability, access semantics and read-performance concerns without assuming a cache fixes every bottleneck.

### Requirements: decoupling-and-event-driven-design
- events-service-fit: Select SQS, SNS or EventBridge for stated buffering, fan-out or event-routing requirements and explain why an alternative does not fit. Sources: D2 Task 2.4; D4 Task 4.4.
- events-delivery-semantics: Design consumer behavior under stated ordering and duplicate-delivery requirements, including safe handling of repeated events. Sources: D2 Task 2.4; existing map.
- events-retry-failure: Propose bounded retry and failed-message handling for a supplied producer/consumer failure, explaining recovery without silent message loss. Sources: D2 Task 2.4; existing map.
- events-workflow: Select a Step Functions workflow for supplied multi-step coordination and failure requirements and distinguish orchestration from transport. Sources: D2 Task 2.4; D4 Task 4.4.
Passing target: Design and explain a fresh decoupled workflow covering all four criteria, including normal delivery, repeated delivery and a bounded failure/recovery path.

### Requirements: high-availability-and-scaling
- availability-failure-design: Identify single points of failure and design recovery across required AZ/Region failure boundaries, including dependent-service and data failover behavior. Sources: D1 Task 1.3; D2 Task 2.4; D3 Task 3.4.
- availability-scale-policy: Choose scale-up/scale-out behavior and scaling signals from supplied demand/growth information, including how limits affect the scaling design. Sources: D1 Task 1.3; D2 Tasks 2.4–2.5; D3 Task 3.4.
- availability-state-dependencies: Explain how application state and tightly coupled dependencies affect recovery and propose changes using the established storage/database/event choices. Sources: D2 Task 2.4; D3 Task 3.4.
- availability-recovery-operation: Describe how to operate and exercise failover/self-healing in the proposed design, including evidence that required availability was restored. Sources: D2 Task 2.4; D3 Tasks 3.1, 3.4.
Passing target: Analyze and improve a fresh architecture across all four criteria under stated demand and failure cases, with explicit recovery behavior and no unjustified assumption of unlimited capacity.

### Requirements: global-traffic-and-content-delivery
- global-dns-routing: Select Route 53 routing and health-check behavior for supplied latency, location and failover requirements and trace how a failed destination changes routing. Sources: D2 Tasks 2.2, 2.4.
- global-edge-selection: Compare CloudFront and Global Accelerator for supplied protocol, content-delivery and performance requirements and justify the selected global service. Source: D3 Task 3.3.
- global-location-tradeoffs: Choose Region/edge and origin placement for stated latency and availability requirements, identifying a bottleneck or failure concern in the proposed global path. Sources: D1 Task 1.1; D3 Task 3.3.
Passing target: Design and explain a fresh global traffic path satisfying all three criteria, including health-dependent routing, edge-service choice and placement trade-offs.

### Requirements: observability-and-operational-metrics
- observability-measurable-goals: Translate stated business SLAs/KPIs into measurable application/infrastructure indicators and explain what successful versus degraded operation looks like. Source: D3 Task 3.3.
- observability-signals: Choose CloudWatch metrics/logs, X-Ray traces or VPC Flow Logs to answer a specific operational question, distinguishing detection from diagnostic evidence. Sources: D1 Task 1.1; D3 Tasks 3.1, 3.3; supporting CloudWatch/X-Ray service list.
- observability-alarms: Design actionable monitoring and event notifications for supplied failure symptoms, with meaningful triggers, destinations and response expectations. Sources: D1 Task 1.4; D2 Task 2.2; D3 Task 3.1.
- observability-centralization: Design cross-account logging/monitoring and operational event routing consistent with the accepted governance boundaries. Sources: D1 Task 1.4; D3 Task 3.1.
Passing target: Produce and justify a fresh monitoring/diagnostic plan covering all four criteria, including measurable outcomes and a signal-to-response flow; security-specific detection rules remain in the security topic.

### Requirements: performance-analysis-and-rightsizing
- performance-bottleneck: Use supplied measurements and access/demand information to locate a compute, storage, database or network bottleneck rather than guessing a service replacement. Source: D3 Task 3.3.
- performance-remediation: Compare caching, buffering, replicas or other already-covered platform changes against a stated bottleneck and recommend a justified candidate. Sources: D2 Task 2.5; D3 Task 3.3.
- performance-experiment: Design a measurement-based remediation/right-sizing comparison, including representative load, success metrics and a decision that follows from supplied results. Source: D3 Task 3.3.
Passing target: Analyze a fresh measured workload and justify a tested improvement across all three criteria without introducing services outside the accepted platform scope.

### Requirements: backup-and-disaster-recovery
- recovery-objectives: Derive recovery design constraints from supplied RTO/RPO requirements and distinguish recovery-time and data-loss obligations. Sources: D1 Task 1.3; D2 Task 2.2.
- recovery-strategy: Select backup/restore, pilot light, warm standby or multi-site recovery for stated objectives and trade-offs, justifying why another strategy is unsuitable. Sources: D1 Task 1.3; D2 Task 2.2.
- recovery-data-protection: Design automated backup/restoration and required replication across specified AZs/Regions, explaining their distinct protections and stated security/retention requirements. Sources: D1 Task 1.3; D2 Task 2.2; D3 Task 3.2.
- recovery-testing: Define and interpret a recovery exercise that verifies application/data restoration against RTO/RPO and identifies corrective actions from failed objectives. Sources: D2 Task 2.2; D3 Task 3.1.
Passing target: Produce and validate a fresh recovery plan satisfying all four criteria, including failure boundaries, data restoration and measurable recovery evidence; ordinary availability is not automatically disaster recovery.

### Requirements: infrastructure-and-deployment-strategies
- deployment-iac-change: Plan a repeatable infrastructure/application change using IaC and configuration management, identifying the intended resources, change boundaries and validation. Sources: D2 Task 2.1; D3 Task 3.1.
- deployment-release-fit: Select rolling, blue/green or all-at-once deployment behavior for stated business/availability constraints and explain upgrade and rollback paths. Sources: D2 Task 2.1; D3 Task 3.1.
- deployment-safe-rollback: Evaluate a supplied application/database compatibility change and propose staged validation and rollback that avoid an incompatible old/new deployment. Sources: D2 Task 2.1; existing map.
Passing target: Design and critique a fresh deployment plan across all three criteria, explaining repeatability, release trade-offs and a valid rollback path rather than assuming infrastructure rollback restores all data changes.

### Requirements: operational-automation-and-patching
- operations-configuration: Design configuration-management and drift-detection/remediation steps using Systems Manager or already-covered management tools, distinguishing desired state from a one-time command. Sources: D2 Task 2.1; D3 Task 3.1.
- operations-patching: Plan patch/update execution for supplied compliance and availability constraints, including staged rollout, validation and a defined recovery path. Sources: D2 Task 2.3; D3 Task 3.2.
- operations-safe-automation: Prioritize a repeatable operational activity for automation and define bounded actions, permissions and verification from detection through recovery. Sources: D3 Tasks 3.1–3.2.
Passing target: Produce and explain a fresh configuration/patching/automation plan satisfying all three criteria without assuming every workload can be patched with zero interruption.

### Requirements: cost-optimization-and-allocation
- cost-purchasing: Select on-demand, commitment-based or interruptible purchasing for stated usage and interruption constraints, explaining effects on cost and performance rather than inventing current prices. Sources: D1 Task 1.5; D2 Task 2.6; D3 Task 3.5.
- cost-resource-usage: Use supplied usage/rightsizing/storage information to identify unused, overprovisioned or mismatched resources and prioritize changes that retain required performance. Sources: D1 Task 1.5; D2 Task 2.6; D3 Task 3.5.
- cost-transfer-model: Model relevant data-transfer paths using supplied volumes and rates, compare architectural alternatives and identify which change reduces the stated cost. Sources: D2 Task 2.6; D3 Task 3.5.
- cost-allocation-controls: Design tagging/allocation, reporting, budgets and usage alerts for supplied business-unit ownership and expenditure-awareness requirements; use granular usage evidence to investigate a cost change. Sources: D1 Task 1.5; D2 Task 2.6; D3 Task 3.5.
Passing target: Analyze and explain a fresh cost/usage case across all four criteria, preserving stated performance and resilience constraints and using supplied pricing instead of memorized or assumed current rates.

### Requirements: migration-assessment-and-planning
- migration-portfolio: Assess supplied applications, dependencies and assets using Application Discovery Service/Migration Hub roles; identify migration candidates and readiness gaps. Source: D4 Task 4.1.
- migration-seven-rs: Select among the seven migration strategies for supplied workload constraints and justify the choice against a plausible alternative. Source: D4 Task 4.1.
- migration-waves-tco: Prioritize dependency-aware migration waves and compare supplied TCO assumptions, making sequencing and cost/risk reasoning explicit. Source: D4 Task 4.1.
Passing target: Produce and justify a fresh portfolio migration plan covering all three criteria, including strategy selection, dependencies, sequencing and explicit cost assumptions.

### Requirements: migration-tools-and-cutover
- cutover-application-transfer: Select Application Discovery Service and/or Application Migration Service roles for stated platform, connectivity and downtime constraints, distinguishing discovery from actual transfer. Source: D4 Task 4.2.
- cutover-database-transfer: Select DMS and any required SCT/schema-conversion or replication steps for stated source/target and consistency constraints. Source: D4 Task 4.2.
- cutover-data-transfer: Choose among DataSync, Transfer Family, Snow Family and S3 Transfer Acceleration for supplied volume, bandwidth, protocol and offline/online constraints, identifying relevant security controls. Source: D4 Task 4.2.
- cutover-runbook: Design a cutover/rollback sequence with connectivity/DNS, identity, governance and data-validation prerequisites, explaining the point at which traffic and write ownership change. Source: D4 Task 4.2; existing map downtime/rollback sticking point.
Passing target: Produce and explain a fresh migration/cutover plan across all four criteria, including mechanism choice, security, validation and a bounded rollback path; naming a migration tool alone is insufficient.

### Requirements: workload-modernization
- modernization-target-architecture: Compose a target compute/container/storage/database design from already-covered platform choices and justify it against the existing workload's requirements. Source: D4 Task 4.3.
- modernization-managed-serverless: Identify a justified managed/serverless/purpose-built modernization opportunity and explain changed operational responsibilities and limitations. Sources: D4 Task 4.4; D2 Task 2.1.
- modernization-incremental-decoupling: Plan incremental application/integration changes that decouple appropriate components while preserving the required behavior and a validated transition path. Source: D4 Task 4.4; existing map incremental-change sticking point.
Passing target: Propose and justify a fresh modernization architecture and incremental transition satisfying all three criteria, reusing established platform capabilities rather than adding a second checklist of service-selection trivia.

## Primary ownership and disclosed exclusions

Repeated source-task references mean a task spans several topics, not that the same criterion must be examined
multiple times. Primary ownership is:

- IAM: policy authorization, trust and credentials. Governance: account/OU and organizational guardrail structure.
- VPC: address/route/control flows. Private/hybrid networking: applying those foundations to service and external paths.
- Encryption: keys, certificates and secret lifecycle. Security: detection/audit/mitigation. Operations: patch execution and safe operational automation.
- Compute/storage/database: platform selection and intrinsic data/access properties. Availability: fleet/dependency failures and recovery operation.
- Events: delivery/workflow mechanics. Modernization: integrating established choices into an incremental target architecture.
- Observability: signals, measurable goals and telemetry routing. Performance: diagnosis/experimentation using those signals.
- Storage/database: replication arrangement. Disaster recovery: objectives, coordinated backup/restoration and recovery testing.
- Deployment: release/change and application compatibility. Cutover: migrating workloads/data and transferring traffic/write ownership.
- Cost: ongoing purchasing/usage/allocation decisions. Migration planning: portfolio strategy, TCO assumptions and sequencing.

Excluded from required scope unless separately approved:

- Emerging/pretest AI controls identified in the guide, unrelated service-list entries and GameLift.
- Exhaustive service-feature/API memorization, fixed numerical quota/pricing recall and every possible variant of a named service.
- Frontend development, in-depth operating-system administration and 12-factor methodology, which the guide identifies outside its target role.
- Building/provisioning a production AWS environment, implementation-level automation code, live fault injection or paid labs.
- Certification score predictions, official exam-pass claims and a timed practice-question regime.

Named service comparisons bound the candidate services for each criterion; unlisted service alternatives cannot
become mandatory exam knowledge without an amendment. Where a criterion uses already-covered platform choices,
reuse those explicit choices rather than expanding the service list. Supply numerical limits/prices in scenarios;
do not require recall of undocumented values. Service names define architectural roles, not all of their features.

No entire content-domain task is excluded. This is an architectural-understanding scope, not a claim that the
guide is exhaustive or that every service mentioned in it is mandatory. Deployment, migration and recovery
criteria require reasoned plans rather than execution in a live AWS account.

## Guide-task cross-check

All 20 stored guide tasks have an explicit requirement home. References below name primary examples; the topic
criteria above provide the remaining task references and success conditions.

| Guide task | Requirement homes |
| --- | --- |
| D1 1.1: network connectivity | vpc-address-plan, hybrid-vpc-topology, hybrid-on-premises-links, hybrid-dns, hybrid-flow-troubleshooting, private-endpoint-selection, global-location-tradeoffs |
| D1 1.2: security controls | iam-cross-account-s3, iam-federation, vpc-network-controls, encryption-at-rest-access, encryption-in-transit, security-signal-selection, security-central-audit |
| D1 1.3: resilience | availability-failure-design, availability-scale-policy, recovery-objectives, recovery-strategy, recovery-data-protection |
| D1 1.4: multi-account environment | governance-account-structure, governance-policy-controls, governance-landing-zone, governance-resource-sharing, observability-alarms, observability-centralization |
| D1 1.5: cost visibility | cost-purchasing, cost-resource-usage, cost-allocation-controls |
| D2 2.1: deployment strategy | deployment-iac-change, deployment-release-fit, deployment-safe-rollback, operations-configuration, compute-platform |
| D2 2.2: business continuity | recovery-objectives, recovery-strategy, recovery-data-protection, recovery-testing, global-dns-routing, observability-alarms |
| D2 2.3: security controls | iam-least-privilege, vpc-network-controls, private-endpoint-selection, encryption-at-rest-access, encryption-in-transit, security-web-defense, operations-patching |
| D2 2.4: reliability | availability-failure-design, availability-scale-policy, availability-state-dependencies, availability-recovery-operation, events-service-fit, database-availability-reads, global-dns-routing |
| D2 2.5: performance | compute-instance-fit, storage-access-fit, database-access-fit, database-cache-fit, performance-remediation |
| D2 2.6: cost optimization | cost-purchasing, cost-resource-usage, cost-transfer-model, cost-allocation-controls, storage-lifecycle-retention |
| D3 3.1: operational excellence | observability-signals, observability-alarms, deployment-release-fit, operations-configuration, operations-safe-automation, availability-recovery-operation, recovery-testing |
| D3 3.2: security improvement | iam-least-privilege, encryption-secret-lifecycle, encryption-data-obligations, security-central-audit, security-response-priority, operations-patching, recovery-data-protection |
| D3 3.3: performance improvement | observability-measurable-goals, performance-bottleneck, performance-remediation, performance-experiment, global-edge-selection |
| D3 3.4: reliability improvement | availability-failure-design, availability-scale-policy, availability-state-dependencies, availability-recovery-operation |
| D3 3.5: cost opportunities | cost-purchasing, cost-resource-usage, cost-transfer-model, cost-allocation-controls |
| D4 4.1: migration candidates | migration-portfolio, migration-seven-rs, migration-waves-tco |
| D4 4.2: migration approach | cutover-application-transfer, cutover-database-transfer, cutover-data-transfer, cutover-runbook, governance-landing-zone, hybrid-on-premises-links |
| D4 4.3: target architecture | compute-platform, compute-container-hosting, storage-access-fit, storage-hybrid-access, database-access-fit, modernization-target-architecture |
| D4 4.4: modernization | events-service-fit, events-workflow, modernization-managed-serverless, modernization-incremental-decoupling |

## Evidence mapping

States below map historical production to the approved criteria; they do not establish whole-topic exam readiness.
All cited session paths are `subjects/aws-certified-solutions-architect-pro/sessions.md`. Sources were not used to retroactively
grade these historical attempts. No completed local topic exam or passed status is recorded.

| Requirement | State | Evidence and limitations |
| --- | --- | --- |
| iam-cross-account-s3 | resolved historically, unaided redo after explanation | Line 5 records the identity/bucket-policy placement and restricted-prefix read redo; retain `graded: agent judgement`, not source verification. |
| iam-role-credentials | unknown | Line 5 explicitly says role trust and temporary credentials were not covered; no matching resolved production. |
| iam-federation | unknown | Line 5 explicitly says federation was not covered; no matching resolved production. |
| iam-least-privilege | unknown, partial evidence | Line 5 covers a restricted S3 object prefix, not an audit of a supplied broader IAM design. |
| vpc-route-flow | unknown, partial evidence | Line 3 records basic subnet/IGW and NAT selection, but per-AZ route details were agent-supplied according to `goal.md`; full traffic-flow criterion is not established. |
| vpc-failure-domains | unknown, partial evidence | Line 3 records identifying a second-AZ NAT after clarification, not a complete failure/routing analysis. |
| All other requirement IDs in the proposed sections | unknown | No matching resolved production is recorded; evidence is `none`. Reported service familiarity and the map-created entry on line 4 do not establish coverage. |

The resolved historical S3 subskill does not establish general IAM mastery, role-assumption readiness or an
exam pass. The stored guide supports why these concepts belong in scope; agent judgement supplies the answer
assessment regardless of source availability. Additional documentation is not a readiness condition.
Retain the judgement basis in feedback and logs rather than relabeling it as source verification.

## Approval and prescribed next action

Approval authorizes only addition of these checklists and targets. It does not approve a scope expansion, reset
any topic, start an exam, enroll in paid labs or change the subject goal. After approval, mapmaker re-reads the
map, adds `## Topic Scope` and `Scope: accepted` to each approved section, saves atomically and appends one session.
Historical evidence and source content stay unchanged.

The first unpassed topic is `iam-and-cross-account-access`, with no prerequisites. Using the approved criteria
and historical evidence mapping, its first unknown requirement is `iam-role-credentials`. Offer
learning on that requirement with a confirmed role handoff and feedback identified as agent judgement.
Do not offer a whole-topic exam from the S3 redo alone. A future exam must cover all four approved criteria
using fresh applications; the topic-only guide does not block grading or local pass/status updates.

## Application record

- Applied on 2026-10-05: 22 accepted topic checklists, 81 unique requirement IDs and 22 passing targets.
- Preserved existing topic lines byte-for-byte and historical session bytes; appended one mapmaker session at line 6.
- Persisted local source shorthand and the proposal's ownership/exclusion boundaries beside accepted scope.
- Agent-judgement grading follows the current Contract 9, replacing this proposal's obsolete source-first fallback.
- No goal, sources, mistakes or cards changed; no exam started, pass invented or learning-role handoff performed.
- Structural checks validated scope order, unique IDs, targets, 20 guide-task mappings, nine local source links,
  unchanged topic lines and exactly one session append. Repository checks are recorded in the companion plan.
