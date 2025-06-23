# S3 Metadata for Change Request Tracking

## Understanding S3 Object Metadata

S3 supports two types of metadata:

- **System Metadata**: Managed by AWS (Content-Type, Last-Modified, etc.)
- **User-Defined Metadata**: Custom key-value pairs you control

### Key Limitations & Rules

- **2KB total limit** for all user-defined metadata combined
- Keys must be **lowercase**
- Keys can only contain letters, numbers, and hyphens
- Keys are prefixed with `x-amz-meta-` automatically
- Values are stored as strings only

## AWS CLI Implementation

### Basic S3 Move with Metadata

```bash
# Standard move with change request metadata
aws s3 mv source-file.txt s3://my-bucket/destination-file.txt \
  --metadata "change-request-id=CR-12345,operator=john.doe,timestamp=2025-06-23T17:00:00Z"

# Copy with metadata (preserves source)
aws s3 cp local-file.txt s3://my-bucket/remote-file.txt \
  --metadata "change-request-id=CR-12345,purpose=security-remediation,approved-by=jane.smith"
```

### Advanced Metadata with JSON Input

```bash
# Using CLI JSON input for complex metadata
aws s3api copy-object \
  --copy-source "source-bucket/source-key" \
  --bucket "dest-bucket" \
  --key "dest-key" \
  --metadata '{
    "change-request-id": "CR-12345",
    "operator": "john.doe", 
    "timestamp": "2025-06-23T17:00:00Z",
    "approval-status": "approved",
    "risk-level": "low",
    "department": "security"
  }' \
  --metadata-directive "REPLACE"
```

### Retrieving Metadata

```bash
# Check metadata on an object
aws s3api head-object --bucket my-bucket --key my-file.txt

# Filter for just user metadata
aws s3api head-object --bucket my-bucket --key my-file.txt \
  --query 'Metadata' --output table
```

## Python Boto3 Implementation

### Complete Move Operation with Metadata

```python
import boto3
from datetime import datetime
import os
from typing import Dict, Optional

class S3MetadataManager:
    def __init__(self, region_name: str = 'us-east-1'):
        self.s3_client = boto3.client('s3', region_name=region_name)
    
    def move_with_metadata(self, 
                          source_bucket: str, 
                          source_key: str,
                          dest_bucket: str, 
                          dest_key: str,
                          change_request_id: str,
                          operator: Optional[str] = None,
                          additional_metadata: Optional[Dict[str, str]] = None) -> bool:
        """
        Move S3 object with change request metadata
        """
        try:
            # Build standard metadata
            metadata = {
                'change-request-id': change_request_id,
                'operator': operator or os.getenv('USER', 'unknown'),
                'timestamp': datetime.utcnow().isoformat(),
                'operation': 'move'
            }
            
            # Add any additional metadata
            if additional_metadata:
                metadata.update(additional_metadata)
            
            # Validate metadata size (approximate)
            metadata_size = sum(len(k) + len(v) for k, v in metadata.items())
            if metadata_size > 1800:  # Leave buffer for AWS prefixes
                raise ValueError(f"Metadata too large: {metadata_size} bytes")
            
            # Copy with metadata
            copy_source = {'Bucket': source_bucket, 'Key': source_key}
            self.s3_client.copy_object(
                CopySource=copy_source,
                Bucket=dest_bucket,
                Key=dest_key,
                Metadata=metadata,
                MetadataDirective='REPLACE'
            )
            
            # Delete source (completing the move)
            self.s3_client.delete_object(Bucket=source_bucket, Key=source_key)
            
            print(f"Successfully moved {source_bucket}/{source_key} to {dest_bucket}/{dest_key}")
            print(f"Change Request ID: {change_request_id}")
            return True
            
        except Exception as e:
            print(f"Error moving object: {str(e)}")
            return False
    
    def get_change_request_metadata(self, bucket: str, key: str) -> Optional[Dict[str, str]]:
        """
        Retrieve change request metadata from S3 object
        """
        try:
            response = self.s3_client.head_object(Bucket=bucket, Key=key)
            metadata = response.get('Metadata', {})
            
            # Filter for change request related metadata
            cr_metadata = {}
            for key, value in metadata.items():
                if any(keyword in key.lower() for keyword in 
                      ['change-request', 'operator', 'timestamp', 'approval']):
                    cr_metadata[key] = value
            
            return cr_metadata
        except Exception as e:
            print(f"Error retrieving metadata: {str(e)}")
            return None
    
    def batch_move_with_metadata(self, 
                                operations: list,
                                change_request_id: str) -> Dict[str, bool]:
        """
        Batch move multiple objects with same change request ID
        
        operations format: [
            {
                'source_bucket': 'bucket1',
                'source_key': 'file1.txt',
                'dest_bucket': 'bucket2', 
                'dest_key': 'file1.txt'
            }
        ]
        """
        results = {}
        
        for i, op in enumerate(operations):
            operation_metadata = {
                'batch-operation': 'true',
                'batch-sequence': str(i + 1),
                'batch-total': str(len(operations))
            }
            
            success = self.move_with_metadata(
                source_bucket=op['source_bucket'],
                source_key=op['source_key'],
                dest_bucket=op['dest_bucket'],
                dest_key=op['dest_key'],
                change_request_id=change_request_id,
                additional_metadata=operation_metadata
            )
            
            results[f"{op['source_bucket']}/{op['source_key']}"] = success
        
        return results

# Usage example
if __name__ == "__main__":
    manager = S3MetadataManager()
    
    # Single file move
    success = manager.move_with_metadata(
        source_bucket='source-bucket',
        source_key='sensitive-data.csv',
        dest_bucket='secure-bucket',
        dest_key='archived/sensitive-data.csv',
        change_request_id='CR-12345',
        operator='security-team',
        additional_metadata={
            'purpose': 'security-remediation',
            'approval-date': '2025-06-23',
            'risk-level': 'high'
        }
    )
    
    # Check metadata
    metadata = manager.get_change_request_metadata('secure-bucket', 'archived/sensitive-data.csv')
    print("Retrieved metadata:", metadata)
```

