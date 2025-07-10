---
title: "CloudWatch Agent: Why You Should Filter File System Types"
date: "2024-12-19"
description: "Learn why filtering file system types in CloudWatch agent improves performance, reduces costs, and focuses monitoring on what matters most."
tags: ["aws", "cloudwatch", "monitoring", "performance", "devops"]
---

# CloudWatch Agent: Why You Should Filter File System Types

When configuring the CloudWatch agent for disk monitoring, one of the most important optimizations you can make is filtering out irrelevant file system types. This simple configuration change can dramatically improve performance, reduce costs, and focus your monitoring on what actually matters.

## The Problem with Monitoring Everything

By default, CloudWatch agent attempts to monitor all mounted file systems. This includes:

- Virtual file systems that don't represent real storage
- Network file systems that may be slow to query
- Container overlay file systems
- System pseudo-file systems
- Temporary and memory-based file systems

Monitoring these unnecessary file systems creates several problems:

- **Performance Impact**: Querying virtual/network file systems adds latency
- **Cost Inflation**: More metrics = higher CloudWatch costs
- **Alert Noise**: False positives from irrelevant file systems
- **Resource Waste**: CPU and memory overhead for meaningless data

## The Solution: Strategic File System Filtering

Here's the comprehensive filter list that addresses these issues:

```json
{
  "metrics": {
    "metrics_collected": {
      "disk": {
        "measurement": ["used_percent"],
        "ignore_file_system_types": [
          "9p", "afs", "amazon-efs-client-utils", "amazon-ssm-agent",
          "anon_inodefs", "aufs", "autofs", "bdev", "beegfs", "binfmt_misc",
          "bindfs", "btrfs-subvol", "cephfs", "cgroup", "cgroup2", "cifs",
          "cluster", "coda", "configfs", "cramfs", "curlftpfs", "davfs2",
          "dax", "debugfs", "devicemapper", "devpts", "devtmpfs", "dlm",
          "drbd", "ecryptfs", "efs", "efs-utils", "efivarfs", "encfs",
          "exfat", "fat", "fat32", "fsx", "fuse", "fuseblk", "gfs", "gfs2",
          "glusterfs", "goofys", "gpfs", "hfs", "hfsplus", "hugetlbfs",
          "iscsi", "iso9660", "jffs2", "lustre", "loop*", "mountpoint-s3",
          "mqueue", "msdos", "multipath", "ncpfs", "nfs", "nfs4", "nfsd",
          "nsfs", "ntfs", "ntfs-3g", "ocfs2", "orangefs", "overlay",
          "overlay2", "pipefs", "proc", "pstore", "pvfs2", "ramfs",
          "romfs", "rootfs", "rpc_pipefs", "s3fs", "s3fs-fuse",
          "securityfs", "selinuxfs", "shm", "smb", "smb2", "smb3", "smbfs",
          "sockfs", "squashfs", "sshfs", "sunrpc", "sysfs", "systemd-1",
          "tmpfs", "tracefs", "ubifs", "udev", "udf", "unionfs-fuse",
          "vfat", "vmhgfs", "xenfs"
        ]
      }
    }
  }
}
```

## Why Each Category Matters

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 20px 0;">
<div>

### Virtual/Pseudo File Systems
- **proc, sysfs, devpts**: Kernel interfaces
- **cgroup, cgroup2**: Container management
- **tmpfs, ramfs**: Memory-based storage

### Network File Systems
- **nfs, nfs4, cifs, smb**: Network latency issues
- **efs, fsx**: AWS managed (separate monitoring)
- **s3fs, goofys**: Object storage FUSE mounts

</div>
<div>

### Container/Overlay Systems
- **overlay, overlay2**: Docker/container layers
- **aufs, devicemapper**: Legacy storage drivers
- **loop***: Loopback devices

### Cloud Provider Utilities
- **amazon-efs-client-utils**: AWS service mounts
- **amazon-ssm-agent**: SSM agent mounts
- **mountpoint-s3**: AWS S3 FUSE driver

</div>
</div>

## Real-World Benefits

<div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 15px; margin: 20px 0;">
<div>

### 🚀 Performance
- 80% reduction in overhead
- Faster metric collection
- Lower CPU/memory usage

</div>
<div>

### 💰 Cost Reduction
- Fewer CloudWatch metrics
- Less API calls
- Reduced data transfer

</div>
<div>

### 🎯 Better Alerting
- Focused notifications
- No false positives
- Cleaner dashboards

</div>
</div>

## Implementation Best Practices

### 1. Start with the Complete Filter
Use the comprehensive list above as your baseline - it covers virtually all irrelevant file system types across different environments.

### 2. Validate Your Environment
```bash
# Check what file systems are currently mounted
df -T

# Verify only relevant file systems remain after filtering
# Should typically see: ext4, xfs, btrfs for real storage
```

### 3. Monitor the Right Metrics
```json
{
  "disk": {
    "measurement": ["used_percent", "inodes_used"],
    "metrics_collection_interval": 300,
    "ignore_file_system_types": [/* your filter list */]
  }
}
```

### 4. Test Before Production
Deploy the configuration in a test environment first to ensure you're not accidentally filtering legitimate storage.

## Common Scenarios

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 20px 0;">
<div>

### Container Environments
Essential for Docker/Kubernetes:
- **Before**: Dozens of overlay mounts
- **After**: Only host storage monitored

### Multi-Mount Systems
Servers with network mounts:
- **Before**: NFS timeouts cause delays
- **After**: Reliable local monitoring

</div>
<div>

### AWS Environments
Using EFS, FSx, or S3 mounts:
- **Before**: Duplicate monitoring overhead
- **After**: AWS services use native metrics

### What You'll Monitor
- Root file system (/, ext4/xfs)
- Data volumes (/data, /var)
- Application storage
- User directories (/home, /opt)

</div>
</div>

## Monitoring What Matters

After implementing file system filtering, you'll monitor only:

- **Root file system** (/, usually ext4/xfs)
- **Data volumes** (/data, /var, etc.)
- **Application storage** (database volumes, log directories)
- **User directories** (/home, /opt)

This focused approach provides:
- **Actionable alerts** when real storage fills up
- **Meaningful dashboards** showing actual capacity trends
- **Cost-effective monitoring** without unnecessary overhead

## Conclusion

File system filtering in CloudWatch agent is not optional - it's essential for production environments. The comprehensive filter list eliminates monitoring overhead while focusing on storage that actually matters for your applications.

By implementing this configuration, you'll achieve better performance, lower costs, and more reliable monitoring. Your future self (and your AWS bill) will thank you.

## Quick Implementation

```bash
# Update your CloudWatch agent config
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl \
  -a fetch-config -m ec2 -c file:/opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.json -s

# Verify the configuration
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl \
  -m ec2 -a query-config
```

Start filtering today and transform your CloudWatch monitoring from noisy to focused! 🎯