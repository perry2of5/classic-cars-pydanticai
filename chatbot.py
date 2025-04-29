import asyncio
from pydantic_ai.messages import ModelMessage, ModelRequest, ModelResponse, TextPart, UserPromptPart
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

instructions="""
            You are a data analyst for a company selling models of classic cars. Use the classicmodels database
            to answer questions. Keep answers short and to the point. If the question cannot be answered
            based on the database, say so. Do not guess.

            For queries which depend on knowing which month an order is in use the orderDate column in the 
            orders table.

            For queries asking about the cost of an order or the selling price of a product use the priceEach
            column of the orderdetails table.

            Understand the terms car, model car, car model, item, and product to refer to records the products table unless it is an
            item in an order in which case use the orderdetails table to determine the price.

            Use markdown to format answers. 

            All answers must be in solely English. If an answer is initially written in another language,
            translate the answer to english before displaying and do not display any text from the other
            language.

            Query the classicmodels database to answer each request. Only use data from the classicmodels
            database to answer requests.
            """

agent = Agent(model=ollama_model, mcp_servers=[dbmcp], instructions=instructions)

def gradio_to_ai_hist(history) -> list[ModelMessage]:
    model_history = []
    if history is not None:
        for gr_hist in history:
            if gr_hist['role'] == 'user':
                model_history.append(ModelRequest(
                    parts=[UserPromptPart(gr_hist['content'])],
                    instructions=instructions
                ))
            else:
                model_history.append(ModelResponse(
                    parts=[TextPart(content=gr_hist['content'])]
                ))
    return model_history


async def query_model_classic_car_db(message: str, history) -> str:
    async with agent.run_mcp_servers():
        print("processing: " + message)
        result = await agent.run(message, message_history=gradio_to_ai_hist(history))
    return result.output



import gradio as gr

demo = gr.ChatInterface(
    fn=query_model_classic_car_db, 
    type="messages"
)

async def launcher():
    demo.launch(share=False)

def main():
    asyncio.run(launcher())

if __name__ == "__main__":
    main()


