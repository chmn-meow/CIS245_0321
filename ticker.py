# This week we will work with dictionaries. Create a program that includes a dictionary of stocks. Your dictionary should include at least
# 10 ticker symbols. The key should be the stock ticker symbol and the value should be the current price of the stock (the values can be
# fictional). Ask the user to enter a ticker symbol. Your program will search the dictionary for the ticker symbol and then print the
# ticker symbol and the stock price. If the ticker symbol isn’t located print a message indicating that the ticker symbol wasn’t found.

tickers = {
    "MSFT": {
        "name": "Microsoft Corporation",
        "open": "212.2000",
        "high": "213.2850",
        "low": "210.0000",
        "price": "210.3900",
        "volume": "22843119",
        "latest trading day": "2020-11-20",
        "previous close": "212.4200",
        "change": "-2.0300",
        "change percent": "-0.9557%",
    },
    "INTC": {
        "name": "Intel Corporation",
        "open": "45.6600",
        "high": "45.8800",
        "low": "45.3300",
        "price": "45.3900",
        "volume": "24199278",
        "latest trading day": "2020-11-20",
        "previous close": "45.6200",
        "change": "-0.2300",
        "change percent": "-0.5042%",
    },
    "GOOGL": {
        "name": "Alphabet Inc.",
        "open": "1762.0000",
        "high": "1768.3625",
        "low": "1735.0000",
        "price": "1736.3800",
        "volume": "1385322",
        "latest trading day": "2020-11-20",
        "previous close": "1758.5700",
        "change": "-22.1900",
        "change percent": "-1.2618%",
    },
    "AMD": {
        "name": "Advanced Micro Devices Inc.",
        "open": "85.2800",
        "high": "86.1000",
        "low": "84.4700",
        "price": "84.6400",
        "volume": "35008427",
        "latest trading day": "2020-11-20",
        "previous close": "85.5400",
        "change": "-0.9000",
        "change percent": "-1.0521%",
    },
    "FB": {
        "name": "Facebook Inc.",
        "open": "272.5600",
        "high": "273.0000",
        "low": "269.4100",
        "price": "269.7000",
        "volume": "18122412",
        "latest trading day": "2020-11-20",
        "previous close": "272.9400",
        "change": "-3.2400",
        "change percent": "-1.1871%",
    },
    "NVDA": {
        "name": "NVIDIA Corporation",
        "open": "538.1600",
        "high": "539.7799",
        "low": "522.6000",
        "price": "523.5100",
        "volume": "8527245",
        "latest trading day": "2020-11-20",
        "previous close": "537.6100",
        "change": "-14.1000",
        "change percent": "-2.6227%",
    },
    "CRM": {
        "name": "salesforce.com, inc.",
        "open": "263.5900",
        "high": "265.0200",
        "low": "257.8200",
        "price": "258.0400",
        "volume": "7289605",
        "latest trading day": "2020-11-20",
        "previous close": "264.6500",
        "change": "-6.6100",
        "change percent": "-2.4976%",
    },
    "AAPL": {
        "name": "Apple Inc.",
        "open": "118.6400",
        "high": "118.7700",
        "low": "117.2900",
        "price": "117.3400",
        "volume": "73604287",
        "latest trading day": "2020-11-20",
        "previous close": "118.6400",
        "change": "-1.3000",
        "change percent": "-1.0958%",
    },
    "TSM": {
        "name": "Taiwan Semiconductor Manufacturing Company Limited",
        "open": "96.6600",
        "high": "97.2000",
        "low": "95.3000",
        "price": "95.3300",
        "volume": "5313318",
        "latest trading day": "2020-11-20",
        "previous close": "96.6100",
        "change": "-1.2800",
        "change percent": "-1.3249%",
    },
    "AMZN": {
        "name": "Amazon.com Inc.",
        "open": "3117.0200",
        "high": "3132.8900",
        "low": "3098.0456",
        "price": "3099.4000",
        "volume": "3380138",
        "latest trading day": "2020-11-20",
        "previous close": "3117.0200",
        "change": "-17.6200",
        "change percent": "-0.5653%",
    },
}


class Ticker:
    def __init__(self, symbol, dictionary):
        self.symbol = symbol
        self.copy = dictionary

    def display(self):
        print(f"The information for the ticker {self.symbol} is as follows:")
        itr = 2
        print(f"1. symbol -> {self.symbol}")
        for k, v in self.__dict__["copy"].items():
            print(f"{itr}. {k} -> {v}")
            itr += 1


def get_ticker(prompt):
    err = "I don't understand. Could you try again?"
    msg = input(f"{prompt}\n> ")
    if not msg:
        return get_ticker(err)
    else:
        return get_search(msg)


def get_search(inpt):
    if inpt.upper() in tickers.keys():
        for key in tickers.keys():
            if inpt.upper() == key:
                prompt = f"Is the company {tickers[key]['name']}'s symbol of {key} what you were looking for?"
                if get_yn(prompt):
                    obj = Ticker(key, tickers[key])
                    return obj
                else:
                    prompt = "Sorry. Try another one."
                    return get_ticker(prompt)
    else:
        prompt = "Haven't heard of that one, try again."
        return get_ticker(prompt)


def get_yn(prompt):
    err = "I couldn't catch that. Let's do this again."
    msg = input(f"{prompt} [y/n]\n> ")
    if not msg:
        return get_yn(err)
    elif "y" in msg:
        if msg == "y" or msg == "yes" or msg == "ya":
            return True
        else:
            return get_yn(err)
    elif "n" in msg:
        if msg == "n" or msg == "no" or msg == "na":
            return False
        else:
            return get_yn(err)
    else:
        return get_yn(err)


# technically, the beginning of the program
print("Hello, and welcome to the MoneyBot 3000!")

# true program start
end_program = False
while not end_program:

    # we need to know what ticker user wants to see
    ticker_prompt = "What ticker shall we start with?"
    obj = get_ticker(ticker_prompt)

    # check if want table
    tbl_prompt = f"Would you like their data table?"
    if get_yn(tbl_prompt):
        obj.display()
    else:
        pass

    # ask for continue.  If yes, continue loop.  If no, terminate.
    cont_prompt = "Would you like to look up another ticker?"
    if get_yn(cont_prompt):
        pass
    else:
        end_program = True