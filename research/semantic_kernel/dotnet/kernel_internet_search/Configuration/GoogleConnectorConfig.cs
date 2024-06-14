using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace kernel_internet_search.Configuration
{
    internal class GoogleConnectorConfig
    {
        /// <summary>
        /// API key, required
        /// </summary>
        public string APIKey { get; set; } = string.Empty;

        /// <summary>
        /// SearchCenterConnectionId
        /// </summary>
        public string SearchCenterConnectionId { get; set; } = string.Empty;


    }
}
