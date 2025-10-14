"""
Supervisor Agent - Routes queries to specialized agents
"""
from typing import Dict, Any
from core.llm import llm_manager
from core.memory import memory_manager
from utils.prompts import SUPERVISOR_SYSTEM_PROMPT
from agents.rag_agent import rag_agent
from agents.search_agent import search_agent
from agents.code_agent import code_agent
from agents.tool_agent import tool_agent
from agents.chat_agent import chat_agent


class SupervisorAgent:
    """Main orchestrator that routes to specialized agents"""
    
    def __init__(self):
        self.llm = llm_manager.get_primary_llm()
        self.name = "Supervisor"
        
        # Map of available agents
        self.agents = {
            'RAG': rag_agent,
            'SEARCH': search_agent,
            'CODE': code_agent,
            'TOOL': tool_agent,
            'CHAT': chat_agent
        }
    
    def route_query(self, query: str, session_id: str = "default") -> str:
        """
        Determine which agent should handle the query
        
        Returns:
            Agent name(s) as comma-separated string
        """
        try:
            # Get conversation context
            history = memory_manager.get_context_string(session_id, last_n=2)
            
            # Create routing prompt
            if history:
                prompt = f"""{SUPERVISOR_SYSTEM_PROMPT}

Recent conversation:
{history}

Current Query: {query}

Which agent(s) should handle this?"""
            else:
                prompt = f"""{SUPERVISOR_SYSTEM_PROMPT}

Query: {query}

Which agent(s) should handle this?"""
            
            # Get routing decision
            response = self.llm.invoke(prompt)
            routing = response.content.strip().upper()
            
            # Validate routing
            valid_agents = ['RAG', 'SEARCH', 'CODE', 'TOOL', 'CHAT']
            selected_agents = [a.strip() for a in routing.split(',')]
            selected_agents = [a for a in selected_agents if a in valid_agents]
            
            if not selected_agents:
                # Default to CHAT if routing unclear
                return 'CHAT'
            
            return ','.join(selected_agents)
        
        except Exception as e:
            print(f"Routing error: {e}")
            return 'CHAT'
    
    def process(self, query: str, session_id: str = "default") -> Dict[str, Any]:
        """
        Main processing method
        
        Args:
            query: User query
            session_id: Session identifier
        
        Returns:
            Final response with answer and metadata
        """
        try:
            # Route to appropriate agent(s)
            routing = self.route_query(query, session_id)
            agent_names = routing.split(',')
            
            results = []
            
            # Execute each selected agent
            for agent_name in agent_names:
                if agent_name not in self.agents:
                    continue
                
                agent = self.agents[agent_name]
                
                # Call appropriate agent
                if agent_name == 'RAG':
                    result = agent.process(query)
                elif agent_name == 'SEARCH':
                    result = agent.process(query)
                elif agent_name == 'CODE':
                    result = agent.process(query)
                elif agent_name == 'TOOL':
                    result = agent.process(query)
                elif agent_name == 'CHAT':
                    result = agent.process(query, session_id)
                else:
                    continue
                
                results.append({
                    'agent': agent_name,
                    'result': result
                })
            
            # Synthesize results if multiple agents
            if len(results) == 1:
                final_answer = results[0]['result'].get('answer', '')
                sources = results[0]['result'].get('sources', [])
                citations = results[0]['result'].get('citations', {})
                agent_used = results[0]['agent']
            else:
                # Combine results from multiple agents
                answer_parts = []
                all_sources = []
                all_citations = {}
                agents_used = []
                
                for r in results:
                    agent_name = r['agent']
                    agents_used.append(agent_name)
                    result = r['result']
                    
                    if result.get('success'):
                        answer_parts.append(f"**[{agent_name} Agent]**\n{result.get('answer', '')}")
                        
                        if 'sources' in result:
                            all_sources.extend(result['sources'])
                        
                        if 'citations' in result:
                            all_citations.update(result['citations'])
                
                final_answer = "\n\n".join(answer_parts)
                sources = all_sources
                citations = all_citations
                agent_used = ", ".join(agents_used)
            
            # Save to memory
            memory_manager.add_message(session_id, query, final_answer)
            
            return {
                'success': True,
                'answer': final_answer,
                'sources': sources,
                'citations': citations,
                'agent_used': agent_used,
                'routing': routing
            }
        
        except Exception as e:
            return {
                'success': False,
                'answer': f"Error processing query: {str(e)}",
                'sources': [],
                'citations': {},
                'agent_used': 'ERROR',
                'routing': ''
            }


# Global instance
supervisor = SupervisorAgent()

