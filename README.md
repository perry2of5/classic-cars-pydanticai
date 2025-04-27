This example shows how to use pydantic AI, qwen2.5:14b-instruct running in ollama, and the a (database of model classic cars sold)[https://github.com/amitkashyap121/MySQL_Database_Classic_Cars] in a mySQL DB.

To run, you need to run the qwen2.5:14b-instruct in ollama. 
```
ollama run qwen2.5:14b-instruct
```

Start the database in Docker.
```
docker-compose up -d
```

Then run main.py:
```
uv run main.py
```

The MySql MCP server is run using uvx. The Qwen model takes a little time even on my M4 Max, but it gets the right answer.

The classic cars DB is "borrowed" from 
[classic cars db](https://github.com/amitkashyap121/MySQL_Database_Classic_Cars)

