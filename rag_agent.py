import asyncio
from beeai_framework.agents.requirement import RequirementAgent
from beeai_framework.backend import ChatModel
from beeai_framework.memory import UnconstrainedMemory
from beeai_framework.tools.search.wikipedia import WikipediaTool
from beeai_framework.tools.weather import OpenMeteoTool
from beeai_framework.tools.handoff import HandoffTool
from beeai_framework.tools.think import ThinkTool
from beeai_framework.logger import Logger

async def main():
    # Initialize logger
    logger = Logger("multi-agent-system", level="TRACE")
    logger.info("Starting multi-agent system")

    # Create specialized agents
    logger.debug("Creating knowledge agent")
    knowledge_agent = RequirementAgent(
        llm=ChatModel.from_name("ollama:granite3.3"),
        tools=[ThinkTool(), WikipediaTool()],
        memory=UnconstrainedMemory(),
        instructions="Provide detailed, accurate information using available knowledge sources. Think through problems step by step."
    )

    logger.debug("Creating weather agent")
    weather_agent = RequirementAgent(
        llm=ChatModel.from_name("ollama:granite3.3"),
        tools=[ThinkTool(), OpenMeteoTool()],
        memory=UnconstrainedMemory(),
        instructions="Provide comprehensive weather information and forecasts. Always think before using tools."
    )

    # Create a coordinator agent that manages handoffs
    logger.debug("Creating coordinator agent")
    coordinator_agent = RequirementAgent(
        llm=ChatModel.from_name("ollama:granite3.3"),
        memory=UnconstrainedMemory(),
        tools=[
            HandoffTool(
                target=knowledge_agent,
                name="knowledge_specialist",
                description="For general knowledge and research questions"
            ),
            HandoffTool(
                target=weather_agent,
                name="weather_expert",
                description="For weather-related queries"
            ),
        ],
        instructions="""You coordinate between specialist agents.
        - For weather queries: use weather_expert
        - For research/knowledge questions: use knowledge_specialist
        - For mixed queries: break them down and use multiple specialists

        Always introduce yourself and explain which specialist will help."""
    )

    logger.info("Running query: What's the weather in Paris and tell me about its history?")
    try:
        response = await coordinator_agent.run("What's the weather in Paris and tell me about its history?")
        logger.info("Query completed successfully")
        print(response.last_message.text)
        
        # Print full response details for debugging
        if hasattr(response, 'state') and hasattr(response.state, 'steps'):
            logger.debug(f"Response had {len(response.state.steps)} steps")
            for i, step in enumerate(response.state.steps):
                tool_name = step.tool.name if step.tool else 'no tool'
                error_msg = step.error.explain() if step.error else None
                logger.debug(f"Step {i}: {tool_name} - Error: {error_msg}")
                if step.error:
                    logger.warning(f"Step {i} had error: {error_msg}")
    except Exception as e:
        logger.error(f"Error during agent execution: {e}", exc_info=True)
        raise

    logger.info("Multi-agent system execution completed")

if __name__ == "__main__":
    asyncio.run(main())