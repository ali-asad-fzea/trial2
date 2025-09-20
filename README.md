# GitHub Codespaces ♥️ Jupyter Notebooks

Welcome to your shiny new codespace! We've got everything fired up and running for you to explore Python and Jupyter notebooks.

You've got a blank canvas to work on from a git perspective as well. There's a single initial commit with what you're seeing right now - where you go from here is up to you!

Everything you do here is contained within this one codespace. There is no repository on GitHub yet. If and when you’re ready you can click "Publish Branch" and we’ll create your repository and push up your project. If you were just exploring then and have no further need for this code then you can simply delete your codespace and it's gone forever.

## Multi-agent demo

This workspace includes a simple autonomous two-agent example (user-agent and service-agent) that completes a debit card replacement workflow with no human input.

Run it:

```bash
python run_demo.py
```

You should see a short exchange of `REQUEST` and `RESPONSE` messages culminating in a `DONE` message with an approval ticket.

### Notes: ADK and A2A integration
- This demo uses an in-memory transport and a minimal message schema (`conversation_id`, `sender`, `recipient`, `type`, `content`).
- To integrate with external agent frameworks:
	- ADK (Google Agent Development Kit): map this schema to ADK conversations/turns and tool-calls per the docs.
	- A2A (Agent-to-Agent Protocol): adapt the `Message` container to A2A envelopes and wire a transport (HTTP, MQ, etc.).
