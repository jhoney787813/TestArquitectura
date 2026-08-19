using CqrsMediatorApi.Application.ReadModels;
using CqrsMediatorApi.Infrastructure.Persistence;
using MediatR;

namespace CqrsMediatorApi.Application.Queries;

public class GetPoliciesSummaryQueryHandler : IRequestHandler<GetPoliciesSummaryQuery, IEnumerable<PolicyReadModel>>
{
    private readonly InMemoryDbContext _dbContext;

    public GetPoliciesSummaryQueryHandler(InMemoryDbContext dbContext)
    {
        _dbContext = dbContext;
    }

    public Task<IEnumerable<PolicyReadModel>> Handle(GetPoliciesSummaryQuery request, CancellationToken cancellationToken)
    {
        var items = _dbContext.ReadDb.Values.AsEnumerable();
        if (!string.IsNullOrEmpty(request.PolicyType))
        {
            items = items.Where(x => x.DisplayTitle.Contains(request.PolicyType, StringComparison.OrdinalIgnoreCase));
        }

        return Task.FromResult(items);
    }
}
