namespace CqrsMediatorApi.Application.Common.Exceptions;

public class ValidationDomainException : Exception
{
    public IDictionary<string, string[]> Errors { get; }

    public ValidationDomainException(string message) : base(message)
    {
        Errors = new Dictionary<string, string[]>();
    }

    public ValidationDomainException(IDictionary<string, string[]> errors) 
        : base("Ocurrieron una o más fallas de validación en la canalización MediatR.")
    {
        Errors = errors;
    }
}
