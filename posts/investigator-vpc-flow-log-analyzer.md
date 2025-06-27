---
title: "investiGATOR: A Comprehensive AWS VPC Flow Log Analysis Tool"
date: "2025-06-27"
description: "A powerful Python tool that provides both CLI and web interfaces for analyzing AWS VPC Flow Logs, detecting security threats, and investigating network traffic patterns with intelligent WHOIS integration and automated discovery."
tags: ["aws", "vpc", "security", "python", "network-analysis", "flow-logs", "fastapi", "boto3"]
---

# investiGATOR: A Comprehensive AWS VPC Flow Log Analysis Tool

Network security in AWS requires deep visibility into traffic patterns, connection attempts, and potential threats. Manual analysis of VPC Flow Logs is time-consuming and error-prone. That's why I built **investiGATOR** - a comprehensive tool that transforms raw VPC Flow Log data into actionable security intelligence.

## 🎯 The Problem: VPC Flow Log Analysis at Scale

AWS VPC Flow Logs contain valuable security information, but analyzing them manually presents several challenges:

- **Volume Overload**: Production environments generate millions of flow log entries
- **Manual Correlation**: Connecting related events across time windows is tedious
- **Context Missing**: Raw IP addresses lack organizational context
- **Tool Fragmentation**: Multiple tools needed for different analysis types
- **Time-Intensive**: Security investigations take hours instead of minutes

## 🚀 The Solution: Intelligent Flow Log Analysis

investiGATOR addresses these challenges through:

### Comprehensive Analysis Engine

- **12 different analysis types** for thorough traffic investigation
- **Automated threat detection** for SSH brute force, data exfiltration, and lateral movement
- **Protocol intelligence** with human-readable protocol names
- **WHOIS integration** for automatic organization lookup

### Modern Interfaces

- **Web dashboard** with interactive results and calendar pickers
- **Command-line interface** for automation and scripting

### AWS Integration

- **Auto-discovery** of instance IPs, VPC CIDR blocks, and CloudWatch log groups
- **Multi-account support** with AWS profile integration
- **Intelligent log filtering** to focus on relevant traffic

## 🏗️ Architecture Overview

investiGATOR follows a modular, service-oriented architecture:

```python
# Core Architecture Components
ARCHITECTURE = {
    'cli_interface': {
        'argument_parser': 'Command-line argument handling',
        'configuration_builder': 'Config generation from args',
        'analysis_runner': 'Orchestrates analysis execution'
    },
    'web_interface': {
        'fastapi_app': 'Modern web API with FastAPI',
        'analysis_service': 'Web-based analysis orchestration',
        'result_processors': 'Structured data for web display'
    },
    'analysis_engine': {
        'traffic_analyzers': '12 specialized analysis modules',
        'protocol_utils': 'Protocol name resolution',
        'whois_integration': 'External IP organization lookup'
    },
    'aws_integration': {
        'instance_discovery': 'EC2 instance information retrieval',
        'log_group_finder': 'VPC Flow Log group auto-discovery',
        'log_downloader': 'CloudWatch Logs integration'
    }
}
```

## 💡 Analysis Types & Capabilities

### Security-Focused Analyses

**SSH Traffic Analysis:**

```python
# SSH inbound traffic analysis
def ssh_inbound_traffic(logs, config):
    """Detect SSH brute force attempts and successful connections"""
    results = defaultdict(int)
    
    for log in logs:
        if (log.get("dstaddr") in config["instance_ips"] and 
            log.get("dstport") == "22"):
            key = (log.get("srcaddr"), log.get("action"))
            results[key] += 1
    
    # Batch WHOIS lookup for external IPs
    whois_cache = _batch_whois_lookup(source_ips, config["vpc_cidr_prefix"])
    return format_results_with_context(results, whois_cache)
```

**External Traffic Monitoring:**

- **External inbound**: Identify incoming threats and reconnaissance
- **External outbound**: Detect data exfiltration and command & control
- **Top external flows**: Analyze highest volume external connections

**Sensitive Port Analysis:**

- **RDP (3389)**: Remote desktop connection attempts
- **Database ports**: SQL Server (1433), MySQL (3306), PostgreSQL (5432)
- **NoSQL databases**: MongoDB (27017), Redis (6379)
- **Search engines**: Elasticsearch (9200)

### Network Analysis Features

**Traffic Summarization:**

```python
def overall_traffic_summary(logs, config):
    """Analyze traffic by protocol and action"""
    results = defaultdict(int)
    
    for log in logs:
        key = (log.get("protocol"), log.get("action"))
        results[key] += 1
    
    # Convert protocol numbers to human-readable names
    formatted_results = [
        {
            "protocol": get_protocol_name(protocol),
            "action": action,
            "count": count
        }
        for (protocol, action), count in sorted_results
    ]
    return formatted_results
```

