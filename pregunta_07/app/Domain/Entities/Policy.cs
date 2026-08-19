namespace CqrsMediatorApi.Domain.Entities;

public enum PolicyStatus
{
    Draft,
    Active,
    Cancelled
}

public class Policy
{
    public string PolicyId { get; private set; } = string.Empty;
    public string PolicyType { get; private set; } = string.Empty;
    public string InsuredName { get; private set; } = string.Empty;
    public string InsuredEmail { get; private set; } = string.Empty;
    public decimal Amount { get; private set; }
    public PolicyStatus Status { get; private set; }
    public string? PaymentReference { get; private set; }
    public DateTime CreatedAt { get; private set; }
    public DateTime UpdatedAt { get; private set; }

    private Policy() { }

    public static Policy Create(string policyType, string insuredName, string insuredEmail, decimal amount)
    {
        if (amount <= 0)
            throw new ArgumentException("El monto de la póliza debe ser mayor a cero.");

        if (!insuredEmail.Contains("@"))
            throw new ArgumentException("Formato de correo electrónico inválido.");

        var policyId = $"POL-NET9-{Guid.NewGuid().ToString("N")[..8].ToUpper()}";

        return new Policy
        {
            PolicyId = policyId,
            PolicyType = policyType.ToUpper(),
            InsuredName = insuredName,
            InsuredEmail = insuredEmail,
            Amount = amount,
            Status = PolicyStatus.Draft,
            CreatedAt = DateTime.UtcNow,
            UpdatedAt = DateTime.UtcNow
        };
    }

    public void Emit(string paymentReference)
    {
        if (Status == PolicyStatus.Active)
            throw new InvalidOperationException("La póliza ya se encuentra activa.");

        Status = PolicyStatus.Active;
        PaymentReference = paymentReference;
        UpdatedAt = DateTime.UtcNow;
    }
}
