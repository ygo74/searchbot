using Microsoft.Extensions.Configuration;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace kernel_internet_search.Configuration
{
    public static class ConfigurationExtensions
    {
        public static IConfiguration BindSection(this IConfiguration configuration, string key, object instance)
        {
            configuration.GetSection(key).Bind(instance);
            return configuration;
        }

    }
}
