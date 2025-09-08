---
title: "AWS Config Aggregators: Tracking Deleted Resources Across Your Organization"
date: "2025-09-09"
description: "Learn how AWS Config Aggregators can help you track and audit deleted resources across multiple accounts and regions, providing crucial visibility for compliance and security investigations."
tags: ["aws", "config", "compliance", "security", "governance", "multi-account"]
---

# AWS Config Aggregators: Tracking Deleted Resources Across Your Organization

When resources mysteriously disappear from your AWS environment, the investigation can be challenging. Was it deleted intentionally? By whom? When? AWS Config Aggregators provide a powerful solution for tracking deleted resources across your entire organization, giving you the visibility needed for compliance, security, and operational investigations.

## 🎯 The Challenge: Visibility Across Accounts

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 20px 0;">
<div>

### 🔍 Common Scenarios
<ul>
<li><strong>Compliance Audits</strong>: "Show me all deleted S3 buckets last quarter"</li>
<li><strong>Security Incidents</strong>: "What resources were deleted during the breach window?"</li>
<li><strong>Cost Investigation</strong>: "Why did our EC2 costs drop suddenly?"</li>
<li><strong>Change Management</strong>: "Track all infrastructure changes across accounts"</li>
</ul>

</div>
<div>

### ⚠️ Without Aggregators
<ul>
<li>Manual account-by-account checking</li>
<li>Inconsistent Config setup across accounts</li>
<li>Limited cross-region visibility</li>
<li>Time-consuming investigations</li>
<li>Potential compliance gaps</li>
</ul>

</div>
</div>

## Understanding AWS Config Aggregators

AWS Config Aggregators collect configuration data from multiple accounts and regions into a centralized view. This includes both current resources and historical data about deleted resources.

### Key Benefits

**Centralized Visibility**: View configuration data from all accounts and regions in one place

**Historical Tracking**: Access configuration history including deleted resources

**Compliance Reporting**: Generate organization-wide compliance reports

**Cross-Account Queries**: Search for resources across your entire AWS organization

## Setting Up Config Aggregators

### 1. Organization-Wide Aggregator

For AWS Organizations, create an aggregator in your management account:

```bash
# Create organization-wide aggregator
aws configservice put-configuration-aggregator \
  --configuration-aggregator-name "OrgWideAggregator" \
  --organization-aggregation-source '{
    "RoleArn": "arn:aws:iam::123456789012:role/aws-service-role/organizations.amazonaws.com/AWSServiceRoleForOrganizations",
    "AwsRegions": ["us-east-1", "us-west-2", "eu-west-1"],
    "AllAwsRegions": false
  }'
```

### 2. Account-Based Aggregator

For specific accounts outside an organization:

```bash
# Create account-based aggregator
aws configservice put-configuration-aggregator \
  --configuration-aggregator-name "MultiAccountAggregator" \
  --account-aggregation-sources '[{
    "AccountIds": ["111111111111", "222222222222", "333333333333"],
    "AwsRegions": ["us-east-1", "us-west-2"],
    "AllAwsRegions": false
  }]'
```

### 3. Required IAM Permissions

The aggregator needs permissions to access Config data from member accounts:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "config:GetComplianceDetailsByConfigRule",
        "config:GetComplianceDetailsByResource",
        "config:GetComplianceSummaryByConfigRule",
        "config:GetComplianceSummaryByResourceType",
        "config:GetResourceConfigHistory",
        "config:ListDiscoveredResources",
        "config:GetAggregateComplianceDetailsByConfigRule",
        "config:GetAggregateConfigRuleComplianceSummary",
        "config:GetAggregateDiscoveredResourceCounts",
        "config:GetAggregateResourceConfig"
      ],
      "Resource": "*"
    }
  ]
}
```

## Tracking Deleted Resources

### Query Deleted Resources

Use the Config API to find deleted resources across your organization:

```python
import boto3
from datetime import datetime, timedelta

