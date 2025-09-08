---
title: "AWS Config Aggregators: The Hidden Gap in Deleted Resource Tracking"
date: "2025-09-08"
description: "Discover why AWS Config Aggregators don't show deleted resources and learn alternative approaches for tracking resource deletions across your organization."
tags: ["aws", "config", "compliance", "security", "governance", "multi-account"]
---

# AWS Config Aggregators: The Hidden Gap in Deleted Resource Tracking

You've set up AWS Config Aggregators expecting comprehensive visibility across your organization, including deleted resources. But when you try to query for recently deleted S3 buckets or EC2 instances, you discover a frustrating limitation: **Config Aggregators don't retain deleted resource data**. This gap can leave you blind during critical compliance audits and security investigations.

## 🚨 The Problem: Aggregators Don't Track Deletions

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 20px 0;">
<div>

### 💔 What You Expected

<ul>
<li><strong>Centralized deletion tracking</strong> across all accounts</li>
<li><strong>Historical queries</strong> for deleted resources</li>
<li><strong>Compliance reporting</strong> with deletion timelines</li>
<li><strong>Security investigation</strong> capabilities</li>
</ul>

</div>
<div>

### 😞 What You Actually Get

<ul>
<li><strong>Only current resources</strong> in aggregator views</li>
<li><strong>No deletion history</strong> in centralized queries</li>
<li><strong>Account-by-account investigation</strong> still required</li>
<li><strong>Compliance gaps</strong> for audit requirements</li>
</ul>

</div>
</div>

## Understanding the Limitation

AWS Config Aggregators collect configuration data from multiple accounts and regions into a centralized view. However, **they only aggregate currently existing resources**. When a resource is deleted from the source account's Config service, it disappears from the aggregator as well.

### What Aggregators Actually Provide

**Current Resource Inventory**: View active resources across accounts and regions

**Live Compliance Status**: Check current compliance state organization-wide

**Active Resource Queries**: Search for existing resources across your AWS organization

### What's Missing

**Deleted Resource History**: No centralized view of deleted resources

**Deletion Timelines**: Can't query when resources were removed

**Historical Compliance**: Limited ability to show past compliance states

## The Reality: Individual Account Queries Required

### Why Aggregators Don't Show Deleted Resources

Config Aggregators work by collecting data from individual Config services in member accounts. When a resource is deleted:

1. **Source account Config** marks the resource as `ResourceDeleted`
2. **Aggregator sync** removes the deleted resource from centralized view
3. **Historical data** remains only in the source account's Config history

### Querying Deleted Resources (Account-by-Account)

To find deleted resources, you must query each account individually:

```python
import boto3
from datetime import datetime, timedelta

def find_deleted_resources_per_account(account_ids, regions, resource_type, days_back=30):
    """
    Find deleted resources by querying each account individually
    Note: This CANNOT use Config Aggregators - must query each account
    """
    deleted_resources = []
    
    for account_id in account_ids:
        for region in regions:
            try:
                # Assume role in target account
                sts = boto3.client('sts')
                role_arn = f"arn:aws:iam::{account_id}:role/ConfigQueryRole"
                
                assumed_role = sts.assume_role(
                    RoleArn=role_arn,
                    RoleSessionName='DeletedResourceQuery'
                )
                
                # Create Config client for target account
                config_client = boto3.client(
                    'config',
                    region_name=region,
                    aws_access_key_id=assumed_role['Credentials']['AccessKeyId'],
                    aws_secret_access_key=assumed_role['Credentials']['SecretAccessKey'],
                    aws_session_token=assumed_role['Credentials']['SessionToken']
                )
                
                # Query configuration history for deleted resources
                end_time = datetime.utcnow()
                start_time = end_time - timedelta(days=days_back)
                
                # This is the key limitation: must query each account individually
                response = config_client.get_resource_config_history(
                    resourceType=resource_type,
                    laterTime=start_time,
                    earlierTime=end_time
                )
                
                for item in response['configurationItems']:
                    if item['configurationItemStatus'] == 'ResourceDeleted':
                        deleted_resources.append({
                            'ResourceId': item['resourceId'],
                            'ResourceType': resource_type,
                            'AccountId': account_id,
                            'Region': region,
                            'DeletionTime': item['configurationItemCaptureTime'],
                            'ResourceName': item.get('resourceName', 'N/A')
                        })
                        
            except Exception as e:
                print(f"Error querying account {account_id} in {region}: {str(e)}")
                continue
    
    return deleted_resources

# Example usage - requires individual account queries
deleted_resources = find_deleted_resources_per_account(
    account_ids=['111111111111', '222222222222', '333333333333'],
    regions=['us-east-1', 'us-west-2'],
    resource_type='AWS::S3::Bucket',
    days_back=7
)

for resource in deleted_resources:
    print(f"Deleted {resource['ResourceType']}: {resource['ResourceName']} in {resource['AccountId']}/{resource['Region']}")
```

### SQL Queries Don't Work Across Aggregators

Config's advanced query feature has the same limitation - you cannot query deleted resources across aggregators:

```sql
-- ❌ This WON'T work in Config Aggregator advanced queries
-- Deleted resources are not available in aggregated data
SELECT 
    resourceId,
    resourceType,
    accountId,
    awsRegion,
    configurationItemCaptureTime
WHERE 
    configurationItemStatus = 'ResourceDeleted'
    AND configurationItemCaptureTime > '2024-12-17T00:00:00.000Z'
-- Returns: No results (even if resources were deleted)
```

