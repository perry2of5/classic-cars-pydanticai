import asyncio

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStdio
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

ollama_model = OpenAIModel(
    model_name='qwen2.5:14b-instruct', provider=OpenAIProvider(base_url='http://localhost:11434/v1')
)

dbmcp = MCPServerStdio(  
    'uvx',
    args=[
        '--from',
        'mysql-mcp-server',
        'mysql_mcp_server',
    ],
    env={
        "MYSQL_HOST":"127.0.0.1",
        "MYSQL_PORT":"3306",
        "MYSQL_USER":"someuser",
        "MYSQL_PASSWORD":"Password1!",
        "MYSQL_DATABASE":"classicmodels",    
    }
)

agent = Agent(ollama_model, mcp_servers=[dbmcp])


async def run():
    async with agent.run_mcp_servers():
        result = await agent.run(
            """
            Please do the following:
                1 access the classicmodels database containing the orders, orderdetails,
                and products tables and retrieve the schema.
                2 Use the schema to write a determine which 10 products are most commonly
                sold in December?
                3 run the query and present the top 10 products in a table
            """)
    print(result.output)

asyncio.run(run())