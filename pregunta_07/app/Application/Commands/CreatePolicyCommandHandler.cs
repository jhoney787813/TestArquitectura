using CqrsMediatorApi.Application.ReadModels;
using CqrsMediatorApi.Domain.Entities;
using CqrsMediatorApi.Infrastructure.Persistence;
using MediatR;

namespace CqrsMediatorApi.Application.Commands;

public class CreatePolicyCommandHandler : IRequestHandler<CreatePolicyCommand, CreatePolicyResult>
{
    private readonly InMemoryDbContext _dbContext;

    public CreatePolicyCommandHandler(InMemoryDbContext dbContext)
    {
        _dbContext = dbContext;
    }

    public Task<CreatePolicyResult> Handle(CreatePolicyCommand request, CancellationToken cancellationToken)
    {
        // 1. Crear Entidad de Dominio (Write Model ACID)
        var policy = Policy.Create(request.PolicyType, request.InsuredName, request.InsuredEmail, request.Amount);
        
        // 2. Persistir en Write DB
        _dbContext.WriteDb[policy.PolicyId] = policy;

        // 3. Proyectar asíncronamente al Read Model (Eventual Consistency)
        var readModel = new PolicyReadModel(
            policy.PolicyId,
            $"Póliza de {policy.PolicyType} - {policy.InsuredName}",
            policy.Status.ToString().ToUpper(),
            policy.InsuredName,
            $"${policy.Amount:N2} USD",
            null,
            policy.UpdatedAt
        );
        _dbContext.ReadDb[policy.PolicyId] = readModel;

        var result = new CreatePolicyResult(
            "CREATED",
            policy.PolicyId,
            "Comando ejecutado exitosamente mediante MediatR en .NET 9.",
            Guid.NewGuid().ToString("N")[..8]
        );

        return Task.FromResult(result);
    }
}
