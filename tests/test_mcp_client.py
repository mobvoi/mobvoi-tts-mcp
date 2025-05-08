from mcp.server.fastmcp import FastMCPClient
import asyncio

async def main():
    # 创建 MCP 客户端
    client = FastMCPClient()
    
    # 首先列出所有可用的工具
    tools = await client.list_tools()
    print("可用的工具列表:", tools)
    
    # 调用 text_to_speech 工具
    result = await client.call_tool(
        "text_to_speech",
        {
            "text": "你好，这是一个测试",
            "speaker": "xiaoyi_meet",
            "audio_type": "mp3"
        }
    )
    print("转换结果:", result)

if __name__ == "__main__":
    asyncio.run(main())