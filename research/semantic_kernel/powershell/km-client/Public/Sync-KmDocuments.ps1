

Function Sync-KMDocument
{
    [CmdletBinding(DefaultParameterSetName="Default")]
    param(
        [Parameter(ParameterSetName="Default", Position=0, Mandatory=$true, ValueFromPipeline=$false, ValueFromPipelineByPropertyName=$true)]
        [String]
        $FilePath,

        [Parameter(ParameterSetName="Default", Position=1, Mandatory=$true, ValueFromPipeline=$false, ValueFromPipelineByPropertyName=$true)]
        [String]
        $DocumentId,

        [Parameter(ParameterSetName="Default", Position=2, Mandatory=$true, ValueFromPipeline=$false, ValueFromPipelineByPropertyName=$true)]
        [String]
        $Index="default",

        [Parameter(ParameterSetName="Default", Position=3, Mandatory=$false, ValueFromPipeline=$false, ValueFromPipelineByPropertyName=$true)]
        [String]
        $ServiceUri="http://localhost:9001"

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
        $formUpload = @{}
        $FormUpload["file1"] = Get-Item -Path $FilePath
        $FormUpload["documentId"] = $DocumentId
        $FormUpload["index"] = $Index


        $url = "$($ServiceUri)"
        if (!$url.EndsWith("/")) {$url += "/"}
        $url += "upload"

        Trace-Message -Message "Start upload" -CommandName $MyInvocation.MyCommand.Name
        $result = Invoke-WebRequest -Method post -Uri $url -Form $formUpload
        Trace-Message -Message "Upload status $($result.StatusCode)" -CommandName $MyInvocation.MyCommand.Name
        if ($result.StatusCode -ne 202)
        {
            Throw "Error during upload for file $FilePath"
        }

        # Wait for ingestion
        Wait-KMDocumentIngestion -DocumentId $DocumentId -Index $Index -ServiceUri $ServiceUri
    }
}