```sql
-- ✅ This ONLY works when querying individual accounts
-- Must run this query in each account's Config service separately
SELECT 
    resourceId,
    resourceType,
    configurationItemCaptureTime,
    tags.Environment
WHERE 
    configurationItemStatus = 'ResourceDeleted'
    AND tags.Environment = 'Production'
    AND configurationItemCaptureTime > '2024-12-17T00:00:00.000Z'
```

## 🔧 Alternative Solutions

### 1. CloudTrail for Deletion Events

Use CloudTrail to track deletion API calls across accounts:

```python
def find_deletions_via_cloudtrail(account_ids, start_time, end_time):
    """
    Query CloudTrail for deletion events across accounts
    """
    deletion_events = []
    
    for account_id in account_ids:
        cloudtrail = boto3.client('cloudtrail')
        
        # Query for deletion events
        response = cloudtrail.lookup_events(
            LookupAttributes=[
                {
                    'AttributeKey': 'EventName',
                    'AttributeValue': 'DeleteBucket'  # Example for S3
                }
            ],
            StartTime=start_time,
            EndTime=end_time
        )
        
        for event in response['Events']:
            deletion_events.append({
                'EventName': event['EventName'],
                'EventTime': event['EventTime'],
                'Username': event['Username'],
                'Resources': event.get('Resources', [])
            })
    
    return deletion_events
```

### 2. Custom Multi-Account Deletion Tracker

Build your own centralized deletion tracking:

```python
def build_deletion_inventory(organization_accounts):
    """
    Build centralized deletion inventory by querying all accounts
    """
    all_deletions = []
    
    for account in organization_accounts:
        account_deletions = find_deleted_resources_per_account(
            account_ids=[account['Id']],
            regions=['us-east-1', 'us-west-2'],
            resource_type='AWS::S3::Bucket',
            days_back=30
        )
        all_deletions.extend(account_deletions)
    
    # Store in centralized database/S3 for reporting
    store_deletion_data(all_deletions)
    
    return all_deletions
```

### 3. EventBridge for Real-Time Tracking

Set up EventBridge rules to capture deletion events:

```json
{
  "Rules": [
    {
      "Name": "S3BucketDeletions",
      "EventPattern": {
        "source": ["aws.s3"],
        "detail-type": ["AWS API Call via CloudTrail"],
        "detail": {
          "eventSource": ["s3.amazonaws.com"],
          "eventName": ["DeleteBucket"]
        }
      },
      "Targets": [
        {
          "Id": "1",
          "Arn": "arn:aws:lambda:us-east-1:123456789012:function:ProcessDeletion"
        }
      ]
    }
  ]
}
```

## 🛠️ Workaround Strategies

### 1. Understand the Limitation

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 20px 0;">
<div>

### ✅ What Aggregators ARE Good For

<ul>
<li><strong>Current resource inventory</strong> across accounts</li>
<li><strong>Live compliance monitoring</strong> organization-wide</li>
<li><strong>Active resource queries</strong> and reporting</li>
<li><strong>Real-time configuration drift</strong> detection</li>
</ul>

</div>
<div>

### ❌ What Aggregators CAN'T Do

<ul>
<li><strong>Track deleted resources</strong> centrally</li>
<li><strong>Provide deletion history</strong> across accounts</li>
<li><strong>Support historical compliance</strong> queries</li>
<li><strong>Show resource lifecycle</strong> end-to-end</li>
</ul>

</div>
</div>

### 2. Implement Complementary Solutions

**CloudTrail Integration**: Track deletion API calls across accounts

**Custom Automation**: Build Lambda functions to query accounts individually

**EventBridge Rules**: Capture deletion events in real-time

**External Storage**: Store deletion data in S3/DynamoDB for centralized access

### 3. Set Proper Expectations

**For Current Resources**: Use Config Aggregators for live inventory and compliance

**For Deleted Resources**: Plan for individual account queries or alternative solutions

**For Compliance**: Combine Config data with CloudTrail logs for complete audit trails

**For Automation**: Build custom solutions that work around the aggregator limitation

## 💡 Recommended Architecture

<div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 15px; margin: 20px 0;">
<div>

### 🏗️ Current Resources

<ul>
<li><strong>Config Aggregators</strong>: Live inventory</li>
<li><strong>Compliance monitoring</strong>: Real-time status</li>
<li><strong>Resource queries</strong>: Cross-account search</li>
</ul>

</div>
<div>

### 🗑️ Deleted Resources

<ul>
<li><strong>CloudTrail</strong>: API call tracking</li>
<li><strong>Custom Lambda</strong>: Multi-account queries</li>
<li><strong>S3/DynamoDB</strong>: Centralized storage</li>
</ul>

</div>
<div>

### 📊 Reporting

<ul>
<li><strong>Combine both sources</strong>: Complete picture</li>
<li><strong>Automated collection</strong>: Scheduled queries</li>
<li><strong>Dashboard integration</strong>: Unified view</li>
</ul>

</div>
</div>

## Conclusion

AWS Config Aggregators are powerful for tracking **current** resources across your organization, but they have a critical limitation: **deleted resources disappear from aggregated views**. Understanding this gap is essential for:

- **Setting realistic expectations** for compliance and audit capabilities
- **Planning complementary solutions** for deletion tracking
- **Designing proper architecture** that combines multiple AWS services
- **Avoiding surprises** during critical investigations

Config Aggregators remain valuable for live resource inventory and compliance monitoring. For deleted resource tracking, plan to implement CloudTrail analysis, custom automation, or third-party solutions that can provide the centralized deletion visibility you need.

---

*Have you discovered this Config Aggregator limitation in your environment? What alternative approaches have you implemented for tracking deleted resources? Share your workarounds in the comments below.*
