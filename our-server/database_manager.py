import os
import mysql.connector
from mysql.connector import Error
import sqlite3
import json
from typing import Optional, Dict, Any, List
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self):
        # MySQL connection configurations
        self.mysql_configs = [
            {
                'host': '127.0.0.1',
                'port': 3306,
                'user': 'u-root',
                'password': 'p-105585',
                'charset': 'utf8mb4',
                'autocommit': True
            },
            {
                'host': '127.0.0.1',
                'port': 3306,
                'user': 'root',
                'password': '',
                'charset': 'utf8mb4',
                'autocommit': True
            },
            {
                'host': 'localhost',
                'port': 3306,
                'user': 'root',
                'password': '',
                'charset': 'utf8mb4',
                'autocommit': True
            }
        ]
        
        # Database configurations
        self.databases = {
            'admin': {
                'name': 'aimodel',
                'description': 'Admin Panel Database',
                'tables': ['users', 'settings', 'logs', 'backups']
            },
            'server': {
                'name': 'modelsraver',
                'description': 'Main Server Database',
                'tables': ['conversations', 'models', 'sessions', 'analytics', 'agents', 'providers']
            },
            'main': {
                'name': 'modelsraver',
                'description': 'Primary Database',
                'tables': ['users', 'agents', 'providers', 'conversations', 'sessions', 'analytics']
            }
        }
        
        # SQLite database for local storage
        self.sqlite_db = 'zombiecoder_ai.db'
        
    def get_mysql_connection(self, database: str = None) -> Optional[mysql.connector.MySQLConnection]:
        """Get MySQL connection for specified database"""
        for config in self.mysql_configs:
            try:
                connection_config = config.copy()
                if database:
                    connection_config['database'] = database
                    
                connection = mysql.connector.connect(**connection_config)
                logger.info(f"✅ MySQL connected to {database or 'server'} using {config['host']}:{config['port']}")
                return connection
                
            except Exception as e:
                logger.warning(f"⚠️ MySQL connection failed with {config['host']}:{config['port']}: {e}")
                continue
        
        logger.error("❌ All MySQL connection attempts failed")
        return None
    
    def get_sqlite_connection(self) -> Optional[sqlite3.Connection]:
        """Get SQLite connection for local storage"""
        try:
            os.makedirs('logs', exist_ok=True)
            
            connection = sqlite3.connect(self.sqlite_db)
            connection.row_factory = sqlite3.Row
            logger.info(f"✅ SQLite connected to {self.sqlite_db}")
            return connection
            
        except Exception as e:
            logger.error(f"❌ SQLite connection error: {e}")
            return None
    
    def test_connection(self, database_type: str = 'mysql', database: str = None) -> bool:
        """Test database connection"""
        if database_type == 'mysql':
            connection = self.get_mysql_connection(database)
            if connection:
                try:
                    cursor = connection.cursor()
                    cursor.execute("SELECT VERSION()")
                    version = cursor.fetchone()
                    logger.info(f"✅ MySQL Version: {version[0]}")
                    cursor.close()
                    connection.close()
                    return True
                except Exception as e:
                    logger.error(f"❌ MySQL test failed: {e}")
                    return False
        else:
            connection = self.get_sqlite_connection()
            if connection:
                try:
                    cursor = connection.cursor()
                    cursor.execute("SELECT sqlite_version()")
                    version = cursor.fetchone()
                    logger.info(f"✅ SQLite Version: {version[0]}")
                    cursor.close()
                    connection.close()
                    return True
                except Exception as e:
                    logger.error(f"❌ SQLite test failed: {e}")
                    return False
        return False
    
    # Agent Management
    def get_all_agents(self) -> List[Dict[str, Any]]:
        """Get all agents from database"""
        connection = self.get_mysql_connection('modelsraver')
        if not connection:
            return []
        
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT id, name, display_name, personality, model_preference, 
                       prompt_template, config, status, created_at, updated_at
                FROM agents 
                ORDER BY created_at DESC
            """)
            agents = cursor.fetchall()
            
            # Parse JSON fields
            for agent in agents:
                if agent.get('model_preference'):
                    try:
                        agent['model_preference'] = json.loads(agent['model_preference'])
                    except:
                        agent['model_preference'] = []
                
                if agent.get('config'):
                    try:
                        agent['config'] = json.loads(agent['config'])
                    except:
                        agent['config'] = {}
            
            cursor.close()
            connection.close()
            return agents
            
        except Exception as e:
            logger.error(f"❌ Error getting agents: {e}")
            return []
    
    def get_agent_by_id(self, agent_id: int) -> Optional[Dict[str, Any]]:
        """Get agent by ID"""
        connection = self.get_mysql_connection('modelsraver')
        if not connection:
            return None
        
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT id, name, display_name, personality, model_preference, 
                       prompt_template, config, status, created_at, updated_at
                FROM agents 
                WHERE id = %s
            """, (agent_id,))
            
            agent = cursor.fetchone()
            if agent:
                # Parse JSON fields
                if agent.get('model_preference'):
                    try:
                        agent['model_preference'] = json.loads(agent['model_preference'])
                    except:
                        agent['model_preference'] = []
                
                if agent.get('config'):
                    try:
                        agent['config'] = json.loads(agent['config'])
                    except:
                        agent['config'] = {}
            
            cursor.close()
            connection.close()
            return agent
            
        except Exception as e:
            logger.error(f"❌ Error getting agent {agent_id}: {e}")
            return None
    
    def create_agent(self, agent_data: Dict[str, Any]) -> bool:
        """Create new agent"""
        connection = self.get_mysql_connection('modelsraver')
        if not connection:
            return False
        
        try:
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO agents (name, display_name, personality, model_preference, 
                                  prompt_template, config, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                agent_data['name'],
                agent_data.get('display_name'),
                agent_data.get('personality'),
                json.dumps(agent_data.get('model_preference', [])),
                agent_data.get('prompt_template'),
                json.dumps(agent_data.get('config', {})),
                agent_data.get('status', 'active')
            ))
            
            connection.commit()
            cursor.close()
            connection.close()
            logger.info(f"✅ Agent created: {agent_data['name']}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error creating agent: {e}")
            return False
    
    def update_agent(self, agent_id: int, agent_data: Dict[str, Any]) -> bool:
        """Update agent"""
        connection = self.get_mysql_connection('modelsraver')
        if not connection:
            return False
        
        try:
            cursor = connection.cursor()
            cursor.execute("""
                UPDATE agents 
                SET name = %s, display_name = %s, personality = %s, 
                    model_preference = %s, prompt_template = %s, config = %s, 
                    status = %s, updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
            """, (
                agent_data['name'],
                agent_data.get('display_name'),
                agent_data.get('personality'),
                json.dumps(agent_data.get('model_preference', [])),
                agent_data.get('prompt_template'),
                json.dumps(agent_data.get('config', {})),
                agent_data.get('status', 'active'),
                agent_id
            ))
            
            connection.commit()
            cursor.close()
            connection.close()
            logger.info(f"✅ Agent updated: {agent_id}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error updating agent {agent_id}: {e}")
            return False
    
    def delete_agent(self, agent_id: int) -> bool:
        """Delete agent"""
        connection = self.get_mysql_connection('modelsraver')
        if not connection:
            return False
        
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM agents WHERE id = %s", (agent_id,))
            
            connection.commit()
            cursor.close()
            connection.close()
            logger.info(f"✅ Agent deleted: {agent_id}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error deleting agent {agent_id}: {e}")
            return False
    
    # Provider Management
    def get_all_providers(self) -> List[Dict[str, Any]]:
        """Get all providers from database"""
        connection = self.get_mysql_connection('modelsraver')
        if not connection:
            return []
        
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT id, name, type, api_url, api_key, config, status, created_at, updated_at
                FROM providers 
                ORDER BY created_at DESC
            """)
            providers = cursor.fetchall()
            
            # Parse JSON fields
            for provider in providers:
                if provider.get('config'):
                    try:
                        provider['config'] = json.loads(provider['config'])
                    except:
                        provider['config'] = {}
            
            cursor.close()
            connection.close()
            return providers
            
        except Exception as e:
            logger.error(f"❌ Error getting providers: {e}")
            return []
    
    def create_provider(self, provider_data: Dict[str, Any]) -> bool:
        """Create new provider"""
        connection = self.get_mysql_connection('modelsraver')
        if not connection:
            return False
        
        try:
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO providers (name, type, api_url, api_key, config, status)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                provider_data['name'],
                provider_data['type'],
                provider_data.get('api_url'),
                provider_data.get('api_key'),
                json.dumps(provider_data.get('config', {})),
                provider_data.get('status', 'active')
            ))
            
            connection.commit()
            cursor.close()
            connection.close()
            logger.info(f"✅ Provider created: {provider_data['name']}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error creating provider: {e}")
            return False
    
    # Conversation Management
    def save_conversation(self, user_id: int, agent_id: int, session_id: str, 
                         message: str, response: str, metadata: Dict[str, Any] = None) -> bool:
        """Save conversation to database"""
        connection = self.get_mysql_connection('modelsraver')
        if not connection:
            return False
        
        try:
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO conversations (user_id, agent_id, session_id, message, response, metadata)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                user_id, agent_id, session_id, message, response, 
                json.dumps(metadata or {})
            ))
            
            connection.commit()
            cursor.close()
            connection.close()
            return True
            
        except Exception as e:
            logger.error(f"❌ Error saving conversation: {e}")
            return False
    
    def get_conversations(self, user_id: int = None, agent_id: int = None, 
                         limit: int = 50) -> List[Dict[str, Any]]:
        """Get conversations from database"""
        connection = self.get_mysql_connection('modelsraver')
        if not connection:
            return []
        
        try:
            cursor = connection.cursor(dictionary=True)
            
            query = """
                SELECT c.id, c.user_id, c.agent_id, c.session_id, c.message, 
                       c.response, c.metadata, c.created_at,
                       a.name as agent_name, a.display_name as agent_display_name
                FROM conversations c
                LEFT JOIN agents a ON c.agent_id = a.id
                WHERE 1=1
            """
            params = []
            
            if user_id:
                query += " AND c.user_id = %s"
                params.append(user_id)
            
            if agent_id:
                query += " AND c.agent_id = %s"
                params.append(agent_id)
            
            query += " ORDER BY c.created_at DESC LIMIT %s"
            params.append(limit)
            
            cursor.execute(query, params)
            conversations = cursor.fetchall()
            
            # Parse JSON fields
            for conv in conversations:
                if conv.get('metadata'):
                    try:
                        conv['metadata'] = json.loads(conv['metadata'])
                    except:
                        conv['metadata'] = {}
            
            cursor.close()
            connection.close()
            return conversations
            
        except Exception as e:
            logger.error(f"❌ Error getting conversations: {e}")
            return []
    
    # Analytics
    def log_analytics(self, event_type: str, user_id: int = None, agent_id: int = None,
                     provider_id: int = None, metadata: Dict[str, Any] = None) -> bool:
        """Log analytics event"""
        connection = self.get_mysql_connection('modelsraver')
        if not connection:
            return False
        
        try:
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO analytics (event_type, user_id, agent_id, provider_id, metadata)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                event_type, user_id, agent_id, provider_id, 
                json.dumps(metadata or {})
            ))
            
            connection.commit()
            cursor.close()
            connection.close()
            return True
            
        except Exception as e:
            logger.error(f"❌ Error logging analytics: {e}")
            return False
    
    def get_analytics(self, event_type: str = None, days: int = 7) -> List[Dict[str, Any]]:
        """Get analytics data"""
        connection = self.get_mysql_connection('modelsraver')
        if not connection:
            return []
        
        try:
            cursor = connection.cursor(dictionary=True)
            
            query = """
                SELECT a.id, a.event_type, a.user_id, a.agent_id, a.provider_id, 
                       a.metadata, a.created_at,
                       ag.name as agent_name, p.name as provider_name
                FROM analytics a
                LEFT JOIN agents ag ON a.agent_id = ag.id
                LEFT JOIN providers p ON a.provider_id = p.id
                WHERE a.created_at >= DATE_SUB(NOW(), INTERVAL %s DAY)
            """
            params = [days]
            
            if event_type:
                query += " AND a.event_type = %s"
                params.append(event_type)
            
            query += " ORDER BY a.created_at DESC"
            
            cursor.execute(query, params)
            analytics = cursor.fetchall()
            
            # Parse JSON fields
            for event in analytics:
                if event.get('metadata'):
                    try:
                        event['metadata'] = json.loads(event['metadata'])
                    except:
                        event['metadata'] = {}
            
            cursor.close()
            connection.close()
            return analytics
            
        except Exception as e:
            logger.error(f"❌ Error getting analytics: {e}")
            return []
    
    # Database Statistics
    def get_database_stats(self) -> Dict[str, Any]:
        """Get database statistics"""
        connection = self.get_mysql_connection('modelsraver')
        if not connection:
            return {}
        
        try:
            cursor = connection.cursor(dictionary=True)
            stats = {}
            
            # Count agents
            cursor.execute("SELECT COUNT(*) as count FROM agents")
            stats['total_agents'] = cursor.fetchone()['count']
            
            # Count active agents
            cursor.execute("SELECT COUNT(*) as count FROM agents WHERE status = 'active'")
            stats['active_agents'] = cursor.fetchone()['count']
            
            # Count providers
            cursor.execute("SELECT COUNT(*) as count FROM providers")
            stats['total_providers'] = cursor.fetchone()['count']
            
            # Count active providers
            cursor.execute("SELECT COUNT(*) as count FROM providers WHERE status = 'active'")
            stats['active_providers'] = cursor.fetchone()['count']
            
            # Count conversations
            cursor.execute("SELECT COUNT(*) as count FROM conversations")
            stats['total_conversations'] = cursor.fetchone()['count']
            
            # Count today's conversations
            cursor.execute("SELECT COUNT(*) as count FROM conversations WHERE DATE(created_at) = CURDATE()")
            stats['today_conversations'] = cursor.fetchone()['count']
            
            # Count analytics events
            cursor.execute("SELECT COUNT(*) as count FROM analytics")
            stats['total_analytics'] = cursor.fetchone()['count']
            
            # Database size
            cursor.execute("""
                SELECT 
                    ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) AS size_mb
                FROM information_schema.tables 
                WHERE table_schema = 'modelsraver'
            """)
            result = cursor.fetchone()
            stats['database_size_mb'] = result['size_mb'] if result['size_mb'] else 0
            
            cursor.close()
            connection.close()
            return stats
            
        except Exception as e:
            logger.error(f"❌ Error getting database stats: {e}")
            return {}

# Initialize database manager
db_manager = DatabaseManager()
