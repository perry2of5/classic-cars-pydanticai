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



Example run:

```
% uv run main.py 
Starting MySQL MCP server with config:
Host: 127.0.0.1
Port: 3306
User: someuser
Database: classicmodels
2025-04-26 17:31:09,488 - mysql_mcp_server - INFO - Starting MySQL MCP server...
2025-04-26 17:31:09,488 - mysql_mcp_server - INFO - Database config: 127.0.0.1/classicmodels as someuser
agent.run
2025-04-26 17:31:09,492 - mcp.server.lowlevel.server - INFO - Processing request of type ListToolsRequest
2025-04-26 17:31:09,492 - mysql_mcp_server - INFO - Listing tools...
2025-04-26 17:31:19,892 - mcp.server.lowlevel.server - INFO - Processing request of type ListToolsRequest
2025-04-26 17:31:19,892 - mysql_mcp_server - INFO - Listing tools...
2025-04-26 17:31:19,895 - mcp.server.lowlevel.server - INFO - Processing request of type ListToolsRequest
2025-04-26 17:31:19,895 - mysql_mcp_server - INFO - Listing tools...
2025-04-26 17:31:19,897 - mcp.server.lowlevel.server - INFO - Processing request of type ListToolsRequest
2025-04-26 17:31:19,897 - mysql_mcp_server - INFO - Listing tools...
2025-04-26 17:31:19,899 - mcp.server.lowlevel.server - INFO - Processing request of type CallToolRequest
2025-04-26 17:31:19,900 - mysql_mcp_server - INFO - Calling tool: execute_sql with arguments: {'query': 'SHOW CREATE TABLE classicmodels.orders;'}
2025-04-26 17:31:19,932 - mcp.server.lowlevel.server - INFO - Processing request of type CallToolRequest
2025-04-26 17:31:19,932 - mysql_mcp_server - INFO - Calling tool: execute_sql with arguments: {'query': 'SHOW CREATE TABLE classicmodels.orderdetails;'}
2025-04-26 17:31:19,938 - mcp.server.lowlevel.server - INFO - Processing request of type CallToolRequest
2025-04-26 17:31:19,938 - mysql_mcp_server - INFO - Calling tool: execute_sql with arguments: {'query': 'SHOW CREATE TABLE classicmodels.products;'}
2025-04-26 17:31:19,946 - mcp.server.lowlevel.server - INFO - Processing request of type ListToolsRequest
2025-04-26 17:31:19,946 - mysql_mcp_server - INFO - Listing tools...
2025-04-26 17:31:33,642 - mcp.server.lowlevel.server - INFO - Processing request of type ListToolsRequest
2025-04-26 17:31:33,643 - mysql_mcp_server - INFO - Listing tools...
2025-04-26 17:31:33,646 - mcp.server.lowlevel.server - INFO - Processing request of type CallToolRequest
2025-04-26 17:31:33,646 - mysql_mcp_server - INFO - Calling tool: execute_sql with arguments: {'query': 'SELECT p.productName, SUM(od.quantityOrdered) AS totalQuantitySold FROM orders o JOIN orderdetails od ON o.orderNumber = od.orderNumber JOIN products p ON od.productCode = p.productCode WHERE MONTH(o.orderDate) = 12 AND YEAR(o.orderDate) BETWEEN 2019 AND 2023 GROUP BY p.productName ORDER BY totalQuantitySold DESC LIMIT 10'}
2025-04-26 17:31:33,662 - mcp.server.lowlevel.server - INFO - Processing request of type ListToolsRequest
2025-04-26 17:31:33,662 - mysql_mcp_server - INFO - Listing tools...
2025-04-26 17:31:40,907 - mcp.server.lowlevel.server - INFO - Processing request of type ListToolsRequest
2025-04-26 17:31:40,907 - mysql_mcp_server - INFO - Listing tools...
2025-04-26 17:31:40,910 - mcp.server.lowlevel.server - INFO - Processing request of type CallToolRequest
2025-04-26 17:31:40,910 - mysql_mcp_server - INFO - Calling tool: execute_sql with arguments: {'query': 'SELECT p.productName, SUM(od.quantityOrdered) AS totalQuantitySold\nFROM orders o JOIN orderdetails od ON o.orderNumber = od.orderNumber\nJOIN products p ON od.productCode = p.productCode\nWHERE MONTH(o.orderDate) = 12\nGROUP BY p.productName\nORDER BY totalQuantitySold DESC LIMIT 10;'}
2025-04-26 17:31:40,928 - mcp.server.lowlevel.server - INFO - Processing request of type ListToolsRequest
2025-04-26 17:31:40,928 - mysql_mcp_server - INFO - Listing tools...
Here is a table showing the top 10 products sold in December:

| Rank | Product Name                                      | Total Quantity Sold |
|------|---------------------------------------------------|---------------------|
| 1    | 1992 Ferrari 360 Spider red                       | 153                 |
| 2    | 1970 Dodge Coronet                                | 141                 |
| 3    | ATA: B757-300                                     | 131                 |
| 4    | F/A 18 Hornet 1/72                                | 125                 |
| 5    | 1957 Chevy Pickup                                 | 124                 |
| 6    | 1928 Ford Phaeton Deluxe                          | 116                 |
| 7    | 1958 Chevy Corvette Limited Edition               | 114                 |
| 8    | American Airlines: B767-300                       | 107                 |
| 9    | Diamond T620 Semi-Skirted Tanker                 | 105                 |
| 10   | 1998 Chrysler Plymouth Prowler                   | 102                 |

This table shows which products are most commonly sold in December based on the quantity sold.
```