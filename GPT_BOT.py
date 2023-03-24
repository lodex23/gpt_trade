import ccxt
import pandas as pd
import jsonlines
import openai
import os


#Set the OpenAI API Key
openai.api_key = "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"


# Connect to Binance API
exchange = ccxt.binance()

# Define currency pair and timeframe
symbol = 'BTC/USDT'
timeframe = '1d'

# Retrieve historical data
ohlcv = exchange.fetch_ohlcv(symbol, timeframe)

# Convert data to a pandas dataframe
df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])

# Convert timestamp to datetime format
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

# Reformat data to GPT-3 format
gpt3_data = []
for index, row in df.iterrows():
    gpt3_data.append(f'{row["timestamp"]:%Y-%m-%d %H:%M:%S}, {row["open"]:.8f}, {row["high"]:.8f}, {row["low"]:.8f}, {row["close"]:.8f}, {row["volume"]:.8f}')



with jsonlines.open("training_data.jsonl", mode="w") as writer:
	for example in gpt3_data:
		writer.write(example)



#Create the GPT-3 Model
model = openai.Model.create(
	"text-davinci-002",
	train_file="training_data.jsonl",
	max_train_time = 2000,
	n_epochs=100
)

prompt = "what will be the closing price of BTC/USDT on March 25, 2023?"
completions = model.generate(prompt=prompt, max_tokens = 1024)


# Print the Generated text
for completion in completions.choices:
	print(completion.text)
