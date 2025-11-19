import asyncio
from beeai_framework.agents.requirement import RequirementAgent
from beeai_framework.agents.requirement.requirements.conditional import ConditionalRequirement
from beeai_framework.agents.experimental.requirements.ask_permission import AskPermissionRequirement
from beeai_framework.backend import ChatModel
from beeai_framework.tools.search.wikipedia import WikipediaTool
from beeai_framework.tools.weather import OpenMeteoTool
from beeai_framework.tools.think import ThinkTool
from beeai_framework.middleware.trajectory import GlobalTrajectoryMiddleware
from beeai_framework.tools import Tool
from beeai_framework.logger import Logger

async def main():
    logger = Logger("my-agent", level="TRACE")
    logger.info("Starting agent application")

    agent = RequirementAgent(
        llm=ChatModel.from_name("ollama:granite3.3"),
        role="friendly AI assistant",
        instructions="Be helpful and conversational in all your interactions. Use your tools to find accurate, current information.",
        tools=[WikipediaTool(), OpenMeteoTool(), ThinkTool()],
        requirements=[
            ConditionalRequirement(
                ThinkTool,
                force_at_step=1,
                force_after=Tool,
                consecutive_allowed=False
            ),
            AskPermissionRequirement([OpenMeteoTool])  # Ask before using weather API
        ]
    )
    logger.debug("About to process user message")
    response = await agent.run(
        "What's the weather in Paris?"
    )
    logger.info("Agent response generated")
    print(response.last_message.text)

if __name__ == "__main__":
    asyncio.run(main())