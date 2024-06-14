using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace kernel_internet_search.Configuration
{
    public class ConfigurationException : Exception
    {
        /// <inheritdoc />
        public ConfigurationException()
        {
        }

        /// <inheritdoc />
        public ConfigurationException(string? message) : base(message)
        {
        }

        /// <inheritdoc />
        public ConfigurationException(string? message, Exception? innerException) : base(message, innerException)
        {
        }
    }
}
