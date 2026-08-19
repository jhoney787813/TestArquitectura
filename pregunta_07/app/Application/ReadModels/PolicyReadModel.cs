namespace CqrsMediatorApi.Application.ReadModels;

public record PolicyReadModel(
    string Id,
    string DisplayTitle,
    string Status,
    string Insured,
    string AmountFormatted,
    string? PaymentRef,
    DateTime UpdatedAt
);
