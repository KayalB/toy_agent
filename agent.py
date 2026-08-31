from anthropic import Anthropic
from dotenv import load_dotenv
from tools import TOOLS, SCHEMAS

load_dotenv()

client = Anthropic()
MODEL_NAME = "claude-sonnet-5"

SYSTEM = (
    "You are working in a Python project. Investigate and run the initial "
    "tests before editing. Use the tools to inspect files rather than "
    "guessing at their contents."
)


def execute(name, tool_input):
    if name not in TOOLS:
        return f"Error: unknown tool '{name}'. Available: {', '.join(TOOLS)}"
    _, fn = TOOLS[name]
    try:
        return fn(**tool_input)
    except TypeError as e:
        return f"Error calling {name}: {e}"


def run_agent(prompt, max_turns=20, verbose=True):
    messages = [{"role": "user", "content": prompt}]
    total_in = 0
    total_out = 0
    stopped = "turn_limit"

    for turn in range(max_turns):
        response = client.messages.create(
            model=MODEL_NAME,
            messages=messages,
            tools=SCHEMAS,
            system=SYSTEM,
            max_tokens=4096,
        )

        total_in += response.usage.input_tokens
        total_out += response.usage.output_tokens

        if response.stop_reason == "max_tokens":
            raise RuntimeError("response truncated, raise max_tokens")

        messages.append({"role": "assistant", "content": response.content})

        tool_uses = [b for b in response.content if b.type == "tool_use"]

        if not tool_uses:
            stopped = "end_turn"
            break

        if verbose:
            print(f"Iteration {turn + 1}  ({response.usage.input_tokens} in / {response.usage.output_tokens} out)")

        results = []
        for block in tool_uses:
            if verbose:
                path = block.input.get("fpath") or block.input.get("path", "")
                print(f"Using tool: {block.name} > {path}")
            results.append({
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": execute(block.name, block.input),
            })
        messages.append({"role": "user", "content": results})

    return {
        "turns": turn + 1,
        "stopped": stopped,
        "tokens_in": total_in,
        "tokens_out": total_out,
        "cost": total_in / 1e6 * 3 + total_out / 1e6 * 15,
        "messages": messages,
    }


if __name__ == "__main__":
    import shutil

    shutil.rmtree("workspace", ignore_errors=True)
    shutil.copytree("env_template", "workspace")

    result = run_agent("The tests in this project are failing. Find out why and fix it.")

    for block in result["messages"][-1]["content"]:
        if block.type == "text":
            print(f'\n"{block.text}"')

    print(f"\nturns={result['turns']} stopped={result['stopped']}")
    print(f"tokens: {result['tokens_in']} in, {result['tokens_out']} out  ~${result['cost']:.4f}")