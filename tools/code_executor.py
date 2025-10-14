"""
Sandboxed Python code execution
"""
import sys
import io
import traceback
from typing import Dict, Any
from contextlib import redirect_stdout, redirect_stderr
import signal
from app.config import settings


class TimeoutException(Exception):
    """Raised when code execution times out"""
    pass


def timeout_handler(signum, frame):
    """Handle timeout signal"""
    raise TimeoutException("Code execution timed out")


class CodeExecutor:
    """Execute Python code in a restricted environment"""
    
    def __init__(self):
        self.timeout = settings.CODE_TIMEOUT_SECONDS
    
    def execute(self, code: str) -> Dict[str, Any]:
        """
        Execute Python code and return results
        
        Returns:
            dict with 'success', 'output', 'error' keys
        """
        # Create isolated namespace
        namespace = {
            '__builtins__': __builtins__,
            'print': print,
        }
        
        # Safe imports allowed
        safe_imports = {
            'math': __import__('math'),
            'datetime': __import__('datetime'),
            'json': __import__('json'),
            're': __import__('re'),
        }
        
        # Try to import data science libraries (if available)
        try:
            import pandas as pd
            import numpy as np
            safe_imports['pd'] = pd
            safe_imports['pandas'] = pd
            safe_imports['np'] = np
            safe_imports['numpy'] = np
        except ImportError:
            pass
        
        try:
            import matplotlib
            matplotlib.use('Agg')  # Non-interactive backend
            import matplotlib.pyplot as plt
            safe_imports['plt'] = plt
            safe_imports['matplotlib'] = matplotlib
        except ImportError:
            pass
        
        namespace.update(safe_imports)
        
        # Capture output
        stdout = io.StringIO()
        stderr = io.StringIO()
        
        try:
            # Set timeout (Unix-like systems only)
            if hasattr(signal, 'SIGALRM'):
                signal.signal(signal.SIGALRM, timeout_handler)
                signal.alarm(self.timeout)
            
            # Execute code
            with redirect_stdout(stdout), redirect_stderr(stderr):
                exec(code, namespace)
            
            # Cancel timeout
            if hasattr(signal, 'SIGALRM'):
                signal.alarm(0)
            
            output = stdout.getvalue()
            errors = stderr.getvalue()
            
            if errors:
                return {
                    'success': False,
                    'output': output,
                    'error': errors
                }
            
            return {
                'success': True,
                'output': output or "Code executed successfully (no output)",
                'error': None
            }
        
        except TimeoutException:
            return {
                'success': False,
                'output': stdout.getvalue(),
                'error': f"Code execution timed out after {self.timeout} seconds"
            }
        
        except Exception as e:
            return {
                'success': False,
                'output': stdout.getvalue(),
                'error': f"{type(e).__name__}: {str(e)}\n{traceback.format_exc()}"
            }
        
        finally:
            # Cleanup
            if hasattr(signal, 'SIGALRM'):
                signal.alarm(0)
            stdout.close()
            stderr.close()


# Global instance
code_executor = CodeExecutor()