### Metadata Validation Helper

```python
def validate_s3_metadata(metadata: Dict[str, str]) -> tuple[bool, str]:
    """
    Validate S3 metadata before applying
    """
    # Check size limit
    total_size = sum(len(k) + len(v) for k, v in metadata.items())
    if total_size > 1800:  # Conservative limit
        return False, f"Metadata size {total_size} bytes exceeds limit"
    
    # Check key format
    for key in metadata.keys():
        if not key.islower():
            return False, f"Key '{key}' must be lowercase"
        if not all(c.isalnum() or c == '-' for c in key):
            return False, f"Key '{key}' contains invalid characters"
    
    # Check for required fields
    required_fields = ['change-request-id']
    for field in required_fields:
        if field not in metadata:
            return False, f"Required field '{field}' missing"
    
    return True, "Valid"

# Example usage
metadata = {
    'change-request-id': 'CR-12345',
    'operator': 'john.doe',
    'timestamp': '2025-06-23T17:00:00Z'
}

is_valid, message = validate_s3_metadata(metadata)
print(f"Metadata valid: {is_valid}, Message: {message}")
```

## Shell Script for Automated Moves

### Complete Automation Script

```bash
#!/bin/bash

# s3-move-with-metadata.sh
# Usage: ./s3-move-with-metadata.sh SOURCE_BUCKET SOURCE_KEY DEST_BUCKET DEST_KEY CR_ID

set -euo pipefail

# Input validation
if [ $# -ne 5 ]; then
    echo "Usage: $0 <source_bucket> <source_key> <dest_bucket> <dest_key> <change_request_id>"
    exit 1
fi

SOURCE_BUCKET="$1"
SOURCE_KEY="$2"
DEST_BUCKET="$3"
DEST_KEY="$4"
CHANGE_REQUEST_ID="$5"

# Get current user and timestamp
OPERATOR="${USER:-unknown}"
TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)

# Build metadata
METADATA="change-request-id=${CHANGE_REQUEST_ID},operator=${OPERATOR},timestamp=${TIMESTAMP},script-version=1.0"

# Log the operation
LOG_FILE="/var/log/s3-operations.log"
echo "$(date): [${CHANGE_REQUEST_ID}] Moving s3://${SOURCE_BUCKET}/${SOURCE_KEY} to s3://${DEST_BUCKET}/${DEST_KEY} by ${OPERATOR}" >> "${LOG_FILE}"

# Perform the move with metadata
echo "Moving s3://${SOURCE_BUCKET}/${SOURCE_KEY} to s3://${DEST_BUCKET}/${DEST_KEY}"
echo "Change Request: ${CHANGE_REQUEST_ID}"

aws s3 mv "s3://${SOURCE_BUCKET}/${SOURCE_KEY}" "s3://${DEST_BUCKET}/${DEST_KEY}" \
    --metadata "${METADATA}"

# Verify the metadata was applied
echo "Verifying metadata..."
aws s3api head-object --bucket "${DEST_BUCKET}" --key "${DEST_KEY}" \
    --query 'Metadata' --output table

echo "Move completed successfully with metadata"
```

## GuardDuty Correlation Script

