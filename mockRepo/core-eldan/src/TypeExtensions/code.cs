using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Hosting;

var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();
var projectName = System.Environment.GetEnvironmentVariable("PROJECTNAME");



app.MapGet("/", () => "Hello from project: " + projectName);

app.Run();
