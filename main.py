import dotenv

from HelloAgentsLLM import HelloAgentsLLM

dotenv.load_dotenv()


if __name__ == '__main__':

    # print(find_primes(int(math.pow(10,7))))


    agent = HelloAgentsLLM(
        provider="zhipu"
    )
    response = agent.think([
        {"role": "system", "content": "You are a helpful assistant that writes Python code."},
        {"role": "user", "content": "你好，你是谁？"}
    ])

    print("LLM响应内容:")
    print(response)
