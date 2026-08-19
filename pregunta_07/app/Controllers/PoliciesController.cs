using CqrsMediatorApi.Application.Commands;
using CqrsMediatorApi.Application.Queries;
using MediatR;
using Microsoft.AspNetCore.Mvc;

namespace CqrsMediatorApi.Controllers;

[ApiController]
[Route("api/v1/[controller]")]
public class PoliciesController : ControllerBase
{
    private readonly IMediator _mediator;

    public PoliciesController(IMediator mediator)
    {
        _mediator = mediator;
    }

    // ✍️ COMMAND STACK (Escritura via MediatR Bus)
    [HttpPost("commands/create")]
    [ProducesResponseType(StatusCodes.Status201Created)]
    [ProducesResponseType(StatusCodes.Status422UnprocessableEntity)]
    public async Task<IActionResult> Create([FromBody] CreatePolicyCommand command)
    {
        var result = await _mediator.Send(command);
        return CreatedAtAction(nameof(GetById), new { policyId = result.PolicyId }, result);
    }

    [HttpPost("commands/emit")]
    [ProducesResponseType(StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    public async Task<IActionResult> Emit([FromBody] EmitPolicyCommand command)
    {
        var result = await _mediator.Send(command);
        return Ok(result);
    }

    // 📖 QUERY STACK (Lectura via MediatR Bus)
    [HttpGet("queries/{policyId}")]
    [ProducesResponseType(StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    public async Task<IActionResult> GetById(string policyId)
    {
        var query = new GetPolicyByIdQuery(policyId);
        var result = await _mediator.Send(query);
        return Ok(new { status = "SUCCESS", source = "READ_MODEL_PROJECTION", data = result });
    }

    [HttpGet("queries")]
    [ProducesResponseType(StatusCodes.Status200OK)]
    public async Task<IActionResult> GetSummary([FromQuery] string? policyType)
    {
        var query = new GetPoliciesSummaryQuery(policyType);
        var results = await _mediator.Send(query);
        return Ok(new { status = "SUCCESS", source = "READ_MODEL_PROJECTION", count = results.Count(), data = results });
    }
}
