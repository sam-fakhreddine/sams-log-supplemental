---
title: "Protecting Your AWS KMS Keys: The 30-Day Deletion Window SCP"
date: "2025-06-24"
description: "How a simple Service Control Policy can prevent accidental KMS key deletions and save your organization from catastrophic data loss scenarios."
tags: ["aws", "kms", "scp", "security", "governance", "encryption", "compliance"]
---

# Protecting Your AWS KMS Keys: The 30-Day Deletion Window SCP

AWS Key Management Service (KMS) is the backbone of encryption across AWS services, protecting everything from S3 objects to RDS databases. But what happens when someone accidentally schedules a critical encryption key for deletion with just a 7-day window? The answer is usually panic, emergency escalations, and potentially irreversible data loss.

Today, I want to share a simple but powerful Service Control Policy (SCP) that can prevent this nightmare scenario by enforcing a minimum 30-day deletion window for all KMS keys in your organization.

## 🚨 The Problem: Accidental Key Deletion

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 20px 0;">
<div>

<h3>⚠️ Risk Factors</h3>
- **Human Error**: Accidental production key scheduling
- **Insufficient Recovery Time**: 7 days too short for detection
- **Weekend/Holiday Gaps**: Friday deletions missed until Monday
- **Cross-Team Dependencies**: Unaware stakeholders

</div>
<div>

<h3>📖 Real Scenario</h3>
Developer cleaning test environment accidentally includes production KMS key in deletion script. Key scheduled Friday afternoon with 7-day window. Production team notices Tuesday - only 3 days left to recover.

</div>
</div>

Consider this scenario: A developer cleaning up a test environment accidentally includes a production KMS key in their deletion script. The key is scheduled for deletion with a 7-day window on Friday afternoon. By the time the production team notices encrypted data becoming inaccessible the following Tuesday, there are only 3 days left to recover - assuming they can even identify the root cause quickly.

## The Solution: Enforcing a 30-Day Minimum

Here's the Service Control Policy that prevents this scenario:

```json
{
  "Sid": "KMSShortDel",
  "Effect": "Deny",
  "Action": "kms:ScheduleKeyDeletion",
  "Resource": "*",
  "Condition": {
    "NumericLessThan": {
      "kms:ScheduleKeyDeletionPendingWindowInDays": "30"
    }
  }
}
```

This policy is elegantly simple yet powerful. Let's break down how it works:

- **Action**: Targets `kms:ScheduleKeyDeletion` specifically
- **Resource**: Applies to all KMS keys (`*`)
- **Condition**: Uses `NumericLessThan` to deny any deletion window shorter than 30 days
- **Effect**: Denies the action when the condition is met

## 🎯 Real-World Benefits

<div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 15px; margin: 20px 0;">
<div>

<h3>🛡️ Extended Recovery</h3>
- 30-day minimum window
- Multiple detection opportunities
- Reduced panic scenarios
- Better incident response

</div>
<div>

<h3>📋 Compliance Ready</h3>
- **SOC 2**: Data protection controls
- **ISO 27001**: Security framework
- **GDPR**: Recovery procedures
- **HIPAA**: Health data protection

</div>
<div>

<h3>⏰ Safety Timeline</h3>
- **Week 1**: Automated detection
- **Week 2**: Security reviews
- **Week 3**: Compliance audits
- **Week 4**: Final intervention

</div>
</div>

### Before vs After

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 20px 0;">
<div>

<h3>❌ Before SCP</h3>
```bash
# Dangerous 7-day window succeeds
aws kms schedule-key-deletion \
  --key-id alias/prod-key \
  --pending-window-in-days 7
```

</div>
<div>

<h3>✅ After SCP</h3>
```bash
# Short window now fails
aws kms schedule-key-deletion \
  --key-id alias/prod-key \
  --pending-window-in-days 7
# Error: Access Denied

# Forces proper 30+ day window
aws kms schedule-key-deletion \
  --key-id alias/prod-key \
  --pending-window-in-days 30
```

</div>
</div>

## Implementation Strategy

### Step 1: Create the Complete SCP

