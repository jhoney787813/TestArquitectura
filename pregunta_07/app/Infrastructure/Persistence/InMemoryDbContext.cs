using System.Collections.Concurrent;
using CqrsMediatorApi.Application.ReadModels;
using CqrsMediatorApi.Domain.Entities;

namespace CqrsMediatorApi.Infrastructure.Persistence;

public class InMemoryDbContext
{
    // Write Database (Modelo de Dominio Normalizado 3NF)
    public ConcurrentDictionary<string, Policy> WriteDb { get; } = new();

    // Read Database (Proyecciones Denormalizadas DTO - Read Replica / Redis)
    public ConcurrentDictionary<string, PolicyReadModel> ReadDb { get; } = new();
}
