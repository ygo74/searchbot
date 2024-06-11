Function Wait-KMDocumentIngestion
{
    [CmdletBinding(DefaultParameterSetName="Default")]
    param(
        [Parameter(ParameterSetName="Default", Position=1, Mandatory=$true, ValueFromPipeline=$false, ValueFromPipelineByPropertyName=$true)]
        [String]
        $DocumentId,

        [Parameter(ParameterSetName="Default", Position=2, Mandatory=$true, ValueFromPipeline=$false, ValueFromPipelineByPropertyName=$true)]
        [String]
        $Index,

        [Parameter(ParameterSetName="Default", Position=3, Mandatory=$true, ValueFromPipeline=$false, ValueFromPipelineByPropertyName=$true)]
        [String]
        $ServiceUri

    )

    Begin
    {
        $startFunction = Get-Date
        Trace-StartFunction -CommandName $MyInvocation.MyCommand.Name
    }
    End
    {
        $endFunction = Get-Date
        Trace-EndFunction -CommandName $MyInvocation.MyCommand.Name -Duration ($endFunction -$startFunction)
    }

    Process
    {

        $url = "$($ServiceUri)"
        if (!$url.EndsWith("/")) {$url += "/"}
        $url += ("upload-status?index={0}&documentId={1}" -f $Index, $DocumentId)

        While($True)
        {
            Trace-Message -Message ("Get Status for documentId {0} in index {1}" -f $DocumentId, $Index) -CommandName $MyInvocation.MyCommand.Name
            $result = Invoke-RestMethod -Method Get -Uri $url
            Trace-Message -Message ("Get Status for documentId {0} in index {1} : {2}" -f $DocumentId, $Index, $result.completed) `
                          -CommandName $MyInvocation.MyCommand.Name

            if ($result.completed)
            {
                break
            }
            Start-Sleep -Seconds 5
        }
    }
}