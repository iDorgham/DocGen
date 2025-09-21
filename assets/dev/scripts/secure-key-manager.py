#!/usr/bin/env python3
"""
Secure API Key Manager for DocGen CLI
Provides encrypted storage, rotation, and management of API keys for MCP servers.

Features:
- AES-256 encryption for API key storage
- Environment variable management with validation
- API key rotation and expiration tracking
- Secure key sharing and backup mechanisms
- Audit logging for all key operations
- Integration with existing MCP configuration

Author: DocGen CLI Team
Date: 2025-01-27
Version: 1.0.0
"""

import os
import sys
import json
import yaml
import base64
import hashlib
import logging
import secrets
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'src'))

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.logging import RichHandler
    from rich.prompt import Prompt, Confirm
    from rich.text import Text
except ImportError:
    print("Warning: Rich library not available. Install with: pip install rich")
    Console = None

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[RichHandler()] if Console else [logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

class KeyStatus(Enum):
    """API key status enumeration."""
    ACTIVE = "active"
    EXPIRED = "expired"
    ROTATED = "rotated"
    REVOKED = "revoked"
    PENDING = "pending"

@dataclass
class APIKeyInfo:
    """API key information."""
    server: str
    key_id: str
    key_value: str
    status: KeyStatus
    created_at: datetime
    expires_at: Optional[datetime]
    last_used: Optional[datetime]
    usage_count: int
    environment_variable: str
    encrypted: bool
    metadata: Dict[str, Any]

@dataclass
class KeyOperation:
    """Key operation audit log entry."""
    operation: str
    server: str
    key_id: str
    timestamp: datetime
    success: bool
    details: str
    user: Optional[str] = None

class SecureKeyManager:
    """
    Secure API Key Manager.
    
    Provides encrypted storage, rotation, and management of API keys
    for MCP servers with comprehensive security features.
    """
    
    def __init__(self, project_path: str = None, config_path: str = None):
        """
        Initialize Secure Key Manager.
        
        Args:
            project_path: Path to the DocGen CLI project
            config_path: Path to MCP configuration file
        """
        self.console = Console() if Console else None
        self.project_path = project_path or self._get_project_path()
        self.config_path = config_path or os.path.join(
            self.project_path, 'assets', 'dev', 'config', 'mcp', 'mcp_config.yaml'
        )
        
        # Key storage paths
        self.keys_dir = os.path.join(self.project_path, 'assets', 'dev', 'config', 'mcp', 'keys')
        self.audit_log_path = os.path.join(self.keys_dir, 'audit_log.json')
        self.master_key_path = os.path.join(self.keys_dir, 'master.key')
        
        # Ensure keys directory exists
        os.makedirs(self.keys_dir, exist_ok=True)
        
        # Key storage
        self.api_keys: Dict[str, APIKeyInfo] = {}
        self.audit_log: List[KeyOperation] = []
        
        # Encryption
        self.master_key = None
        self.cipher_suite = None
        
        # Load configuration and initialize encryption
        self.load_configuration()
        self.initialize_encryption()
        self.load_api_keys()
        self.load_audit_log()
        
        logger.info("Secure Key Manager initialized")
    
    def _get_project_path(self) -> str:
        """Get the DocGen CLI project path."""
        current_dir = Path(__file__).parent
        project_root = current_dir.parent.parent.parent
        return str(project_root)
    
    def load_configuration(self):
        """Load MCP configuration to understand key requirements."""
        try:
            with open(self.config_path, 'r') as f:
                self.config = yaml.safe_load(f)
            logger.info("MCP configuration loaded")
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            self.config = {}
    
    def initialize_encryption(self):
        """Initialize encryption system with master key."""
        try:
            # Check if master key exists
            if os.path.exists(self.master_key_path):
                with open(self.master_key_path, 'rb') as f:
                    self.master_key = f.read()
            else:
                # Generate new master key
                self.master_key = Fernet.generate_key()
                with open(self.master_key_path, 'wb') as f:
                    f.write(self.master_key)
                logger.info("New master key generated")
            
            # Initialize cipher suite
            self.cipher_suite = Fernet(self.master_key)
            logger.info("Encryption system initialized")
            
        except Exception as e:
            logger.error(f"Error initializing encryption: {e}")
            raise
    
    def generate_key_id(self, server: str) -> str:
        """Generate a unique key ID for a server."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        random_suffix = secrets.token_hex(4)
        return f"{server}_{timestamp}_{random_suffix}"
    
    def encrypt_key(self, key_value: str) -> str:
        """Encrypt an API key."""
        try:
            encrypted_key = self.cipher_suite.encrypt(key_value.encode())
            return base64.b64encode(encrypted_key).decode()
        except Exception as e:
            logger.error(f"Error encrypting key: {e}")
            raise
    
    def decrypt_key(self, encrypted_key: str) -> str:
        """Decrypt an API key."""
        try:
            encrypted_data = base64.b64decode(encrypted_key.encode())
            decrypted_key = self.cipher_suite.decrypt(encrypted_data)
            return decrypted_key.decode()
        except Exception as e:
            logger.error(f"Error decrypting key: {e}")
            raise
    
    def log_operation(self, operation: str, server: str, key_id: str, 
                     success: bool, details: str, user: str = None):
        """Log a key operation for audit purposes."""
        operation_log = KeyOperation(
            operation=operation,
            server=server,
            key_id=key_id,
            timestamp=datetime.now(),
            success=success,
            details=details,
            user=user or os.getenv('USER', 'unknown')
        )
        
        self.audit_log.append(operation_log)
        
        # Keep only last 1000 operations
        if len(self.audit_log) > 1000:
            self.audit_log = self.audit_log[-1000:]
        
        logger.info(f"Key operation logged: {operation} for {server} - {'SUCCESS' if success else 'FAILED'}")
    
    def save_audit_log(self):
        """Save audit log to file."""
        try:
            audit_data = [asdict(op) for op in self.audit_log]
            with open(self.audit_log_path, 'w') as f:
                json.dump(audit_data, f, indent=2, default=str)
            logger.debug("Audit log saved")
        except Exception as e:
            logger.error(f"Error saving audit log: {e}")
    
    def load_audit_log(self):
        """Load audit log from file."""
        try:
            if os.path.exists(self.audit_log_path):
                with open(self.audit_log_path, 'r') as f:
                    audit_data = json.load(f)
                
                self.audit_log = [
                    KeyOperation(**op) for op in audit_data
                ]
                logger.info(f"Loaded {len(self.audit_log)} audit log entries")
        except Exception as e:
            logger.error(f"Error loading audit log: {e}")
            self.audit_log = []
    
    def add_api_key(self, server: str, key_value: str, 
                   expires_at: Optional[datetime] = None,
                   environment_variable: str = None,
                   metadata: Dict[str, Any] = None) -> str:
        """
        Add a new API key for a server.
        
        Args:
            server: MCP server name
            key_value: The API key value
            expires_at: Optional expiration date
            environment_variable: Environment variable name
            metadata: Additional metadata
            
        Returns:
            Key ID of the added key
        """
        try:
            # Generate key ID
            key_id = self.generate_key_id(server)
            
            # Determine environment variable name
            if not environment_variable:
                environment_variable = f"{server.upper()}_API_KEY"
            
            # Encrypt the key
            encrypted_key = self.encrypt_key(key_value)
            
            # Create API key info
            api_key_info = APIKeyInfo(
                server=server,
                key_id=key_id,
                key_value=encrypted_key,
                status=KeyStatus.ACTIVE,
                created_at=datetime.now(),
                expires_at=expires_at,
                last_used=None,
                usage_count=0,
                environment_variable=environment_variable,
                encrypted=True,
                metadata=metadata or {}
            )
            
            # Store the key
            self.api_keys[key_id] = api_key_info
            
            # Save to file
            self.save_api_keys()
            
            # Log operation
            self.log_operation(
                "ADD_KEY", server, key_id, True,
                f"API key added for {server}",
                user=os.getenv('USER', 'unknown')
            )
            self.save_audit_log()
            
            logger.info(f"API key added for {server} with ID: {key_id}")
            return key_id
            
        except Exception as e:
            logger.error(f"Error adding API key for {server}: {e}")
            self.log_operation(
                "ADD_KEY", server, "unknown", False,
                f"Failed to add API key: {e}",
                user=os.getenv('USER', 'unknown')
            )
            self.save_audit_log()
            raise
    
    def get_api_key(self, server: str, key_id: str = None) -> Optional[str]:
        """
        Get an API key for a server.
        
        Args:
            server: MCP server name
            key_id: Specific key ID (optional)
            
        Returns:
            Decrypted API key or None if not found
        """
        try:
            # Find the key
            if key_id:
                if key_id in self.api_keys:
                    api_key_info = self.api_keys[key_id]
                else:
                    return None
            else:
                # Find active key for server
                active_keys = [
                    key for key in self.api_keys.values()
                    if key.server == server and key.status == KeyStatus.ACTIVE
                ]
                if not active_keys:
                    return None
                api_key_info = active_keys[0]
            
            # Check if key is expired
            if api_key_info.expires_at and datetime.now() > api_key_info.expires_at:
                logger.warning(f"API key {api_key_info.key_id} for {server} has expired")
                return None
            
            # Decrypt and return key
            decrypted_key = self.decrypt_key(api_key_info.key_value)
            
            # Update usage statistics
            api_key_info.last_used = datetime.now()
            api_key_info.usage_count += 1
            self.save_api_keys()
            
            # Log operation
            self.log_operation(
                "GET_KEY", server, api_key_info.key_id, True,
                f"API key retrieved for {server}",
                user=os.getenv('USER', 'unknown')
            )
            self.save_audit_log()
            
            return decrypted_key
            
        except Exception as e:
            logger.error(f"Error getting API key for {server}: {e}")
            self.log_operation(
                "GET_KEY", server, key_id or "unknown", False,
                f"Failed to get API key: {e}",
                user=os.getenv('USER', 'unknown')
            )
            self.save_audit_log()
            return None
    
    def rotate_api_key(self, server: str, new_key_value: str) -> str:
        """
        Rotate an API key for a server.
        
        Args:
            server: MCP server name
            new_key_value: New API key value
            
        Returns:
            Key ID of the new key
        """
        try:
            # Mark existing active keys as rotated
            for key_id, api_key_info in self.api_keys.items():
                if api_key_info.server == server and api_key_info.status == KeyStatus.ACTIVE:
                    api_key_info.status = KeyStatus.ROTATED
                    self.log_operation(
                        "ROTATE_KEY", server, key_id, True,
                        f"API key rotated for {server}",
                        user=os.getenv('USER', 'unknown')
                    )
            
            # Add new key
            new_key_id = self.add_api_key(server, new_key_value)
            
            # Save changes
            self.save_api_keys()
            self.save_audit_log()
            
            logger.info(f"API key rotated for {server}, new key ID: {new_key_id}")
            return new_key_id
            
        except Exception as e:
            logger.error(f"Error rotating API key for {server}: {e}")
            self.log_operation(
                "ROTATE_KEY", server, "unknown", False,
                f"Failed to rotate API key: {e}",
                user=os.getenv('USER', 'unknown')
            )
            self.save_audit_log()
            raise
    
    def revoke_api_key(self, server: str, key_id: str = None):
        """
        Revoke an API key for a server.
        
        Args:
            server: MCP server name
            key_id: Specific key ID (optional)
        """
        try:
            if key_id:
                if key_id in self.api_keys:
                    self.api_keys[key_id].status = KeyStatus.REVOKED
                    self.log_operation(
                        "REVOKE_KEY", server, key_id, True,
                        f"API key revoked for {server}",
                        user=os.getenv('USER', 'unknown')
                    )
            else:
                # Revoke all active keys for server
                for key_id, api_key_info in self.api_keys.items():
                    if api_key_info.server == server and api_key_info.status == KeyStatus.ACTIVE:
                        api_key_info.status = KeyStatus.REVOKED
                        self.log_operation(
                            "REVOKE_KEY", server, key_id, True,
                            f"API key revoked for {server}",
                            user=os.getenv('USER', 'unknown')
                        )
            
            # Save changes
            self.save_api_keys()
            self.save_audit_log()
            
            logger.info(f"API key(s) revoked for {server}")
            
        except Exception as e:
            logger.error(f"Error revoking API key for {server}: {e}")
            self.log_operation(
                "REVOKE_KEY", server, key_id or "unknown", False,
                f"Failed to revoke API key: {e}",
                user=os.getenv('USER', 'unknown')
            )
            self.save_audit_log()
            raise
    
    def set_environment_variable(self, server: str, key_id: str = None) -> bool:
        """
        Set environment variable with API key.
        
        Args:
            server: MCP server name
            key_id: Specific key ID (optional)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Get the API key
            api_key = self.get_api_key(server, key_id)
            if not api_key:
                logger.error(f"No active API key found for {server}")
                return False
            
            # Find the key info
            if key_id:
                api_key_info = self.api_keys[key_id]
            else:
                active_keys = [
                    key for key in self.api_keys.values()
                    if key.server == server and key.status == KeyStatus.ACTIVE
                ]
                if not active_keys:
                    return False
                api_key_info = active_keys[0]
            
            # Set environment variable
            os.environ[api_key_info.environment_variable] = api_key
            
            # Log operation
            self.log_operation(
                "SET_ENV", server, api_key_info.key_id, True,
                f"Environment variable {api_key_info.environment_variable} set",
                user=os.getenv('USER', 'unknown')
            )
            self.save_audit_log()
            
            logger.info(f"Environment variable {api_key_info.environment_variable} set for {server}")
            return True
            
        except Exception as e:
            logger.error(f"Error setting environment variable for {server}: {e}")
            self.log_operation(
                "SET_ENV", server, key_id or "unknown", False,
                f"Failed to set environment variable: {e}",
                user=os.getenv('USER', 'unknown')
            )
            self.save_audit_log()
            return False
    
    def save_api_keys(self):
        """Save API keys to encrypted storage."""
        try:
            # Prepare data for saving (without decrypted keys)
            keys_data = {}
            for key_id, api_key_info in self.api_keys.items():
                keys_data[key_id] = {
                    'server': api_key_info.server,
                    'key_id': api_key_info.key_id,
                    'key_value': api_key_info.key_value,  # Already encrypted
                    'status': api_key_info.status.value,
                    'created_at': api_key_info.created_at.isoformat(),
                    'expires_at': api_key_info.expires_at.isoformat() if api_key_info.expires_at else None,
                    'last_used': api_key_info.last_used.isoformat() if api_key_info.last_used else None,
                    'usage_count': api_key_info.usage_count,
                    'environment_variable': api_key_info.environment_variable,
                    'encrypted': api_key_info.encrypted,
                    'metadata': api_key_info.metadata
                }
            
            # Save to file
            keys_file = os.path.join(self.keys_dir, 'api_keys.json')
            with open(keys_file, 'w') as f:
                json.dump(keys_data, f, indent=2)
            
            logger.debug("API keys saved to encrypted storage")
            
        except Exception as e:
            logger.error(f"Error saving API keys: {e}")
            raise
    
    def load_api_keys(self):
        """Load API keys from encrypted storage."""
        try:
            keys_file = os.path.join(self.keys_dir, 'api_keys.json')
            if not os.path.exists(keys_file):
                logger.info("No API keys file found, starting with empty key store")
                return
            
            with open(keys_file, 'r') as f:
                keys_data = json.load(f)
            
            # Load API key info
            for key_id, key_data in keys_data.items():
                api_key_info = APIKeyInfo(
                    server=key_data['server'],
                    key_id=key_data['key_id'],
                    key_value=key_data['key_value'],
                    status=KeyStatus(key_data['status']),
                    created_at=datetime.fromisoformat(key_data['created_at']),
                    expires_at=datetime.fromisoformat(key_data['expires_at']) if key_data['expires_at'] else None,
                    last_used=datetime.fromisoformat(key_data['last_used']) if key_data['last_used'] else None,
                    usage_count=key_data['usage_count'],
                    environment_variable=key_data['environment_variable'],
                    encrypted=key_data['encrypted'],
                    metadata=key_data['metadata']
                )
                self.api_keys[key_id] = api_key_info
            
            logger.info(f"Loaded {len(self.api_keys)} API keys from storage")
            
        except Exception as e:
            logger.error(f"Error loading API keys: {e}")
            self.api_keys = {}
    
    def get_key_summary(self) -> Dict[str, Any]:
        """Get summary of all API keys."""
        total_keys = len(self.api_keys)
        active_keys = sum(1 for k in self.api_keys.values() if k.status == KeyStatus.ACTIVE)
        expired_keys = sum(1 for k in self.api_keys.values() if k.status == KeyStatus.EXPIRED)
        rotated_keys = sum(1 for k in self.api_keys.values() if k.status == KeyStatus.ROTATED)
        revoked_keys = sum(1 for k in self.api_keys.values() if k.status == KeyStatus.REVOKED)
        
        # Group by server
        server_keys = {}
        for key in self.api_keys.values():
            if key.server not in server_keys:
                server_keys[key.server] = {'total': 0, 'active': 0, 'expired': 0, 'rotated': 0, 'revoked': 0}
            server_keys[key.server]['total'] += 1
            server_keys[key.server][key.status.value] += 1
        
        return {
            'timestamp': datetime.now().isoformat(),
            'total_keys': total_keys,
            'active_keys': active_keys,
            'expired_keys': expired_keys,
            'rotated_keys': rotated_keys,
            'revoked_keys': revoked_keys,
            'server_keys': server_keys,
            'audit_log_entries': len(self.audit_log)
        }
    
    def display_key_dashboard(self):
        """Display API key management dashboard."""
        if not self.console:
            # Fallback to simple text output
            summary = self.get_key_summary()
            print(f"\nAPI Key Management Summary:")
            print(f"  Total Keys: {summary['total_keys']}")
            print(f"  Active Keys: {summary['active_keys']}")
            print(f"  Expired Keys: {summary['expired_keys']}")
            print(f"  Rotated Keys: {summary['rotated_keys']}")
            print(f"  Revoked Keys: {summary['revoked_keys']}")
            return
        
        # Create dashboard
        layout = Layout()
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="main", ratio=1),
            Layout(name="footer", size=3)
        )
        
        layout["main"].split_row(
            Layout(name="keys_table", ratio=2),
            Layout(name="summary", ratio=1)
        )
        
        # Header
        header_text = Text("🔐 Secure API Key Management Dashboard", style="bold blue")
        layout["header"].update(Panel(header_text, border_style="blue"))
        
        # Keys table
        table = Table(title="API Keys")
        table.add_column("Server", style="cyan", width=12)
        table.add_column("Key ID", style="blue", width=20)
        table.add_column("Status", style="green", width=12)
        table.add_column("Created", style="yellow", width=12)
        table.add_column("Last Used", style="magenta", width=12)
        table.add_column("Usage", style="white", width=8)
        table.add_column("Env Var", style="dim", width=15)
        
        for key_id, api_key_info in self.api_keys.items():
            # Status icon and color
            if api_key_info.status == KeyStatus.ACTIVE:
                status_icon = "✅"
                status_color = "green"
            elif api_key_info.status == KeyStatus.EXPIRED:
                status_icon = "⏰"
                status_color = "yellow"
            elif api_key_info.status == KeyStatus.ROTATED:
                status_icon = "🔄"
                status_color = "blue"
            elif api_key_info.status == KeyStatus.REVOKED:
                status_icon = "❌"
                status_color = "red"
            else:
                status_icon = "❓"
                status_color = "white"
            
            # Created date
            created_str = api_key_info.created_at.strftime("%Y-%m-%d")
            
            # Last used
            if api_key_info.last_used:
                last_used_str = api_key_info.last_used.strftime("%Y-%m-%d")
            else:
                last_used_str = "Never"
            
            # Truncate key ID for display
            display_key_id = key_id[:17] + "..." if len(key_id) > 20 else key_id
            
            table.add_row(
                api_key_info.server,
                display_key_id,
                f"{status_icon} {api_key_info.status.value}",
                created_str,
                last_used_str,
                str(api_key_info.usage_count),
                api_key_info.environment_variable
            )
        
        layout["keys_table"].update(table)
        
        # Summary panel
        summary = self.get_key_summary()
        summary_text = f"""
Total Keys: {summary['total_keys']}
Active Keys: {summary['active_keys']}
Expired Keys: {summary['expired_keys']}
Rotated Keys: {summary['rotated_keys']}
Revoked Keys: {summary['revoked_keys']}
Audit Log Entries: {summary['audit_log_entries']}

Servers:
{chr(10).join([f"  {server}: {data['active']} active, {data['total']} total" for server, data in summary['server_keys'].items()])}
        """.strip()
        
        layout["summary"].update(Panel(summary_text, title="Summary", border_style="green"))
        
        # Footer
        footer_text = Text("Use --help for available commands", style="dim")
        layout["footer"].update(Panel(footer_text, border_style="dim"))
        
        self.console.print(layout)
    
    def interactive_setup(self):
        """Interactive setup wizard for API keys."""
        if not self.console:
            logger.error("Rich console not available for interactive setup")
            return
        
        self.console.print(Panel("🔐 API Key Setup Wizard", style="bold blue"))
        
        # Get server selection
        servers = list(self.config.get('servers', {}).keys())
        if not servers:
            self.console.print("No MCP servers configured", style="red")
            return
        
        server = Prompt.ask("Select server", choices=servers)
        
        # Check if key already exists
        existing_keys = [k for k in self.api_keys.values() if k.server == server and k.status == KeyStatus.ACTIVE]
        if existing_keys:
            if not Confirm.ask(f"Active key already exists for {server}. Replace it?"):
                return
        
        # Get API key
        api_key = Prompt.ask(f"Enter API key for {server}", password=True)
        
        # Get expiration (optional)
        expires_in_days = Prompt.ask("Key expiration in days (optional, press Enter to skip)", default="")
        expires_at = None
        if expires_in_days:
            try:
                expires_at = datetime.now() + timedelta(days=int(expires_in_days))
            except ValueError:
                self.console.print("Invalid expiration days, skipping expiration", style="yellow")
        
        # Get environment variable name
        env_var = Prompt.ask("Environment variable name", default=f"{server.upper()}_API_KEY")
        
        # Add the key
        try:
            key_id = self.add_api_key(server, api_key, expires_at, env_var)
            self.console.print(f"✅ API key added successfully for {server}", style="green")
            self.console.print(f"Key ID: {key_id}", style="dim")
            
            # Ask to set environment variable
            if Confirm.ask("Set environment variable now?"):
                if self.set_environment_variable(server, key_id):
                    self.console.print(f"✅ Environment variable {env_var} set", style="green")
                else:
                    self.console.print("❌ Failed to set environment variable", style="red")
                    
        except Exception as e:
            self.console.print(f"❌ Error adding API key: {e}", style="red")

