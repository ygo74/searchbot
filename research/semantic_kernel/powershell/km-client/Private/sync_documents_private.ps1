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

function Invoke-InternalInventoryApiRequest
{
    [cmdletbinding(DefaultParameterSetName="Default")]
    param(

        [Parameter(ParameterSetName="ByUri",  Position=0, Mandatory=$true, ValueFromPipeline=$false, ValueFromPipelineByPropertyName=$false)]
        [String]
        $RelativeUri,

        [Parameter(ParameterSetName="Default",  Position=1, Mandatory=$false, ValueFromPipeline=$false, ValueFromPipelineByPropertyName=$false)]
        [Parameter(ParameterSetName="ByUri",  Position=1, Mandatory=$true, ValueFromPipeline=$false, ValueFromPipelineByPropertyName=$false)]
        [ValidateSet("GET","POST","PUT","DELETE","PATCH")]
        [String]
        $Method="GET",

        [Parameter(ParameterSetName="Default",  Position=2, Mandatory=$false, ValueFromPipeline=$true, ValueFromPipelineByPropertyName=$false)]
        [Parameter(ParameterSetName="ByUri",  Position=2, Mandatory=$false, ValueFromPipeline=$true, ValueFromPipelineByPropertyName=$false)]
        [PsObject]
        $InputObject
    )

    Begin
    {

        $ErrorActionPreference = "Stop"
        $watch = Trace-StartFunction -InvocationMethod $MyInvocation.MyCommand
        if ($PSCmdlet.ParameterSetName -eq "Default")
        {
            $uri = "{0}/{1}" -f $script:RestUri, $ControllerRoute
        }
        else
        {
            $uri = "{0}/{1}" -f $script:RestUri, $RelativeUri
        }
        # Get Authorization Header
        $headers = Get-InternalAuthorizationHeader


    }

    End
    {
        Trace-EndFunction -InvocationMethod $MyInvocation.MyCommand -watcher $watch
    }

    Process
    {
        try
        {

            $commandArgs = @{
                Method = $Method
                UseBasicParsing = $true
                ContentType = "application/json"
                Headers = $Headers
                Uri = $uri
            }

            if ($null -ne $InputObject)
            {
                if ($Method -eq "GET")
                {
                    throw "Unable to GET Uri with a request Body"
                }

                $body = $InputObject | ConvertTo-Json -Depth 5
                write-verbose ($body)

                if ($InputObject -is [System.Object[]])
                {
                    $nbElements = $InputObject.Count
                    if ($InputObject.Count -eq 1)
                    {
                        $body = "[$body]"
                    }

                }

                $commandArgs.Add("body", $body)
            }

            $result = Invoke-RestMethod @commandArgs

            # Check if we have a payload response
            $dataValue = $result | Get-Member -Name data -ErrorAction SilentlyContinue
            $errorsValue = $result | Get-Member -Name errors -ErrorAction SilentlyContinue

            if (($null -ne $dataValue) -and ($null -ne $errorsValue))
            {
                if ($result.errors.Count -gt 0)
                {
                    throw (ConvertFrom-InternalGraphqlErrors -Errors $result.errors)
                }
            }

            return $result

        }
        catch [System.Net.WebException]
        {
            if ($null -eq $_.Exception.Response)
            {
                throw $_
            }

            Trace-Message -Message "ERROR" -InvocationMethod $MyInvocation.MyCommand
            $errorMessage = $_.exception.Response | ConvertTo-Json
            Trace-Message -Message $errorMessage -InvocationMethod $MyInvocation.MyCommand
            $respStream = $_.Exception.Response.GetResponseStream()
            $reader = New-Object System.IO.StreamReader($respStream)
            $respBody = $reader.ReadToEnd()
            if (![string]::IsNullOrWhiteSpace($respBody))
            {
                $respBody = $respBody | ConvertFrom-Json
                Trace-Message -Message $respBody -InvocationMethod $MyInvocation.MyCommand
                $errorMessage = ConvertFrom-InternalRestApilErrors -Errors $respBody
                # foreach($resultErr in $respBody)
                # {
                #     # $errorMessage += "{0} - {1} : {2}`n" -f ($resultErr.path -join ","), $resultErr.message, $resultErr.extensions.message
                #     $errorMessage += "$resultErr`n"
                #     $errorMessage += "$($resultErr.errors)`n"

                # }
                Trace-Message -Message $errorMessage -InvocationMethod $MyInvocation.MyCommand
                throw $errorMessage
            }

            throw $_
        }
        catch
        {
            throw $_
        }
    }

}

function ConvertFrom-InternalRestApilErrors
{
    [CmdletBinding()]
    param(
        [Object[]]
        $Errors
    )


    $groupbyErrors = $Errors | Group-Object -Property title

    $Message = ""

    foreach($errorType in $groupbyErrors)
    {
        $status = $errorType.Group[0].status
        $detail = $errorType.Group[0].detail
        $title  = $errorType.Group[0].title

        $Message += "Http Error Code : {0} - {1}" -f $status, $title
        if (![string]::IsNullOrWhiteSpace($detail)) { $Message += " - {0}" -f $detail }
        foreach($errorMessage in $errorType.Group)
        {
            foreach($errorDetail in $errorMessage.errors)
            {
                # Get Error fields members
                $errorFields = $errorDetail | Get-Member -MemberType NoteProperty

                foreach($errorField in $errorFields)
                {
                    $errorFieldName = $errorField.Name
                    $Message += ("`r`n`t=> {0} - {1}" -f $errorFieldName, ($errorDetail.$errorFieldName -join ",") )
                }
            }
        }
    }

    $Message += "`r`n"

    $Message
}
