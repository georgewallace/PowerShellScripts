$info=$(Invoke-WebRequest "https://docs.microsoft.com/en-us/azure/automation/troubleshoot/runbooks" -usebasicparsing).Content
write-output $info.Length.ToString()
