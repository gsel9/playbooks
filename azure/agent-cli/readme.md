# AI Agents

**Why Are AI agents useful?**
- Automation (routine tasks)
- Enhanced Decision-Making
- Scalability
- 24/7 Availability

Examples of use cases:
- Personal productivity
- Research
- Sales
- Customer service
- Developer

### Security risks of AI Agents
- Data Leakage and Privacy Exposure: AI agents often access sensitive business or user data to perform tasks.
- Prompt Injection and Manipulation Attacks: Malicious users can craft inputs that override an agent’s intended behavio
- Unauthorized Access and Privilege Escalation: Weak authentication or access controls
- Data Poisoning: Attackers may corrupt training or contextual data
- Supply Chain Vulnerabilities: Agents often rely on external APIs, plugins, or model endpoints, which expand the attack surface
- Over-Reliance on Autonomous Actions: Highly autonomous agents may execute unintended actions if not carefully constrained or validated.
- Inadequate Auditability and Logging: Without detailed logging, it’s difficult to trace actions or detect malicious behavior early.
- Model Inversion and Output Leakage: Attackers might exploit model outputs to infer sensitive data used during training or prompting.

**Mitigation Strategies**
To reduce these risks, developers should adopt a security-by-design approach that includes:
- Enforcing role-based access controls (RBAC) and least privilege permissions.
- Adding prompt filtering and validation layers to prevent injection attacks.
- Sandboxing or gating sensitive operations behind human-in-the-loop approvals.
- Maintaining comprehensive logging and traceability for all agent actions.
- Auditing third-party dependencies and integrations regularly.
- Continuously retraining and validating models to detect data drift or poisoning attempts.

## Setup

NOTE: Need to sign in to azure to run the app

1. Go to portal.azure: Click subscription -> resource groups -> create a new resource group for the agentic app resources
2. In portal.azure, create a Foundry resource attached to the agentic app resource group
3. Go to ai.azure and agentic app resource -> model catalog and deploy a gpt-4.1 base model
4. Go to portal.azure and open a terminal (PowerShell: settings -> classic version)

Minimal agent setup: A minimal configuration that includes Azure AI hub, Azure AI project, and Foundry Tools resources.

Standard agent setup: A more comprehensive configuration that includes the basic agent setup plus Azure Key Vault, Azure AI Search, and Azure Storage.

### Developing apps that use agents
High-level steps that you must implement in your code:
1. Connect to the AI Foundry project for your agent, using the project endpoint and Entra ID authentication.
2. Get a reference to an existing agent that you created in the Microsoft Foundry portal, or create a new one specifying:
    - The model deployment in the project that the agent should use to interpret and respond to prompts.
    - Instructions that determine the functionality and behavior of the agent.
    - Tools and resources that the agent can use to perform tasks.
3. Create a thread for a chat session with the agent. All conversations with an agent are conducted on a stateful thread that retains message history and data artifacts generated during the chat.
4. Add messages to the thread and invoke it with the agent.
5. Check the thread status, and when ready, retrieve the messages and data artifacts.
6. Repeat the previous two steps as a chat loop until the conversation can be concluded.
7. When finished, delete the agent and the thread to clean up the resources and delete data that is no longer required.

## Options for implementing custom tools
- Custom function
- Azure Functions
- OpenAPI specification tools
- Azure Logic Apps

#### Knowledge tools
Knowledge tools enhance the context or knowledge of your agent. Available tools include:
- Bing Search: Uses Bing search results to ground prompts with real-time live data from the web.
- File search: Grounds prompts with data from files in a vector store.
- Azure AI Search: Grounds prompts with data from Azure AI Search query results.
- Microsoft Fabric: Uses the Fabric Data Agent to ground prompts with data from your Fabric data stores.

#### Action tools
Action tools perform an action or run a function. Available tools include:
- Code Interpreter: A sandbox for model-generated Python code that can access and process uploaded files.
- Custom function: Call your custom function code – you must provide function definitions and implementations.
- Azure Function: Call code in serverless Azure Functions.
- OpenAPI Spec: Call external APIs based on the OpenAPI 3.0 spec.
By connecting built-in and custom tools, you can allow your agent to perform countless tasks on your behalf.
