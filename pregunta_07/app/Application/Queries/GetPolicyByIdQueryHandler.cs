using CqrsMediatorApi.Application.ReadModels;
using CqrsMediatorApi.Infrastructure.Persistence;
using MediatR;

namespace CqrsMediatorApi.Application.Queries;

public class GetPolicyByIdQueryHandler : IRequestHandler<GetPolicyByIdQuery, PolicyReadModel>
{
    private readonly InMemoryDbContext _dbContext;

    public GetPolicyByIdQueryHandler(InMemoryDbContext dbContext)
    {
        _dbContext = dbContext;
    }

    public Task<PolicyReadModel> Handle(GetPolicyByIdQuery request, CancellationToken cancellationToken)
    {
        if (!_dbContext.ReadDb.TryGetValue(request.PolicyId, out var readModel))
            throw new KeyNotFoundException($"La póliza '{request.PolicyId}' no fue encontrada en la base de datos de lectura.");

        return Task.FromResult(readModel);
    }
}