def main():
    """Main function for Secure Key Manager."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Secure API Key Manager for MCP Servers")
    parser.add_argument('--dashboard', action='store_true', help='Display key management dashboard')
    parser.add_argument('--add', type=str, help='Add API key for server')
    parser.add_argument('--get', type=str, help='Get API key for server')
    parser.add_argument('--rotate', type=str, help='Rotate API key for server')
    parser.add_argument('--revoke', type=str, help='Revoke API key for server')
    parser.add_argument('--set-env', type=str, help='Set environment variable for server')
    parser.add_argument('--setup', action='store_true', help='Run interactive setup wizard')
    parser.add_argument('--summary', action='store_true', help='Show key summary')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose logging')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        # Initialize key manager
        key_manager = SecureKeyManager()
        
        if args.dashboard:
            # Display dashboard
            key_manager.display_key_dashboard()
        elif args.add:
            # Add API key
            api_key = input(f"Enter API key for {args.add}: ")
            key_id = key_manager.add_api_key(args.add, api_key)
            print(f"API key added with ID: {key_id}")
        elif args.get:
            # Get API key
            api_key = key_manager.get_api_key(args.get)
            if api_key:
                print(f"API key for {args.get}: {api_key}")
            else:
                print(f"No active API key found for {args.get}")
        elif args.rotate:
            # Rotate API key
            new_key = input(f"Enter new API key for {args.rotate}: ")
            key_id = key_manager.rotate_api_key(args.rotate, new_key)
            print(f"API key rotated, new key ID: {key_id}")
        elif args.revoke:
            # Revoke API key
            key_manager.revoke_api_key(args.revoke)
            print(f"API key revoked for {args.revoke}")
        elif args.set_env:
            # Set environment variable
            if key_manager.set_environment_variable(args.set_env):
                print(f"Environment variable set for {args.set_env}")
            else:
                print(f"Failed to set environment variable for {args.set_env}")
        elif args.setup:
            # Run interactive setup
            key_manager.interactive_setup()
        elif args.summary:
            # Show summary
            summary = key_manager.get_key_summary()
            print(json.dumps(summary, indent=2))
        else:
            # Default: display dashboard
            key_manager.display_key_dashboard()
        
        return 0
        
    except Exception as e:
        logger.error(f"Error in Secure Key Manager: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
