# sinterklaas-keybasebot
Code for running a simple Keybase bot that generates Sinterklaas poems on command.

![](https://oskarvanderwal.keybase.pub/sinterklaas/Peek%202020-03-13%2013-47__2.gif)

## Quick-Start

Make sure you have a [GPT-2 model](https://huggingface.co/transformers/model_doc/gpt2.html) and tokenizer trained on a corpus with sinterklaas poems. You also need to have [Keybase](keybase.io) installed on your device and the application running, before starting the sinterklaas bot.

Make sure you have all the dependencies installed, for example through:

```
python m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Start the bot with the following command:

```
python main.py --user <KEYBASE-USERNAME> --key <KEYBASE-PAPERKEY> --model <GPT2-MODEL> --tokenizer <GPT2-TOKENIZER>
```
