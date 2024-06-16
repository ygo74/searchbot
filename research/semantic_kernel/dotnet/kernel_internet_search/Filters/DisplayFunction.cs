using Microsoft.Extensions.Logging;
using Microsoft.SemanticKernel;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace kernel_internet_search.Filters
{

#pragma warning disable SKEXP0001
    internal class DisplayFunction(ILoggerFactory loggerFactory) : IFunctionInvocationFilter
    {
        private readonly ILogger _logger = loggerFactory.CreateLogger<DisplayFunction>();

        public async Task OnFunctionInvocationAsync(FunctionInvocationContext context, Func<FunctionInvocationContext, Task> next)
        {
            // Perform some actions before function invocation
            var sb = new StringBuilder();
            foreach (var arg in context.Arguments)
            {
                sb.AppendLine($"{arg.Key} : {arg.Value}");
            }

            _logger.LogInformation("Call function {0}.{1} with arguments {2}", context.Function.PluginName, context.Function.Name, sb.ToString());

            await next(context);
            // Perform some actions after function invocation
            _logger.LogInformation("Result fromm function {0}.{1} : {2}", context.Function.PluginName, context.Function.Name, context.Result);
        }
    }
#pragma warning restore SKEXP0001
}
