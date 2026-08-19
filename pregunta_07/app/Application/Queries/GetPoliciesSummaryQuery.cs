using CqrsMediatorApi.Application.ReadModels;
using MediatR;

namespace CqrsMediatorApi.Application.Queries;

public record GetPoliciesSummaryQuery(string? PolicyType) : IRequest<IEnumerable<PolicyReadModel>>;
