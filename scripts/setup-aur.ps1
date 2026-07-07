param(
    [string]$PubKeyPath = "$PSScriptRoot\..\.aur-deploy\aur.pub",
    [string]$AccountUrl = "https://aur.archlinux.org/account"
)

$pub = Get-Content $PubKeyPath -ErrorAction Stop
Write-Host ""
Write-Host "=== AUR direct install setup ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Open: $AccountUrl"
Write-Host "2. Log in or register an AUR account."
Write-Host "3. Paste this SSH public key into 'SSH Public Key':"
Write-Host ""
Write-Host $pub
Write-Host ""
Write-Host "4. Then run:"
Write-Host "   gh workflow run publish-aur.yml --repo ilunya100000/IlunyaBrowser"
Write-Host ""
Write-Host "After publish:"
Write-Host "   yay -S ilunyabrowser"
Write-Host ""

Start-Process $AccountUrl