While the core policy focuses on deletion windows, consider this comprehensive KMS protection SCP:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "KMSShortDel",
      "Effect": "Deny",
      "Action": "kms:ScheduleKeyDeletion",
      "Resource": "*",
      "Condition": {
        "NumericLessThan": {
          "kms:ScheduleKeyDeletionPendingWindowInDays": "30"
        }
      }
    },
    {
      "Sid": "KMSProductionProtection",
      "Effect": "Deny",
      "Action": [
        "kms:ScheduleKeyDeletion",
        "kms:DisableKey"
      ],
      "Resource": "*",
      "Condition": {
        "StringLike": {
          "kms:KeySpec": "*",
          "aws:RequestedRegion": "*"
        },
        "ForAllValues:StringLike": {
          "kms:ResourceAliases": [
            "alias/prod-*",
            "alias/production-*"
          ]
        }
      },
      "Principal": "*"
    }
  ]
}
```

### Step 2: Gradual Rollout

**Phase 1: Non-Production (Week 1)**

- Apply SCP to development and staging OUs
- Monitor for any legitimate use cases requiring shorter windows
- Adjust policy if needed based on feedback

**Phase 2: Production (Week 2)**

- Apply SCP to production OUs
- Communicate changes to all teams
- Provide training on new deletion procedures

**Phase 3: Organization-wide (Week 3)**

- Apply SCP at root organization level
- Document new procedures in runbooks
- Update automation scripts to use 30+ day windows

### Step 3: Monitoring and Alerting

Create CloudWatch alarms to monitor key deletion activities:

```python
import boto3
import json

def create_kms_deletion_alarm():
    cloudwatch = boto3.client('cloudwatch')
    
    # Create alarm for any key deletion scheduling
    cloudwatch.put_metric_alarm(
        AlarmName='KMS-Key-Deletion-Scheduled',
        ComparisonOperator='GreaterThanThreshold',
        EvaluationPeriods=1,
        MetricName='ScheduleKeyDeletion',
        Namespace='AWS/KMS',
        Period=300,
        Statistic='Sum',
        Threshold=0.0,
        ActionsEnabled=True,
        AlarmActions=[
            'arn:aws:sns:us-east-1:123456789012:security-alerts'
        ],
        AlarmDescription='Alert when KMS key deletion is scheduled'
    )
```

## 💬 Common Objections

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 20px 0;">
<div>

<h3>💬 "30 days too long for dev"</h3>
**Solution**: Environment-specific SCPs
```json
{
  "Sid": "KMSDevShortDel",
  "Condition": {
    "NumericLessThan": {
      "kms:ScheduleKeyDeletionPendingWindowInDays": "14"
    }
  }
}
```

<h3>🤖 "Breaks our automation"</h3>
**Solution**: Fix the automation!
```bash
sed -i 's/--pending-window-in-days 7/--pending-window-in-days 30/g' cleanup-scripts/*.sh
```

</div>
<div>

<h3>🚨 "Need immediate deletion"</h3>
**Solution**: Disable first, then schedule
```bash
# Immediate security response
aws kms disable-key --key-id alias/compromised-key

# Proper deletion window
aws kms schedule-key-deletion \
  --key-id alias/compromised-key \
  --pending-window-in-days 30
```

<h3>🔒 "Too restrictive"</h3>
**Solution**: Break-glass procedure with temporary SCP detachment and approval workflow

</div>
</div>

## 📊 Measuring Success

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 20px 0;">
<div>

<h3>❌ Before Implementation</h3>
- **Deletion window**: 7-14 days
- **Accidental deletions**: 2-3/month
- **Recovery incidents**: 1-2/quarter
- **Recovery time**: 4-8 hours

</div>
<div>

<h3>✅ After Implementation</h3>
- **Deletion window**: 30+ days
- **Accidental deletions**: 0/month
- **Recovery incidents**: 0
- **Prevented incidents**: 3-4/quarter

</div>
</div>

## Advanced Considerations

### Multi-Region Deployments

Ensure the SCP applies across all regions where you use KMS:

```json
{
  "Condition": {
    "NumericLessThan": {
      "kms:ScheduleKeyDeletionPendingWindowInDays": "30"
    },
    "StringEquals": {
      "aws:RequestedRegion": [
        "us-east-1",
        "us-west-2",
        "eu-west-1"
      ]
    }
  }
}
```

### Exception Handling

For legitimate cases requiring shorter windows, implement a break-glass procedure:

1. **Temporary SCP Detachment**: Remove account from SCP-protected OU
2. **Approval Workflow**: Require security team approval
3. **Monitoring**: Enhanced logging during exception period
4. **Re-attachment**: Return account to protected OU after operation

## Conclusion

The KMS 30-day deletion window SCP represents a perfect example of "defense in depth" - a simple policy that provides significant protection against human error and operational mistakes. While it may seem like a small change, the impact on your organization's data protection posture is substantial.

The policy costs nothing to implement, requires no ongoing maintenance, and can prevent catastrophic data loss scenarios that could cost millions in recovery efforts and business disruption. In the world of cloud security, few controls offer such a favorable risk-to-effort ratio.

Remember: encryption keys are the foundation of your data security. Protecting them with appropriate governance controls isn't just a best practice - it's essential for maintaining trust in your cloud infrastructure.

---

*Have you implemented similar KMS protection policies in your organization? What other Service Control Policies have proven valuable for preventing operational mistakes? Share your experiences in the comments below.*
