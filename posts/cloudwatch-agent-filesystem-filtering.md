---
title: "CloudWatch Agent: Why You Should Filter File System Types"
date: "2025-07-10"
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

<h3>🗂️ Virtual/Pseudo File Systems</h3>
<ul>
<li><strong>proc, sysfs, devpts</strong>: Kernel interfaces</li>
<li><strong>cgroup, cgroup2</strong>: Container management</li>
<li><strong>tmpfs, ramfs</strong>: Memory-based storage</li>
</ul>

<h3>🌐 Network File Systems</h3>
<ul>
<li><strong>nfs, nfs4, cifs, smb</strong>: Network latency issues</li>
<li><strong>efs, fsx</strong>: AWS managed (separate monitoring)</li>
<li><strong>s3fs, goofys</strong>: Object storage FUSE mounts</li>
</ul>

</div>
<div>

<h3>📦 Container/Overlay Systems</h3>
<ul>
<li><strong>overlay, overlay2</strong>: Docker/container layers</li>
<li><strong>aufs, devicemapper</strong>: Legacy storage drivers</li>
<li><strong>loop</strong>*: Loopback devices</li>
</ul>

<h3>☁️ Cloud Provider Utilities</h3>
<ul>
<li><strong>amazon-efs-client-utils</strong>: AWS service mounts</li>
<li><strong>amazon-ssm-agent</strong>: SSM agent mounts</li>
<li><strong>mountpoint-s3</strong>: AWS S3 FUSE driver</li>
</ul>

</div>
</div>

## Real-World Benefits

<div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 15px; margin: 20px 0;">
<div>

<h3>🚀 Performance</h3>
<ul>
<li>80% reduction in overhead</li>
<li>Faster metric collection</li>
<li>Lower CPU/memory usage</li>
</ul>

</div>
<div>

<h3>💰 Cost Reduction</h3>
<ul>
<li>Fewer CloudWatch metrics</li>
<li>Less API calls</li>
<li>Reduced data transfer</li>
</ul>

</div>
<div>

<h3>🎯 Better Alerting</h3>
<ul>
<li>Focused notifications</li>
<li>No false positives</li>
<li>Cleaner dashboards</li>
</ul>

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

<h3>🐳 Container Environments</h3>
Essential for Docker/Kubernetes:
<ul>
<li><strong>Before</strong>: Dozens of overlay mounts</li>
<li><strong>After</strong>: Only host storage monitored</li>
</ul>

<h3>🔗 Multi-Mount Systems</h3>
Servers with network mounts:
<ul>
<li><strong>Before</strong>: NFS timeouts cause delays</li>
<li><strong>After</strong>: Reliable local monitoring</li>
</ul>

</div>
<div>

<h3>☁️ AWS Environments</h3>
Using EFS, FSx, or S3 mounts:
<ul>
<li><strong>Before</strong>: Duplicate monitoring overhead</li>
<li><strong>After</strong>: AWS services use native metrics</li>
</ul>

<h3>🎯 What You'll Monitor</h3>
<ul>
<li>Root file system (/, ext4/xfs)</li>
<li>Data volumes (/data, /var)</li>
<li>Application storage</li>
<li>User directories (/home, /opt)</li>
</ul>

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