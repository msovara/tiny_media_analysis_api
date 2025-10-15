# PowerShell script to connect to Lengau
Write-Host "Connecting to Lengau cluster..."
Write-Host "You will be prompted for your password"
Write-Host ""

# Try to connect with X11 forwarding
ssh -X msovara@lengau.chpc.ac.za

Write-Host "Connection ended."





