using System.Diagnostics;
using MediatR;
using Microsoft.Extensions.Logging;

namespace CqrsMediatorApi.Application.Behaviors;

public class LoggingBehavior<TRequest, TResponse> : IPipelineBehavior<TRequest, TResponse>
    where TRequest : IRequest<TResponse>
{
    private readonly ILogger<LoggingBehavior<TRequest, TResponse>> _logger;

    public LoggingBehavior(ILogger<LoggingBehavior<TRequest, TResponse>> logger)
    {
        _logger = logger;
    }

    public async Task<TResponse> Handle(TRequest request, RequestHandlerDelegate<TResponse> next, CancellationToken cancellationToken)
    {
        var requestName = typeof(TRequest).Name;
        _logger.LogInformation("🔀 [MEDIATR BUS] Despachando {RequestName} en .NET 9", requestName);

        var stopwatch = Stopwatch.StartNew();
        var response = await next();
        stopwatch.Stop();

        _logger.LogInformation("✅ [MEDIATR SUCCESS] {RequestName} procesado exitosamente en {ElapsedMs} ms", requestName, stopwatch.ElapsedMilliseconds);
        return response;
    }
}
