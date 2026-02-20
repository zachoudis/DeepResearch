# DeepResearch 🚀

An intelligent multi-agent research system that performs comprehensive web research on any topic, generates detailed reports, and delivers results via email. Built with modern LLM engineering practices and agent orchestration patterns.

## 🎯 Overview

DeepResearch is a production-ready research automation platform that leverages multiple specialized AI agents working in coordination to:
- Generate clarifying questions to refine user queries
- Plan and execute parallel web searches
- Synthesize findings into comprehensive reports
- Deliver results via formatted email

## 🏗️ Architecture

### Multi-Agent System Design

The system implements a **hierarchical agent orchestration pattern** where specialized agents handle distinct responsibilities:

```
User Query
    ↓
Query Optimizer Agent → Optimized Query
    ↓
Questions Generator Agent → Clarifying Questions
    ↓
User Answers → Enriched Query
    ↓
Planner Agent → Search Plan (5 parallel searches)
    ↓
Search Agents (parallel) → Search Results
    ↓
Writer Agent → Comprehensive Report
    ↓
Email Agent → Formatted Email Delivery
```

### Agent Components

1. **Query Optimizer Agent** - Refines and enhances user queries for better research outcomes
2. **Questions Generator Agent** - Generates contextual clarifying questions using structured outputs
3. **Planner Agent** - Creates strategic search plans with reasoning for each search term
4. **Search Agent** - Performs web searches with tool use and summarizes results
5. **Writer Agent** - Synthesizes research into comprehensive markdown reports
6. **Email Agent** - Formats and delivers reports via email using function calling

## 🛠️ Key AI/LLM Engineering Techniques

### 1. **Structured Outputs with Pydantic**
- **Type-safe agent responses** using Pydantic models
- **Guaranteed schema compliance** for downstream processing
- **Automatic validation** of agent outputs

```python
class Questions(BaseModel):
    questions: list[Question] = Field(description="A list of meaningful questions")

questions_generator_agent = Agent(
    output_type=Questions,  # Enforces structured output
    ...
)
```

### 2. **Function Calling / Tool Use**
- **WebSearchTool** integration for real-time web search capabilities
- **Custom function tools** for email delivery
- **Tool choice control** via `ModelSettings(tool_choice="required")`

```python
search_agent = Agent(
    tools=[WebSearchTool(search_context_size="low")],
    model_settings=ModelSettings(tool_choice="required"),
)
```

### 3. **Async Agent Orchestration**
- **Concurrent agent execution** using `asyncio` for parallel searches
- **Async generators** for streaming responses
- **Non-blocking I/O** throughout the pipeline

```python
async def perform_searches(self, search_plan: WebSearchPlan):
    tasks = [asyncio.create_task(self.search(item)) for item in search_plan.searches]
    for task in asyncio.as_completed(tasks):
        result = await task
        # Process results as they complete
```

### 4. **Streaming Responses**
- **Real-time status updates** via async generators
- **Progressive UI updates** in Gradio interface
- **User feedback** during long-running operations

```python
async def run_full(self, query: str):
    yield "Starting research..."
    search_plan = await self.plan_searches(query)
    yield "Searches planned, starting to search..."
    # Stream updates throughout the process
```

### 5. **Observability & Tracing**
- **Distributed tracing** with OpenAI trace IDs
- **End-to-end request tracking** across agent calls
- **Debugging and monitoring** capabilities

```python
trace_id = gen_trace_id()
with trace("Research trace", trace_id=trace_id):
    # All agent calls within this context are traced
    print(f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}")
```

### 6. **Query Enrichment Pattern**
- **Multi-turn interaction** to gather context
- **Query refinement** through clarifying questions
- **Context accumulation** for improved agent performance

```python
enriched_query = f"""
    Main Topic: {query}
    Clarifications:
    Q1: {question1} A1: {answer1}
    Q2: {question2} A2: {answer2}
    Q3: {question3} A3: {answer3}
"""
```

### 7. **Error Handling & Resilience**
- **Graceful degradation** for failed searches
- **Exception handling** in parallel operations
- **Null-safe processing** of partial results

```python
try:
    result = await Runner.run(search_agent, input)
    return str(result.final_output)
except Exception:
    return None  # Continue with other searches
```