def find_deleted_resources(aggregator_name, resource_type, days_back=30):
    """
    Find deleted resources across the organization using Config Aggregator
    """
    config_client = boto3.client('config')
    
    # Calculate time range
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=days_back)
    
    try:
        # Get aggregate discovered resources
        response = config_client.get_aggregate_discovered_resource_counts(
            ConfigurationAggregatorName=aggregator_name,
            Filters={
                'ResourceType': resource_type,
                'AccountId': None,  # All accounts
                'Region': None      # All regions
            }
        )
        
        deleted_resources = []
        
        # For each resource, check if it's been deleted
        for resource_count in response['GroupedResourceCounts']:
            account_id = resource_count['GroupName'].split(':')[0]
            region = resource_count['GroupName'].split(':')[1]
            
            # Get detailed resource information
            resources_response = config_client.list_aggregate_discovered_resources(
                ConfigurationAggregatorName=aggregator_name,
                ResourceType=resource_type,
                Filters={
                    'AccountId': account_id,
                    'Region': region
                }
            )
            
            for resource in resources_response['ResourceIdentifiers']:
                # Get resource configuration history
                history_response = config_client.get_aggregate_resource_config(
                    ConfigurationAggregatorName=aggregator_name,
                    ResourceIdentifier={
                        'SourceAccountId': account_id,
                        'SourceRegion': region,
                        'ResourceId': resource['ResourceId'],
                        'ResourceType': resource_type,
                        'ResourceName': resource.get('ResourceName', '')
                    }
                )
                
                config_item = history_response['ConfigurationItem']
                
                # Check if resource was deleted in our time window
                if (config_item['ConfigurationItemStatus'] == 'ResourceDeleted' and
                    start_time <= config_item['ConfigurationItemCaptureTime'].replace(tzinfo=None) <= end_time):
                    
                    deleted_resources.append({
                        'ResourceId': resource['ResourceId'],
                        'ResourceType': resource_type,
                        'AccountId': account_id,
                        'Region': region,
                        'DeletionTime': config_item['ConfigurationItemCaptureTime'],
                        'ResourceName': resource.get('ResourceName', 'N/A')
                    })
        
        return deleted_resources
        
    except Exception as e:
        print(f"Error querying deleted resources: {str(e)}")
        return []

# Example usage
deleted_s3_buckets = find_deleted_resources(
    aggregator_name='OrgWideAggregator',
    resource_type='AWS::S3::Bucket',
    days_back=7
)

for bucket in deleted_s3_buckets:
    print(f"Deleted S3 Bucket: {bucket['ResourceName']} in {bucket['AccountId']}/{bucket['Region']} at {bucket['DeletionTime']}")
```

### Advanced Queries with SQL

Use Config's advanced query feature for complex investigations:

```sql
-- Find all deleted EC2 instances in the last 30 days
SELECT 
    resourceId,
    resourceType,
    accountId,
    awsRegion,
    configurationItemCaptureTime,
    tags
WHERE 
    resourceType = 'AWS::EC2::Instance'
    AND configurationItemStatus = 'ResourceDeleted'
    AND configurationItemCaptureTime > '2024-12-17T00:00:00.000Z'
ORDER BY configurationItemCaptureTime DESC
```

```sql
-- Find deleted resources by specific tag
SELECT 
    resourceId,
    resourceType,
    accountId,
    awsRegion,
    configurationItemCaptureTime,
    tags.Environment
WHERE 
    configurationItemStatus = 'ResourceDeleted'
    AND tags.Environment = 'Production'
    AND configurationItemCaptureTime > '2024-12-17T00:00:00.000Z'
```

## 📊 Practical Use Cases

### 1. Compliance Reporting

Generate reports showing all deleted resources for audit purposes:

```python
def generate_deletion_report(aggregator_name, start_date, end_date):
    """
    Generate a comprehensive deletion report for compliance
    """
    resource_types = [
        'AWS::S3::Bucket',
        'AWS::EC2::Instance',
        'AWS::RDS::DBInstance',
        'AWS::Lambda::Function',
        'AWS::IAM::Role'
    ]
    
    report = {
        'report_period': f"{start_date} to {end_date}",
        'deleted_resources': []
    }
    
    for resource_type in resource_types:
        deleted = find_deleted_resources(aggregator_name, resource_type, 30)
        report['deleted_resources'].extend(deleted)
    
    # Sort by deletion time
    report['deleted_resources'].sort(
        key=lambda x: x['DeletionTime'], 
        reverse=True
    )
    
    return report
```

### 2. Security Investigation

Track resource deletions during security incidents:

```python
def security_investigation(aggregator_name, incident_start, incident_end):
    """
    Investigate resource deletions during a security incident timeframe
    """
    suspicious_deletions = []
    
    # Focus on security-sensitive resources
    sensitive_resources = [
        'AWS::IAM::Role',
        'AWS::IAM::Policy', 
        'AWS::S3::Bucket',
        'AWS::CloudTrail::Trail',
        'AWS::Config::ConfigurationRecorder'
    ]
    
    for resource_type in sensitive_resources:
        # Custom time range for incident window
        deletions = find_deleted_resources_in_timeframe(
            aggregator_name, 
            resource_type, 
            incident_start, 
            incident_end
        )
        suspicious_deletions.extend(deletions)
    
    return suspicious_deletions
