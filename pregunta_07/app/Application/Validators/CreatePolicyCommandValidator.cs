using CqrsMediatorApi.Application.Commands;
using FluentValidation;

namespace CqrsMediatorApi.Application.Validators;

public class CreatePolicyCommandValidator : AbstractValidator<CreatePolicyCommand>
{
    public CreatePolicyCommandValidator()
    {
        RuleFor(x => x.PolicyType)
            .NotEmpty().WithMessage("El tipo de póliza es obligatorio.")
            .Must(type => new[] { "VIDA", "AUTO", "HOGAR", "SALUD" }.Contains(type.ToUpper()))
            .WithMessage("Tipo de póliza inválido. Permitidos: VIDA, AUTO, HOGAR, SALUD.");

        RuleFor(x => x.InsuredName)
            .NotEmpty().WithMessage("El nombre del asegurado es obligatorio.")
            .MinimumLength(3).WithMessage("El nombre del asegurado debe tener al menos 3 caracteres.");

        RuleFor(x => x.InsuredEmail)
            .NotEmpty().WithMessage("El correo electrónico es obligatorio.")
            .EmailAddress().WithMessage("El correo electrónico no tiene un formato válido.");

        RuleFor(x => x.Amount)
            .GreaterThan(0).WithMessage("El monto de la póliza debe ser estrictamente mayor a 0.");
    }
}
