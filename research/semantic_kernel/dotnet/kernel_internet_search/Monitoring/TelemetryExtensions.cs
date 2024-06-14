using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;
using OpenTelemetry;
using OpenTelemetry.Logs;
using OpenTelemetry.Metrics;
using OpenTelemetry.Resources;
using OpenTelemetry.Trace;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace kernel_internet_search.Monitoring
{
    public static class TelemetryExtensions
    {
        public static HostApplicationBuilder AddTelemetryService(
          this HostApplicationBuilder builder)
        {

            var resourceBuilder = ResourceBuilder
                .CreateDefault()
                .AddService("kernel_internet_search");

            using var traceProvider = Sdk.CreateTracerProviderBuilder()
                .SetResourceBuilder(resourceBuilder)
                .AddSource("Microsoft.SemanticKernel*")
                .AddSource("kernel_internet_search")
                .AddConsoleExporter()
                .Build();

            using var meterProvider = Sdk.CreateMeterProviderBuilder()
                .AddMeter("Microsoft.SemanticKernel*")
                .SetResourceBuilder(resourceBuilder)
                .AddConsoleExporter()
                .Build();

            builder.Services.AddSingleton<ILoggerFactory>(sp =>
            {
                return LoggerFactory.Create(logBuilder =>
                {
                    logBuilder.AddOpenTelemetry(options =>
                    {
                        options.SetResourceBuilder(resourceBuilder);
                        options.AddConsoleExporter();

                        options.IncludeFormattedMessage = true;
                        options.IncludeScopes = true;
                    });

                    logBuilder.SetMinimumLevel(LogLevel.Trace);
                });
            });

            builder.Services.AddOpenTelemetry()
                .WithTracing(otelBuilder =>
                {
                    otelBuilder.SetResourceBuilder(resourceBuilder);
                    otelBuilder.AddConsoleExporter();
                });



            return builder;
        }
    }
}
