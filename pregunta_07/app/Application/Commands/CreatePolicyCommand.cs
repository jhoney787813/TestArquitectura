using MediatR;

namespace CqrsMediatorApi.Application.Commands;

public record CreatePolicyResult(
    string Status,
    string PolicyId,
    string Message,
    string TraceId
);

public record CreatePolicyCommand(
    string PolicyType,
    string InsuredName,
    string InsuredEmail,
    decimal Amount
) : IRequest<CreatePolicyResult>;
