from improver import CodeImprover
import time
async def multi_improve(user_input: str, max_round: int = 3):
    initial_input = user_input
    improver_agent = CodeImprover()
    for round in range(max_round):
        round_improvement = await improver_agent.run(user_input=initial_input)
        initial_input = round_improvement
        time.sleep(3)

    return initial_input


if __name__ == "__main__":
    import asyncio
    with open("base.py", 'r') as f_in:
        code_base = f_in.read()
    user_input = code_base

    asyncio.run(multi_improve(user_input=user_input))
    
        