```

### 3. Cost Analysis

Correlate resource deletions with cost changes:

```python
def cost_impact_analysis(aggregator_name, resource_deletions):
    """
    Analyze the cost impact of deleted resources
    """
    cost_client = boto3.client('ce')  # Cost Explorer
    
    analysis = []
    
    for deletion in resource_deletions:
        # Get cost data for the resource if available
        if deletion['ResourceType'] in ['AWS::EC2::Instance', 'AWS::RDS::DBInstance']:
            # Query Cost Explorer for resource-specific costs
            cost_data = get_resource_costs(
                cost_client,
                deletion['ResourceId'],
                deletion['DeletionTime']
            )
            
            analysis.append({
                'resource': deletion,
                'estimated_monthly_cost': cost_data.get('monthly_cost', 0),
                'cost_impact': 'High' if cost_data.get('monthly_cost', 0) > 1000 else 'Low'
            })
    
    return analysis
```

## 🛠️ Best Practices

### 1. Aggregator Configuration

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 20px 0;">
<div>

### ✅ Do
<ul>
<li><strong>Use organization-wide aggregators</strong> for centralized management</li>
<li><strong>Include all relevant regions</strong> where you have resources</li>
<li><strong>Set up proper IAM permissions</strong> for cross-account access</li>
<li><strong>Monitor aggregator health</strong> and data freshness</li>
</ul>

</div>
<div>

### ❌ Don't
<ul>
<li><strong>Create multiple overlapping aggregators</strong> unnecessarily</li>
<li><strong>Include unused regions</strong> to avoid extra costs</li>
<li><strong>Forget to update permissions</strong> when adding accounts</li>
<li><strong>Ignore aggregation failures</strong> in member accounts</li>
</ul>

</div>
</div>

### 2. Monitoring and Alerting

Set up CloudWatch alarms for aggregator health:

```python
def create_aggregator_monitoring(aggregator_name):
    """
    Create CloudWatch alarms for Config Aggregator monitoring
    """
    cloudwatch = boto3.client('cloudwatch')
    
    # Alarm for aggregation failures
    cloudwatch.put_metric_alarm(
        AlarmName=f'ConfigAggregator-{aggregator_name}-Failures',
        ComparisonOperator='GreaterThanThreshold',
        EvaluationPeriods=2,
        MetricName='NumberOfFailedAggregations',
        Namespace='AWS/Config',
        Period=300,
        Statistic='Sum',
        Threshold=0,
        ActionsEnabled=True,
        AlarmActions=[
            'arn:aws:sns:us-east-1:123456789012:config-alerts'
        ],
        AlarmDescription=f'Config Aggregator {aggregator_name} has aggregation failures',
        Dimensions=[
            {
                'Name': 'AggregatorName',
                'Value': aggregator_name
            }
        ]
    )
```

### 3. Data Retention

Understand Config's data retention policies:

- **Configuration history**: Retained for the period specified in your delivery channel
- **Deleted resources**: Available in aggregator as long as the source account retains the data
- **Query results**: Available through the Config API and console

## 💰 Cost Considerations

<div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 15px; margin: 20px 0;">
<div>

### 📊 Config Costs
<ul>
<li><strong>Configuration items</strong>: $0.003 per item</li>
<li><strong>Config rules</strong>: $0.001 per evaluation</li>
<li><strong>Aggregator</strong>: No additional cost</li>
</ul>

</div>
<div>

### 💾 Storage Costs
<ul>
<li><strong>S3 delivery channel</strong>: Standard S3 pricing</li>
<li><strong>Retention period</strong>: Affects storage costs</li>
<li><strong>Cross-region</strong>: Data transfer charges</li>
</ul>

</div>
<div>

### 🎯 Optimization Tips
<ul>
<li>Monitor only necessary resource types</li>
<li>Set appropriate retention periods</li>
<li>Use lifecycle policies on S3 buckets</li>
<li>Regular cleanup of old data</li>
</ul>

</div>
</div>

## Conclusion

AWS Config Aggregators provide essential visibility into resource changes across your organization, including deleted resources. By implementing proper aggregation strategies, you can:

- **Enhance compliance** with centralized audit trails
- **Improve security** through comprehensive change tracking  
- **Streamline investigations** with cross-account visibility
- **Support governance** with organization-wide reporting

The investment in setting up Config Aggregators pays dividends in operational efficiency, security posture, and compliance readiness. Start with an organization-wide aggregator and expand your monitoring as your AWS footprint grows.

---

*Have you implemented Config Aggregators in your organization? What challenges have you faced with tracking deleted resources across multiple accounts? Share your experiences in the comments below.*