**Rejected Traffic Analysis:**

- Security group effectiveness monitoring
- Blocked connection attempt patterns
- Potential attack vector identification

## 🖥️ Web Interface Features

The modern web interface provides an intuitive dashboard for security teams:

### Interactive Analysis Dashboard

```python
@app.post("/api/analyze")
async def analyze_logs(
    profile: str = Form(...),
    instance_id: str = Form(...),
    region: Optional[str] = Form(None),
    start_time: str = Form("24h"),
    end_time: str = Form("now"),
    analysis: str = Form("all")
):
    """Run comprehensive VPC Flow Log analysis"""
    service = AnalysisService()
    return await service.run_analysis(request_data)
```

### Key Web Features

- **Calendar-based time selection** for precise time range analysis
- **Real-time processing updates** with progress indicators
- **JSON-formatted results** with syntax highlighting
- **Responsive design** that works on desktop, tablet, and mobile
- **AWS profile switching** for multi-account environments
- **Theme support** with light and dark modes

## 🔧 Implementation Highlights

### Intelligent WHOIS Integration

One of investiGATOR's key features is automatic organization lookup for external IP addresses:

```python
def _batch_whois_lookup(ips: Set[str], vpc_cidr_prefix: str) -> Dict[str, str]:
    """Batch WHOIS lookup for external IPs to reduce API calls"""
    external_ips = {ip for ip in ips if is_external_ip(ip, vpc_cidr_prefix)}
    return {ip: get_whois_info(ip)["org"] for ip in external_ips}
```

This provides immediate context about who owns external IP addresses, helping security teams quickly identify:

- Known cloud providers (AWS, Google, Cloudflare)
- Suspicious hosting providers
- Geographic regions of traffic sources
- Legitimate business partners vs. unknown entities

### Auto-Discovery Capabilities

investiGATOR automatically discovers AWS resources to minimize configuration:

```python
def get_instance_info(instance_id, region, profile):
    """Auto-discover instance IPs, VPC CIDR, and related resources"""
    ec2 = boto3.client('ec2', region_name=region)
    
    response = ec2.describe_instances(InstanceIds=[instance_id])
    instance = response['Reservations'][0]['Instances'][0]
    
    return {
        'private_ips': [instance['PrivateIpAddress']],
        'primary_ip': instance['PrivateIpAddress'],
        'vpc_id': instance['VpcId'],
        'vpc_cidr_prefix': get_vpc_cidr_prefix(instance['VpcId']),
        'region': region
    }
```

### Performance Optimizations

- **Streaming log processing** for large datasets
- **Batch WHOIS lookups** to minimize API calls
- **Intelligent caching** of AWS API responses
- **Parallel processing** for multi-threaded analysis

## 📊 Real-World Usage Examples

### Security Incident Investigation

```bash
# Investigate SSH brute force attempts
poetry run vpc-flow-investigator \
  --instance-id i-0123456789abcdef0 \
  --analysis ssh-inbound \
  --start-time 24h

# Results show:
# Source IP            Action     Organization          Count     
# -----------------------------------------------------------------
# 203.0.113.1         REJECT     Malicious Hosting     156       
# 198.51.100.2        REJECT     Unknown ISP           89        
# 192.0.2.3           ACCEPT     Corporate VPN         12        
```

### Data Exfiltration Detection

```bash
# Monitor external outbound connections
poetry run vpc-flow-investigator \
  --instance-id i-0123456789abcdef0 \
  --analysis external-outbound \
  --start-time 1w

# Identify unusual external connections that might indicate data exfiltration
```

### Compliance Auditing

```bash
# Analyze sensitive port access
poetry run vpc-flow-investigator \
  --instance-id i-0123456789abcdef0 \
  --analysis sensitive-ports \
  --start-time 1M

# Generate reports showing database access patterns for compliance
```

### Web Interface Analysis

The web interface provides the same powerful analysis with a modern UI:

1. **Select AWS profile** and target instance
2. **Choose time range** using calendar pickers
3. **Pick analysis type** or run comprehensive analysis
4. **View results** in structured, searchable format
5. **Export data** for further analysis or reporting

## 🛠️ Technical Implementation

### Modular Analyzer Architecture

Each analysis type is implemented as a specialized analyzer:

```python
class ExternalInboundAnalyzer(BaseAnalyzer):
    @staticmethod
    def analyze(logs: List[Dict[str, Any]], config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Analyze external inbound traffic with WHOIS context"""
        results = defaultdict(int)
        external_ips = set()
        
        for log in logs:
            if (log.get("dstaddr") in config["instance_ips"] and 
                not log.get("srcaddr", "").startswith(config["vpc_cidr_prefix"])):
                srcaddr = log.get("srcaddr", "unknown")
                key = (srcaddr, log.get("action", "unknown"))
                results[key] += 1
                external_ips.add(srcaddr)
        
        # Batch WHOIS lookups for performance
        whois_cache = {ip: get_whois_info(ip)["org"] for ip in external_ips}
        
        return format_structured_results(results, whois_cache)
```