### 8. **Agent Prompt Engineering**
- **Role-based instructions** for each agent specialization
- **Context-aware prompts** with structured reasoning
- **Output format specifications** in agent instructions

### 9. **State Management**
- **Gradio State components** for multi-step workflows
- **UI state transitions** between query → questions → report
- **Persistent context** across user interactions

### 10. **Model Selection Strategy**
- **Cost optimization** using `gpt-4o-mini` for most tasks
- **Task-appropriate model selection** based on complexity
- **Balanced performance/cost** trade-offs

## 📦 Technology Stack

- **LLM Framework**: OpenAI Agents SDK (`openai-agents`)
- **Structured Outputs**: Pydantic
- **Web Framework**: Gradio (for interactive UI)
- **Async Runtime**: Python `asyncio`
- **Email Service**: SendGrid API
- **Web Search**: OpenAI WebSearchTool
- **Environment Management**: `python-dotenv`

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- OpenAI API key
- SendGrid API key (optional, for email functionality)

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd DeepResearch

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys
```

### Environment Variables

```env
OPENAI_API_KEY=your_openai_api_key
SENDGRID_API_KEY=your_sendgrid_api_key  # Optional
```

### Running the Application

```bash
python deep_research.py
```

The Gradio interface will launch in your browser at `http://127.0.0.1:7860`

## 💡 Usage Flow

1. **Enter Research Query**: User provides initial research topic
2. **Clarifying Questions**: System generates 3 contextual questions
3. **User Answers**: User provides answers to refine the query
4. **Research Execution**: 
   - Query optimization
   - Search planning (5 parallel searches)
   - Web search execution
   - Result synthesis
5. **Report Generation**: Comprehensive markdown report created
6. **Email Delivery**: Report sent via formatted email (optional)

## 🎓 LLM Engineering Best Practices Demonstrated

- ✅ **Separation of Concerns**: Each agent has a single, well-defined responsibility
- ✅ **Composability**: Agents can be combined and orchestrated flexibly
- ✅ **Type Safety**: Pydantic models ensure correct data structures
- ✅ **Observability**: Full tracing and logging for debugging
- ✅ **Error Handling**: Graceful failure handling in distributed systems
- ✅ **Performance**: Parallel execution for improved latency
- ✅ **User Experience**: Streaming updates and interactive workflows
- ✅ **Cost Optimization**: Efficient model selection and usage
- ✅ **Tool Integration**: Seamless integration with external APIs
- ✅ **Prompt Engineering**: Well-structured, role-based instructions

## 📊 System Capabilities

- **Parallel Search Execution**: Up to 5 concurrent web searches
- **Intelligent Query Planning**: Strategic search term generation with reasoning
- **Comprehensive Reporting**: 5-10 page detailed markdown reports
- **Real-time Updates**: Streaming status updates during research
- **Email Integration**: Automated report delivery
- **Interactive UI**: Multi-step workflow with state management

## 🔍 Technical Highlights

### Agent Orchestration Pattern
The `ResearchManager` class coordinates multiple agents, managing:
- Sequential dependencies (query → plan → search → write)
- Parallel execution (multiple searches simultaneously)
- Error recovery and partial results handling
- Streaming updates for user feedback

### Structured Data Flow
- **Input**: User query (string)
- **Intermediate**: Structured Pydantic models (Questions, WebSearchPlan, etc.)
- **Output**: Formatted markdown report + email

### Async/Await Patterns
- All agent calls are async for non-blocking execution
- Async generators enable streaming responses
- `asyncio.as_completed()` ensures optimal parallel processing

## 🎯 Use Cases

- Academic research assistance
- Market research and competitive analysis
- Technical documentation research
- News and current events analysis
- Product research and comparison

## 📝 Future Enhancements

- [ ] Support for multiple research sources (academic papers, news, etc.)
- [ ] Citation tracking and source attribution
- [ ] Customizable report formats
- [ ] Multi-language support
- [ ] Research history and caching
- [ ] Advanced query optimization techniques

## 🤝 Contributing

This is a portfolio project demonstrating LLM engineering practices. Contributions and feedback are welcome!

## 📄 License

[Your License Here]

## 👤 Author

Built as a portfolio project showcasing expertise in:
- Multi-agent system design
- LLM orchestration and prompt engineering
- Structured outputs and type safety
- Async programming patterns
- Production-ready AI applications

---

**Built with ❤️ for LLM Engineering**
