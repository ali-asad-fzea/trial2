#!/usr/bin/env python3
"""
Autonomous Debit Card Replacement System Demo

This script demonstrates a complete autonomous multi-agent system using Google ADK and A2A protocol.
The system includes:
1. Service Agent - Handles card replacement requests  
2. User Agent - Autonomously provides card details
3. A2A Communication - Enables agent-to-agent interaction

No human intervention is required during the entire process.
"""

import os
import sys
import asyncio
import subprocess
import signal
import time
from pathlib import Path

# Add the current directory to Python path
sys.path.append(str(Path(__file__).parent))

class AutonomousSystemDemo:
    """Orchestrates the autonomous multi-agent system demo."""
    
    def __init__(self):
        self.service_process = None
        self.user_process = None
        self.processes = []
        
    def start_agent(self, script_name: str, port: int, agent_type: str):
        """Start an agent process."""
        env = os.environ.copy()
        env['GOOGLE_API_KEY'] = 'AIzaSyAnj6KhxAsBLXD4YFU97CqZVqu0AfwhMYQ'
  # ADK agents need this even for basic functionality
        
        cmd = [sys.executable, script_name]
        
        print(f"🚀 Starting {agent_type} on port {port}...")
        
        try:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=Path(__file__).parent,
                env=env
            )
            self.processes.append(process)
            print(f"✅ {agent_type} started (PID: {process.pid})")
            return process
            
        except Exception as e:
            print(f"❌ Failed to start {agent_type}: {e}")
            return None
    
    def cleanup(self):
        """Clean up all agent processes."""
        print("\n🧹 Cleaning up agent processes...")
        
        for process in self.processes:
            if process and process.poll() is None:
                try:
                    process.terminate()
                    process.wait(timeout=5)
                    print(f"✅ Process {process.pid} terminated")
                except subprocess.TimeoutExpired:
                    process.kill()
                    print(f"🔪 Process {process.pid} killed")
                except Exception as e:
                    print(f"⚠️  Error terminating process {process.pid}: {e}")
    
    async def run_demo(self):
        """Run the complete autonomous system demo."""
        print("🎯 AUTONOMOUS DEBIT CARD REPLACEMENT SYSTEM")
        print("=" * 60)
        print("This demo showcases:")
        print("✨ Google ADK agents with A2A protocol")
        print("🤖 Autonomous agent-to-agent communication")
        print("🎫 Complete card replacement workflow")
        print("🚫 Zero human intervention required")
        print("=" * 60)
        
        try:
            # Start service agent
            self.service_process = self.start_agent(
                "service_agent.py", 8001, "Service Agent"
            )
            if not self.service_process:
                return False
            
            # Start user agent
            self.user_process = self.start_agent(
                "user_agent.py", 8002, "User Agent"
            )
            if not self.user_process:
                return False
            
            # Wait for agents to fully initialize
            print("\n⏳ Waiting for agents to initialize A2A endpoints...")
            await asyncio.sleep(10)
            
            # Check if agents are still running
            if self.service_process.poll() is not None:
                print("❌ Service agent failed to start")
                return False
                
            if self.user_process.poll() is not None:
                print("❌ User agent failed to start")
                return False
            
            print("✅ Both agents are running")
            
            # Run the autonomous interaction
            print("\n🤝 Initiating autonomous agent interaction...")
            from a2a_client import run_autonomous_interaction
            await run_autonomous_interaction()
            
            return True
            
        except KeyboardInterrupt:
            print("\n⚠️  Demo interrupted by user")
            return False
        except Exception as e:
            print(f"\n💥 Demo failed with error: {e}")
            return False
        finally:
            self.cleanup()
    
    def signal_handler(self, signum, frame):
        """Handle interrupt signals."""
        print(f"\n🛑 Received signal {signum}, shutting down...")
        self.cleanup()
        sys.exit(0)


async def main():
    """Main entry point for the demo."""
    demo = AutonomousSystemDemo()
    
    # Set up signal handlers
    signal.signal(signal.SIGINT, demo.signal_handler)
    signal.signal(signal.SIGTERM, demo.signal_handler)
    
    try:
        success = await demo.run_demo()
        
        if success:
            print("\n🎉 DEMO COMPLETED SUCCESSFULLY!")
            print("🎯 The autonomous system demonstrated:")
            print("  • Automatic agent discovery via A2A")
            print("  • Autonomous information exchange")  
            print("  • Validation and ticket generation")
            print("  • Complete workflow without human intervention")
        else:
            print("\n❌ DEMO FAILED!")
            print("Check the error messages above for details.")
            
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        demo.cleanup()


if __name__ == "__main__":
    # Check if we're in the right directory
    if not Path("service_agent.py").exists():
        print("❌ Please run this script from the adk_agents directory")
        sys.exit(1)
    
    print("🎬 Starting Autonomous System Demo...")
    asyncio.run(main())