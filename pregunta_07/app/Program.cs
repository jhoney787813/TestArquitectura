using CqrsMediatorApi.Application.Behaviors;
using CqrsMediatorApi.Application.Common.Exceptions;
using CqrsMediatorApi.Infrastructure.Persistence;
using FluentValidation;
using MediatR;
using Microsoft.AspNetCore.Diagnostics;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container (.NET 9 Web API)
builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();

// Register In-Memory Persistence Context
builder.Services.AddSingleton<InMemoryDbContext>();

// Register MediatR 12.0 in .NET 9
builder.Services.AddMediatR(cfg =>
{
    cfg.RegisterServicesFromAssembly(typeof(Program).Assembly);
    cfg.AddBehavior(typeof(IPipelineBehavior<,>), typeof(LoggingBehavior<,>));
    cfg.AddBehavior(typeof(IPipelineBehavior<,>), typeof(ValidationBehavior<,>));
});

// Register FluentValidation Validators
builder.Services.AddValidatorsFromAssembly(typeof(Program).Assembly);

var app = builder.Build();

// Global Exception Handler Middleware (RFC 7807 ProblemDetails)
app.UseExceptionHandler(errorApp =>
{
    errorApp.Run(async context =>
    {
        var exceptionHandlerFeature = context.Features.Get<IExceptionHandlerFeature>();
        if (exceptionHandlerFeature != null)
        {
            var ex = exceptionHandlerFeature.Error;
            if (ex is ValidationDomainException valEx)
            {
                context.Response.StatusCode = StatusCodes.Status422UnprocessableEntity;
                context.Response.ContentType = "application/problem+json";
                await context.Response.WriteAsJsonAsync(new
                {
                    type = "https://api.seguros.com/errors/validation_failed",
                    title = "Falla de Validacion en Pipeline Behavior",
                    status = 422,
                    detail = valEx.Message,
                    errors = valEx.Errors,
                    trace_id = Guid.NewGuid().ToString("N")[..8]
                });
            }
            else if (ex is KeyNotFoundException knfEx)
            {
                context.Response.StatusCode = StatusCodes.Status404NotFound;
                context.Response.ContentType = "application/problem+json";
                await context.Response.WriteAsJsonAsync(new
                {
                    type = "https://api.seguros.com/errors/resource_not_found",
                    title = "Recurso no encontrado",
                    status = 404,
                    detail = knfEx.Message
                });
            }
            else
            {
                context.Response.StatusCode = StatusCodes.Status500InternalServerError;
                await context.Response.WriteAsJsonAsync(new
                {
                    title = "Internal Server Error",
                    status = 500,
                    detail = ex.Message
                });
            }
        }
    });
});

app.MapControllers();

// Health Check Endpoint
app.MapGet("/health", (InMemoryDbContext db) => new
{
    status = "UP",
    framework = ".NET 9.0 (ASP.NET Core Web API)",
    architecture = "CQRS + MediatR 12.0 Pipeline Behaviors",
    write_db_records = db.WriteDb.Count,
    read_db_records = db.ReadDb.Count
});

app.Run();