### Correlating Metadata with GuardDuty Findings

```python
import boto3
from datetime import datetime, timedelta
from typing import List, Dict, Optional

class GuardDutyMetadataCorrelator:
    def __init__(self, region_name: str = 'us-east-1'):
        self.guardduty = boto3.client('guardduty', region_name=region_name)
        self.s3 = boto3.client('s3', region_name=region_name)
        self.cloudtrail = boto3.client('cloudtrail', region_name=region_name)
    
    def correlate_finding_with_metadata(self, 
                                      detector_id: str, 
                                      finding_id: str) -> Optional[Dict]:
        """
        Correlate GuardDuty finding with S3 object metadata
        """
        try:
            # Get finding details
            response = self.guardduty.get_findings(
                DetectorId=detector_id,
                FindingIds=[finding_id]
            )
            
            finding = response['Findings'][0]
            
            # Extract S3 information
            if 'S3BucketDetails' not in finding['Resource']:
                return None
            
            bucket_name = finding['Resource']['S3BucketDetails']['Name']
            finding_time = datetime.fromisoformat(finding['CreatedAt'].replace('Z', '+00:00'))
            
            # Look for related CloudTrail events
            events = self.cloudtrail.lookup_events(
                LookupAttributes=[
                    {
                        'AttributeKey': 'ResourceName',
                        'AttributeValue': bucket_name
                    }
                ],
                StartTime=finding_time - timedelta(hours=2),
                EndTime=finding_time + timedelta(minutes=30)
            )
            
            # Check metadata for objects involved in recent events
            metadata_results = []
            for event in events['Events']:
                if any(action in event['EventName'] for action in ['PutObject', 'CopyObject']):
                    # Extract object key from CloudTrail event
                    object_key = self.extract_object_key_from_event(event)
                    if object_key:
                        metadata = self.get_object_metadata(bucket_name, object_key)
                        if metadata:
                            metadata_results.append({
                                'object_key': object_key,
                                'event_time': event['EventTime'],
                                'metadata': metadata,
                                'event_name': event['EventName']
                            })
            
            return {
                'finding_id': finding_id,
                'bucket_name': bucket_name,
                'finding_time': finding_time,
                'related_metadata': metadata_results
            }
            
        except Exception as e:
            print(f"Error correlating finding: {str(e)}")
            return None
    
    def extract_object_key_from_event(self, event: Dict) -> Optional[str]:
        """
        Extract object key from CloudTrail event
        """
        try:
            # Parse the event to find object key
            if 'Resources' in event:
                for resource in event['Resources']:
                    if resource['ResourceType'] == 'AWS::S3::Object':
                        return resource['ResourceName']
            return None
        except:
            return None
    
    def get_object_metadata(self, bucket: str, key: str) -> Optional[Dict]:
        """
        Get metadata for specific S3 object
        """
        try:
            response = self.s3.head_object(Bucket=bucket, Key=key)
            return response.get('Metadata', {})
        except:
            return None
    
    def add_context_to_finding(self, 
                              detector_id: str, 
                              finding_id: str, 
                              change_request_id: str):
        """
        Add change request context to GuardDuty finding
        """
        try:
            # Add finding feedback with change request context
            self.guardduty.create_finding_feedback(
                DetectorId=detector_id,
                FindingId=finding_id,
                Feedback='USEFUL',
                Comments=f'Associated with approved change request: {change_request_id}. '
                        f'This activity was authorized and tracked.'
            )
            print(f"Added context to finding {finding_id}")
        except Exception as e:
            print(f"Error adding context: {str(e)}")

# Usage example
correlator = GuardDutyMetadataCorrelator()
result = correlator.correlate_finding_with_metadata('detector-123', 'finding-456')

if result:
    print(f"Found {len(result['related_metadata'])} objects with metadata")
    for item in result['related_metadata']:
        if 'change-request-id' in item['metadata']:
            cr_id = item['metadata']['change-request-id']
            print(f"Object {item['object_key']} linked to {cr_id}")
            correlator.add_context_to_finding('detector-123', 'finding-456', cr_id)
```

## Best Practices Summary

### Metadata Schema Standards

```python
# Recommended metadata structure
STANDARD_METADATA = {
    'change-request-id': 'CR-XXXXX',      # Required
    'operator': 'username',               # Who performed action
    'timestamp': 'ISO8601',               # When action occurred
    'purpose': 'description',             # Why action was needed
    'approval-status': 'approved',        # Approval state
    'risk-level': 'low|medium|high',      # Risk assessment
    'department': 'team-name',            # Responsible team
    'automation': 'true|false'            # Automated vs manual
}
```

