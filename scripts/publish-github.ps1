param(
    [string]$GithubUser = "izosi",
    [string]$RepoName = "IlunyaBrowser",
    [string]$Version = "1.0.0"
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Root

function Require-GhAuth {
    gh auth status *> $null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "GitHub CLI is not authenticated."
        Write-Host "Run: gh auth login"
        exit 1
    }
}

$ExePath = Join-Path $Root "dist\IlunyaBrowser.exe"
if (-not (Test-Path $ExePath)) {
    Write-Host "Building Windows executable..."
    & (Join-Path $Root "build.bat")
}

Require-GhAuth

if (-not (git rev-parse --is-inside-work-tree 2>$null)) {
    git init
}

if (-not (git config user.name)) {
    $Name = gh api user --jq .login
    git config user.name $Name
    git config user.email "$Name@users.noreply.github.com"
}

git add -A
if (-not (git diff --cached --quiet)) {
    git commit -m "Release v$Version"
}

$RemoteUrl = "https://github.com/$GithubUser/$RepoName.git"
if (-not (git remote get-url origin 2>$null)) {
    git branch -M main
    gh repo create "$GithubUser/$RepoName" --public --source=. --remote=origin --push
} else {
    git push -u origin main
}

git tag -a "v$Version" -m "Release v$Version" -f
git push origin "v$Version" -f

$ReleaseNotes = @"
## IlunyaBrowser v$Version

### Windows
Download **IlunyaBrowser.exe** below and run it.

### Linux (Arch)
```bash
yay -S ilunyabrowser
```

AUR: https://aur.archlinux.org/packages/ilunyabrowser
"@

gh release upload "v$Version" $ExePath --clobber 2>$null
if ($LASTEXITCODE -ne 0) {
    gh release create "v$Version" $ExePath `
        --title "IlunyaBrowser v$Version" `
        --notes $ReleaseNotes
} else {
    gh release edit "v$Version" --notes $ReleaseNotes
}

Write-Host ""
Write-Host "Done."
Write-Host "Repository: https://github.com/$GithubUser/$RepoName"
Write-Host "Release:    https://github.com/$GithubUser/$RepoName/releases/tag/v$Version"
Write-Host ""
Write-Host "Next: publish AUR package from packaging/aur/"
