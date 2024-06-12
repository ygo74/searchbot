

Function Select-KMDocument
{
    [CmdletBinding(DefaultParameterSetName="Default")]
    param(
        [Parameter(ParameterSetName="Default", Position=0, Mandatory=$true, ValueFromPipeline=$false, ValueFromPipelineByPropertyName=$true)]
        [String]
        $Question,

        [Parameter(ParameterSetName="Default", Position=1, Mandatory=$true, ValueFromPipeline=$false, ValueFromPipelineByPropertyName=$true)]
        [String]
        $Index="index",

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
        $body = @{}
        $body["question"] = $Question
        $body["index"] = $Index

        $bodyJson = $body | ConvertTo-Json

        $url = "$($ServiceUri)"
        if (!$url.EndsWith("/")) {$url += "/"}
        $url += "ask"

        Trace-Message -Message "Start ask" -CommandName $MyInvocation.MyCommand.Name
        $result = Invoke-RestMethod -Method post -Uri $url -Body $bodyJson -ContentType "application/json"
        Trace-Message -Message "End ask" -CommandName $MyInvocation.MyCommand.Name
        if ($result.noResult)
        {
            Trace-Message -Message "No result" -CommandName $MyInvocation.MyCommand.Name
        }

        return $result
    }
}