Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

$form = New-Object System.Windows.Forms.Form
$form.Size = New-Object System.Drawing.Size(300,300)

$enterButton = New-Object System.Windows.Forms.Button
$enterButton.Text = 'Enter'
$enterButton.DialogResult = [System.Windows.Forms.DialogResult]::OK
$enterButton.Location = New-Object System.Drawing.Point(75, 220)
$enterButton.Size = New-Object System.Drawing.Size(75, 25)
$form.AcceptButton = $enterButton
$form.Controls.Add($enterButton)

$cListBox = New-Object System.Windows.Forms.ListBox
$cListBox.Location = New-Object System.Drawing.Point(20, 20)
$cListBox.Size = New-Object System.Drawing.Size(75, 100)
$cListBox.Height = 200
$cListBox.SelectionMode = 'MultiExtended'

$dListBox = New-Object System.Windows.Forms.ListBox
$dListBox.Location = New-Object System.Drawing.Point(200, 20)
$dListBox.Size = New-Object System.Drawing.Size(75, 100)
$dListBox.Height = 200
$dListBox.SelectionMode = 'MultiExtended'

$bugData = Import-Csv -Path "$PSScriptRoot\..\testData\bugs.csv"
$devicesData = Import-Csv -Path "$PSScriptRoot\..\testData\devices.csv"
$testerDevices = Import-Csv -Path "$PSScriptRoot\..\testData\tester_device.csv"
$testers = Import-Csv -Path "$PSScriptRoot\..\testData\testers.csv"

$availCountries = ($testers.Country | Select-Object -Unique)
$availDevices = ($devicesData.Description | Select-Object -Unique)

$null = $cListBox.Items.AddRange($availCountries)
$null = $dListBox.Items.AddRange($availDevices)

$form.Controls.Add($cListBox)
$form.Controls.Add($dListBox)
$form.TopMost = $true

$result = $form.ShowDialog()
if ($result -eq [System.Windows.Forms.DialogResult]::OK)
{
    $outputResults = @{}

    $countries = $cListBox.SelectedItems
    $devices = $dListBox.SelectedItems

    # get all of the testers based on countries selected
    # seeds the hashtable search with tester experience
    $currentTesters = $testers | Where-Object { $countries -contains $PSItem.Country }
    $testerIdArr = @($currentTesters.testerId)
    $testerIdToName = @{}
    foreach ($t in $currentTesters)
    {
        $outputResults[$t.testerId] = 0
        $testerIdToName[$t.testerId] = $t.firstName
    }

    # get the associated device IDs based on selected devices
    $deviceIds = $devicesData | Where-Object { $devices -contains $PSItem.Description }
    $devArr = @($deviceIds.deviceId)
    
    # get the list of bugs made against chosen devices, associated with appropriate testers
    $allBugsCreated = $bugData | Where-Object { $devArr -contains $PSItem.DeviceId -and $testerIdArr -contains $PSItem.testerId }
    foreach ($bug in $allBugsCreated)
    {
        $outputResults[$bug.testerId] = $outputResults[$bug.testerId] + 1
    }

    $outputResults.GetEnumerator() | Sort Value -Descending | ForEach-Object {
        Write-Output "$($testerIdToName[$_.Key]) - $($_.Value)"
    }
}