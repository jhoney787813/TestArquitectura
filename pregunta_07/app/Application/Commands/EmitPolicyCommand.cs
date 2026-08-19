using MediatR;

namespace CqrsMediatorApi.Application.Commands;

public record EmitPolicyResult(
    string Status,
    string PolicyId,
    string CurrentStatus,
    string TraceId
);

public record EmitPolicyCommand(
    string PolicyId,
    string PaymentReference
) : IRequest<EmitPolicyResult>;
