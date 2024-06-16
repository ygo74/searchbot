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
    internal class DisplayPrompt(ILogger logger) : IPromptRenderFilter
    {

        private readonly ILogger _logger = logger;

        public async Task OnPromptRenderAsync(PromptRenderContext context, Func<PromptRenderContext, Task> next)
        {
            // Example: get function information
            var functionName = context.Function.Name;

            await next(context);

            _logger.LogInformation(context.RenderedPrompt);
        }
    }
#pragma warning restore SKEXP0001
}
