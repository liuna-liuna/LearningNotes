#
# This script is to disable Chrome AutoUpdate by add items into registry
#
#
# to run this script:
# powershell set-executionpolicy remotesigned
# powershell -File C:\4install\DisableChromeAutoUpdate.ps1
#
[System.Console]::writeline('[Info] Kill GoogleUpdate')
Stop-Process -Force -ProcessName GoogleUpdate -ErrorAction SilentlyContinue

[Environment]::SetEnvironmentVariable("DisableChromeAutoupdate", "true", "Process")
if ($env:DisableChromeAutoupdate -eq 'true'){
    [System.Console]::writeline('[Info] Disable chrome autoupdate')
    if (-Not(Test-Path HKLM:\SOFTWARE\Policies\Google)) {
        New-Item -Path HKLM:\SOFTWARE\Policies\Google
    }
    if (-Not(Test-Path HKLM:\SOFTWARE\Policies\Google\Update)) {
        New-Item -Path HKLM:\SOFTWARE\Policies\Google\Update
    }
    New-ItemProperty -Force -Path HKLM:\SOFTWARE\Policies\Google\Update -Name AutoUpdateCheckPeriodMinutes -PropertyType DWord -Value 0
    New-ItemProperty -Force -Path HKLM:\SOFTWARE\Policies\Google\Update -Name UpdateDefault -PropertyType DWord -Value 0
    
    if((Get-Process GoogleUpdate -ErrorAction SilentlyContinue) -ne $null) {
        [System.Console]::writeline('[Info] Kill GoogleUpdate')
        Stop-Process -Force -ProcessName GoogleUpdate -ErrorAction SilentlyContinue
    }
    if((Get-Process chromedriver -ErrorAction SilentlyContinue) -ne $null)  {
        [System.Console]::writeline('[Info] Kill chromedriver')
        Stop-Process -Force -ProcessName chromedriver -ErrorAction SilentlyContinue
    }
    if((Get-Process chrome -ErrorAction SilentlyContinue) -ne $null)  {
        [System.Console]::writeline('[Info] Kill chrome')
        Stop-Process -Force -ProcessName chrome -ErrorAction SilentlyContinue
    } 
    if(Test-Path ${env:ProgramFiles(x86)}\Google\Update) {
        [System.Console]::writeline('[Info] Delete Folder ProgramFiles(x86)\Google\Update')
        Remove-Item ${env:ProgramFiles(x86)}\Google\Update -Recurse -Force -Confirm:$false
    }
    if(Test-Path $env:ProgramFiles\Chrome\Update) {
        [System.Console]::writeline('[Info] Delete Folder ProgramFiles\Chrome\Update')
        Remove-Item $env:ProgramFiles\Chrome\Update -Recurse -Force -Confirm:$false
    }   
}
[System.Console]::writeline('[Info] Done')