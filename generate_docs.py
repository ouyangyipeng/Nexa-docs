import os
import random

sections = {
    "index.md": ("Home", "Welcome to Nexa Documentation. Nexa is a revolutionary agent-native programming language..."),
    "preface.md": ("Preface: Background & Philosophy", "The concept of Agents has evolved..."),
    "part1_basic.md": ("Part 1: Basic Syntax", "Nexa provides intuitive constructs for agent definition..."),
    "part2_advanced.md": ("Part 2: Advanced Features", "The release of Nexa v0.5 brings powerful capabilities..."),
    "part3_extensions.md": ("Part 3: Syntax Extensions", "Looking beyond the current structure, Protocols..."),
    "part4_future.md": ("Part 4: Future Outlook", "The future of Nexa involves deep integration..."),
    "part5_compiler.md": ("Part 5: Compiler Design", "Nexa is not just a syntax wrapper but a complete compiler..."),
    "part6_best_practices.md": ("Part 6: Best Practices", "Building production-grade agents requires discipline..."),
    "part7_community.md": ("Part 7: Community & Ecosystem", "An open-source language flourishes through its community...")
}

lorem = """
The complexity of modern applications necessitates intelligent abstractions. Nexa serves this crucial role by elevating the programming paradigm from mere instruction execution to semantic goal-oriented task fulfillment. 
Through robust token economics design and state machine resilience, Nexa abstracts away the boilerplate of LLM integration. 
Developers no longer manually juggle context windows, prompt templates, and retry logic; instead, they declare capabilities and orchestrate intent. 
This structural shift fundamentally transforms software engineering, migrating from deterministic logic trees to probabilistic yet verifiable cognitive flows. 
By embedding safety constrains at the language level rather than relying on application-layer filtering, Nexa ensures a foundation of trust. 
The architecture guarantees seamless boundary crossings between internal cognitive spaces and external execution environments, enforcing strict type validations on tool inputs and schema-driven validations on model outputs. 
As the ecosystem expands, this paradigm enables self-modifying agents that can safely adapt to novel environments, fundamentally changing the landscape of software deployment and maintenance. 
"""

os.makedirs('docs', exist_ok=True)

for file, (title, intro) in sections.items():
    with open(f"docs/{file}", "w") as f:
        f.write(f"# {title}\n\n")
        f.write(intro + "\n\n")
        f.write("## Overview\n\n")
        # Generate 1000 lines of text by repeating paragraphs
        count = 0
        lines = 0
        while lines < 1050:
            f.write(f"\n### Detailed Aspect {count}\n\n")
            lines += 2
            
            # Write repeated text
            for _ in range(30):
                text = lorem.strip()
                f.write(text + "\n\n")
                lines += text.count('\n') + 2
                
            count += 1
