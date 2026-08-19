using CqrsMediatorApi.Application.ReadModels;
using MediatR;

namespace CqrsMediatorApi.Application.Queries;

public record GetPolicyByIdQuery(string PolicyId) : IRequest<PolicyReadModel>;
