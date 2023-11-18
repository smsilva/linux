# 1. Connect using Cisco AnyConnect Client

# 2. Run PowerShell as Administrator

# 3. Get DNS Servers IPs
Get-DnsClientServerAddress -AddressFamily IPv4 | Select-Object -ExpandProperty ServerAddresses | Out-File -encoding ascii -FilePath \\wsl.localhost\Ubuntu\tmp\ips.txt

# 4. Get Search Domains
Get-DnsClientGlobalSetting | Select-Object -ExpandProperty SuffixSearchList | Out-File -encoding ascii -FilePath \\wsl.localhost\Ubuntu\tmp\nameservers.txt

# 5. Show Cisco AnyConnect Net Interfaces
Get-NetIPInterface | Where-Object {$_.InterfaceAlias -Match "Cisco AnyConnect"}

# 6. Set Metric to 6000 (For now, this command must be run manually after each connection)
Get-NetAdapter | Where-Object {$_.InterfaceDescription -Match "Cisco AnyConnect"} | Set-NetIPInterface -InterfaceMetric 6000

# 7. Go to WSL and run the script dns.sh

# 8. Restart WSL Service
Restart-Service WslService
