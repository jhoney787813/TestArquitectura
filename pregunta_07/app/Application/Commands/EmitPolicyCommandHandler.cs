using CqrsMediatorApi.Application.ReadModels;
using CqrsMediatorApi.Infrastructure.Persistence;
using MediatR;

namespace CqrsMediatorApi.Application.Commands;

public class EmitPolicyCommandHandler : IRequestHandler<EmitPolicyCommand, EmitPolicyResult>
{
    private readonly InMemoryDbContext _dbContext;

    public EmitPolicyCommandHandler(InMemoryDbContext dbContext)
    {
        _dbContext = dbContext;
    }

    public Task<EmitPolicyResult> Handle(EmitPolicyCommand request, CancellationToken cancellationToken)
    {
        if (!_dbContext.WriteDb.TryGetValue(request.PolicyId, out var policy))
            throw new KeyNotFoundException($"Póliza '{request.PolicyId}' no encontrada en el modelo de escritura.");

        // Ejecutar método de dominio
        policy.Emit(request.PaymentReference);

        // Actualizar Proyección Read Model
        if (_dbContext.ReadDb.TryGetValue(request.PolicyId, out var readModel))
        {
            _dbContext.ReadDb[request.PolicyId] = readModel with 
            { 
                Status = policy.Status.ToString().ToUpper(), 
                PaymentRef = request.PaymentReference,
                UpdatedAt = DateTime.UtcNow
            };
        }

        var result = new EmitPolicyResult(
            "EMITTED",
            policy.PolicyId,
            policy.Status.ToString().ToUpper(),
            Guid.NewGuid().ToString("N")[..8]
        );

        return Task.FromResult(result);
    }
}
