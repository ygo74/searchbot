param storageAccounts_salanguagepoc_name string = 'salanguagepoc'
param accounts_ls_poc_keyphrase_name string = 'ls-poc-keyphrase'
param searchServices_lspockeyphrase_asa3vvpn4h63x4o_name string = 'lspockeyphrase-asa3vvpn4h63x4o'

resource searchServices_lspockeyphrase_asa3vvpn4h63x4o_name_resource 'Microsoft.Search/searchServices@2023-11-01' = {
  name: searchServices_lspockeyphrase_asa3vvpn4h63x4o_name
  location: 'Switzerland North'
  sku: {
    name: 'free'
  }
  properties: {
    replicaCount: 1
    partitionCount: 1
    hostingMode: 'Default'
    publicNetworkAccess: 'Enabled'
    networkRuleSet: {
      ipRules: []
    }
    encryptionWithCmk: {}
    disableLocalAuth: false
    authOptions: {
      apiKeyOnly: {}
    }
    semanticSearch: 'disabled'
  }
}

resource storageAccounts_salanguagepoc_name_resource 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: storageAccounts_salanguagepoc_name
  location: 'switzerlandnorth'
  sku: {
    name: 'Standard_LRS'
    tier: 'Standard'
  }
  kind: 'Storage'
  properties: {
    minimumTlsVersion: 'TLS1_2'
    allowBlobPublicAccess: true
    networkAcls: {
      bypass: 'AzureServices'
      virtualNetworkRules: []
      ipRules: []
      defaultAction: 'Allow'
    }
    supportsHttpsTrafficOnly: true
    encryption: {
      services: {
        file: {
          keyType: 'Account'
          enabled: true
        }
        blob: {
          keyType: 'Account'
          enabled: true
        }
      }
      keySource: 'Microsoft.Storage'
    }
  }
}

resource storageAccounts_salanguagepoc_name_default 'Microsoft.Storage/storageAccounts/blobServices@2023-01-01' = {
  parent: storageAccounts_salanguagepoc_name_resource
  name: 'default'
  sku: {
    name: 'Standard_LRS'
    tier: 'Standard'
  }
  properties: {
    cors: {
      corsRules: [
        {
          allowedOrigins: [
            'https://language.cognitive.azure.com'
          ]
          allowedMethods: [
            'DELETE'
            'GET'
            'POST'
            'OPTIONS'
            'PUT'
          ]
          maxAgeInSeconds: 500
          exposedHeaders: [
            '*'
          ]
          allowedHeaders: [
            '*'
          ]
        }
      ]
    }
    deleteRetentionPolicy: {
      allowPermanentDelete: false
      enabled: false
    }
  }
}

resource Microsoft_Storage_storageAccounts_fileServices_storageAccounts_salanguagepoc_name_default 'Microsoft.Storage/storageAccounts/fileServices@2023-01-01' = {
  parent: storageAccounts_salanguagepoc_name_resource
  name: 'default'
  sku: {
    name: 'Standard_LRS'
    tier: 'Standard'
  }
  properties: {
    protocolSettings: {
      smb: {}
    }
    cors: {
      corsRules: []
    }
    shareDeleteRetentionPolicy: {
      enabled: true
      days: 7
    }
  }
}

resource Microsoft_Storage_storageAccounts_queueServices_storageAccounts_salanguagepoc_name_default 'Microsoft.Storage/storageAccounts/queueServices@2023-01-01' = {
  parent: storageAccounts_salanguagepoc_name_resource
  name: 'default'
  properties: {
    cors: {
      corsRules: []
    }
  }
}

resource Microsoft_Storage_storageAccounts_tableServices_storageAccounts_salanguagepoc_name_default 'Microsoft.Storage/storageAccounts/tableServices@2023-01-01' = {
  parent: storageAccounts_salanguagepoc_name_resource
  name: 'default'
  properties: {
    cors: {
      corsRules: []
    }
  }
}

resource accounts_ls_poc_keyphrase_name_resource 'Microsoft.CognitiveServices/accounts@2023-10-01-preview' = {
  name: accounts_ls_poc_keyphrase_name
  location: 'switzerlandnorth'
  sku: {
    name: 'F0'
  }
  kind: 'TextAnalytics'
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    apiProperties: {
      qnaAzureSearchEndpointId: searchServices_lspockeyphrase_asa3vvpn4h63x4o_name_resource.id
    }
    customSubDomainName: accounts_ls_poc_keyphrase_name
    networkAcls: {
      defaultAction: 'Allow'
      virtualNetworkRules: []
      ipRules: []
    }
    userOwnedStorage: [
      {
        resourceId: storageAccounts_salanguagepoc_name_resource.id
      }
    ]
    publicNetworkAccess: 'Enabled'
  }
}