### FastAPI Web Service

The web interface uses FastAPI for modern, async web service capabilities:

```python
class AnalysisService:
    async def run_analysis(self, request: AnalysisRequest) -> JSONResponse:
        """Complete analysis workflow with error handling"""
        try:
            # Build configuration from request
            config = ConfigurationBuilder.build_config(request)
            
            # Auto-discover AWS resources
            instance_info = InstanceInfoService.get_and_validate_instance_info(
                request.instance_id, request.region, request.profile
            )
            
            # Download and process logs
            log_file = LogDownloadService.download_and_validate_logs(config)
            logs = list(filter_logs(read_log_file(log_file), config))
            
            # Run analysis and return structured results
            results = AnalysisResultProcessor.process_logs(logs, config)
            return JSONResponse(content=results)
            
        except Exception as e:
            log_query_end(logger, query_id, False, error=str(e))
            raise HTTPException(status_code=500, detail=str(e))
```

## 🚀 Getting Started

### Quick Installation

```bash
# Clone the repository
git clone https://github.com/sam-fakhreddine/investiGATOR.git
cd investiGATOR

# Install with Poetry
poetry install

# Verify installation
poetry run vpc-flow-investigator --help
```

### Web Interface

```bash
# Start the web server
poetry run vpc-flow-web

# Open browser to http://localhost:8000
```

### Command Line Usage

```bash
# Basic analysis
poetry run vpc-flow-investigator --instance-id i-0123456789abcdef0

# Specific analysis type
poetry run vpc-flow-investigator \
  --instance-id i-0123456789abcdef0 \
  --analysis ssh-inbound \
  --start-time 24h

# Multi-account with custom time range
poetry run vpc-flow-investigator \
  --instance-id i-0123456789abcdef0 \
  --profile production \
  --start-time "2024-01-01T00:00:00" \
  --end-time "2024-01-02T00:00:00"
```

## 📈 Impact & Benefits

### Quantifiable Improvements

investiGATOR transforms security operations by providing:

- **Rapid Investigation**: Reduce analysis time from hours to minutes
- **Comprehensive Coverage**: 12 analysis types cover all major threat vectors
- **Contextual Intelligence**: WHOIS integration provides immediate threat context
- **Automated Discovery**: Zero-configuration AWS resource detection
- **Flexible Interfaces**: Both CLI and web options for different use cases

### Use Cases

**Security Teams:**

- Incident response and forensic analysis
- Threat hunting and proactive monitoring
- Brute force attack detection
- Data exfiltration investigation

**Network Engineers:**

- Traffic pattern analysis
- Bandwidth monitoring
- Service dependency mapping
- Performance troubleshooting

**Compliance Officers:**

- Access audit trails
- Sensitive port monitoring
- Traffic flow documentation
- Regulatory reporting

## 🔮 Future Enhancements

### Advanced Analytics

- **Machine learning integration** for anomaly detection
- **Behavioral analysis** to establish traffic baselines
- **Predictive threat modeling** based on historical patterns

### Extended Integration

- **Multi-cloud support** for hybrid environments
- **SIEM integration** with popular security platforms
- **Threat intelligence feeds** for enhanced context

### Enhanced Visualization

- **Interactive dashboards** with charts and graphs
- **Geographic mapping** of traffic sources
- **Timeline visualization** for incident reconstruction

## 🎉 Conclusion

investiGATOR represents a significant advancement in AWS VPC Flow Log analysis, transforming raw network data into actionable security intelligence. By combining comprehensive analysis capabilities with modern interfaces and intelligent automation, it enables security teams to respond faster and more effectively to network-based threats.

The tool's modular architecture, AWS integration, and dual interface approach make it suitable for both interactive investigation and automated security workflows. Whether you're investigating a security incident, conducting threat hunting, or performing compliance audits, investiGATOR provides the visibility and context needed for effective network security analysis.

## 🔗 Resources

- **Repository**: [github.com/sam-fakhreddine/investiGATOR](https://github.com/sam-fakhreddine/investiGATOR)
- **AWS VPC Flow Logs**: [AWS Documentation](https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs.html)
- **FastAPI Framework**: [fastapi.tiangolo.com](https://fastapi.tiangolo.com)
- **Poetry Dependency Management**: [python-poetry.org](https://python-poetry.org)

---

*Network security is only as good as your visibility. investiGATOR transforms VPC Flow Logs from data into intelligence.* 🔍
