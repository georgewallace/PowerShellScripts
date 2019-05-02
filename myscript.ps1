[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
$info=$(Invoke-WebRequest "https://docs.microsoft.com/en-us/azure/automation/troubleshoot/runbooks").Content
write-output $info.Length.ToString()
